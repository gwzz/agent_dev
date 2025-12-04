"""Middleware for API authentication and rate limiting."""

import time
import logging
from typing import Optional, Dict, Set
from collections import defaultdict
from datetime import datetime, timedelta

from fastapi import status, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple in-memory rate limiter."""
    
    def __init__(self, requests: int = 100, window: int = 3600):  # 100 requests per hour by default
        self.requests = requests
        self.window = window  # in seconds
        self.requests_log: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if a request from given identifier is allowed."""
        now = time.time()
        # Remove old requests outside the window
        self.requests_log[identifier] = [
            req_time for req_time in self.requests_log[identifier] 
            if now - req_time < self.window
        ]
        
        # Check if we've exceeded the limit
        if len(self.requests_log[identifier]) >= self.requests:
            return False
        
        # Add this request to the log
        self.requests_log[identifier].append(now)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter(requests=100, window=3600)  # 100 requests per hour


def rate_limit_middleware(request: Request) -> None:
    """Rate limiting middleware function."""
    # Use client IP as identifier
    client_ip = request.client.host
    if not rate_limiter.is_allowed(client_ip):
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Too many requests."
        )


def add_api_key_auth(api_keys: Set[str]):
    """Factory function to create API key authentication middleware."""
    def auth_middleware(request: Request) -> None:
        # Check for API key in header
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            # Also check for API key in query parameter as fallback
            api_key = request.query_params.get("api_key")
        
        if not api_key or api_key not in api_keys:
            logger.warning(f"Unauthorized access attempt from IP: {request.client.host}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing API key"
            )
    
    return auth_middleware


# Example API keys (in production, these should be stored securely)
EXAMPLE_API_KEYS = {
    "demo-key-123",
    "test-key-456"
}


def auth_middleware(request: Request) -> None:
    """Default authentication middleware that checks for API key."""
    # Check for API key in header
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        # Also check for API key in query parameter as fallback
        api_key = request.query_params.get("api_key")
    
    # Allow requests without API key in development mode
    import os
    if not api_key and os.getenv("ENVIRONMENT") != "production":
        return  # Allow in development
    
    if not api_key or api_key not in EXAMPLE_API_KEYS:
        logger.warning(f"Unauthorized access attempt from IP: {request.client.host}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key. In development, you can add ?api_key=demo-key-123 to the URL."
        )