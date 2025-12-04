"""Router for cryptocurrency endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging

from ..services import CryptoService
from ..agent_manager import AgentManager, get_agent_manager
from ..models import QueryRequest

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/crypto",
    tags=["crypto"],
    responses={404: {"description": "Crypto endpoint not found"}},
)


@router.get("/price/{crypto}",
          summary="Get Cryptocurrency Price",
          description="Get current price of a cryptocurrency in USD")
async def get_price(crypto: str) -> Dict[str, Any]:
    """
    Get current price for a cryptocurrency.

    Args:
        crypto: The cryptocurrency name or symbol (e.g., 'bitcoin', 'btc', 'ethereum', 'eth')

    Returns:
        Price information for the cryptocurrency
    """
    if not crypto or not crypto.strip():
        raise HTTPException(status_code=400, detail="Cryptocurrency name cannot be empty")

    result = CryptoService.get_price(crypto.strip())

    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("error_message", "Unknown error"))

    return result


@router.get("/price-change/{crypto}/{days}",
          summary="Get Cryptocurrency Price Change Summary",
          description="Get a summary of price changes for a cryptocurrency over a specified period")
async def get_price_change_summary(crypto: str, days: int) -> Dict[str, Any]:
    """
    Get a summary of price changes for a cryptocurrency over a specified period.

    Args:
        crypto: The cryptocurrency name or symbol (e.g., 'bitcoin', 'btc', 'ethereum', 'eth')
        days: The number of days to look back (e.g., 7, 30, 90)

    Returns:
        Price change summary information for the cryptocurrency
    """
    if not crypto or not crypto.strip():
        raise HTTPException(status_code=400, detail="Cryptocurrency name cannot be empty")

    if days <= 0:
        raise HTTPException(status_code=400, detail="Number of days must be a positive integer")

    if days > 365:
        raise HTTPException(status_code=400, detail="Maximum supported time period is 365 days")

    result = CryptoService.get_price_change_summary(crypto.strip(), days)

    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("error_message", "Unknown error"))

    return result


@router.post("/agent",
           summary="Crypto Agent (AI-powered)",
           description="Query the AI agent for cryptocurrency information using natural language")
async def crypto_agent(
    request: QueryRequest,
    manager: AgentManager = Depends(get_agent_manager)
) -> Dict[str, Any]:
    """
    AI-powered agent endpoint that can handle complex natural language queries.
    
    This endpoint uses Google ADK agents to interpret and respond to queries about:
    - Cryptocurrency prices and market data
    - Price comparisons and trends
    - Natural language understanding
    
    Example queries:
    - "What's the price of Bitcoin and Ethereum?"
    - "Compare the prices of BTC and ETH"
    - "How much is Cardano worth?"
    """
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        result = await manager.run_crypto_agent(request.query.strip())
        
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
        logger.error(f"Error in crypto agent: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}")

