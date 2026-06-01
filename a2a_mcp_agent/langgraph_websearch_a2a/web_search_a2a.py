# Build a LangGraph Agent
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

# Wrap in A2A Server
from dotenv import load_dotenv
import os
import uvicorn
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps import A2AStarletteApplication
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from a2a.utils import new_agent_text_message


# Build a LangGraph Agent
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

tools = [TavilySearchResults(max_results=2)]
prompt = """You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow up question, you are allowed to do that!
"""
model = ChatOpenAI(model="gpt-4o")

class MyAgent:
    def __init__(self):
        self.system = prompt
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges("llm", self.exists_action, {True: "action", False: END})
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def call_openai(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Back to the model!")
        return {'messages': results}

    async def answer_query(self, human_prompt: str) -> str:
        if self.graph is None:
            raise RuntimeError("""Agent not initialized. Call initialize() first.""")
        
        response = await self.graph.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": human_prompt,
                    }
                ]
            }
        )
        return response["messages"][-1].content

# langGraph Main
#async def main():
#    agent = MyAgent()
#    result =  await agent.answer_query("What is the current stock price of IBM and Microsoft?")
#    print(result)


# Wrap in A2A Server
class ProviderAgentExecutor(AgentExecutor):
    """This is an agent for finding healthcare providers based on location and specialty."""
    
    def __init__(self) -> None:
        # Don't await in __init__ - it's not async
        self.agent = None
    
    def _ensure_initialized(self) -> None:
        """Lazy initialization of the agent."""
        if self.agent is None:
            self.agent = MyAgent()
    
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        self._ensure_initialized()
        
        prompt = context.get_user_input()
        response = await self.agent.answer_query(prompt)
        await event_queue.enqueue_event(new_agent_text_message(response))
    
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        pass

def main():
    print("Running Web Search Agent")
    load_dotenv()
    
    HOST = os.environ.get("AGENT_HOST", "0.0.0.0")
    PORT = int(os.environ.get("PROVIDER_AGENT_PORT", 8083))
    
    skill = AgentSkill(
        id="research_assistant",
        name="Web Search Agent",
        description="Searches the web for information based on user queries.",
        tags=["search", "information", "web"],

        examples=[
            "What is the current stock price of IBM and Microsoft?",
            "What is the capital of France?",
        ],
    )
    
    agent_card = AgentCard(
        name="WebSearchAgent",
        description="An agent that can search the web for information based on a user's query.",
        url=f"http://{HOST}:{PORT}/",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=False),
        skills=[skill],
    )
    
    request_handler = DefaultRequestHandler(
        agent_executor=ProviderAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )
    
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )
    
    uvicorn.run(server.build(), host=HOST, port=PORT)

if __name__ == "__main__":
    #import asyncio
    #asyncio.run(main())
    main()