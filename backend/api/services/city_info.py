"""City information service layer."""

from typing import Dict, Any
import logging

from agent_tools.services import (
    get_weather,
    get_current_time,
    get_city_population,
    get_coordinates,
    convert_time_between_cities,
)

logger = logging.getLogger(__name__)


class CityInfoService:
    """Service for city information operations."""
    
    @staticmethod
    def get_weather(city: str) -> Dict[str, Any]:
        """Get weather information for a city."""
        try:
            logger.info(f"Getting weather for city: {city}")
            result = get_weather(city)
            return result
        except Exception as e:
            logger.error(f"Error getting weather for {city}: {str(e)}")
            return {
                "status": "error",
                "error_message": f"Failed to get weather: {str(e)}"
            }
    
    @staticmethod
    def get_current_time(city: str) -> Dict[str, Any]:
        """Get current time for a city."""
        try:
            logger.info(f"Getting current time for city: {city}")
            result = get_current_time(city)
            return result
        except Exception as e:
            logger.error(f"Error getting time for {city}: {str(e)}")
            return {
                "status": "error",
                "error_message": f"Failed to get time: {str(e)}"
            }
    
    @staticmethod
    def get_population(city: str) -> Dict[str, Any]:
        """Get population information for a city."""
        try:
            logger.info(f"Getting population for city: {city}")
            result = get_city_population(city)
            return result
        except Exception as e:
            logger.error(f"Error getting population for {city}: {str(e)}")
            return {
                "status": "error",
                "error_message": f"Failed to get population: {str(e)}"
            }
    
    @staticmethod
    def get_coordinates(city: str) -> Dict[str, Any]:
        """Get coordinates for a city."""
        try:
            logger.info(f"Getting coordinates for city: {city}")
            result = get_coordinates(city)
            return result
        except Exception as e:
            logger.error(f"Error getting coordinates for {city}: {str(e)}")
            return {
                "status": "error",
                "error_message": f"Failed to get coordinates: {str(e)}"
            }
    
    @staticmethod
    def convert_time(from_city: str, to_city: str, time: str) -> Dict[str, Any]:
        """Convert time between two cities."""
        try:
            logger.info(f"Converting time from {from_city} to {to_city}")
            result = convert_time_between_cities(from_city, to_city, time)
            return result
        except Exception as e:
            logger.error(f"Error converting time: {str(e)}")
            return {
                "status": "error",
                "error_message": f"Failed to convert time: {str(e)}"
            }
