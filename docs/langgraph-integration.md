# LangGraph Integration with Memanto

## Overview

This guide explains how to integrate LangGraph with Memanto for building stateful AI workflows with persistent memory.

## Installation

```bash
pip install memanto langgraph
```

## Basic Usage

### Example: Agent with Persistent Memory

```python
from memanto import Memanto
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    messages: List[Dict[str, str]]
    memory: Dict[str, Any]

async def agent_node(state):
    memanto = Memanto()
    user_input = state["messages"][-1]["content"] if state["messages"] else ""
    
    # Save to Memanto
    memanto.save("conversation", {
        "input": user_input,
        "timestamp": str(time.time())
    })
    
    # Generate response
    response = f"Processed: {user_input}"
    
    state["messages"].append({"role": "assistant", "content": response})
    state["memory"] = memanto.load_all()
    
    return state

# Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("agent_node", agent_node)
workflow.set_entry_point("agent_node")
workflow.add_conditional_edges(
    "agent_node",
    lambda x: END if len(x["messages"]) > 10 else "agent_node",
    {
        "agent_node": "agent_node",
        END: END
    }
)

app = workflow.compile()
```

## Benefits

- Persistent memory across sessions
- Stateful workflows with automatic checkpointing
- Simple integration with existing Memanto functions

## Resources

- Memanto Documentation: https://memanto.dev/docs
- LangGraph Documentation: https://langchain-ai.github.io/langgraph/
