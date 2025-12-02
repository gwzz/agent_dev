"""Public agent entrypoints and tool exports for crypto tools."""

from google.adk.agents import Agent

from crypto_tools.services.price import (
    get_crypto_price,
)

__all__ = [
    "get_crypto_price",
    "root_agent",
]


root_agent = Agent(
    name="crypto_agent",
    model="gemini-3-pro-preview",
    description=(
        "Agent to answer questions about cryptocurrency prices."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about cryptocurrency prices. "
        "Use the get_crypto_price tool to get the current price of a cryptocurrency in USD. "
        "The tool accepts cryptocurrency names or symbols like 'bitcoin', 'ethereum', 'btc', 'eth', etc."
    ),
    tools=[get_crypto_price],
)