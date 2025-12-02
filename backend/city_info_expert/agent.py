# # City Info Expert agent module
# from multi_tool_agent import (
#     convert_time_between_cities,
#     get_city_population,
#     get_coordinates,
#     get_current_time,
#     get_weather,
# )

# __all__ = [
#     'get_weather',
#     'get_current_time',
#     'get_city_population',
#     'get_coordinates',
#     'convert_time_between_cities',
# ]
"""Public agent entrypoints and tool exports."""

from google.adk.agents import Agent

from agent_tools.services import (
    convert_time_between_cities,
    get_city_population,
    get_coordinates,
    get_current_time,
    get_weather,
)

__all__ = [
    "convert_time_between_cities",
    "get_city_population",
    "get_coordinates",
    "get_current_time",
    "get_weather",
    "root_agent",
]


root_agent = Agent(
    name="city_info_expert_agent",
    model="gemini-3-pro-preview",
    description=(
        "Agent to answer questions about the time and weather in a city, convert time between different regions, get geographical coordinates, and retrieve city population data."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city, convert time between different regions, get geographical coordinates, and retrieve city population data. "
        "Use the appropriate tool for each request: get_weather for weather information, get_current_time for current time in a city, "
        "convert_time_between_cities to convert time between two different cities, get_coordinates to get latitude and longitude for a city, "
        "and get_city_population to get population information for a city."
    ),
    tools=[get_weather, get_current_time, convert_time_between_cities, get_coordinates, get_city_population],
)