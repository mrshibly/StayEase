import uuid
from fastapi import APIRouter, HTTPException, Path
from app.models import MessageRequest, MessageResponse, ChatHistoryResponse, ChatMessage
from agent.graph import build_graph
from langchain_core.messages import HumanMessage
from datetime import datetime

router = APIRouter()

# Instantiate the compiled LangGraph (in a real app, this might be globally initialized)
agent_graph = build_graph()

@router.post("/{conversation_id}/message", response_model=MessageResponse)
async def send_message(
    request: MessageRequest,
    conversation_id: str = Path(..., description="The unique ID of the conversation session")
):
    """
    Process a guest message through the LangGraph AI agent.
    """
    try:
        # In a real app, load existing messages from DB based on conversation_id
        # For skeleton, we create a fresh state
        initial_state = {
            "messages": [HumanMessage(content=request.message)],
            "intent": None,
            "tool_input": None,
            "tool_output": None,
            "conversation_id": conversation_id
        }
        
        # Invoke the graph
        final_state = agent_graph.invoke(initial_state)
        
        # Extract the last message (agent response)
        last_message = final_state["messages"][-1].content
        intent = final_state.get("intent")
        tool_data = final_state.get("tool_output")
        
        # In a real app, save updated state/messages to DB
        
        return MessageResponse(
            response=last_message,
            intent=intent,
            data=tool_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{conversation_id}/history", response_model=ChatHistoryResponse)
async def get_history(
    conversation_id: str = Path(..., description="The unique ID of the conversation session")
):
    """
    Retrieve the message history for a specific conversation session.
    """
    # Skeleton logic: Fetch from DB using conversation_id
    # If not found -> raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Mock response
    mock_history = [
        ChatMessage(role="user", content="I need a room in Cox's Bazar", timestamp=datetime.now()),
        ChatMessage(role="agent", content="I found 2 properties...", timestamp=datetime.now())
    ]
    
    return ChatHistoryResponse(
        conversation_id=conversation_id,
        messages=mock_history
    )
