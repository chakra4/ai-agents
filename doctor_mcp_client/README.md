# Doctor MCP Client

This is a simple Python client that connects to the `doctor_mcp` server over Streamable HTTP and executes the `list_doctors` tool.

## Prerequisites

1.  Make sure the **Doctor Search Server** is running on port 8001. 
    You can start it by going to the `doctor_mcp` directory and running:
    ```bash
    python server.py
    ```
    *(Or using the Docker instructions provided in that directory)*.

2.  Python 3.9+ is installed on your machine.

## Setup & Run

**Step 1: Install Dependencies**
It is recommended to use a virtual environment, but you can install the `mcp` library directly:
```bash
pip install -r requirements.txt
```

**Step 2: Run the Client**
With the server running in another terminal tab/window, execute:
```bash
python client.py
```

## What the Script Does
1. Connects to `http://localhost:8001/mcp`.
2. Initializes the Model Context Protocol (MCP) session.
3. Asks the server for a list of available tools.
4. Makes two test calls to the `list_doctors` tool:
   - Queries for doctors in **Atlanta, GA**.
   - Queries for doctors anywhere in **TX**.
5. Receives and pretty-prints the JSON results from the server.
