"""
UBIC v1.5 Compliance Endpoints
Makes this a proper BRICK with standard communication protocols
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import structlog
from datetime import datetime

logger = structlog.get_logger(__name__)
router = APIRouter()


class UBICCapabilitiesResponse(BaseModel):
    """UBIC capabilities response"""
    brick_name: str
    brick_version: str
    capabilities: List[str]
    supported_protocols: List[str]
    endpoints: Dict[str, str]
    status: str


class UBICMessageRequest(BaseModel):
    """UBIC message request"""
    from_brick: str
    to_brick: str
    message_type: str
    payload: Dict[str, Any]
    session_id: Optional[str] = None


class UBICMessageResponse(BaseModel):
    """UBIC message response"""
    success: bool
    message_id: str
    response_payload: Dict[str, Any]
    timestamp: str


@router.get("/capabilities", response_model=UBICCapabilitiesResponse)
async def get_capabilities():
    """
    UBIC v1.5 Compliance: /capabilities endpoint
    Returns BRICK capabilities and available services
    """
    
    return UBICCapabilitiesResponse(
        brick_name="I PROACTIVE BRICK Orchestration Intelligence",
        brick_version="1.0.0",
        capabilities=[
            "multi_agent_orchestration",
            "strategic_analysis",
            "brick_development",
            "revenue_optimization",
            "gap_analysis",
            "ai_routing",
            "memory_persistence",
            "real_time_collaboration"
        ],
        supported_protocols=[
            "UBIC v1.5",
            "REST API",
            "WebSocket (planned)",
            "BRICK-to-BRICK messaging"
        ],
        endpoints={
            "/health": "Health check and system status",
            "/capabilities": "BRICK capabilities (UBIC v1.5)",
            "/message": "BRICK-to-BRICK messaging (UBIC v1.5)",
            "/send": "Send orchestration request (UBIC v1.5)",
            "/orchestration/execute": "Execute multi-agent orchestration",
            "/orchestration/status": "Get orchestration status",
            "/orchestration/sessions": "List orchestration sessions",
            "/memory/create": "Create AI memory",
            "/memory/search": "Search AI memories",
            "/chat/send": "Send chat message",
            "/strategic/dashboard": "Strategic intelligence dashboard",
            "/revenue/proposals": "BRICK development proposals"
        },
        status="operational"
    )


@router.post("/message", response_model=UBICMessageResponse)
async def receive_message(request: UBICMessageRequest):
    """
    UBIC v1.5 Compliance: /message endpoint
    Receives messages from other BRICKs
    """
    
    try:
        logger.info("Received UBIC message", 
                   from_brick=request.from_brick,
                   to_brick=request.to_brick,
                   message_type=request.message_type)
        
        # Process message based on type
        if request.message_type == "orchestration_request":
            response_payload = await _handle_orchestration_request(request.payload)
        elif request.message_type == "status_query":
            response_payload = await _handle_status_query(request.payload)
        elif request.message_type == "capability_query":
            response_payload = await _handle_capability_query(request.payload)
        elif request.message_type == "data_sync":
            response_payload = await _handle_data_sync(request.payload)
        else:
            response_payload = {
                "status": "unknown_message_type",
                "message": f"Message type '{request.message_type}' not supported"
            }
        
        message_id = f"msg_{int(datetime.now().timestamp() * 1000)}"
        
        logger.info("UBIC message processed successfully", message_id=message_id)
        
        return UBICMessageResponse(
            success=True,
            message_id=message_id,
            response_payload=response_payload,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        logger.error("Failed to process UBIC message", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Message processing failed: {str(e)}"
        )


@router.post("/send")
async def send_orchestration_request(
    goal: str,
    task_type: str = "strategic_analysis",
    context: Dict[str, Any] = {},
    session_id: Optional[str] = None
):
    """
    UBIC v1.5 Compliance: /send endpoint
    Simplified interface for triggering orchestration
    """
    
    try:
        # Import orchestrator
        from app.api.v1.endpoints.orchestration import get_ai_orchestrator
        
        orchestrator = await get_ai_orchestrator()
        
        # Generate session ID if not provided
        session_id = session_id or f"session_{int(datetime.now().timestamp() * 1000)}"
        
        logger.info("UBIC /send triggered orchestration", 
                   goal=goal,
                   task_type=task_type,
                   session_id=session_id)
        
        # Execute orchestration
        results = await orchestrator.orchestrate_task(
            task_type=task_type,
            goal=goal,
            context=context,
            session_id=session_id
        )
        
        return {
            "success": True,
            "message": "Orchestration completed successfully",
            "session_id": session_id,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error("UBIC /send orchestration failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Orchestration failed: {str(e)}"
        )


# Helper functions for message processing

async def _handle_orchestration_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle orchestration request from another BRICK"""
    
    from app.api.v1.endpoints.orchestration import get_ai_orchestrator
    
    orchestrator = await get_ai_orchestrator()
    
    results = await orchestrator.orchestrate_task(
        task_type=payload.get("task_type", "strategic_analysis"),
        goal=payload.get("goal", ""),
        context=payload.get("context", {}),
        session_id=payload.get("session_id", f"session_{int(datetime.now().timestamp() * 1000)}")
    )
    
    return {
        "status": "completed",
        "results": results
    }


async def _handle_status_query(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle status query from another BRICK"""
    
    return {
        "status": "operational",
        "services": {
            "multi_model_router": "operational",
            "strategic_intelligence": "operational",
            "revenue_analysis": "operational",
            "memory_service": "operational"
        },
        "uptime": "operational",
        "last_orchestration": "recent"
    }


async def _handle_capability_query(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle capability query from another BRICK"""
    
    return {
        "capabilities": [
            "multi_agent_orchestration",
            "strategic_analysis",
            "brick_development",
            "revenue_optimization"
        ],
        "ai_models": ["gpt-4", "claude", "gemini"],
        "max_concurrent_tasks": 10
    }


async def _handle_data_sync(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle data synchronization from another BRICK"""
    
    return {
        "status": "synced",
        "records_processed": payload.get("record_count", 0),
        "sync_timestamp": datetime.now().isoformat()
    }
