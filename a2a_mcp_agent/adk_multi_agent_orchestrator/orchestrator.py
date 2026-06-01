import asyncio

from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.runners import InMemoryRunner


async def create_orchestrator():
    """Create an orchestrator that connects to remote A2A agents."""
    
    # 1. Create remote agent references
    doctor_finder_agent = RemoteA2aAgent(
        agent_card="http://0.0.0.0:8082",
        name="DoctorFinderAgent"
    )
    
    web_analyst_agent = RemoteA2aAgent(
        agent_card="http://127.0.0.1:8083",
        name="WebSearchAgent"
    )
    
    # 2. Create the orchestrator agent that can delegate to remote agents
    orchestrator = LlmAgent(
        name="MultiAgentOrchestrator",
        model="gemini-3.5-flash",
        instruction="""You are a multi-agent orchestrator that coordinates between specialized agents.

Available agents:
1. DoctorFinderAgent - Helps find doctors based on location and specialty
2. WebSearchAgent - Searches the web for information

Based on the user's request, determine which agent(s) to delegate to:
- For medical/doctor-related queries, use the DoctorFinderAgent
- For web search queries, use the WebSearchAgent
- For complex requests, coordinate between both agents as needed

Always provide clear, actionable responses and explain which agents you consulted.""",
        sub_agents=[doctor_finder_agent, web_analyst_agent],
    )
    
    return orchestrator


async def run_orchestrator(user_input: str):
    """Run the orchestrator with a user query."""
    orchestrator = await create_orchestrator()
    
    print(f"\n{'='*60}")
    print(f"User Query: {user_input}")
    print(f"{'='*60}\n")
    
    # Invoke the orchestrator agent
    runner = InMemoryRunner(agent=orchestrator)

    response = ""
    for event in await runner.run_debug(user_input, quiet=True): 
        if event.is_final_response() and event.content:
            response = (event.content.parts[0].text)
            print(f"Orchestrator Final Response:\n{response}\n")

    print(f"Orchestrator Response:\n{response}\n")
    return response


if __name__ == "__main__":
    # Example usage - run locally without exposing endpoints
    user_query = "Find a doctor in Texas"
    #user_query = "What is the current stock price of IBM and Microsoft?"
    asyncio.run(run_orchestrator(user_query))
