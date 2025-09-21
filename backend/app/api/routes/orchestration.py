"""
Orchestration endpoints for managing AI system coordination.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import structlog

from app.core.database import get_db
from app.services.orchestrator import OrchestrationService

logger = structlog.get_logger()
router = APIRouter()


class SessionCreateRequest(BaseModel):
    """Request model for creating orchestration session."""
    session_name: str
    context: Dict[str, Any]


class AnalysisRequest(BaseModel):
    """Request model for strategic analysis."""
    analysis_type: str
    parameters: Optional[Dict[str, Any]] = {}


class SessionResponse(BaseModel):
    """Response model for orchestration session."""
    session_id: str
    session_name: str
    status: str
    created_at: str
    recent_collaborations: List[Dict[str, Any]]


@router.post("/orchestration/sessions", response_model=Dict[str, str])
async def create_orchestration_session(
    request: SessionCreateRequest,
    app_request: Request
):
    """Create a new orchestration session."""
    try:
        orchestrator: OrchestrationService = app_request.app.state.orchestrator
        
        session_id = await orchestrator.start_orchestration_session(
            request.session_name,
            request.context
        )
        
        logger.info("Created orchestration session", session_id=session_id)
        
        return {
            "session_id": session_id,
            "status": "created",
            "message": "Orchestration session created successfully"
        }
        
    except Exception as e:
        logger.error("Failed to create orchestration session", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/orchestration/sessions/{session_id}", response_model=SessionResponse)
async def get_orchestration_session(
    session_id: str,
    app_request: Request
):
    """Get orchestration session status and details."""
    try:
        orchestrator: OrchestrationService = app_request.app.state.orchestrator
        
        session_data = await orchestrator.get_session_status(session_id)
        
        return SessionResponse(**session_data)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to get orchestration session", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/orchestration/sessions/{session_id}/analyze")
async def execute_strategic_analysis(
    session_id: str,
    request: AnalysisRequest,
    app_request: Request
):
    """Execute strategic analysis for a session."""
    try:
        orchestrator: OrchestrationService = app_request.app.state.orchestrator
        
        result = await orchestrator.execute_strategic_analysis(
            session_id,
            request.analysis_type
        )
        
        logger.info("Executed strategic analysis", session_id=session_id, analysis_type=request.analysis_type)
        
        return {
            "session_id": session_id,
            "analysis_type": request.analysis_type,
            "result": result,
            "status": "completed"
        }
        
    except Exception as e:
        logger.error("Failed to execute strategic analysis", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/orchestration/sessions")
async def list_orchestration_sessions(app_request: Request):
    """List all orchestration sessions."""
    try:
        orchestrator: OrchestrationService = app_request.app.state.orchestrator
        
        # Get active sessions
        active_sessions = []
        for session_id, session_data in orchestrator.active_sessions.items():
            session_info = await orchestrator.get_session_status(session_id)
            active_sessions.append(session_info)
        
        return {
            "sessions": active_sessions,
            "total": len(active_sessions),
            "status": "success"
        }
        
    except Exception as e:
        logger.error("Failed to list orchestration sessions", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/orchestration/sessions/{session_id}")
async def close_orchestration_session(
    session_id: str,
    app_request: Request
):
    """Close an orchestration session."""
    try:
        orchestrator: OrchestrationService = app_request.app.state.orchestrator
        
        await orchestrator._close_session(session_id)
        
        logger.info("Closed orchestration session", session_id=session_id)
        
        return {
            "session_id": session_id,
            "status": "closed",
            "message": "Orchestration session closed successfully"
        }
        
    except Exception as e:
        logger.error("Failed to close orchestration session", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/orchestration/capabilities")
async def get_orchestration_capabilities():
    """Get available orchestration capabilities."""
    return {
        "capabilities": {
            "crewai": {
                "status": "available",
                "agents": [
                    "strategic_analyst",
                    "technical_implementer", 
                    "revenue_optimizer"
                ],
                "description": "Multi-agent collaboration for strategic analysis"
            },
            "mem0": {
                "status": "available",
                "features": [
                    "context_persistence",
                    "session_memory",
                    "analysis_results"
                ],
                "description": "Persistent memory for AI collaboration"
            },
            "analytics": {
                "status": "available",
                "features": [
                    "performance_tracking",
                    "collaboration_logging",
                    "strategic_analysis"
                ],
                "description": "Comprehensive analytics and monitoring"
            }
        },
        "supported_analysis_types": [
            "bricks_roadmap",
            "revenue_opportunity",
            "strategic_gap_detection",
            "resource_optimization"
        ]
    }
