import json
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq
from agent.state import AgentState
from agent.tools import search_available_properties, get_listing_details, create_booking
from app.core.config import settings
import os

# Initialize real LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=settings.groq_api_key)

def classify_intent(state: AgentState) -> dict:
    """
    Analyzes the user's message using an LLM to determine intent and extract parameters.
    """
    messages = state["messages"]
    
    system_prompt = """You are an intent classification routing agent for StayEase.
Classify the user's latest message into one of these intents:
1. 'search': User wants to find properties based on location, dates, and guests.
2. 'details': User wants more info about a specific listing (needs a listing ID).
3. 'book': User wants to book a listing.
4. 'escalate': User asks something outside these bounds.

Respond ONLY with a JSON object. No markdown formatting, no other text.
Format:
{
  "intent": "search" | "details" | "book" | "escalate",
  "parameters": {} // Include extracted keys like location, check_in, check_out, guests, listing_id, guest_name if applicable. Leave empty if none.
}
"""
    response = llm.invoke([SystemMessage(content=system_prompt)] + messages)
    
    try:
        content = response.content.replace("```json", "").replace("```", "").strip()
        data = json.loads(content)
        intent = data.get("intent", "escalate")
        params = data.get("parameters", {})
    except Exception as e:
        print("Error parsing LLM response:", response.content)
        intent = "escalate"
        params = {}
    
    return {
        "intent": intent,
        "tool_input": params
    }

def execute_tool(state: AgentState) -> dict:
    """
    Executes the appropriate tool based on the classified intent and extracted parameters.
    """
    intent = state["intent"]
    params = state["tool_input"]
    
    output = None
    try:
        if intent == "search":
            output = search_available_properties.invoke(params)
        elif intent == "details":
            output = get_listing_details.invoke(params)
        elif intent == "book":
            output = create_booking.invoke(params)
    except Exception as e:
        print(f"Tool execution error: {e}")
        output = json.dumps({"error": str(e)})
        
    return {"tool_output": json.loads(output) if output else {}}

def generate_response(state: AgentState) -> dict:
    """
    Generates a natural language response using the LLM based on the tool's raw output.
    """
    intent = state["intent"]
    tool_data = state["tool_output"]
    
    system_prompt = f"""You are the StayEase Agent. The user's intent was '{intent}'.
The system has executed a tool and returned this raw data: {json.dumps(tool_data)}
Write a friendly, helpful natural language response to the user based ONLY on this data. Do not make up information."""

    response = llm.invoke([SystemMessage(content=system_prompt)] + state["messages"])
    
    return {"messages": [AIMessage(content=response.content)]}

def escalate(state: AgentState) -> dict:
    """
    Returns a handoff message to escalate the conversation to a human agent.
    """
    handoff_msg = "I'm sorry, I can only help with searching properties, getting details, and booking. Let me connect you with a human agent who can help."
    return {"messages": [AIMessage(content=handoff_msg)]}
