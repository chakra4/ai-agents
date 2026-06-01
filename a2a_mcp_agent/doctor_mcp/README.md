# Doctor Search MCP Server

This is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server built using the `FastMCP` framework. It provides a `list_doctors` tool that allows an LLM to query a local database (`doctors.json`) and filter doctors by state and/or city.

## Prerequisites

- Python 3.9 or higher (for running locally)
- Docker (for running via container)

## Tools Provided

### `list_doctors`
Returns a list of doctors filtered by state and/or city.
- `state` (optional): The US state code to filter by (e.g., 'GA', 'TX').
- `city` (optional): The city name to filter by (e.g., 'Atlanta', 'Houston').

---

## 1. Running from the Command Line (Locally)

It is recommended to use a virtual environment to manage dependencies.

**Step 1: Create and activate a virtual environment (optional but recommended)**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

**Step 2: Install the required dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: Run the server**
```bash
python server.py
```

*Note: The server is now configured to run using **Streamable HTTP** transport on **port 8081**. You can access the MCP endpoint at `http://localhost:8081/mcp`.*

---

## 2. Running with Docker

Running with Docker ensures the environment is isolated and contains all necessary dependencies.

**Step 1: Build the Docker image**
```bash
docker build -t doctor-mcp-server .
```

**Step 2: Run the Docker container**
Since the server runs on port 8081, you must map the container's port to your host machine:
```bash
docker run -p 8081:8081 doctor-mcp-server
```

---

## Using with Claude Desktop

To use this server with Claude Desktop, you need to add it to your Claude Desktop configuration file (e.g., `claude_desktop_config.json`).

### Using Streamable HTTP:
```json
{
  "mcpServers": {
    "doctor-search": {
      "url": "http://localhost:8081/mcp"
    }
  }
}
```
