from typing import TypedDict, Annotated, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    Represents the state of the LangGraph agent.
    
    Fields:
    - messages: Conversation history and intermediate tool outputs.
    - intent: The classified intent of the user ("search", "details", "book", "escalate").
    - tool_input: Extracted parameters for the tool to execute.
    - tool_output: The raw output returned by the executed tool.
    - conversation_id: A unique ID linking messages to a specific session.
    """
    messages: Annotated[list[BaseMessage], add_messages]
    intent: Optional[str]
    tool_input: Optional[dict]
    tool_output: Optional[dict]
    conversation_id: str
