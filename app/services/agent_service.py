from agent.graph import build_graph
from langchain_core.messages import HumanMessage
from datetime import datetime

class AgentService:
    def __init__(self):
        self.agent_graph = build_graph()
        
    def process_message(self, conversation_id: str, message: str) -> dict:
        """
        Processes a single message through the LangGraph agent.
        """
        initial_state = {
            "messages": [HumanMessage(content=message)],
            "intent": None,
            "tool_input": None,
            "tool_output": None,
            "conversation_id": conversation_id
        }
        
        final_state = self.agent_graph.invoke(initial_state)
        
        return {
            "response": final_state["messages"][-1].content,
            "intent": final_state.get("intent"),
            "data": final_state.get("tool_output")
        }

    def get_chat_history(self, conversation_id: str) -> list:
        """
        Retrieves the chat history for a specific conversation session.
        """
        # Mock history retrieval logic
        return [
            {
                "role": "user",
                "content": "I need a room in Cox's Bazar",
                "timestamp": datetime.now()
            },
            {
                "role": "agent",
                "content": "I found 2 properties...",
                "timestamp": datetime.now()
            }
        ]

agent_service = AgentService()
