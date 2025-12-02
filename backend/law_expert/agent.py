"""Public agent entrypoints and tool exports for law tools."""

from google.adk.agents import Agent

from law_tools.services import (
    get_jurisdiction_info,
    get_statute_info,
    get_recent_cases,
    get_legal_definition,
)

__all__ = [
    "get_jurisdiction_info",
    "get_statute_info", 
    "get_recent_cases",
    "get_legal_definition",
    "root_agent",
]


root_agent = Agent(
    name="law_expert_agent",
    model="gemini-3-pro-preview",
    description=(
        "Agent to answer questions about legal jurisdictions, statutes, recent cases, and legal definitions."
    ),
    instruction=(
        "You are a helpful legal expert agent who can answer user questions about legal topics. "
        "Use the appropriate tool for each request: get_jurisdiction_info to determine legal jurisdictions and court systems, "
        "get_statute_info to provide information about specific laws and statutes, "
        "get_recent_cases to provide information about recent significant legal cases in various areas of law, "
        "and get_legal_definition to provide definitions of legal terms and concepts. "
        "Always emphasize that you are providing general legal information, not specific legal advice, "
        "and recommend that users consult with qualified legal professionals for their specific situations."
    ),
    tools=[get_jurisdiction_info, get_statute_info, get_recent_cases, get_legal_definition],
)