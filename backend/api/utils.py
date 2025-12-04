"""Utility functions for API responses and error handling."""

import logging
from typing import Any, Dict, Optional
from fastapi import HTTPException
from pydantic import BaseModel, ValidationError
import traceback

logger = logging.getLogger(__name__)


class APIResponse(BaseModel):
    """Standard API response format."""
    status: str
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response format."""
    error: str
    details: Optional[str] = None
    timestamp: str = None
    path: Optional[str] = None


def create_success_response(data: Optional[Dict[str, Any]] = None, message: Optional[str] = None) -> APIResponse:
    """Create a success response."""
    return APIResponse(
        status="success",
        message=message,
        data=data
    )


def create_error_response(error: str, message: Optional[str] = None) -> APIResponse:
    """Create an error response."""
    return APIResponse(
        status="error",
        error=error,
        message=message
    )


def handle_agent_error(error: Exception, agent_name: str, query: str) -> HTTPException:
    """Handle agent errors and create appropriate HTTP exception."""
    error_msg = f"Error running {agent_name} agent: {str(error)}"
    logger.error(error_msg, exc_info=True)

    # Log the query that caused the error (truncated to avoid logging sensitive info)
    logger.error(f"Query that caused error: {query[:100]}...")

    # Log the full stack trace for debugging
    logger.error(f"Full stack trace: {traceback.format_exc()}")

    return HTTPException(
        status_code=500,
        detail=error_msg
    )


def format_agent_result(result: Any) -> Dict[str, Any]:
    """Format agent result into a consistent structure."""
    if hasattr(result, 'dict') and callable(getattr(result, 'dict')):
        # If result is a Pydantic model, convert to dict
        return result.dict()
    elif isinstance(result, dict):
        return result
    else:
        # For other types, wrap in a standard structure
        return {
            "content": str(result),
            "raw_result": result
        }


def validate_query(query: str) -> str:
    """Validate query input and return cleaned query."""
    if not query or not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty or whitespace only"
        )

    query = query.strip()

    if len(query) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Query is too long. Please keep it under 1000 characters."
        )

    # Additional validation: check for potentially harmful content
    dangerous_patterns = ["<script", "javascript:", "vbscript:", "onerror=", "onload="]
    for pattern in dangerous_patterns:
        if pattern.lower() in query.lower():
            raise HTTPException(
                status_code=400,
                detail=f"Query contains potentially harmful content: {pattern}"
            )

    return query


def validate_agent_name(agent_name: str) -> str:
    """Validate agent name."""
    valid_agents = {"city_info", "crypto", "law"}
    if agent_name not in valid_agents:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid agent name: {agent_name}. Valid options: {', '.join(valid_agents)}"
        )
    return agent_name