"""Router for general API utility endpoints."""

from fastapi import APIRouter
from typing import Dict, Any

from ..models import HealthCheckResponse
from ..config import get_settings

router = APIRouter(
    tags=["general"],
    responses={404: {"description": "General endpoint not found"}},
)


@router.get("/",
         summary="API Root",
         description="Returns basic information about the API and available endpoints",
         responses={
             200: {
                 "description": "API root information",
                 "content": {
                     "application/json": {
                         "example": {
                             "message": "AI Agent Experts API",
                             "endpoints": {
                                 "/city-info": "City information expert agent",
                                 "/crypto": "Cryptocurrency expert agent",
                                 "/law": "Legal expert agent",
                                 "/docs": "Interactive API documentation (Swagger UI)",
                                 "/redoc": "Alternative API documentation (ReDoc)"
                             },
                             "description": "This API provides access to AI agents for city information, cryptocurrency data, and legal expertise."
                         }
                     }
                 }
             }
         })
async def root():
    """
    Root endpoint for the API.

    Returns:
        - message: Welcome message
        - endpoints: Available API endpoints
        - description: Brief description of the API
    """
    return {
        "message": "AI Agent Experts API",
        "endpoints": {
            "/city-info": "City information expert agent",
            "/crypto": "Cryptocurrency expert agent",
            "/law": "Legal expert agent",
            "/docs": "Interactive API documentation (Swagger UI)",
            "/redoc": "Alternative API documentation (ReDoc)"
        },
        "description": "This API provides access to AI agents for city information, cryptocurrency data, and legal expertise."
    }


@router.get("/health",
         summary="Health Check",
         description="Check the health status of the API",
         responses={
             200: {
                 "description": "API health status",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "healthy",
                             "available_services": ["city_info", "crypto", "law"],
                             "version": "1.0.0"
                         }
                     }
                 }
             }
         })
async def health_check(
    settings = get_settings()
) -> Dict[str, Any]:
    """
    Health check endpoint for the API.

    Returns:
        - status: Health status of the API
        - available_services: List of available services
        - version: API version
    """
    return {
        "status": "healthy",
        "available_services": ["city_info", "crypto", "law"],
        "version": settings.app_version
    }
