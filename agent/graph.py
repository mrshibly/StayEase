from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import classify_intent, execute_tool, generate_response, escalate

def route_intent(state: AgentState) -> str:
    """
    Conditional routing logic based on the classified intent.
    Returns the name of the next node to execute.
    """
    intent = state.get("intent")
    if intent == "escalate":
        return "escalate"
    elif intent in ["search", "details", "book"]:
        return "execute_tool"
    else:
        return "escalate" # Default fallback

def build_graph() -> StateGraph:
    """
    Constructs and returns the compiled LangGraph for the StayEase agent.
    """
    # 1. Initialize graph with state schema
    workflow = StateGraph(AgentState)
    
    # 2. Add nodes
    workflow.add_node("classify_intent", classify_intent)
    workflow.add_node("execute_tool", execute_tool)
    workflow.add_node("generate_response", generate_response)
    workflow.add_node("escalate", escalate)
    
    # 3. Define edges
    # Start -> classify
    workflow.set_entry_point("classify_intent")
    
    # classify -> (conditional) -> tool OR escalate
    workflow.add_conditional_edges(
        "classify_intent",
        route_intent,
        {
            "execute_tool": "execute_tool",
            "escalate": "escalate"
        }
    )
    
    # tool -> generate response
    workflow.add_edge("execute_tool", "generate_response")
    
    # Ends
    workflow.add_edge("generate_response", END)
    workflow.add_edge("escalate", END)
    
    # 4. Compile and return
    return workflow.compile()
