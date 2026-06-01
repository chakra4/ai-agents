# Stock Price A2A Agent

This is an Agent-to-Agent (A2A) compatible AI assistant built using [LangGraph](https://langchain-ai.github.io/langgraph/) and the [Google Agent Development Kit (ADK)](https://adk.dev). It acts as a Stock Market Assistant that provides real-time stock price information using the Yahoo Finance API (via `yfinance`).

The agent is exposed as an A2A service on port `8083`.

## Features

- **Real-time Stock Prices**: Query current stock prices for any ticker symbol
- **Detailed Information**: Get current price, previous close, day high/low, and volume
- **LangGraph Architecture**: Built with LangGraph for robust state management and tool calling
- **A2A Compatible**: Can be integrated with other A2A agents and orchestrators

## Prerequisites

- **Python 3.12+** (for local execution)
- **Docker** (for containerized execution)
- A valid **Google API Key** for access to Gemini models

---

## Running Locally

1. **Navigate to the directory:**
   ```bash
   cd langgraph_a2a
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
   ```

4. **Run the agent:**
   ```bash
   python web_search_a2.py
   ```
   The agent will start and listen on `http://0.0.0.0:8083`.

---

## Running in Docker

1. **Navigate to the directory and build the Docker image:**
   ```bash
   cd langgraph_a2a
   docker build -t stock-a2a-agent .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8083:8083 \
     -e GOOGLE_API_KEY="your_google_api_key_here" \
     stock-a2a-agent
   ```

---

## Usage Examples

Once the agent is running, you can interact with it through the A2A interface. Here are some example queries:

- "What's the current price of Apple stock?"
- "Get me the stock price for GOOGL"
- "Show me Microsoft stock information"
- "What's TSLA trading at?"

The agent will use the `get_stock_price` tool to fetch real-time data from Yahoo Finance.

---

## Endpoints

Once the agent is running (either locally or in Docker), it acts as an A2A server.

You can view its **Agent Card** (which describes its metadata, capabilities, and endpoints to other orchestrator agents) by visiting:
- `http://0.0.0.0:8083/.well-known/agent.json`

---

## Architecture

The agent is built using LangGraph with the following components:

1. **State Graph**: Manages conversation state and message flow
2. **LLM Node**: Uses Gemini 2.0 Flash for natural language understanding
3. **Tool Node**: Executes the `get_stock_price` tool to fetch stock data
4. **Conditional Edges**: Determines whether to call tools or end the conversation

### Tool: get_stock_price

The agent has access to a `get_stock_price` tool that:
- Accepts a stock ticker symbol (e.g., 'AAPL', 'GOOGL', 'MSFT')
- Fetches real-time data from Yahoo Finance
- Returns current price, previous close, day high/low, and volume

---

## Supported Stock Symbols

The agent supports any valid stock ticker symbol available on Yahoo Finance, including:
- US stocks (e.g., AAPL, GOOGL, MSFT, TSLA)
- International stocks (e.g., NESN.SW, 7203.T)
- ETFs and indices

---

## Troubleshooting

### Error: "GOOGLE_API_KEY environment variable must be set"
Make sure you have set the `GOOGLE_API_KEY` environment variable:
```bash
export GOOGLE_API_KEY="your_google_api_key_here"
```

### Error: "Unable to fetch price for [SYMBOL]"
This usually means:
- The ticker symbol is invalid or not found on Yahoo Finance
- There's a network connectivity issue
- Yahoo Finance API is temporarily unavailable

### Port Already in Use
If port 8083 is already in use, you can modify the port in `stock_agent.py` or use Docker port mapping:
```bash
docker run -p 8084:8083 -e GOOGLE_API_KEY="..." stock-a2a-agent
```

---

## Integration with Other Agents

This A2A agent can be integrated with orchestrator agents (like the ADK Multi-Agent Orchestrator) to provide stock price information as part of a larger multi-agent system.

Example orchestrator configuration:
```python
{
    "name": "StockPriceAgent",
    "url": "http://localhost:8083",
    "description": "Provides real-time stock price information"
}
```

---

## Development

### Project Structure
```
langgraph_a2a/
├── stock_agent.py      # Main agent implementation
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
└── README.md          # This file
```

### Key Dependencies
- `langgraph`: State graph framework for building agents
- `langchain-google-genai`: Google Gemini integration
- `yfinance`: Yahoo Finance API wrapper
- `google-adk`: Google Agent Development Kit for A2A support
- `fastapi` & `uvicorn`: Web server for A2A endpoints

---

## License

This project is part of the Building AI Systems 2026 course materials.