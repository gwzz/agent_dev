"""Cryptocurrency service layer."""

from typing import Dict, Any
import logging

from crypto_tools.services import get_crypto_price, get_crypto_price_change_summary

logger = logging.getLogger(__name__)


class CryptoService:
    """Service for cryptocurrency operations."""

    @staticmethod
    def get_price(crypto: str) -> Dict[str, Any]:
        """Get cryptocurrency price."""
        try:
            logger.info(f"Getting price for cryptocurrency: {crypto}")
            result = get_crypto_price(crypto)
            return result
        except Exception as e:
            logger.error(f"Error getting price for {crypto}: {str(e)}")
            return {
                "status": "error",
                "error_message": f"Failed to get cryptocurrency price: {str(e)}"
            }

    @staticmethod
    def get_price_change_summary(crypto: str, days: int) -> Dict[str, Any]:
        """Get cryptocurrency price change summary."""
        try:
            logger.info(f"Getting price change summary for cryptocurrency: {crypto}, days: {days}")
            result = get_crypto_price_change_summary(crypto, days)
            return result
        except Exception as e:
            logger.error(f"Error getting price change summary for {crypto}: {str(e)}")
            return {
                "status": "error",
                "error_message": f"Failed to get cryptocurrency price change summary: {str(e)}"
            }
