from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class BuildStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class Build(Base):
    """SQLite record for each requested Docker image build."""

    __tablename__ = "builds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    repository_url: Mapped[str] = mapped_column(String(500), nullable=False)
    image_name: Mapped[str] = mapped_column(String(255), nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default=BuildStatus.QUEUED.value)
    logs: Mapped[str] = mapped_column(Text, default="")
    gemini_explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    jenkins_queue_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    jenkins_build_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
