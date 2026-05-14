"""
LangGraph + Memanto Integration Example
Demonstrates cross-session memory persistence for LangGraph agents.
"""

import time
from typing import TypedDict, List, Dict, Any
from memanto import Memanto
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    messages: List[Dict[str, str]]
    session_id: str
    memory_summary: str

# Initialize Memanto for persistent storage
memanto = Memanto(namespace="langgraph_example")

def chatbot_node(state: AgentState) -> AgentState:
    """Process user input and store in Memanto."""
    # Get the latest user message
    user_msg = state["messages"][-1] if state["messages"] else {"content": ""}
    user_input = user_msg.get("content", "")
    
    if user_input.strip():
        # Store in Memanto with timestamp
        memanto.save(f"conversation_{state['session_id']}", {
            "input": user_input,
            "timestamp": time.time(),
            "response": ""  # Will be filled after processing
        })
    
    # Simple echo bot for demonstration
    response = f"You said: {user_input}"
    
    # Update the stored conversation with response
    if user_input.strip():
        memanto.save(f"conversation_{state['session_id']}", {
            "input": user_input,
            "timestamp": time.time(),
            "response": response
        })
    
    # Get memory summary
    all_memories = memanto.load_all()
    memory_count = len(all_memories) if isinstance(all_memories, dict) else 0
    
    return {
        **state,
        "messages": state["messages"] + [{"role": "assistant", "content": response}],
        "memory_summary": f"Stored {memory_count} interactions in persistent memory"
    }

def should_continue(state: AgentState) -> bool:
    """Continue after 3 exchanges."""
    return len(state["messages"]) < 6  # 3 user + 3 assistant messages

# Build the workflow
workflow = StateGraph(AgentState)
workflow.add_node("chatbot", chatbot_node)
workflow.set_entry_point("chatbot")
workflow.add_conditional_edges(
    "chatbot",
    should_continue,
    {
        True: "chatbot",
        False: END
    }
)

app = workflow.compile()

if __name__ == "__main__":
    # Example usage
    initial_state = {
        "messages": [{"role": "user", "content": "Hello, I'm testing persistent memory!"}],
        "session_id": "demo_session_001",
        "memory_summary": ""
    }
    
    result = app.invoke(initial_state)
    print("Final state:", result)
