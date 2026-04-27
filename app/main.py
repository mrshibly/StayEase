from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="API for the StayEase conversational AI agent powered by LangGraph.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api")

@app.get("/health")
async def health_check():
    """
    Basic health check endpoint.
    """
    return {"status": "healthy"}
