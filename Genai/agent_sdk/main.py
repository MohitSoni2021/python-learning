import os
from agents import Agent, Runner, WebSearchTool
from openai import AsyncOpenAI
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel

# disable tracing
os.environ["OPENAI_AGENTS_DISABLE_TRACING"] = "1"

client = AsyncOpenAI(
    api_key="dummy",
    base_url="http://localhost:11434/v1"
)

model = OpenAIChatCompletionsModel(
    model="qwen2.5:7b",
    openai_client=client
)

agent = Agent(
    name="Assistant",
    model=model,
    tools=[
        WebSearchTool()
    ]
)

res = Runner.run_sync(agent, "what is on the website codinggita.com")

print(res.final_output)