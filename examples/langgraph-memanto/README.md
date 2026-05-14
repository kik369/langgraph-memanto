# LangGraph + Memanto Integration Example

This example demonstrates how to use Memanto as a persistent memory layer for LangGraph agents.

## Features
- Cross-session memory persistence
- Automatic storage of conversations
- Simple LangGraph workflow integration

## Usage
```python
from langgraph_memanto_example import app

initial_state = {
    "messages": [{"role": "user", "content": "Hello!"}],
    "session_id": "unique_session_id",
    "memory_summary": ""
}

result = app.invoke(initial_state)
```

## Technical Details
- Uses Memanto namespace: `langgraph_example`
- Stores conversations with timestamps
- Demonstrates cross-session recall capability
