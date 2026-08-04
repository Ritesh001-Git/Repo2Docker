from sqlalchemy.orm import Session

from app.config import Settings
from app.database import SessionLocal
from app.models import Build, BuildStatus
from app.schemas import BuildCreate
from app.services.gemini_service import GeminiService
from app.services.jenkins_service import JenkinsService


class BuildService:
    """Coordinates database updates, Jenkins execution, and Gemini explanations."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def create_build(self, db: Session, payload: BuildCreate) -> Build:
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
            db.commit()
        except Exception as exc:
            build = db.get(Build, build_id)
            if build:
                build.status = BuildStatus.FAILED.value
                build.logs = f"{build.logs or ''}\n\nRepo2Docker backend error: {exc}".strip()
                build.gemini_explanation = gemini.explain_failure(build.logs)
                db.commit()
        finally:
            db.close()

    def build_commands(self, build: Build) -> tuple[str | None, str | None]:
        if build.status != BuildStatus.SUCCESS.value or not self.settings.dockerhub_username:
            return None, None
        image = f"{self.settings.dockerhub_username}/{build.image_name}:latest"
        return f"docker pull {image}", f"docker run -d -p {build.port}:{build.port} {image}"
