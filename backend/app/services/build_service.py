from sqlalchemy.orm import Session
from time import monotonic

from app.config import Settings
from app.database import SessionLocal
from app.models import Build, BuildStatus
from app.schemas import BuildCreate
from app.services.gemini_service import GeminiService
from app.services.jenkins_service import JenkinsService
from app.services.kubernetes_preview_service import KubernetesPreviewService
from app.services.metrics_service import (
    ACTIVE_BUILDS,
    BUILD_DURATION,
    BUILD_FAILURE,
    BUILD_REQUESTS,
    BUILD_SUCCESS,
    GEMINI_EXPLANATIONS,
    JENKINS_TRIGGER_ERRORS,
    PREVIEW_DEPLOYMENTS,
    RUNNING_PREVIEW_APPS,
)


class BuildService:
    """Coordinates database updates, Jenkins execution, and Gemini explanations."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def create_build(self, db: Session, payload: BuildCreate) -> Build:
        BUILD_REQUESTS.inc()
        build = Build(
            repository_url=str(payload.repository_url),
            image_name=payload.image_name,
            port=payload.port,
            status=BuildStatus.QUEUED.value,
        )
        db.add(build)
        db.commit()
        db.refresh(build)
        return build

    def get_build(self, db: Session, build_id: int) -> Build | None:
        return db.get(Build, build_id)

    def run_build(self, build_id: int) -> None:
        db = SessionLocal()
        jenkins = JenkinsService(self.settings)
        gemini = GeminiService(self.settings)
        preview = KubernetesPreviewService(self.settings)
        started_at = monotonic()
        ACTIVE_BUILDS.inc()

        try:
            build = db.get(Build, build_id)
            if not build:
                return

            build.status = BuildStatus.RUNNING.value
            db.commit()

            queue_url = jenkins.trigger_build(
                build.repository_url, build.image_name, build.port
            )
            build.jenkins_queue_url = queue_url
            db.commit()

            build_url = jenkins.wait_for_executable_url(queue_url)
            build.jenkins_build_url = build_url
            db.commit()

            final_result = None
            for logs, result in jenkins.watch_build(build_url):
                build.logs = logs
                db.commit()
                final_result = result

            build.logs = jenkins.get_console_text(build_url)
            build.status = (
                BuildStatus.SUCCESS.value
                if final_result == "SUCCESS"
                else BuildStatus.FAILED.value
            )
            if build.status == BuildStatus.FAILED.value:
                build.gemini_explanation = gemini.explain_failure(build.logs)
                GEMINI_EXPLANATIONS.inc()
                BUILD_FAILURE.inc()
            else:
                BUILD_SUCCESS.inc()
                self._deploy_preview_if_enabled(db, build, preview)
            db.commit()
        except Exception as exc:
            JENKINS_TRIGGER_ERRORS.inc()
            build = db.get(Build, build_id)
            if build:
                build.status = BuildStatus.FAILED.value
                build.logs = f"{build.logs or ''}\n\nRepo2Docker backend error: {exc}".strip()
                build.gemini_explanation = gemini.explain_failure(build.logs)
                GEMINI_EXPLANATIONS.inc()
                BUILD_FAILURE.inc()
                db.commit()
        finally:
            ACTIVE_BUILDS.dec()
            BUILD_DURATION.observe(monotonic() - started_at)
            db.close()

    def build_commands(self, build: Build) -> tuple[str | None, str | None]:
        if build.status != BuildStatus.SUCCESS.value or not self.settings.dockerhub_username:
            return None, None
        image = f"{self.settings.dockerhub_username}/{build.image_name}:latest"
        return f"docker pull {image}", f"docker run -d -p {build.port}:{build.port} {image}"

    def _deploy_preview_if_enabled(
        self,
        db: Session,
        build: Build,
        preview: KubernetesPreviewService,
    ) -> None:
        if not self.settings.preview_deploy_enabled:
            build.preview_status = "disabled"
            return

        try:
            PREVIEW_DEPLOYMENTS.labels(status="attempted").inc()
            deployment = preview.deploy_preview(build.id, build.image_name, build.port)
            if not deployment:
                build.preview_status = "disabled"
                return
            build.preview_namespace = deployment.namespace
            build.preview_url = deployment.url
            build.preview_status = deployment.status
            RUNNING_PREVIEW_APPS.inc()
            PREVIEW_DEPLOYMENTS.labels(status="created").inc()
            db.commit()
        except Exception as exc:
            build.preview_status = "failed"
            build.logs = (
                f"{build.logs or ''}\n\nPreview deployment warning: {exc}"
            ).strip()
            PREVIEW_DEPLOYMENTS.labels(status="failed").inc()
