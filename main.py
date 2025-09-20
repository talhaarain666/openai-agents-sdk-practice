from agents import Agent,Runner,OpenAIChatCompletionsModel,ModelSettings,function_tool,enable_verbose_stdout_logging,set_default_openai_key,set_default_openai_client
import os
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent
from agents.agent import StopAtTools
from dotenv import load_dotenv
import asyncio

# for debugging purpose
# enable_verbose_stdout_logging()

load_dotenv()

# for tracing purpose
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

@function_tool
def weather (city:str)->str:
    return f"The weather in {city} is sunny"

# @function_tool
# def weather_in_khi (city:str)->str:
#     return f"The weather in {city} is sunny"

@function_tool
def get_support_details (city:str)->str:
    return f"Support details for {city} is as follows ..." 


# only required if you want to use gemini and to set the api key globally
gemini_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=gemini_client
)

agent = Agent(
    name="Haiku Agent",
    # instructions="You are a helpful assistant",
    instructions="Always respond in haiku format",
    tools=[weather,get_support_details],
    model=model,

    # this will make the agent to use only one tool and then stop
    # tool_use_behavior="stop_on_first_tool"
    
    tool_use_behavior=StopAtTools(stop_at_tool_names=["weather_in_khi"]),

    # if we want to make tool choice mandatory. default is None (None means auto-select)
    # model_settings=ModelSettings(tool_choice="required"),

    # reset_tool_choice will reset the tool choice after each tool use. default True
    # reset_tool_choice=False
)

# run synchronously
# max_turns is optional, default is 5 . It will limit the number of times the agent can use tools.
#  If the agent reaches the max_turns, it will stop and return the final output
result = Runner.run_sync(agent,"What is the weather in karachi? - also share support details",max_turns=3)
print(result.final_output)

# asynchronously
# async def stream_agent():
    # run streamed is an async function
#     result = Runner.run_streamed(agent,"What is the weather in Tokyo and Karachi?")

#     async for event in result.stream_events():

#         # to see each event in the stream
#         # print(f"\n[EVENT] : {event}\n")
#         # print(f"\n[EVENT TYPE] : {event.type}\n")

#         # to see only the data events in the stream
#         if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
#             print(f"\n[DATA] : {event.data.delta}\n")
#     print(result.final_output)

# asyncio.run(stream_agent())
# for event in result.events:
#     print(event)
