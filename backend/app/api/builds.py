from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.schemas import BuildCreate, BuildCreated, BuildLogsResponse, BuildStatusResponse
from app.services.build_service import BuildService


router = APIRouter()


def get_build_service() -> BuildService:
    return BuildService(get_settings())


@router.post("/build", response_model=BuildCreated)
def create_build(
    payload: BuildCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    service: BuildService = Depends(get_build_service),
):
    build = service.create_build(db, payload)
    background_tasks.add_task(service.run_build, build.id)
    return BuildCreated(build_id=build.id, status=build.status)


@router.get("/status/{build_id}", response_model=BuildStatusResponse)
def get_status(
    build_id: int,
    db: Session = Depends(get_db),
    service: BuildService = Depends(get_build_service),
):
    build = service.get_build(db, build_id)
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    return build


@router.get("/logs/{build_id}", response_model=BuildLogsResponse)
def get_logs(
    build_id: int,
    db: Session = Depends(get_db),
    service: BuildService = Depends(get_build_service),
):
    build = service.get_build(db, build_id)
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    pull_command, run_command = service.build_commands(build)
    return BuildLogsResponse(
        id=build.id,
        status=build.status,
        logs=build.logs or "",
        gemini_explanation=build.gemini_explanation,
        pull_command=pull_command,
        run_command=run_command,
    )
