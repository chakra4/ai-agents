import asyncio
import json
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def main():
    # The endpoint where our FastMCP server is listening for HTTP connections
    url = "http://localhost:8001/mcp"
    print(f"Attempting to connect to MCP server at {url}...")
    
    try:
        # Establish the Streamable HTTP connection
        async with streamable_http_client(url) as (read_stream, write_stream, _):
            print("Connection established. Initializing session...")
            
            # Start the client session
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                print("Session initialized successfully!\n")
                
                # Verify the tool is available
                tools = await session.list_tools()
                tool_names = [t.name for t in tools.tools]
                print(f"Available tools on server: {tool_names}")
                
                if "list_doctors" not in tool_names:
                    print("Error: 'list_doctors' tool not found on the server.")
                    return
                
                # --- Example 1: Call the tool with State and City ---
                print("\n" + "="*50)
                print("Test 1: Calling 'list_doctors' with state='GA', city='Atlanta'")
                print("="*50)
                
                result1 = await session.call_tool("list_doctors", arguments={"state": "GA", "city": "Atlanta"})
                
                for content in result1.content:
                    if content.type == "text":
                        try:
                            # FastMCP typically serializes Python dicts/lists to JSON strings
                            parsed_json = json.loads(content.text)
                            print(json.dumps(parsed_json, indent=2))
                        except json.JSONDecodeError:
                            print(content.text)
                    else:
                        print(f"[{content.type} content]")

                # --- Example 2: Call the tool with only State ---
                print("\n" + "="*50)
                print("Test 2: Calling 'list_doctors' with state='TX'")
                print("="*50)
                
                result2 = await session.call_tool("list_doctors", arguments={"state": "TX"})
                
                for content in result2.content:
                    if content.type == "text":
                        try:
                            parsed_json = json.loads(content.text)
                            print(json.dumps(parsed_json, indent=2))
                        except json.JSONDecodeError:
                            print(content.text)
                    else:
                        print(f"[{content.type} content]")

    except ConnectionRefusedError:
        print(f"\n[!] Connection Refused: Could not connect to {url}")
        print("Please ensure the MCP server is currently running (e.g., `python server.py` in the doctor_mcp directory).")
    except Exception as e:
        print(f"\n[!] An error occurred: {e}")

if __name__ == "__main__":
    # Run the asynchronous main function
    asyncio.run(main())
