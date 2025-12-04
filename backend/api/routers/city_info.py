"""Router for city information endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging

from ..services import CityInfoService
from ..agent_manager import AgentManager, get_agent_manager
from ..models import QueryRequest
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/city-info",
    tags=["city-info"],
    responses={404: {"description": "City Info endpoint not found"}},
)


class TimeConversionRequest(BaseModel):
    """Request model for time conversion."""
    from_city: str = Field(..., description="The source city")
    to_city: str = Field(..., description="The destination city")
    time: str = Field(..., description="The time to convert (e.g., '14:30')")


@router.get("/weather/{city}",
          summary="Get Weather Information",
          description="Get current weather information for a specific city")
async def get_weather_endpoint(city: str) -> Dict[str, Any]:
    """Get weather information for a specific city."""
    if not city or not city.strip():
        raise HTTPException(status_code=400, detail="City name cannot be empty")

    result = CityInfoService.get_weather(city.strip())
    
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("error_message", "Unknown error"))
    
    return result


@router.get("/time/{city}",
          summary="Get Current Time",
          description="Get current local time for a specific city")
async def get_time_endpoint(city: str) -> Dict[str, Any]:
    """Get current time for a specific city."""
    if not city or not city.strip():
        raise HTTPException(status_code=400, detail="City name cannot be empty")

    result = CityInfoService.get_current_time(city.strip())
    
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("error_message", "Unknown error"))
    
    return result


@router.get("/coordinates/{city}",
          summary="Get Geographic Coordinates",
          description="Get latitude and longitude for a specific city")
async def get_coordinates_endpoint(city: str) -> Dict[str, Any]:
    """Get geographic coordinates for a specific city."""
    if not city or not city.strip():
        raise HTTPException(status_code=400, detail="City name cannot be empty")

    result = CityInfoService.get_coordinates(city.strip())
    
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("error_message", "Unknown error"))
    
    return result


@router.get("/population/{city}",
          summary="Get Population Information",
          description="Get population information for a specific city from Wikipedia")
async def get_population_endpoint(city: str) -> Dict[str, Any]:
    """Get population information for a specific city."""
    if not city or not city.strip():
        raise HTTPException(status_code=400, detail="City name cannot be empty")

    result = CityInfoService.get_population(city.strip())
    
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("error_message", "Unknown error"))
    
    return result


@router.post("/time/convert",
           summary="Convert Time Between Cities",
           description="Convert a specific time from one city to another")
async def convert_time_endpoint(request: TimeConversionRequest) -> Dict[str, Any]:
    """Convert time between two cities."""
    if not request.from_city or not request.from_city.strip():
        raise HTTPException(status_code=400, detail="Source city cannot be empty")
    
    if not request.to_city or not request.to_city.strip():
        raise HTTPException(status_code=400, detail="Destination city cannot be empty")
    
    if not request.time or not request.time.strip():
        raise HTTPException(status_code=400, detail="Time cannot be empty")

    result = CityInfoService.convert_time(
        request.from_city.strip(), 
        request.to_city.strip(), 
        request.time.strip()
    )
    
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("error_message", "Unknown error"))
    
    return result


@router.post("/agent",
           summary="City Info Agent (AI-powered)",
           description="Query the AI agent for city information using natural language")
async def city_info_agent(
    request: QueryRequest,
    manager: AgentManager = Depends(get_agent_manager)
) -> Dict[str, Any]:
    """
    AI-powered agent endpoint that can handle complex natural language queries.
    
    This endpoint uses Google ADK agents to interpret and respond to queries about:
    - Weather, time, coordinates, and population for cities
    - Complex multi-part questions
    - Natural language understanding
    
    Example queries:
    - "What's the weather in London and the current time in Tokyo?"
    - "Tell me about Paris - its coordinates and population"
    """
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        result = await manager.run_city_info_agent(request.query.strip())
        
        if result.status == "error":
            error_msg = result.error_message or "Agent execution failed"
            raise HTTPException(status_code=500, detail=error_msg)
        
        return {
            "status": result.status,
            "content": result.content,
            "usage": result.usage,
            "metadata": result.metadata
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in city info agent: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}")

