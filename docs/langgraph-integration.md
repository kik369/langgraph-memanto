# LangGraph Integration with Memanto

## Overview

This guide explains how to integrate LangGraph with Memanto for building stateful AI agents with persistent memory.

## Installation

```bash
pip install memanto langgraph
```

## Why Integrate?

Memanto provides persistent, scalable storage for LangGraph workflows, enabling:

- Cross-session memory persistence
- Stateful agent conversations
- Checkpointing and recovery
- Integration with existing Memanto functions

## Basic Example

```python
from memanto import Memanto
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    messages: List[Dict[str, str]]
    memory: Dict[str, Any]

# Initialize Memanto
memanto = Memanto()

def agent_node(state):
    # Get or create Memanto instance
    if 'memanto_instance' not in state:
        state['memanto_instance'] = Memanto()
    memanto = state['memanto_instance']
    
    # Process user input
    user_input = state.get('messages', [{}])[-1].get('content', '')
    
    # Store in Memanto
    if user_input:
        memanto.save("conversation", {
            "input": user_input,
            "timestamp": str(time.time())
        })
    
    # Generate response
    response = f"AI response to: {user_input}"
    
    # Update state
    new_messages = list(state.get('messages', []))
    new_messages.append({"role": "assistant", "content": response})
    
    return {
        **state,
        "messages": new_messages,
        "response": response,
        "memory": memanto.load_all()
    }

# Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    lambda x: END if len([m for m in x.get('messages', []) if m.get('role') == 'assistant']) >= 3
                else "agent",
    {
        "agent": "agent",
        END: END
    }
)

app = workflow.compile()
```

## Benefits

✅ Persistent memory across sessions
✅ Stateful workflows with automatic checkpointing
✅ Scalable storage for conversation histories
✅ Easy integration with existing Memanto functions

## Resources

- Memanto Documentation: https://memanto.dev/docs
- LangGraph Documentation: https://langchain-ai.github.io/langgraph/
- Memanto GitHub: https://github.com/moorcheh-ai/memanto
