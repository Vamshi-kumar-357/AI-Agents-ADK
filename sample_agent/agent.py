import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm







def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

weather_tool = FunctionTool(
    # name="get_weather",
    func=get_weather,
    # description="Retrieves the current weather report for a specified city.",
    # parameters={"city": {"type": "string", "description": "The city name."}},
    # returns={"status": "string", "report": "string"},
)

time_tool = FunctionTool(
    # name="get_current_time",
    func=get_current_time,
    # description="Returns the current time in a specified city.",
    # parameters={"city": {"type": "string", "description": "The city name."}},
    # returns={"status": "string", "report": "string"},
)


root_agent = LlmAgent(
    model=LiteLlm(model="ollama_chat/qwen3:4b"), # LiteLLM model string format
    name="openai_agent",
    instruction="You are a helpful agent who can answer user questions about the time and weather in a city.",
    tools = [weather_tool, time_tool]
    # ... other agent parameters
)

