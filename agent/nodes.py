import json
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from agent.state import AgentState
from agent.tools import search_available_properties, get_listing_details, create_booking

# Mock LLM for skeleton - normally we'd import and call Groq here
def _mock_llm_call(messages: list) -> str:
    # Basic keyword routing for skeleton simulation
    last_msg = messages[-1].content.lower()
    if "search" in last_msg or "find" in last_msg or "room" in last_msg:
        return json.dumps({"intent": "search", "parameters": {"location": "Cox's Bazar", "check_in": "2026-05-01", "check_out": "2026-05-03", "guests": 2}})
    elif "detail" in last_msg or "tell me about" in last_msg:
        return json.dumps({"intent": "details", "parameters": {"listing_id": 1}})
    elif "book" in last_msg or "reserve" in last_msg:
        return json.dumps({"intent": "book", "parameters": {"listing_id": 1, "guest_name": "John Doe", "check_in": "2026-05-01", "check_out": "2026-05-03", "guests": 2}})
    else:
        return json.dumps({"intent": "escalate", "parameters": {}})

def classify_intent(state: AgentState) -> dict:
    """
    Analyzes the user's message using an LLM to determine intent and extract parameters.
    """
    messages = state["messages"]
    # In a real app: response = llm.invoke([SystemMessage(content="Classify intent into: search, details, book, escalate")] + messages)
    
    response_json = _mock_llm_call(messages)
    data = json.loads(response_json)
    
    return {
        "intent": data["intent"],
        "tool_input": data.get("parameters", {})
    }

def execute_tool(state: AgentState) -> dict:
    """
    Executes the appropriate tool based on the classified intent and extracted parameters.
    """
    intent = state["intent"]
    params = state["tool_input"]
    
    output = None
    if intent == "search":
        output = search_available_properties.invoke(params)
    elif intent == "details":
        output = get_listing_details.invoke(params)
    elif intent == "book":
        output = create_booking.invoke(params)
        
    return {"tool_output": json.loads(output) if output else {}}

def generate_response(state: AgentState) -> dict:
    """
    Generates a natural language response using the LLM based on the tool's raw output.
    """
    intent = state["intent"]
    tool_data = state["tool_output"]
    
    # In a real app: response = llm.invoke(...)
    # Mocking response generation based on intent
    if intent == "search":
        num_found = len(tool_data) if isinstance(tool_data, list) else 0
        reply = f"I found {num_found} properties available for your dates. Here they are..."
    elif intent == "details":
        reply = f"Here are the details for {tool_data.get('title', 'the property')}..."
    elif intent == "book":
        reply = f"Great! Your booking (ID: {tool_data.get('booking_id')}) is confirmed."
    else:
        reply = "I've processed your request."
        
    return {"messages": [AIMessage(content=reply)]}

def escalate(state: AgentState) -> dict:
    """
    Returns a handoff message to escalate the conversation to a human agent.
    """
    handoff_msg = "I'm sorry, I can only help with searching properties, getting details, and booking. Let me connect you with a human agent who can help."
    return {"messages": [AIMessage(content=handoff_msg)]}
