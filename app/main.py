from fastapi import FastAPI
from app.routes import chat

app = FastAPI(
    title="StayEase AI Agent API",
    description="API for the StayEase conversational AI agent powered by LangGraph.",
    version="1.0.0"
)

# Include the chat routes
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

@app.get("/health")
async def health_check():
    """
    Basic health check endpoint.
    """
    return {"status": "healthy"}
