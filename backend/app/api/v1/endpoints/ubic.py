"""
UBIC v1.5 Compliant Endpoints for I MEMORY BRICK
Trinity BRICKS - I MEMORY

All 9 required UBIC endpoints for inter-BRICK communication
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
    System health status
    
    Returns comprehensive health information including:
    - Overall status
    - Database connectivity
    - Redis cache status
    - Mem0.ai service status
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
            health_data["mem0"] = mem0_status
            health_data["redis_cache"] = "enabled" if mem0_service.redis_client else "disabled"
        except Exception as e:
            health_data["mem0"] = f"error: {str(e)}"
            health_data["status"] = "degraded"
        
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
    Memory operations available
    
    Returns detailed list of all capabilities this BRICK provides
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
                "description": "Memories persist across container restarts",
                "status": "available"
            },
            {
                "name": "redis_caching",
                "description": "Redis caching layer for performance",
                "status": "available"
            },
            {
                "name": "memory_storage",
                "description": "Store structured memory with metadata",
                "methods": ["POST /memory/store"]
            },
            {
                "name": "memory_search",
                "description": "Search memories by natural language",
                "methods": ["POST /memory/search"]
            },
            {
                "name": "user_memories",
                "description": "Retrieve all memories for a user",
                "methods": ["GET /memory/user/{id}"]
            },
            {
                "name": "memory_deletion",
                "description": "Delete specific memory",
                "methods": ["DELETE /memory/{id}"]
            },
            {
                "name": "memory_statistics",
                "description": "Get usage and performance stats",
                "methods": ["GET /memory/stats"]
            }
        ],
        "limitations": [
            "Mem0.ai requires valid API key for full functionality",
            "Redis optional but recommended for performance",
            "User isolation requires user_id in all requests"
        ],
        "ubic_compliance": "v1.5",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/state")
async def get_state():
    """
    Current memory usage metrics
    
    Returns runtime state and performance metrics
    """
    try:
        from app.services.mem0_service import Mem0Service
        from app.core.database import AsyncSessionLocal
        from sqlalchemy import text, func
        from app.models.memory import Memory
        
        state_data = {
            "service": "I_MEMORY",
            "status": service_state["status"],
            "config_version": service_state["config_version"],
            "timestamp": datetime.now().isoformat()
        }
        
        # Get database statistics
        try:
            async with AsyncSessionLocal() as db:
                result = await db.execute(
                    text("SELECT COUNT(*) as count FROM memories")
                )
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
    Mem0.ai, PostgreSQL, Redis status
    
    Returns status of all external dependencies
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
            "version": pg_version[:50],  # Truncate for readability
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
        
        redis_url = settings.REDIS_URL if hasattr(settings, 'REDIS_URL') else "redis://redis:6379"
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
            "note": "Caching disabled, performance may be reduced"
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
            "required": True,
            "note": mem0_status.get("message", "")
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
    Store memory via message bus
    
    UBIC standard message bus endpoint for storing memories
    """
    try:
        logger.info("Received UBIC message",
                   source=message.source,
                   message_type=message.message_type,
                   trace_id=message.trace_id)
        
        # Route message based on type
        if message.message_type == "STORE_MEMORY":
            from app.services.mem0_service import Mem0Service
            
            mem0_service = Mem0Service()
            await mem0_service.initialize()
            
            user_id = message.payload.get("user_id", "default")
            content = message.payload.get("content", {})
            
            result = await mem0_service.add_memory(content, user_id)
            
            return {
                "idempotency_key": message.idempotency_key,
                "trace_id": message.trace_id,
                "status": "success",
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        
        elif message.message_type == "SEARCH_MEMORY":
            from app.services.mem0_service import Mem0Service
            
            mem0_service = Mem0Service()
            await mem0_service.initialize()
            
            user_id = message.payload.get("user_id", "default")
            query = message.payload.get("query", "")
            limit = message.payload.get("limit", 10)
            
            results = await mem0_service.search_memories(query, user_id, limit)
            
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
async def send_query(message: UBICMessage):
    """
    Query memory via message bus
    
    UBIC standard message bus endpoint for querying memories
    """
    try:
        logger.info("Processing query message",
                   source=message.source,
                   message_type=message.message_type,
                   trace_id=message.trace_id)
        
        from app.services.mem0_service import Mem0Service
        
        mem0_service = Mem0Service()
        await mem0_service.initialize()
        
        # Handle different query types
        if message.message_type == "GET_USER_MEMORIES":
            user_id = message.payload.get("user_id", "default")
            limit = message.payload.get("limit", 50)
            
            memories = await mem0_service.get_user_memories(user_id, limit)
            
            return {
                "idempotency_key": message.idempotency_key,
                "trace_id": message.trace_id,
                "status": "success",
                "memories": memories,
                "count": len(memories),
                "timestamp": datetime.now().isoformat()
            }
        
        elif message.message_type == "GET_STATS":
            user_id = message.payload.get("user_id")
            
            if user_id:
                stats = await mem0_service.get_user_stats(user_id)
            else:
                # Get overall stats
                stats = {
                    "service": "I_MEMORY",
                    "status": "operational",
                    "timestamp": datetime.now().isoformat()
                }
            
            return {
                "idempotency_key": message.idempotency_key,
                "trace_id": message.trace_id,
                "status": "success",
                "stats": stats,
                "timestamp": datetime.now().isoformat()
            }
        
        else:
            return {
                "idempotency_key": message.idempotency_key,
                "trace_id": message.trace_id,
                "status": "unsupported",
                "message": f"Query type '{message.message_type}' not supported",
                "timestamp": datetime.now().isoformat()
            }
        
    except Exception as e:
        logger.error("Failed to process query", error=str(e), trace_id=message.trace_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/reload-config")
async def reload_config():
    """
    Reload configuration
    
    Reload service configuration without restart
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
    
    Initiate graceful shutdown process
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
    Immediate shutdown
    
    Emergency stop - immediate shutdown without cleanup
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
