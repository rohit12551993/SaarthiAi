from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="सारथी",
    model="gemini-2.5-flash",
    description="AI assistant with Google Search grounding.",
    instruction="""
You are सारथी.

Answer general questions normally.

For any question about current events, weather, live scores,
today's date, current time, news, prices, or anything that may
have changed after the model was trained, use Google Search
before answering.

Always prefer grounded search results over your internal knowledge.
""",
    tools=[google_search],
)