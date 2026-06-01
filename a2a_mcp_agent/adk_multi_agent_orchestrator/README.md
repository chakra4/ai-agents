# Multi-Agent Orchestrator (Local)

This orchestrator uses Google ADK's `RemoteA2aAgent` class to coordinate between two specialized agents running locally.

## Architecture

The orchestrator runs as a local Python script and connects to remote A2A agents:

```
┌─────────────────────────────────────────┐
│   Multi-Agent Orchestrator (Local)      │
│   - Coordinates between remote agents   │
│   - Routes requests intelligently       │
└──────────┬──────────────────────────────┘
           │
     ┌─────┴──────┐
     │            │
┌────▼──────┐  ┌──▼────────────┐
│ DoctorFinder│  │WebSearch      │
│ Agent (8082) │  │ Agent (8083)   │
└─────────────┘  └────────────────┘
```

## Running Locally

### 1. Start the DoctorFinderAgent (Terminal 1)
```bash
cd healthcare_a2a
python a2a_agent.py
# Server runs on http://0.0.0.0:8082
```

### 2. Start the WebSearchAgent (Terminal 2)
```bash
cd langgraph_a2a
python stock_search_a2a.py
# Server runs on http://0.0.0.0:8083
```

### 3. Run the orchestrator locally (Terminal 3)
```bash
cd adk_multi_agent_orchestrator
python orchestrator.py
```

The orchestrator will process the query and delegate to the appropriate remote agents.

## Usage

Modify the `if __name__ == "__main__":` block in `orchestrator.py` to test different queries:

```python
# Example medical query
user_query = "Find a cardiologist in New York"
asyncio.run(run_orchestrator(user_query))

# Example financial query
user_query = "What's the stock price of AAPL?"
asyncio.run(run_orchestrator(user_query))

# Example combined query
user_query = "Find a doctor in California and check healthcare stock prices"
asyncio.run(run_orchestrator(user_query))
```

## Programmatic Usage

Import and use the orchestrator in your own scripts:

```python
from orchestrator import run_orchestrator
import asyncio

result = asyncio.run(run_orchestrator("Your query here"))
```

## Key Features

- **No HTTP exposure**: Runs locally without exposing endpoints
- **Intelligent routing**: Routes requests to appropriate agents
- **Easy testing**: Modify the query and run directly
- **Flexible integration**: Can be imported and used in other scripts

## Dependencies

Requires:
- `google-adk-agents`
- `google-adk-a2a`

Install with:
```bash
pip install -r requirements.txt
```
