from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central place for environment-driven configuration."""

    app_name: str = "Repo2Docker"
    database_url: str = "sqlite:///./repo2docker.db"

    jenkins_url: str = "http://localhost:8080"
    jenkins_job_name: str = "repo2docker"
    jenkins_username: str = ""
    jenkins_api_token: str = ""
    jenkins_poll_interval_seconds: int = 5
    jenkins_request_timeout_seconds: int = 20

    dockerhub_username: str = ""
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    cors_origins: str = "http://localhost:5173"

    preview_deploy_enabled: bool = False
    preview_base_url: str = "http://localhost"
    preview_namespace_prefix: str = "repo2docker-preview"
    preview_image_pull_policy: str = "Always"
    preview_cpu_request: str = "100m"
    preview_memory_request: str = "128Mi"
    preview_cpu_limit: str = "500m"
    preview_memory_limit: str = "512Mi"
    preview_min_replicas: int = 1
    preview_max_replicas: int = 3
    preview_cpu_target_percentage: int = 70

    otel_tracing_enabled: bool = False
    otel_service_name: str = "repo2docker-backend"
    otel_exporter_otlp_endpoint: str = "http://jaeger-collector.observability.svc.cluster.local:4317"
    otel_exporter_otlp_insecure: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
