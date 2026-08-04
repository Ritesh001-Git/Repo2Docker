from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl, field_validator


class BuildCreate(BaseModel):
    repository_url: HttpUrl
    image_name: str = Field(min_length=1, max_length=255)
    port: int = Field(ge=1, le=65535)

    @field_validator("image_name")
    @classmethod
    def validate_image_name(cls, value: str) -> str:
        cleaned = value.strip().lower()
        allowed = set("abcdefghijklmnopqrstuvwxyz0123456789._-")
        if any(char not in allowed for char in cleaned):
            raise ValueError("Use only lowercase letters, numbers, dots, underscores, and dashes.")
        return cleaned

    @field_validator("repository_url")
    @classmethod
    def validate_github_url(cls, value: HttpUrl) -> HttpUrl:
        if value.host not in {"github.com", "www.github.com"}:
            raise ValueError("Repository URL must be a public GitHub URL.")
        return value


class BuildCreated(BaseModel):
    build_id: int
    status: str


class BuildStatusResponse(BaseModel):
    id: int
    repository_url: str
    image_name: str
    port: int
    status: str
    created_at: datetime
    updated_at: datetime


class BuildLogsResponse(BaseModel):
    id: int
    status: str
    logs: str
    gemini_explanation: str | None = None
    pull_command: str | None = None
    run_command: str | None = None
