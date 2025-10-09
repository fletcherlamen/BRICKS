"""
UBIC v1.5 Orchestration API Endpoints
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
import structlog
import time
from datetime import datetime

from app.services.ai_orchestrator import AIOrchestrator
from app.models.orchestration import UBICResponse

logger = structlog.get_logger(__name__)
router = APIRouter()

# Global orchestrator instance
_orchestrator_instance: Optional[AIOrchestrator] = None


async def get_ai_orchestrator() -> AIOrchestrator:
    """Get or create the global AIOrchestrator instance"""
    global _orchestrator_instance
    
    if _orchestrator_instance is None:
        _orchestrator_instance = AIOrchestrator()
        await _orchestrator_instance.initialize()
        logger.info("AIOrchestrator initialized successfully")
    
    return _orchestrator_instance


class OrchestrationRequest(BaseModel):
    """Request model for orchestration tasks"""
    task_type: str
    goal: str
    context: Dict[str, Any] = {}
    session_id: Optional[str] = None
    priority: Optional[str] = "normal"  # high, normal, low
    automation_mode: Optional[bool] = False  # For BRICK 2 automation


class OrchestrationResponse(BaseModel):
    """Response model for orchestration tasks"""
    session_id: str
    task_type: str
    status: str
    results: Dict[str, Any]
    timestamp: str
    run_id: str


class SessionResponse(BaseModel):
    """Response model for session details"""
    session_id: str
    run_id: str
    goal: str
    task_type: str
    status: str
    confidence: float
    execution_time_ms: int
    created_at: str
    completed_at: Optional[str] = None
    context: Dict[str, Any]
    outputs: Dict[str, Any]
    automation_ready: bool


class SessionsListResponse(BaseModel):
    """Response model for sessions list"""
    sessions: List[SessionResponse]
    total_count: int
    timestamp: str


@router.post("/execute", response_model=UBICResponse)
async def execute_orchestration(
    request: OrchestrationRequest,
    orchestrator: AIOrchestrator = Depends(get_ai_orchestrator)
):
    """Execute TRUE multi-agent orchestration across AI systems"""
    
    try:
        # Generate session ID if not provided
        session_id = request.session_id or f"session_{int(time.time() * 1000)}"
        
        # Execute TRUE multi-agent orchestration using AIOrchestrator
        logger.info("Starting multi-agent orchestration", 
                   task_type=request.task_type,
                   goal=request.goal,
                   session_id=session_id)
        
        # Use AIOrchestrator.orchestrate_task for TRUE orchestration
        results = await orchestrator.orchestrate_task(
            task_type=request.task_type.lower().replace(" ", "_").replace("-", "_"),
            goal=request.goal,
            context=request.context,
            session_id=session_id
        )
        
        # Save to database
        from app.core.database import AsyncSessionLocal
        from app.models.orchestration import OrchestrationSession
        from sqlalchemy import select
        
        async with AsyncSessionLocal() as db:
            # Check if session exists
            stmt = select(OrchestrationSession).where(OrchestrationSession.session_id == session_id)
            result = await db.execute(stmt)
            existing_session = result.scalar_one_or_none()
            
            if not existing_session:
                # Create new session with valid fields only
                new_session = OrchestrationSession(
                    session_id=session_id,
                    goal=request.goal,
                    context={
                        "task_type": request.task_type,
                        "original_context": request.context,
                        "orchestration_results": results
                    },
                    status="completed"
                )
                db.add(new_session)
                await db.commit()
        
        logger.info("Multi-agent orchestration completed successfully", session_id=session_id)
        
        return UBICResponse(
            success=True,
            message="Multi-agent orchestration completed successfully",
            data={
                "session_id": session_id,
                "task_type": request.task_type,
                "results": results,
                "orchestration_type": "multi_agent",
                "agents_used": results.get("agents_involved", [])
            },
            session_id=session_id
        )
    
    except Exception as e:
        logger.error("Multi-agent orchestration failed", error=str(e), task_type=request.task_type)
        return UBICResponse(
            success=False,
            message=f"Orchestration failed: {str(e)}",
            data={"error": str(e), "task_type": request.task_type}
        )


# Legacy endpoints for backward compatibility
@router.post("/execute-legacy", response_model=UBICResponse)
async def execute_orchestration_legacy(
    request: OrchestrationRequest
):
    """Legacy endpoint - redirects to new multi-agent orchestration"""
    
    try:
        # Import RealOrchestrator for legacy support
        from app.services.real_orchestrator import real_orchestrator
        
        # Execute orchestration based on task type
        task_type_lower = request.task_type.lower().replace(" ", "_").replace("-", "_")
        
        if task_type_lower in ["strategic_analysis", "strategic"]:
            results = await real_orchestrator.execute_strategic_analysis(
                goal=request.goal,
                context=request.context,
                session_id=request.session_id
            )
        elif task_type_lower in ["brick_development", "brick", "development"]:
            results = await real_orchestrator.execute_brick_development(
                goal=request.goal,
                context=request.context,
                session_id=request.session_id
            )
        elif task_type_lower in ["revenue_optimization", "revenue", "optimization"]:
            results = await orchestrator.execute_revenue_optimization(
                goal=request.goal,
                context=request.context,
                session_id=request.session_id
            )
        elif task_type_lower in ["gap_analysis", "gap"]:
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
        
        # Structured response for BRICK 2 automation
        automation_response = {
            "run_id": results.get("run_id"),
            "session_id": results.get("session_id"),
            "task_type": request.task_type,
            "status": "completed",
            "confidence": results.get("confidence"),
            "execution_time_ms": results.get("execution_time_ms"),
            "priority": request.priority,
            "automation_mode": request.automation_mode,
            "context": request.context,
            "results": results,
            "automation_ready": True,
            "structured_outputs": {
                "recommendations": results.get("analysis", {}).get("recommendations", []),
                "key_insights": results.get("analysis", {}).get("key_insights", []),
                "risk_assessment": results.get("analysis", {}).get("risk_assessment", {}),
                "revenue_potential": results.get("analysis", {}).get("revenue_potential", {}),
                "systems_built": results.get("real_systems_built", {}),
                "generated_apps": results.get("real_systems_built", {}).get("applications", []),
                "deployment_files": results.get("real_systems_built", {}).get("applications", [{}])[0].get("generated_files", {}),
                "ai_systems_used": results.get("ai_systems_used", []),
                "confidence_score": results.get("confidence", 0.0)
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return UBICResponse(
            status=Status.SUCCESS,
            message="Orchestration completed successfully - BRICK 2 automation ready",
            details=automation_response
        )
        
    except Exception as e:
        logger.error("Unexpected orchestration error", error=str(e))
        return UBICResponse(
            status=Status.ERROR,
            error_code="INTERNAL_ERROR",
            message="Internal server error",
            details={"error": str(e), "automation_ready": False}
        )


@router.post("/strategic-analysis")
async def strategic_analysis(
    request: OrchestrationRequest,
    orchestrator: AIOrchestrator = Depends(get_ai_orchestrator)
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
    orchestrator: AIOrchestrator = Depends(get_ai_orchestrator)
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
    orchestrator: AIOrchestrator = Depends(get_ai_orchestrator)
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
    orchestrator: AIOrchestrator = Depends(get_ai_orchestrator)
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
    orchestrator: AIOrchestrator = Depends(get_ai_orchestrator)
):
    """Get orchestration system status from VPS database"""
    
    try:
        # Get real counts from VPS database
        from app.core.database import AsyncSessionLocal
        from app.models.orchestration import OrchestrationSession
        from app.models.memory import Memory
        from sqlalchemy import select, func
        
        async with AsyncSessionLocal() as db:
            # Count sessions from VPS database
            session_count_result = await db.execute(
                select(func.count(OrchestrationSession.id))
            )
            session_count = session_count_result.scalar() or 0
            
            # Count memories from VPS database
            memory_count_result = await db.execute(
                select(func.count(Memory.id))
            )
            memory_count = memory_count_result.scalar() or 0
        
        return {
            "orchestration_status": "operational",
            "sessions_count": session_count,
            "memories_count": memory_count,
            "system_status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "data_source": "vps_database"
        }
        
    except Exception as e:
        logger.error("Failed to get orchestration status from VPS database", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/sessions", response_model=SessionsListResponse)
async def get_orchestration_sessions(
    orchestrator: AIOrchestrator = Depends(get_ai_orchestrator),
    limit: int = 10,
    status_filter: Optional[str] = None,
    task_type_filter: Optional[str] = None
):
    """Get orchestration sessions with status, goal, and outputs - BRICK 2 Automation Ready"""
    
    try:
        sessions = await orchestrator.get_session_history(limit=limit)
        
        # Filter sessions if requested
        if status_filter:
            sessions = [s for s in sessions if s.get("status", "").lower() == status_filter.lower()]
        if task_type_filter:
            sessions = [s for s in sessions if s.get("task_type", "").lower() == task_type_filter.lower()]
        
        # Format sessions with complete information for BRICK 2 automation
        formatted_sessions = []
        for session in sessions:
            formatted_sessions.append(SessionResponse(
                session_id=session["session_id"],
                run_id=session["run_id"],
                goal=session["goal"],
                task_type=session["task_type"],
                status=session["status"],
                confidence=session["confidence"],
                execution_time_ms=session["execution_time_ms"],
                created_at=session["created_at"],
                completed_at=session.get("completed_at"),
                context=session.get("context", {}),
                outputs={
                    "recommendations": session.get("analysis", {}).get("recommendations", []),
                    "key_insights": session.get("analysis", {}).get("key_insights", []),
                    "risk_assessment": session.get("analysis", {}).get("risk_assessment", {}),
                    "revenue_potential": session.get("analysis", {}).get("revenue_potential", {}),
                    "systems_built": session.get("real_systems_built", {}),
                    "generated_apps": session.get("real_systems_built", {}).get("applications", []),
                    "ai_systems_used": session.get("ai_systems_used", []),
                    "confidence_score": session.get("confidence", 0.0)
                },
                automation_ready=True
            ))
        
        return SessionsListResponse(
            sessions=formatted_sessions,
            total_count=len(formatted_sessions),
            timestamp=datetime.now().isoformat()
        )
        
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


@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_orchestration_session(
    session_id: str,
    orchestrator: AIOrchestrator = Depends(get_ai_orchestrator)
):
    """Get specific orchestration session details with complete outputs - BRICK 2 Automation Ready"""
    
    try:
        # Get session from orchestrator
        sessions = await orchestrator.get_session_history(limit=100)
        session = next((s for s in sessions if s["session_id"] == session_id), None)
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session {session_id} not found"
            )
        
        # Return structured session response for BRICK 2 automation
        return SessionResponse(
            session_id=session["session_id"],
            run_id=session["run_id"],
            goal=session["goal"],
            task_type=session["task_type"],
            status=session["status"],
            confidence=session["confidence"],
            execution_time_ms=session["execution_time_ms"],
            created_at=session["created_at"],
            completed_at=session.get("completed_at"),
            context=session.get("context", {}),
            outputs={
                "recommendations": session.get("analysis", {}).get("recommendations", []),
                "key_insights": session.get("analysis", {}).get("key_insights", []),
                "risk_assessment": session.get("analysis", {}).get("risk_assessment", {}),
                "revenue_potential": session.get("analysis", {}).get("revenue_potential", {}),
                "systems_built": session.get("real_systems_built", {}),
                "generated_apps": session.get("real_systems_built", {}).get("applications", []),
                "deployment_files": session.get("real_systems_built", {}).get("applications", [{}])[0].get("generated_files", {}),
                "ai_systems_used": session.get("ai_systems_used", []),
                "confidence_score": session.get("confidence", 0.0)
            },
            automation_ready=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get orchestration session", error=str(e), session_id=session_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/trigger", response_model=UBICResponse)
async def trigger_orchestration_programmatically(
    request: OrchestrationRequest,
    orchestrator: AIOrchestrator = Depends(get_ai_orchestrator)
):
    """Trigger orchestration programmatically for BRICK 2 automation - Non-UI endpoint"""
    
    try:
        # Validate automation mode
        if not request.automation_mode:
            request.automation_mode = True  # Force automation mode for programmatic calls
        
        # Execute orchestration based on task type
        task_type_lower = request.task_type.lower().replace(" ", "_").replace("-", "_")
        
        if task_type_lower in ["strategic_analysis", "strategic"]:
            results = await orchestrator.execute_strategic_analysis(
                goal=request.goal,
                context=request.context,
                session_id=request.session_id
            )
        elif task_type_lower in ["brick_development", "brick", "development"]:
            results = await orchestrator.execute_brick_development(
                goal=request.goal,
                context=request.context,
                session_id=request.session_id
            )
        elif task_type_lower in ["revenue_optimization", "revenue", "optimization"]:
            results = await orchestrator.execute_revenue_optimization(
                goal=request.goal,
                context=request.context,
                session_id=request.session_id
            )
        elif task_type_lower in ["gap_analysis", "gap"]:
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
        
        # Programmatic response optimized for automation
        programmatic_response = {
            "success": True,
            "run_id": results.get("run_id"),
            "session_id": results.get("session_id"),
            "task_type": request.task_type,
            "status": "completed",
            "confidence": results.get("confidence"),
            "execution_time_ms": results.get("execution_time_ms"),
            "priority": request.priority,
            "automation_mode": True,
            "context": request.context,
            "goal": request.goal,
            "structured_data": {
                "recommendations": results.get("analysis", {}).get("recommendations", []),
                "key_insights": results.get("analysis", {}).get("key_insights", []),
                "risk_assessment": results.get("analysis", {}).get("risk_assessment", {}),
                "revenue_potential": results.get("analysis", {}).get("revenue_potential", {}),
                "systems_built": results.get("real_systems_built", {}),
                "generated_applications": results.get("real_systems_built", {}).get("applications", []),
                "deployment_artifacts": results.get("real_systems_built", {}).get("applications", [{}])[0].get("generated_files", {}),
                "ai_systems_used": results.get("ai_systems_used", []),
                "confidence_score": results.get("confidence", 0.0),
                "automation_ready": True,
                "brick2_compatible": True
            },
            "timestamp": datetime.now().isoformat(),
            "api_version": "1.0",
            "automation_endpoint": True
        }
        
        return UBICResponse(
            status=Status.SUCCESS,
            message="Programmatic orchestration completed - BRICK 2 automation ready",
            details=programmatic_response
        )
        
    except Exception as e:
        logger.error("Programmatic orchestration failed", error=str(e))
        return UBICResponse(
            status=Status.ERROR,
            error_code="AUTOMATION_ERROR",
            message="Programmatic orchestration failed",
            details={
                "error": str(e),
                "automation_mode": True,
                "success": False,
                "brick2_compatible": False
            }
        )
