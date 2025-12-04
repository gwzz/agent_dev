"""Legal information service layer."""

from typing import Dict, Any
import logging

from law_tools.services import (
    get_jurisdiction_info,
    get_statute_info,
    get_recent_cases,
    get_legal_definition,
)

logger = logging.getLogger(__name__)


class LawService:
    """Service for legal information operations."""
    
    @staticmethod
    def get_jurisdiction(jurisdiction: str) -> Dict[str, Any]:
        """Get jurisdiction information."""
        try:
            logger.info(f"Getting jurisdiction info: {jurisdiction}")
            result = get_jurisdiction_info(jurisdiction)
            return result
        except Exception as e:
            logger.error(f"Error getting jurisdiction info: {str(e)}")
            return {
                "status": "error",
                "error_message": f"Failed to get jurisdiction info: {str(e)}"
            }
    
    @staticmethod
    def get_statute(statute_query: str) -> Dict[str, Any]:
        """Get statute information."""
        try:
            logger.info(f"Getting statute info: {statute_query}")
            result = get_statute_info(statute_query)
            return result
        except Exception as e:
            logger.error(f"Error getting statute info: {str(e)}")
            return {
                "status": "error",
                "error_message": f"Failed to get statute info: {str(e)}"
            }
    
    @staticmethod
    def get_cases(law_area: str) -> Dict[str, Any]:
        """Get recent cases information."""
        try:
            logger.info(f"Getting recent cases for: {law_area}")
            result = get_recent_cases(law_area)
            return result
        except Exception as e:
            logger.error(f"Error getting cases: {str(e)}")
            return {
                "status": "error",
                "error_message": f"Failed to get cases: {str(e)}"
            }
    
    @staticmethod
    def get_definition(term: str) -> Dict[str, Any]:
        """Get legal definition."""
        try:
            logger.info(f"Getting legal definition: {term}")
            result = get_legal_definition(term)
            return result
        except Exception as e:
            logger.error(f"Error getting definition: {str(e)}")
            return {
                "status": "error",
                "error_message": f"Failed to get definition: {str(e)}"
            }
