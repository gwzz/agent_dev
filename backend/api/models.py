"""Response models for API endpoints."""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class AgentUsage(BaseModel):
    """Token usage information for agent responses."""
    prompt_tokens: Optional[int] = Field(None, description="Number of tokens in the prompt")
    completion_tokens: Optional[int] = Field(None, description="Number of tokens in the completion")
    total_tokens: Optional[int] = Field(None, description="Total number of tokens used")


class AgentResultData(BaseModel):
    """Data structure for agent result."""
    content: Optional[str] = Field(None, description="Main content of the agent response")
    usage: Optional[AgentUsage] = Field(None, description="Token usage information")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class AgentSuccessResponse(BaseModel):
    """Successful agent response."""
    status: str = Field("success", description="Status of the response")
    result: AgentResultData = Field(..., description="Result data from the agent")


class ErrorDetail(BaseModel):
    """Error detail information."""
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code for programmatic handling")
    timestamp: Optional[str] = Field(None, description="ISO timestamp of the error")


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Health status of the API")
    available_agents: List[str] = Field(..., description="List of available agent types")
    version: Optional[str] = Field(None, description="API version")


class AgentListResponse(BaseModel):
    """Response for listing available agents."""
    agents: List[str] = Field(..., description="List of available agent names")
    count: int = Field(..., description="Number of available agents")


class QueryRequest(BaseModel):
    """Request model for agent queries."""
    model_config = {"json_schema_extra": {
        "example": {
            "query": "What's the weather in London?"
        }
    }}
    
    query: str = Field(..., description="The query to send to the agent", min_length=1, max_length=1000)


class WeatherResponse(BaseModel):
    """Response model for weather information."""
    city: str = Field(..., description="City name")
    temperature: float = Field(..., description="Temperature in Celsius")
    temperature_fahrenheit: float = Field(..., description="Temperature in Fahrenheit")
    description: str = Field(..., description="Weather description")
    humidity: int = Field(..., description="Humidity percentage")
    feels_like: float = Field(..., description="Feels like temperature in Celsius")


class TimeResponse(BaseModel):
    """Response model for time information."""
    city: str = Field(..., description="City name")
    current_time: str = Field(..., description="Current time in the city")
    timezone: str = Field(..., description="Timezone of the city")
    utc_offset: Optional[str] = Field(None, description="UTC offset")


class CoordinatesResponse(BaseModel):
    """Response model for coordinates."""
    city: str = Field(..., description="City name")
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    address: Optional[str] = Field(None, description="Full address")


class PopulationResponse(BaseModel):
    """Response model for population information."""
    city: str = Field(..., description="City name")
    population: Optional[int] = Field(None, description="Approximate population")
    source: Optional[str] = Field(None, description="Data source")


class CryptoPriceResponse(BaseModel):
    """Response model for cryptocurrency price."""
    cryptocurrency: str = Field(..., description="Cryptocurrency name")
    symbol: str = Field(..., description="Cryptocurrency symbol")
    price_usd: float = Field(..., description="Current price in USD")
    last_updated: Optional[str] = Field(None, description="Last update timestamp")
