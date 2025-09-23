"""
UBIC v1.5 Orchestration API Endpoints
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
import structlog
import time
from datetime import datetime

from app.services.real_orchestrator import real_orchestrator
from app.models.ubic import UBICResponse, Status

logger = structlog.get_logger(__name__)
router = APIRouter()


class OrchestrationRequest(BaseModel):
    """Request model for orchestration tasks"""
    task_type: str
    goal: str
    context: Dict[str, Any] = {}
    session_id: Optional[str] = None


class OrchestrationResponse(BaseModel):
    """Response model for orchestration tasks"""
    session_id: str
    task_type: str
    status: str
    results: Dict[str, Any]
    timestamp: str
    run_id: str


def get_orchestrator():
    """Dependency to get real orchestrator instance"""
    return real_orchestrator


@router.post("/execute", response_model=UBICResponse)
async def execute_orchestration(
    request: OrchestrationRequest,
    orchestrator = Depends(get_orchestrator)
):
    """Execute an orchestrated task across multiple AI systems"""
    
    try:
        # Execute orchestration based on task type
        if request.task_type.lower() == "strategic analysis":
            results = await orchestrator.execute_strategic_analysis(
                goal=request.goal,
                context=request.context,
                session_id=request.session_id
            )
        elif request.task_type.lower() == "brick development":
            results = await orchestrator.execute_brick_development(
                goal=request.goal,
                context=request.context,
                session_id=request.session_id
            )
        elif request.task_type.lower() == "revenue optimization":
            results = await orchestrator.execute_revenue_optimization(
                goal=request.goal,
                context=request.context,
                session_id=request.session_id
            )
        elif request.task_type.lower() == "gap analysis":
            results = await orchestrator.execute_gap_analysis(
                goal=request.goal,
                context=request.context,
                session_id=request.session_id
            )
        else:
            # Default to strategic analysis
            results = await orchestrator.execute_strategic_analysis(
                goal=request.goal,
                context=request.context,
                session_id=request.session_id
            )
        
        return UBICResponse(
            status=Status.SUCCESS,
            message="Orchestration completed successfully",
            details={
                "run_id": results.get("run_id"),
                "session_id": results.get("session_id"),
                "task_type": request.task_type,
                "status": "completed",
                "confidence": results.get("confidence"),
                "execution_time_ms": results.get("execution_time_ms"),
                "results": results,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Unexpected orchestration error", error=str(e))
        return UBICResponse(
            status=Status.ERROR,
            error_code="INTERNAL_ERROR",
            message="Internal server error",
            details={"error": str(e)}
        )


@router.post("/strategic-analysis")
async def strategic_analysis(
    request: OrchestrationRequest,
    orchestrator = Depends(get_orchestrator)
):
    """Perform strategic analysis using multiple AI systems"""
    
    try:
        results = await orchestrator.execute_strategic_analysis(
            goal=request.goal,
            context=request.context,
            session_id=request.session_id
        )
        
        return {
            "run_id": results.get("run_id"),
            "session_id": results.get("session_id"),
            "analysis_type": "strategic",
            "status": "completed",
            "confidence": results.get("confidence"),
            "execution_time_ms": results.get("execution_time_ms"),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Strategic analysis failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/brick-development")
async def brick_development(
    request: OrchestrationRequest,
    orchestrator = Depends(get_orchestrator)
):
    """Orchestrate BRICK development using AI systems"""
    
    try:
        results = await orchestrator.execute_brick_development(
            goal=request.goal,
            context=request.context,
            session_id=request.session_id
        )
        
        return {
            "run_id": results.get("run_id"),
            "session_id": results.get("session_id"),
            "development_type": "brick",
            "status": "completed",
            "confidence": results.get("confidence"),
            "execution_time_ms": results.get("execution_time_ms"),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("BRICK development failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/revenue-optimization")
async def revenue_optimization(
    request: OrchestrationRequest,
    orchestrator = Depends(get_orchestrator)
):
    """Perform revenue optimization analysis"""
    
    try:
        results = await orchestrator.execute_revenue_optimization(
            goal=request.goal,
            context=request.context,
            session_id=request.session_id
        )
        
        return {
            "run_id": results.get("run_id"),
            "session_id": results.get("session_id"),
            "optimization_type": "revenue",
            "status": "completed",
            "confidence": results.get("confidence"),
            "execution_time_ms": results.get("execution_time_ms"),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Revenue optimization failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/gap-analysis")
async def gap_analysis(
    request: OrchestrationRequest,
    orchestrator = Depends(get_orchestrator)
):
    """Perform strategic gap analysis"""
    
    try:
        results = await orchestrator.execute_gap_analysis(
            goal=request.goal,
            context=request.context,
            session_id=request.session_id
        )
        
        return {
            "run_id": results.get("run_id"),
            "session_id": results.get("session_id"),
            "analysis_type": "gap",
            "status": "completed",
            "confidence": results.get("confidence"),
            "execution_time_ms": results.get("execution_time_ms"),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Gap analysis failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/status")
async def get_orchestration_status(
    orchestrator = Depends(get_orchestrator)
):
    """Get orchestration system status"""
    
    try:
        session_count = len(orchestrator.sessions)
        memory_count = len(orchestrator.memories)
        
        return {
            "orchestration_status": "operational",
            "sessions_count": session_count,
            "memories_count": memory_count,
            "system_status": "healthy",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get orchestration status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/sessions")
async def get_orchestration_sessions(
    orchestrator = Depends(get_orchestrator),
    limit: int = 10
):
    """Get list of orchestration sessions with real history"""
    
    try:
        sessions = orchestrator.get_session_history(limit=limit)
        
        # Format sessions for frontend
        formatted_sessions = []
        for session in sessions:
            formatted_sessions.append({
                "session_id": session["session_id"],
                "run_id": session["run_id"],
                "goal": session["goal"][:100] + "..." if len(session["goal"]) > 100 else session["goal"],
                "task_type": session["task_type"],
                "status": session["status"],
                "confidence": session["confidence"],
                "duration": f"{session['execution_time_ms'] // 1000}s" if session['execution_time_ms'] >= 1000 else f"{session['execution_time_ms']}ms",
                "timestamp": session["created_at"],
                "time_ago": _get_time_ago(session["created_at"])
            })
        
        return {
            "sessions": formatted_sessions,
            "total_count": len(sessions),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get orchestration sessions", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


def _get_time_ago(timestamp: str) -> str:
    """Get human-readable time ago string"""
    from datetime import datetime, timezone
    
    try:
        created_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        diff = now - created_time
        
        if diff.total_seconds() < 60:
            return f"{int(diff.total_seconds())} seconds ago"
        elif diff.total_seconds() < 3600:
            minutes = int(diff.total_seconds() / 60)
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        elif diff.total_seconds() < 86400:
            hours = int(diff.total_seconds() / 3600)
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            days = int(diff.total_seconds() / 86400)
            return f"{days} day{'s' if days > 1 else ''} ago"
    except:
        return "Unknown"


@router.get("/sessions/{session_id}")
async def get_orchestration_session(session_id: str):
    """Get specific orchestration session details"""
    
    try:
        # This would typically query the database for the specific session
        # For now, return mock data
        return {
            "session_id": session_id,
            "status": "completed",
            "created_at": datetime.now().isoformat(),
            "tasks": [],
            "results": {}
        }
        
    except Exception as e:
        logger.error("Failed to get orchestration session", error=str(e), session_id=session_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
