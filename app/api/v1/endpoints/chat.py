from fastapi import APIRouter, HTTPException, Path
from app.schemas.chat import MessageRequest, MessageResponse, ChatHistoryResponse
from app.services.agent_service import agent_service

router = APIRouter()

@router.post("/{conversation_id}/message", response_model=MessageResponse)
async def send_message(
    request: MessageRequest,
    conversation_id: str = Path(..., description="The unique ID of the conversation session")
):
    """
    Process a guest message through the LangGraph AI agent.
    """
    try:
        result = agent_service.process_message(conversation_id, request.message)
        return MessageResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{conversation_id}/history", response_model=ChatHistoryResponse)
async def get_history(
    conversation_id: str = Path(..., description="The unique ID of the conversation session")
):
    """
    Retrieve the message history for a specific conversation session.
    """
    try:
        history = agent_service.get_chat_history(conversation_id)
        return ChatHistoryResponse(conversation_id=conversation_id, messages=history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
