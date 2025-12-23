"""Public agent entrypoints and tool exports for crypto tools."""

from google.adk.agents import Agent

from crypto_tools.services.price import (
    get_crypto_price,
    get_crypto_price_change_summary,
    predict_crypto_price_trend,
)

__all__ = [
    "get_crypto_price",
    "get_crypto_price_change_summary",
    "predict_crypto_price_trend",
    "root_agent",
]


root_agent = Agent(
    name="crypto_agent",
    model="gemini-3-pro-preview",
    description=(
        "Agent to answer questions about cryptocurrency prices, price change summaries, and price trend predictions."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about cryptocurrency prices, price change summaries, and price trend predictions. "
        "Use the get_crypto_price tool to get the current price of a cryptocurrency in USD. "
        "Use the get_crypto_price_change_summary tool to get a summary of price changes over a specified period. "
        "Use the predict_crypto_price_trend tool to predict whether a cryptocurrency's price will go up or down in the next 24 hours. "
        "The get_crypto_price tool accepts cryptocurrency names or symbols like 'bitcoin', 'btc', 'ethereum', 'eth', etc. "
        "The get_crypto_price_change_summary tool accepts cryptocurrency names along with the number of days to look back (default 7). "
        "The predict_crypto_price_trend tool analyzes recent price data and technical indicators to provide a trend prediction with confidence level."
    ),
    tools=[get_crypto_price, get_crypto_price_change_summary, predict_crypto_price_trend],
)