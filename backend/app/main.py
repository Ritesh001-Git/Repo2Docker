from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.builds import router as builds_router
from app.config import get_settings
from app.database import init_db


settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(builds_router)
