# Healthcare A2A Agent

This is an Agent-to-Agent (A2A) compatible AI assistant built using the [Google Agent Development Kit (ADK)](https://adk.dev). It acts as a Medical Directory Assistant, utilizing a remote Model Context Protocol (MCP) server (`doctor_mcp`) as a tool to find doctors by state and city.

The agent is exposed as an A2A service on port `8082`.

## Prerequisites

- **Python 3.12+** (for local execution)
- **Docker** (for containerized execution)
- A valid **Google API Key** for access to Gemini models.
- The **`doctor_mcp`** server must be running (expected by default at `http://0.0.0.0:8081/mcp`).

---

## Running Locally

1. **Navigate to the directory:**
   ```bash
   cd healthcare_a2a
   ```

2. **Set up a virtual environment and install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set your environment variables:**
   ```bash
   export GOOGLE_API_KEY="your_google_api_key_here"
   
   # Override the MCP server URL if it's running elsewhere
   export MCP_SERVER_URL=http://0.0.0.0:8081/mcp
   ```

4. **Run the agent:**
   ```bash
   python a2a_agent.py
   ```
   The agent will start and listen on `http://0.0.0.0:8082`.

---

## Running in Docker

1. **Navigate to the directory and build the Docker image:**
   ```bash
   cd healthcare_a2a
   docker build -t healthcare-a2a-agent .
   ```

2. **Run the container:**
   *Note: If your `doctor_mcp` server is running locally on your host machine, the Docker container cannot access it via `localhost`. You must use `host.docker.internal` (on macOS/Windows) or the host's IP address (on Linux) to route traffic from the container to the host.*

   ```bash
   docker run -p 8082:8082 \
     -e GOOGLE_API_KEY="your_google_api_key_here" \
     -e MCP_SERVER_URL="http://0.0.0.0:8081/mcp" \
     healthcare-a2a-agent
   ```

---

## Endpoints

Once the agent is running (either locally or in Docker), it acts as an A2A server. 

You can view its **Agent Card** (which describes its metadata, capabilities, and endpoints to other orchestrator agents) by visiting:
- `http://0.0.0.0:8082/.well-known/agent.json`

---

## Troubleshooting & Debugging

If you encounter the following error when starting the A2A agent:
> `RuntimeError: Failed to build agent card for DoctorFinderAgent: Failed to create MCP session...`

This means the A2A agent cannot reach the `doctor_mcp` server during startup. The agent requires the MCP server to be active so it can discover its tools and build the Agent Card.

**Steps to Debug:**

1. **Verify the MCP Server is running:**
   Open a separate terminal and ensure the server is active:
   ```bash
   cd ../doctor_mcp
   python server.py
   ```
   *Note: Ensure you have installed the required dependencies for the server, specifically `fastmcp` (`pip install fastmcp mcp`).*

2. **Test the MCP Endpoint:**
   You can verify the MCP server is listening by running a simple curl command. It should return a `406 Not Acceptable` (because it expects a specific event-stream header), which confirms the server is alive and responding:
   ```bash
   curl -v http://0.0.0.0:8081/mcp
   ```

3. **Check Docker Networking (If running in Docker):**
   If the A2A agent is in a Docker container but the MCP server is on your local host machine, the container cannot reach it via `localhost`. Ensure you passed the correct environment variable to the Docker container:
   ```bash
   -e MCP_SERVER_URL="http://0.0.0.0:8081/mcp"
   ```
   *(Use `host.docker.internal` for Mac/Windows, or your machine's actual IP address for Linux).*
