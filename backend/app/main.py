from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from time import monotonic

from app.api.builds import router as builds_router
from app.config import get_settings
from app.database import init_db
from app.services.metrics_service import HTTP_REQUEST_DURATION
from app.services.tracing_service import configure_tracing


settings = get_settings()

app = FastAPI(title=settings.app_name)
configure_tracing(app, settings)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def observe_requests(request, call_next):
    started_at = monotonic()
    response = await call_next(request)
    if not request.url.path.startswith("/metrics"):
        HTTP_REQUEST_DURATION.labels(
            method=request.method,
            path=request.url.path,
            status_code=str(response.status_code),
        ).observe(monotonic() - started_at)
    return response


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(builds_router)
app.mount("/metrics", make_asgi_app())
