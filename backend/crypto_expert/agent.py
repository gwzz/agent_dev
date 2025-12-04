"""Public agent entrypoints and tool exports for crypto tools."""

from google.adk.agents import Agent

from crypto_tools.services.price import (
    get_crypto_price,
    get_crypto_price_change_summary,
)

__all__ = [
    "get_crypto_price",
    "get_crypto_price_change_summary",
    "root_agent",
]


root_agent = Agent(
    name="crypto_agent",
    model="gemini-3-pro-preview",
    description=(
        "Agent to answer questions about cryptocurrency prices and price change summaries."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about cryptocurrency prices and price change summaries. "
        "Use the get_crypto_price tool to get the current price of a cryptocurrency in USD. "
        "Use the get_crypto_price_change_summary tool to get a summary of price changes over a specified period. "
        "The get_crypto_price tool accepts cryptocurrency names or symbols like 'bitcoin', 'btc', 'ethereum', 'eth', etc. "
        "The get_crypto_price_change_summary tool accepts cryptocurrency names along with the number of days to look back (default 7)."
    ),
    tools=[get_crypto_price, get_crypto_price_change_summary],
)