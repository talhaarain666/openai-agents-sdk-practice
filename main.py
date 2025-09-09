from agents import Agent,Runner,OpenAIChatCompletionsModel,function_tool,enable_verbose_stdout_logging,set_default_openai_key,set_default_openai_client
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

@function_tool
def weather (city:str)->str:
    return f"The weather in {city} is sunny"

gemini_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=gemini_client
)

agent = Agent(
    name="Assistant",
    # instructions="You are a helpful assistant",
    tools=[weather],
    model=model
)

# set_default_openai_client(custom_client)

enable_verbose_stdout_logging()

result = Runner.run_sync(agent,"What is the weather in karachi?")

for event in result.events:
    print(event)

print(result.final_output)