"""
UBIC v1.5 Compliant Endpoints for I MEMORY BRICK
Trinity BRICKS - Required 9 endpoints for inter-BRICK communication
"""

from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
import structlog
from datetime import datetime
import uuid
import asyncio

logger = structlog.get_logger(__name__)
router = APIRouter()

# Global state for service management
service_state = {
    "status": "running",
    "start_time": datetime.now().isoformat(),
    "shutdown_requested": False,
    "config_version": "1.0.0"
}


class UBICMessage(BaseModel):
    """UBIC Standard Message Format"""
    idempotency_key: str = Field(default_factory=lambda: str(uuid.uuid4()))
    priority: str = Field(default="normal")  # normal, high, emergency
    source: str
    target: str = "I_MEMORY"
    message_type: str
    payload: Dict[str, Any]
    trace_id: str = Field(default_factory=lambda: f"trace-{uuid.uuid4()}")


# ============================================
# UBIC v1.5 Required Endpoints (9 total)
# ============================================

@router.get("/health")
async def health_check():
    """
    Health check with dependency status
    Trinity BRICKS I MEMORY - UBIC v1.5 Endpoint 1/9
    """
    try:
        from app.services.mem0_service import Mem0Service
        from app.core.database import engine
        
        health_data = {
            "status": "healthy" if service_state["status"] == "running" else "degraded",
            "service": "I_MEMORY",
            "version": "1.0.0",
            "brick_type": "Trinity_BRICKS",
            "timestamp": datetime.now().isoformat(),
            "uptime_since": service_state["start_time"]
        }
        
        # Check database
        try:
            from sqlalchemy import text
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            health_data["database"] = "connected"
        except Exception as e:
            health_data["database"] = f"error: {str(e)}"
            health_data["status"] = "degraded"
        
        # Check Mem0 service
        try:
            mem0_service = Mem0Service()
            await mem0_service.initialize()
            mem0_status = await mem0_service.get_status()
            health_data["mem0"] = mem0_status.get("status", "unknown")
            health_data["redis_cache"] = "enabled" if mem0_service.redis_client else "disabled"
        except Exception as e:
            health_data["mem0"] = f"error: {str(e)}"
        
        return health_data
        
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        return {
            "status": "error",
            "service": "I_MEMORY",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@router.get("/capabilities")
async def get_capabilities():
    """
    List memory capabilities
    Trinity BRICKS I MEMORY - UBIC v1.5 Endpoint 2/9
    """
    return {
        "service": "I_MEMORY",
        "brick_type": "Trinity_BRICKS",
        "version": "1.0.0",
        "capabilities": [
            {
                "name": "multi_user_isolation",
                "description": "Each user has private memory namespace",
                "status": "available"
            },
            {
                "name": "semantic_search",
                "description": "Natural language memory search",
                "status": "available"
            },
            {
                "name": "persistent_storage",
                "description": "Memories persist across restarts",
                "status": "available"
            },
            {
                "name": "redis_caching",
                "description": "Redis caching for performance",
                "status": "available"
            },
            {
                "name": "memory_add",
                "description": "Store new memory with user isolation",
                "methods": ["POST /memory/add"]
            },
            {
                "name": "memory_search",
                "description": "Semantic search across memories",
                "methods": ["GET /memory/search"]
            },
            {
                "name": "memory_get_all",
                "description": "Retrieve all user memories",
                "methods": ["GET /memory/get-all"]
            },
            {
                "name": "memory_delete",
                "description": "Delete specific memory",
                "methods": ["DELETE /memory/delete"]
            },
            {
                "name": "memory_stats",
                "description": "Memory usage statistics",
                "methods": ["GET /memory/stats"]
            }
        ],
        "limitations": [
            "Mem0.ai requires valid API key for full functionality",
            "Redis optional but recommended for performance"
        ],
        "ubic_compliance": "v1.5",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/state")
async def get_state():
    """
    Operational metrics (not memory contents)
    Trinity BRICKS I MEMORY - UBIC v1.5 Endpoint 3/9
    """
    try:
        from app.services.mem0_service import Mem0Service
        from app.core.database import AsyncSessionLocal
        from sqlalchemy import text
        
        state_data = {
            "service": "I_MEMORY",
            "status": service_state["status"],
            "config_version": service_state["config_version"],
            "timestamp": datetime.now().isoformat()
        }
        
        # Get database statistics
        try:
            async with AsyncSessionLocal() as db:
                result = await db.execute(text("SELECT COUNT(*) FROM memories"))
                memory_count = result.scalar()
                state_data["database_memories"] = memory_count
        except Exception as e:
            state_data["database_memories"] = f"error: {str(e)}"
        
        # Get Mem0 statistics
        try:
            mem0_service = Mem0Service()
            await mem0_service.initialize()
            state_data["mem0_initialized"] = mem0_service.initialized
            state_data["redis_enabled"] = mem0_service.redis_client is not None
        except Exception as e:
            state_data["mem0_error"] = str(e)
        
        return state_data
        
    except Exception as e:
        logger.error("Failed to get state", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/dependencies")
async def get_dependencies():
    """
    List infra/functional dependencies
    Trinity BRICKS I MEMORY - UBIC v1.5 Endpoint 4/9
    """
    dependencies = {
        "service": "I_MEMORY",
        "timestamp": datetime.now().isoformat(),
        "dependencies": []
    }
    
    # Check PostgreSQL
    try:
        from app.core.database import engine
        from sqlalchemy import text
        
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT version()"))
            pg_version = result.scalar()
        
        dependencies["dependencies"].append({
            "name": "PostgreSQL",
            "type": "database",
            "status": "healthy",
            "version": pg_version[:50],
            "required": True
        })
    except Exception as e:
        dependencies["dependencies"].append({
            "name": "PostgreSQL",
            "type": "database",
            "status": "error",
            "error": str(e),
            "required": True
        })
    
    # Check Redis
    try:
        import redis.asyncio as redis
        from app.core.config import settings
        
        redis_url = getattr(settings, 'REDIS_URL', "redis://redis:6379")
        redis_client = redis.from_url(redis_url, decode_responses=True)
        await redis_client.ping()
        redis_info = await redis_client.info()
        await redis_client.close()
        
        dependencies["dependencies"].append({
            "name": "Redis",
            "type": "cache",
            "status": "healthy",
            "version": redis_info.get("redis_version", "unknown"),
            "required": False
        })
    except Exception as e:
        dependencies["dependencies"].append({
            "name": "Redis",
            "type": "cache",
            "status": "unavailable",
            "error": str(e),
            "required": False,
            "note": "Caching disabled"
        })
    
    # Check Mem0.ai
    try:
        from app.services.mem0_service import Mem0Service
        
        mem0_service = Mem0Service()
        await mem0_service.initialize()
        mem0_status = await mem0_service.get_status()
        
        dependencies["dependencies"].append({
            "name": "Mem0.ai",
            "type": "ai_service",
            "status": mem0_status.get("status", "unknown"),
            "mode": mem0_status.get("mode", "unknown"),
            "api_key_configured": mem0_status.get("api_key_configured", False),
            "required": True
        })
    except Exception as e:
        dependencies["dependencies"].append({
            "name": "Mem0.ai",
            "type": "ai_service",
            "status": "error",
            "error": str(e),
            "required": True
        })
    
    return dependencies


@router.post("/message")
async def receive_message(message: UBICMessage):
    """
    Receive commands via message bus
    Trinity BRICKS I MEMORY - UBIC v1.5 Endpoint 5/9
    """
    try:
        logger.info("Received UBIC message",
                   source=message.source,
                   message_type=message.message_type,
                   trace_id=message.trace_id)
        
        from app.services.mem0_service import Mem0Service
        mem0_service = Mem0Service()
        await mem0_service.initialize()
        
        # Route message based on type
        if message.message_type == "ADD_MEMORY":
            user_id = message.payload.get("user_id", "default")
            content = message.payload.get("content", {})
            metadata = message.payload.get("metadata")
            
            result = await mem0_service.add(content, user_id, metadata)
            
            return {
                "idempotency_key": message.idempotency_key,
                "trace_id": message.trace_id,
                "status": "success",
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        
        elif message.message_type == "SEARCH_MEMORY":
            user_id = message.payload.get("user_id", "default")
            query = message.payload.get("query", "")
            limit = message.payload.get("limit", 10)
            
            results = await mem0_service.search(query, user_id, limit)
            
            return {
                "idempotency_key": message.idempotency_key,
                "trace_id": message.trace_id,
                "status": "success",
                "results": results,
                "timestamp": datetime.now().isoformat()
            }
        
        else:
            return {
                "idempotency_key": message.idempotency_key,
                "trace_id": message.trace_id,
                "status": "unsupported",
                "message": f"Message type '{message.message_type}' not supported",
                "timestamp": datetime.now().isoformat()
            }
        
    except Exception as e:
        logger.error("Failed to process message", error=str(e), trace_id=message.trace_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/send")
async def send_event(message: UBICMessage):
    """
    Send events to message bus
    Trinity BRICKS I MEMORY - UBIC v1.5 Endpoint 6/9
    """
    try:
        logger.info("Processing send event",
                   source=message.source,
                   message_type=message.message_type,
                   trace_id=message.trace_id)
        
        from app.services.mem0_service import Mem0Service
        mem0_service = Mem0Service()
        await mem0_service.initialize()
        
        if message.message_type == "GET_ALL_MEMORIES":
            user_id = message.payload.get("user_id", "default")
            limit = message.payload.get("limit", 100)
            
            memories = await mem0_service.get_all(user_id, limit)
            
            return {
                "idempotency_key": message.idempotency_key,
                "trace_id": message.trace_id,
                "status": "success",
                "memories": memories,
                "count": len(memories),
                "timestamp": datetime.now().isoformat()
            }
        
        else:
            return {
                "idempotency_key": message.idempotency_key,
                "trace_id": message.trace_id,
                "status": "unsupported",
                "message": f"Event type '{message.message_type}' not supported",
                "timestamp": datetime.now().isoformat()
            }
        
    except Exception as e:
        logger.error("Failed to send event", error=str(e), trace_id=message.trace_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/reload-config")
async def reload_config():
    """
    Reload configuration
    Trinity BRICKS I MEMORY - UBIC v1.5 Endpoint 7/9
    """
    try:
        logger.info("Reloading configuration")
        
        # Increment config version
        current_version = service_state["config_version"]
        major, minor, patch = current_version.split(".")
        new_version = f"{major}.{minor}.{int(patch) + 1}"
        service_state["config_version"] = new_version
        
        # Reinitialize services
        from app.services.mem0_service import Mem0Service
        mem0_service = Mem0Service()
        await mem0_service.initialize()
        
        return {
            "status": "success",
            "message": "Configuration reloaded",
            "old_version": current_version,
            "new_version": new_version,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to reload config", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/shutdown")
async def graceful_shutdown():
    """
    Graceful shutdown
    Trinity BRICKS I MEMORY - UBIC v1.5 Endpoint 8/9
    """
    try:
        logger.info("Initiating graceful shutdown")
        
        service_state["shutdown_requested"] = True
        service_state["status"] = "shutting_down"
        
        # Cleanup resources
        from app.services.mem0_service import Mem0Service
        mem0_service = Mem0Service()
        await mem0_service.cleanup()
        
        return {
            "status": "shutdown_initiated",
            "message": "Graceful shutdown in progress",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to shutdown gracefully", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/emergency-stop")
async def emergency_stop():
    """
    Immediate halt
    Trinity BRICKS I MEMORY - UBIC v1.5 Endpoint 9/9
    """
    try:
        logger.warning("Emergency stop requested")
        
        service_state["shutdown_requested"] = True
        service_state["status"] = "emergency_stopped"
        
        # Attempt quick cleanup but don't wait
        async def quick_cleanup():
            try:
                from app.services.mem0_service import Mem0Service
                mem0_service = Mem0Service()
                await mem0_service.cleanup()
            except:
                pass
        
        # Fire and forget cleanup
        asyncio.create_task(quick_cleanup())
        
        return {
            "status": "emergency_stopped",
            "message": "Service stopped immediately",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Emergency stop failed", error=str(e))
        return {
            "status": "error",
            "message": f"Emergency stop failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

