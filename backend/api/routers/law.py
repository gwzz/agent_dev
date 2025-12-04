"""Router for legal information endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging

from ..services import LawService
from ..agent_manager import AgentManager, get_agent_manager
from ..models import QueryRequest

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/law",
    tags=["law"],
    responses={404: {"description": "Law endpoint not found"}},
)


@router.get("/jurisdiction/{jurisdiction}",
          summary="Get Jurisdiction Information",
          description="Get information about legal jurisdictions and court systems")
async def get_jurisdiction(jurisdiction: str) -> Dict[str, Any]:
    """
    Get jurisdiction information.

    Args:
        jurisdiction: The jurisdiction to query (e.g., 'federal', 'california', 'new york')

    Returns:
        Jurisdiction information
    """
    if not jurisdiction or not jurisdiction.strip():
        raise HTTPException(status_code=400, detail="Jurisdiction cannot be empty")

    result = LawService.get_jurisdiction(jurisdiction.strip())
    
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("error_message", "Unknown error"))
    
    return result


@router.get("/statute/{statute_query}",
          summary="Get Statute Information",
          description="Get information about specific statutes or laws")
async def get_statute(statute_query: str) -> Dict[str, Any]:
    """
    Get statute information.

    Args:
        statute_query: The statute name or query (e.g., 'gdpr', 'cpra', 'us_constitution')

    Returns:
        Statute information
    """
    if not statute_query or not statute_query.strip():
        raise HTTPException(status_code=400, detail="Statute query cannot be empty")

    result = LawService.get_statute(statute_query.strip())
    
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("error_message", "Unknown error"))
    
    return result


@router.get("/cases/{law_area}",
          summary="Get Recent Cases",
          description="Get information about recent significant cases in various areas of law")
async def get_cases(law_area: str) -> Dict[str, Any]:
    """
    Get recent cases information.

    Args:
        law_area: The area of law (e.g., 'civil_rights', 'privacy', 'criminal')

    Returns:
        Recent cases information
    """
    if not law_area or not law_area.strip():
        raise HTTPException(status_code=400, detail="Law area cannot be empty")

    result = LawService.get_cases(law_area.strip())
    
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("error_message", "Unknown error"))
    
    return result


@router.get("/definition/{term}",
          summary="Get Legal Definition",
          description="Get definitions of legal terms and concepts")
async def get_definition(term: str) -> Dict[str, Any]:
    """
    Get legal definition.

    Args:
        term: The legal term to define (e.g., 'tort', 'plaintiff', 'jurisdiction')

    Returns:
        Legal definition information
    """
    if not term or not term.strip():
        raise HTTPException(status_code=400, detail="Term cannot be empty")

    result = LawService.get_definition(term.strip())
    
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("error_message", "Unknown error"))
    
    return result


@router.post("/agent",
           summary="Law Agent (AI-powered)",
           description="Query the AI agent for legal information using natural language")
async def law_agent(
    request: QueryRequest,
    manager: AgentManager = Depends(get_agent_manager)
) -> Dict[str, Any]:
    """
    AI-powered agent endpoint that can handle complex natural language queries.
    
    This endpoint uses Google ADK agents to interpret and respond to queries about:
    - Legal jurisdictions and court systems
    - Statutes and laws
    - Recent legal cases
    - Legal terminology and definitions
    - Natural language understanding
    
    Example queries:
    - "Tell me about federal jurisdiction and recent privacy cases"
    - "What is GDPR and what are recent cases related to it?"
    - "Explain the concept of tort law"
    """
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        result = await manager.run_law_agent(request.query.strip())
        
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
        logger.error(f"Error in law agent: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}")

