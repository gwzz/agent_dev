"""Service layer for the law tools."""

from .jurisdiction import get_jurisdiction_info
from .statute import get_statute_info
from .case import get_recent_cases
from .definition import get_legal_definition

__all__ = [
    "get_jurisdiction_info",
    "get_statute_info",
    "get_recent_cases",
    "get_legal_definition",
]