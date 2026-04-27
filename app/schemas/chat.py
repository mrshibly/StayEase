from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class MessageRequest(BaseModel):
    message: str = Field(..., description="The message from the guest.")

class MessageResponse(BaseModel):
    response: str = Field(..., description="The natural language response from the agent.")
    intent: Optional[str] = Field(None, description="The classified intent.")
    data: Optional[Dict[str, Any]] = Field(None, description="Raw data returned from tools, if any.")

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the sender (user, agent, etc.).")
    content: str = Field(..., description="Message content.")
    timestamp: datetime = Field(..., description="Time the message was sent.")

class ChatHistoryResponse(BaseModel):
    conversation_id: str = Field(..., description="Unique conversation ID.")
    messages: List[ChatMessage] = Field(..., description="List of messages in the session.")

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message description.")
