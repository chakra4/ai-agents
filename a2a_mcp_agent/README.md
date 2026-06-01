# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project Architecture (Non-Obvious)

This is a **multi-agent A2A system** with 4 independent components that must run separately:
- `doctor_mcp/` - MCP server (port 8081) - MUST start BEFORE healthcare agent
- `adk_healthcare_a2a/` - ADK agent (port 8082) - depends on MCP server being live
- `langgraph_websearch_a2a/` - LangGraph agent (port 8083)
- `adk_multi_agent_orchestrator/` - Local orchestrator (no port) - connects to 8082 & 8083

**Critical startup order**: MCP server → Healthcare agent → Web search agent → Orchestrator

## Package Manager

**Use `uv` for all Python package management** across all directories:
- Install dependencies: `uv pip install -r requirements.txt`
- Run Python scripts: `uv run python script.py`
- Create virtual environments: `uv venv`

## Running Components

Each component runs independently in its own terminal:

```bash
# Terminal 1: MCP Server (MUST start first)
cd doctor_mcp && uv run python server.py

# Terminal 2: Healthcare A2A Agent (requires MCP server running)
cd adk_healthcare_a2a && uv run python a2a_agent.py

# Terminal 3: Web Search A2A Agent
cd langgraph_websearch_a2a && uv run python web_search_a2a.py

# Terminal 4: Orchestrator (requires agents 8082 & 8083 running)
cd adk_multi_agent_orchestrator && uv run python orchestrator.py
```

## Non-Obvious Patterns

### MCP Server Dependency
- Healthcare agent (`a2a_agent.py`) **fails at startup** if MCP server not running
- Error: `RuntimeError: Failed to build agent card for DoctorFinderAgent`
- Agent builds its card by discovering MCP tools during initialization (not lazy)
- MCP server URL configurable via `MCP_SERVER_URL` env var (default: `http://0.0.0.0:8081/mcp`)

### Docker Networking Gotcha
- When healthcare agent runs in Docker but MCP server on host: use `host.docker.internal` (Mac/Windows) or host IP (Linux)
- Cannot use `localhost` from inside container to reach host services

### Agent Initialization Patterns
- **ADK agents**: Use `asyncio.run(create_agent())` at module level, then wrap with `to_a2a()`
- **LangGraph agents**: Lazy initialization in `ProviderAgentExecutor._ensure_initialized()` to avoid async in `__init__`

### Port Assignments (Fixed)
- 8081: MCP server (FastMCP HTTP transport)
- 8082: Healthcare A2A agent (ADK)
- 8083: Web search A2A agent (LangGraph)
- Orchestrator: No port (local script only)

### A2A Agent Cards
- Accessible at `http://HOST:PORT/.well-known/agent.json`
- Orchestrator uses these URLs to discover agent capabilities
- Healthcare agent card built from MCP tool discovery (requires MCP server live)

### Environment Variables
- `GOOGLE_API_KEY` - Required for all ADK/LangGraph agents using Gemini
- `MCP_SERVER_URL` - Healthcare agent only (default: `http://0.0.0.0:8081/mcp`)
- `OPENAI_API_KEY` - Required for LangGraph web search agent (uses GPT-4o)
- `TAVILY_API_KEY` - Required for LangGraph web search tool

### Testing MCP Server
```bash
# Should return 406 Not Acceptable (confirms server alive)
curl -v http://0.0.0.0:8081/mcp
```

## Code Conventions

### Agent Creation Pattern (ADK)
```python
# Module-level async initialization (not in __init__)
doctor_agent = asyncio.run(create_agent())
app = to_a2a(doctor_agent, port=8082)
```

### Agent Creation Pattern (LangGraph)
```python
# Lazy initialization to avoid async in __init__
class ProviderAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent = None  # Don't initialize here
    
    def _ensure_initialized(self):
        if self.agent is None:
            self.agent = MyAgent()  # Initialize on first use
```

### MCP Tool Integration
- Use `McpToolset` with `StreamableHTTPConnectionParams` for remote MCP servers
- MCP tools automatically discovered and added to agent capabilities
- Tool discovery happens during agent initialization (not runtime)

## Debugging
### MCP Server Debugging
Add the doctor_mcp configuration to the GeminiCLI config file (.gemini/settings.json):
{
  "mcpServers": {
    "dmcp": {
      "url": "http://localhost:8081/mcp",
      "type": "http"
    }
  }
}
Test the MCP tools from GeminiCLI chat

### Check the Agent Cards
Healthcare A2A agent (ADK): http://127.0.0.1:8082/.well-known/agent.json
Web search A2A agent (LangGraph): http://127.0.0.1:8083/.well-known/agent.json