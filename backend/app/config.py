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

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
