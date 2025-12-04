"""Custom exceptions for API error handling."""

from typing import Optional, Any, Dict
from fastapi import status


class APIException(Exception):
    """Base exception for API errors."""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)


class AgentNotFoundError(APIException):
    """Raised when requested agent is not found."""
    
    def __init__(self, agent_name: str, available_agents: list):
        message = f"Agent '{agent_name}' not found. Available agents: {', '.join(available_agents)}"
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="AGENT_NOT_FOUND",
            details={"agent_name": agent_name, "available_agents": available_agents}
        )


class InvalidQueryError(APIException):
    """Raised when query validation fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="INVALID_QUERY",
            details=details
        )


class AgentExecutionError(APIException):
    """Raised when agent execution fails."""
    
    def __init__(self, agent_name: str, original_error: str):
        message = f"Error running agent '{agent_name}': {original_error}"
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="AGENT_EXECUTION_ERROR",
            details={"agent_name": agent_name, "original_error": original_error}
        )


class RateLimitExceededError(APIException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, retry_after: Optional[int] = None):
        message = "Rate limit exceeded. Please try again later."
        details = {}
        if retry_after:
            details["retry_after"] = retry_after
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED",
            details=details
        )


class UnauthorizedError(APIException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Invalid or missing API key"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED"
        )


class ConfigurationError(APIException):
    """Raised when configuration is invalid or missing."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="CONFIGURATION_ERROR",
            details=details
        )
