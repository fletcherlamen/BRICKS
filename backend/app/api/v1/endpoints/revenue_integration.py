"""
Revenue Integration API Endpoints
Phase 4 - Revenue Integration Loop
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel
import structlog

from app.services.ai_orchestrator import AIOrchestrator

logger = structlog.get_logger(__name__)

router = APIRouter()

# Global orchestrator instance
_orchestrator_instance: Optional[AIOrchestrator] = None


def set_orchestrator(orchestrator: AIOrchestrator):
    """Set the global orchestrator instance"""
    global _orchestrator_instance
    _orchestrator_instance = orchestrator


def get_orchestrator() -> AIOrchestrator:
    """Get the global orchestrator instance"""
    if _orchestrator_instance is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Orchestrator not initialized"
        )
    return _orchestrator_instance


# Pydantic Models
class BRICKProposalRequest(BaseModel):
    proposal_context: Optional[Dict[str, Any]] = None


class BRICKProposalResponse(BaseModel):
    status: str
    proposal: Dict[str, Any]
    message: str


class ApprovalRequest(BaseModel):
    approved: bool
    feedback: Optional[str] = None


class RevenueConnectionsResponse(BaseModel):
    status: str
    connections: Dict[str, Any]
    total_connected_bricks: int
    total_revenue_tracked: float
    integration_health: str


# Endpoints

@router.get("/church-kit/metrics")
async def get_church_kit_metrics(orchestrator: AIOrchestrator = Depends(get_orchestrator)):
    """Get Church Kit Generator business metrics"""
    try:
        if not orchestrator.church_kit_connector:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Church Kit connector not available"
            )
        
        result = await orchestrator.church_kit_connector.get_business_metrics()
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get Church Kit metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/church-kit/insights")
async def get_church_kit_insights(orchestrator: AIOrchestrator = Depends(get_orchestrator)):
    """Get Church Kit Generator customer insights"""
    try:
        if not orchestrator.church_kit_connector:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Church Kit connector not available"
            )
        
        result = await orchestrator.church_kit_connector.get_customer_insights()
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get Church Kit insights", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/global-sky/capabilities")
async def get_global_sky_capabilities(orchestrator: AIOrchestrator = Depends(get_orchestrator)):
    """Get Global Sky AI capabilities"""
    try:
        if not orchestrator.global_sky_connector:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Global Sky connector not available"
            )
        
        result = await orchestrator.global_sky_connector.get_ai_capabilities()
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get Global Sky capabilities", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/global-sky/revenue")
async def analyze_global_sky_revenue(orchestrator: AIOrchestrator = Depends(get_orchestrator)):
    """Analyze Global Sky AI revenue streams"""
    try:
        if not orchestrator.global_sky_connector:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Global Sky connector not available"
            )
        
        result = await orchestrator.global_sky_connector.analyze_revenue_streams()
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to analyze Global Sky revenue", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/treasury/financial-health")
async def get_financial_health(orchestrator: AIOrchestrator = Depends(get_orchestrator)):
    """Get overall financial health analysis"""
    try:
        if not orchestrator.treasury_optimizer:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Treasury optimizer not available"
            )
        
        result = await orchestrator.treasury_optimizer.analyze_financial_health()
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get financial health", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/treasury/optimize-resources")
async def optimize_resources(orchestrator: AIOrchestrator = Depends(get_orchestrator)):
    """Get resource optimization recommendations"""
    try:
        if not orchestrator.treasury_optimizer:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Treasury optimizer not available"
            )
        
        result = await orchestrator.treasury_optimizer.optimize_resource_allocation()
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to optimize resources", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/treasury/forecast/{months}")
async def forecast_revenue(months: int, orchestrator: AIOrchestrator = Depends(get_orchestrator)):
    """Forecast revenue for N months"""
    try:
        if not orchestrator.treasury_optimizer:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Treasury optimizer not available"
            )
        
        result = await orchestrator.treasury_optimizer.forecast_revenue(months)
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to forecast revenue", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/proposals/generate", response_model=BRICKProposalResponse)
async def generate_autonomous_proposal(
    request: BRICKProposalRequest,
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """Generate autonomous BRICK development proposal"""
    try:
        if not orchestrator.autonomous_brick_proposer:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Autonomous BRICK proposer not available"
            )
        
        result = await orchestrator.autonomous_brick_proposer.generate_brick_proposal(
            request.proposal_context
        )
        
        return BRICKProposalResponse(
            status=result["status"],
            proposal=result["proposal"],
            message=result["message"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to generate proposal", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/proposals")
async def get_all_proposals(
    status_filter: Optional[str] = None,
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """Get all BRICK development proposals"""
    try:
        if not orchestrator.autonomous_brick_proposer:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Autonomous BRICK proposer not available"
            )
        
        result = await orchestrator.autonomous_brick_proposer.get_all_proposals(status_filter)
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get proposals", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/proposals/{proposal_id}/approve")
async def approve_proposal(
    proposal_id: str,
    request: ApprovalRequest,
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """Approve or reject a BRICK proposal"""
    try:
        if not orchestrator.autonomous_brick_proposer:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Autonomous BRICK proposer not available"
            )
        
        result = await orchestrator.autonomous_brick_proposer.approve_proposal(
            proposal_id,
            request.approved,
            request.feedback
        )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to approve proposal", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/revenue-connections", response_model=RevenueConnectionsResponse)
async def get_revenue_connections(orchestrator: AIOrchestrator = Depends(get_orchestrator)):
    """Get revenue connection status across all BRICKs"""
    try:
        if not orchestrator.autonomous_brick_proposer:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Autonomous BRICK proposer not available"
            )
        
        result = await orchestrator.autonomous_brick_proposer.get_revenue_connection_status()
        
        return RevenueConnectionsResponse(
            status=result["status"],
            connections=result["connections"],
            total_connected_bricks=result["total_connected_bricks"],
            total_revenue_tracked=result["total_revenue_tracked"],
            integration_health=result["integration_health"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get revenue connections", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
