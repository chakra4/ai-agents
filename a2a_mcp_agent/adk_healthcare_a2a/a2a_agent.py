import asyncio
import os
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.a2a.utils.agent_to_a2a import to_a2a
import uvicorn

async def create_agent():
    # 1. Configure the connection to the remote MCP Server
    # The server URL is configurable via environment variable
    mcp_url = os.getenv("MCP_SERVER_URL", "http://0.0.0.0:8081/mcp")
    print(f"Connecting to MCP Server at: {mcp_url}")
    
    connection_params = StreamableHTTPConnectionParams(
        url=mcp_url
    )

    # 2. Create the McpToolset
    mcp_toolset = McpToolset(
        connection_params=connection_params
    )

    # 3. Define the ADK Agent
    # Note: Ensure GOOGLE_API_KEY is set in your environment
    doctor_agent = LlmAgent(
        name="DoctorFinderAgent",
        model="gemini-3.5-flash",
        instruction=""" You are a specialized Medical Directory Assistant. 
        Your goal is to help users find doctors based on their location (State and City).
        Use the 'list_doctors' tool to fetch accurate information.
        If no doctors are found, politely inform the user.
        Always provide the doctor's name, specialty, and contact information if available.
        """,
        tools=[mcp_toolset]
    )

    return doctor_agent

# For A2A deployment, we wrap the agent in an A2A-compliant FastAPI app
doctor_agent = asyncio.run(create_agent())
app = to_a2a(doctor_agent, port=8082)

if __name__ == "__main__":
    # Start the A2A Agent server on port 8082
    print("Starting A2A Agent on http://0.0.0.0:8082")
    uvicorn.run(app, host="0.0.0.0", port=8082)
