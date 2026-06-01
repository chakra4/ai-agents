# LangGraph Agent Development Environment

This project is set up using `uv` for fast Python package management and virtual environment handling.

## Setup

1. Ensure `uv` is installed (already done).
2. The virtual environment is created at `.venv/`.
3. Dependencies are installed via `uv.lock`.

## Installed Packages

- `langgraph`: Core library for building agents.
- `langchain-core`: Core LangChain components.
- `langchain-openai`: OpenAI integrations.
- `langchain-tavily`: Tavily search integration for web search capabilities.
- `langchain-community`: Community integrations.
- `python-dotenv`: For loading environment variables.

## Running the Project

- Activate the environment: `source .venv/bin/activate` (or use `uv run`).
- Run the main script: `uv run python main.py`.
- For development, use `uv run` to execute commands within the environment.

## Environment Variables

Create a `.env` file and add your API keys, e.g.:

```
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
```
```

Load them in your code using `python-dotenv`.

## Next Steps

- Replace `main.py` with your LangGraph agent code.
- Refer to [LangGraph documentation](https://langchain-ai.github.io/langgraph/) for tutorials.