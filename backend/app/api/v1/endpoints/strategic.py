"""
Strategic Intelligence API Endpoints
Phase 3 - Strategic Intelligence Layer
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
class BRICKSEcosystemResponse(BaseModel):
    status: str
    ecosystem: Optional[Dict[str, Any]] = None
    total_existing_bricks: Optional[int] = None
    total_potential_bricks: Optional[int] = None
    total_monthly_revenue: Optional[float] = None
    timestamp: str


class RevenueOpportunitiesResponse(BaseModel):
    status: str
    opportunities: List[Dict[str, Any]]
    total_opportunities: int
    total_potential_revenue: float
    top_opportunity: Optional[Dict[str, Any]]
    timestamp: str


class StrategicGapsResponse(BaseModel):
    status: str
    detected_gaps: Dict[str, List[Dict[str, Any]]]
    total_gaps: int
    high_priority_gaps: int
    gap_severity: str
    strategic_recommendations: List[str]
    timestamp: str


class BRICKPriorityQueueResponse(BaseModel):
    status: str
    priority_queue: List[Dict[str, Any]]
    next_brick_recommendation: Optional[Dict[str, Any]]
    total_bricks_analyzed: int
    timestamp: str


class ConstraintPredictionResponse(BaseModel):
    status: str
    brick_name: str
    predicted_constraints: Dict[str, List[Dict[str, Any]]]
    total_constraints: int
    constraint_risk_score: float
    risk_level: str
    mitigation_strategies: List[Dict[str, Any]]
    recommendation: str
    timestamp: str


class StrategicAnalysisResponse(BaseModel):
    status: str
    analysis_type: str
    strategic_intelligence: Dict[str, Any]
    executive_summary: Dict[str, Any]
    strategic_recommendations: List[Dict[str, Any]]
    confidence_score: float
    next_actions: List[str]
    timestamp: str


class StrategicDashboardResponse(BaseModel):
    status: str
    dashboard_data: Dict[str, Any]
    strategic_health_score: float
    strategic_status: str
    timestamp: str


# Endpoints

@router.get("/ecosystem", response_model=BRICKSEcosystemResponse)
async def get_bricks_ecosystem(
    brick_name: Optional[str] = None,
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """Get BRICKS ecosystem context and specifications"""
    try:
        if not orchestrator.bricks_context_service:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="BRICKS context service not available"
            )
        
        result = await orchestrator.bricks_context_service.get_ecosystem_context(brick_name)
        
        return BRICKSEcosystemResponse(
            status=result["status"],
            ecosystem=result.get("ecosystem"),
            total_existing_bricks=result.get("total_existing_bricks"),
            total_potential_bricks=result.get("total_potential_bricks"),
            total_monthly_revenue=result.get("total_monthly_revenue"),
            timestamp=datetime.now().isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get BRICKS ecosystem", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/revenue-opportunities", response_model=RevenueOpportunitiesResponse)
async def analyze_revenue_opportunities(
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """Analyze revenue opportunities across BRICKS ecosystem"""
    try:
        if not orchestrator.revenue_analysis_service:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Revenue analysis service not available"
            )
        
        result = await orchestrator.revenue_analysis_service.analyze_revenue_opportunities()
        
        return RevenueOpportunitiesResponse(
            status=result["status"],
            opportunities=result["opportunities"],
            total_opportunities=result["total_opportunities"],
            total_potential_revenue=result["total_potential_revenue"],
            top_opportunity=result.get("top_opportunity"),
            timestamp=result["analysis_timestamp"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to analyze revenue opportunities", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/strategic-gaps", response_model=StrategicGapsResponse)
async def detect_strategic_gaps(
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """Detect strategic gaps in BRICKS ecosystem"""
    try:
        if not orchestrator.strategic_gap_service:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Strategic gap service not available"
            )
        
        # Get BRICKS context for gap analysis
        bricks_context = None
        if orchestrator.bricks_context_service:
            context_result = await orchestrator.bricks_context_service.get_ecosystem_context()
            bricks_context = context_result.get("ecosystem")
        
        result = await orchestrator.strategic_gap_service.detect_strategic_gaps(bricks_context)
        
        return StrategicGapsResponse(
            status=result["status"],
            detected_gaps=result["detected_gaps"],
            total_gaps=result["total_gaps"],
            high_priority_gaps=result["high_priority_gaps"],
            gap_severity=result["gap_severity"],
            strategic_recommendations=result["strategic_recommendations"],
            timestamp=result["analysis_timestamp"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to detect strategic gaps", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/priority-queue", response_model=BRICKPriorityQueueResponse)
async def get_brick_priority_queue(
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """Get next BRICK priority queue"""
    try:
        if not orchestrator.brick_priority_service:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="BRICK priority service not available"
            )
        
        # Get BRICKS context
        ecosystem_context = None
        if orchestrator.bricks_context_service:
            context_result = await orchestrator.bricks_context_service.get_ecosystem_context()
            ecosystem_context = context_result.get("ecosystem")
        
        if not ecosystem_context:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="BRICKS ecosystem context required"
            )
        
        result = await orchestrator.brick_priority_service.generate_priority_queue(ecosystem_context)
        
        return BRICKPriorityQueueResponse(
            status=result["status"],
            priority_queue=result["priority_queue"],
            next_brick_recommendation=result.get("next_brick_recommendation"),
            total_bricks_analyzed=result["total_bricks_analyzed"],
            timestamp=result["analysis_timestamp"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get BRICK priority queue", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/predict-constraints/{brick_name}", response_model=ConstraintPredictionResponse)
async def predict_brick_constraints(
    brick_name: str,
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """Predict constraints for a specific BRICK development"""
    try:
        if not orchestrator.constraint_prediction_service:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Constraint prediction service not available"
            )
        
        # Get BRICK data
        brick_data = None
        if orchestrator.bricks_context_service:
            context_result = await orchestrator.bricks_context_service.get_ecosystem_context(brick_name)
            brick_data = context_result.get("brick")
        
        if not brick_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"BRICK '{brick_name}' not found"
            )
        
        result = await orchestrator.constraint_prediction_service.predict_constraints(
            brick_name,
            brick_data
        )
        
        return ConstraintPredictionResponse(
            status=result["status"],
            brick_name=result["brick_name"],
            predicted_constraints=result["predicted_constraints"],
            total_constraints=result["total_constraints"],
            constraint_risk_score=result["constraint_risk_score"],
            risk_level=result["risk_level"],
            mitigation_strategies=result["mitigation_strategies"],
            recommendation=result["recommendation"],
            timestamp=result["prediction_timestamp"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to predict constraints", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/strategic-analysis", response_model=StrategicAnalysisResponse)
async def perform_strategic_analysis(
    analysis_type: str = "comprehensive",
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """Perform comprehensive strategic analysis using STRATEGIC framework"""
    try:
        if not orchestrator.strategic_intelligence_service:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Strategic intelligence service not available"
            )
        
        result = await orchestrator.strategic_intelligence_service.analyze_strategic_situation(
            analysis_type=analysis_type
        )
        
        return StrategicAnalysisResponse(
            status=result["status"],
            analysis_type=result["analysis_type"],
            strategic_intelligence=result["strategic_intelligence"],
            executive_summary=result["executive_summary"],
            strategic_recommendations=result["strategic_recommendations"],
            confidence_score=result["confidence_score"],
            next_actions=result["next_actions"],
            timestamp=result["analysis_timestamp"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to perform strategic analysis", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/dashboard", response_model=StrategicDashboardResponse)
async def get_strategic_dashboard(
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """Get strategic intelligence dashboard with comprehensive insights"""
    try:
        if not orchestrator.strategic_intelligence_service:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Strategic intelligence service not available"
            )
        
        result = await orchestrator.strategic_intelligence_service.get_strategic_dashboard()
        
        return StrategicDashboardResponse(
            status=result["status"],
            dashboard_data=result["dashboard_data"],
            strategic_health_score=result["strategic_health_score"],
            strategic_status=result["strategic_status"],
            timestamp=result["timestamp"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get strategic dashboard", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/income-streams")
async def get_income_stream_mapping(
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """Get income stream mapping across BRICKS ecosystem"""
    try:
        if not orchestrator.revenue_analysis_service:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Revenue analysis service not available"
            )
        
        result = await orchestrator.revenue_analysis_service.map_income_streams()
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get income stream mapping", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
