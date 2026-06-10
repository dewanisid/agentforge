from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints.auth import router as auth_router

app = FastAPI(
    title=settings.app_name,
    description="Multi-agent research and task automation API",
    version=settings.app_version,
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": settings.app_version}
