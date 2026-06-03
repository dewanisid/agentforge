from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title = "AgentForge",
    description = "Multi-agent research and task automation API",
    version = "0.1.0",
)

@app.get("/health")
def health_check():
    return {"status": "ok", "version": app.version}