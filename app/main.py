from fastapi import FastAPI, Depends
from app.core.config import settings
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.tasks import router as task_router

from app.core.rate_limiter import rate_limit

app = FastAPI(
    title=settings.app_name,
    description="Multi-agent research and task automation API",
    version=settings.app_version,
    dependencies = [Depends(rate_limit)],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(task_router, prefix="/api/v1/tasks", tags=["tasks"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": settings.app_version}
