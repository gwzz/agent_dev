"""Population lookup helpers using Wikipedia."""

from __future__ import annotations

import re
from typing import Any

import wikipediaapi

_population_patterns = [
    r"population\s+(?:of)?\s*(?:is|was|around|approximately)?\s*([0-9,]+(?:\.[0-9]+)?(?:\s+million|\s+thousand)?)",
    r"pop\.\s*([0-9,]+(?:\.[0-9]+)?(?:\s+million|\s+thousand)?)",
    r"([0-9,]+(?:\.[0-9]+)?(?:\s+million|\s+thousand)?)\s+inhabitants",
    r"approximately\s+([0-9,]+(?:\.[0-9]+)?(?:\s+million|\s+thousand)?)\s+people",
    r"([0-9,]+(?:\.[0-9]+)?(?:\s+million|\s+thousand)?)\s+people",
    r"([0-9,]+(?:\.[0-9]+)?(?:\s+million|\s+thousand)?)\s+residents",
]


_wiki = wikipediaapi.Wikipedia(
    user_agent="agent-dev-project/1.0 (https://github.com/your-organization/agent-dev)",
    language="en",
)


def get_city_population(city: str) -> dict[str, Any]:
    """Attempt to extract population data for ``city`` from Wikipedia."""
    page = _wiki.page(city)
    if not page.exists():
        return {
            "status": "error",
            "error_message": f"Wikipedia page for '{city}' not found.",
        }

    summary_hit = _search_population_text(page.summary)
    if summary_hit:
        return {
            "status": "success",
            "city": city,
            "population": summary_hit,
            "summary_text": page.summary[:200] + "...",
        }

    for section in page.sections:
        section_text = _section_text(section)
        section_hit = _search_population_text(section_text)
        if section_hit:
            return {
                "status": "success",
                "city": city,
                "population": section_hit,
                "summary_text": section_text[:200] + "...",
            }

    return {
        "status": "error",
        "error_message": f"Population information not found for '{city}' on Wikipedia.",
    }


def _search_population_text(text: str) -> str | None:
    for pattern in _population_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).replace(",", "")
    return None


def _section_text(section: wikipediaapi.WikipediaPage) -> str:
    text = section.text
    for sub_section in section.sections:
        text += " " + _section_text(sub_section)
    return text
