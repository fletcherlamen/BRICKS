"""
I MEMORY BRICK - Custom Memory Endpoints
Trinity BRICKS Specification

Endpoints:
- POST /memory/store       → Direct memory storage
- POST /memory/search      → Semantic search across memories
- GET  /memory/user/{id}   → Retrieve all user memories
- DELETE /memory/{id}      → Delete specific memory
- GET  /memory/stats       → Usage and performance statistics
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel, Field
import structlog
from datetime import datetime

logger = structlog.get_logger(__name__)
router = APIRouter()


class MemoryStoreRequest(BaseModel):
    """Request model for storing memory"""
    user_id: str = Field(..., description="User identifier for isolation")
    content: Dict[str, Any] = Field(..., description="Memory content")


class MemorySearchRequest(BaseModel):
    """Request model for searching memories"""
    user_id: str = Field(..., description="User identifier for isolation")
    query: str = Field(..., description="Natural language search query")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum results")


class MemoryDeleteRequest(BaseModel):
    """Request model for deleting memory"""
    user_id: str = Field(..., description="User identifier for ownership verification")


@router.post("/store")
async def store_memory(request: MemoryStoreRequest):
    """
    Direct memory storage with user isolation
    
    Example:
    ```python
    memory.add({
        "project": "I BUILD",
        "component": "I PROACTIVE",
        "status": "phase_1_complete",
        "test_coverage": 85,
        "last_audit": "2024-10-10"
    }, user_id="user@example.com")
    ```
    """
    try:
        from app.services.mem0_service import Mem0Service
        
        mem0_service = Mem0Service()
        await mem0_service.initialize()
        
        result = await mem0_service.add_memory(
            content=request.content,
            user_id=request.user_id
        )
        
        logger.info("Memory stored via I MEMORY endpoint",
                   user_id=request.user_id,
                   memory_id=result.get("memory_id"))
        
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to store memory", error=str(e), user_id=request.user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store memory: {str(e)}"
        )


@router.post("/search")
async def search_memories(request: MemorySearchRequest):
    """
    Semantic search across user's memories
    
    Example:
    ```python
    results = memory.search(
        "What's the status of I PROACTIVE?",
        user_id="user@example.com"
    )
    ```
    """
    try:
        from app.services.mem0_service import Mem0Service
        
        mem0_service = Mem0Service()
        await mem0_service.initialize()
        
        results = await mem0_service.search_memories(
            query=request.query,
            user_id=request.user_id,
            limit=request.limit
        )
        
        logger.info("Memory search completed",
                   user_id=request.user_id,
                   query=request.query,
                   results_count=len(results))
        
        return {
            "status": "success",
            "query": request.query,
            "user_id": request.user_id,
            "results": results,
            "count": len(results),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to search memories", error=str(e), user_id=request.user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search memories: {str(e)}"
        )


@router.get("/user/{user_id}")
async def get_user_memories(
    user_id: str,
    limit: int = Query(default=50, ge=1, le=1000)
):
    """
    Retrieve all memories for a specific user
    
    Multi-user isolation ensures users can only see their own memories
    
    Example:
    ```python
    user_a_memories = memory.get_all(user_id="user_a")
    user_b_memories = memory.get_all(user_id="user_b")
    # Memories are completely isolated
    ```
    """
    try:
        from app.services.mem0_service import Mem0Service
        
        mem0_service = Mem0Service()
        await mem0_service.initialize()
        
        memories = await mem0_service.get_user_memories(
            user_id=user_id,
            limit=limit
        )
        
        logger.info("Retrieved user memories",
                   user_id=user_id,
                   count=len(memories))
        
        return {
            "status": "success",
            "user_id": user_id,
            "memories": memories,
            "count": len(memories),
            "limit": limit,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get user memories", error=str(e), user_id=user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user memories: {str(e)}"
        )


@router.delete("/{memory_id}")
async def delete_memory(
    memory_id: str,
    request: MemoryDeleteRequest
):
    """
    Delete a specific memory with ownership verification
    
    User ID is required to verify ownership before deletion
    """
    try:
        from app.services.mem0_service import Mem0Service
        
        mem0_service = Mem0Service()
        await mem0_service.initialize()
        
        deleted = await mem0_service.delete_memory(
            memory_id=memory_id,
            user_id=request.user_id
        )
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Memory {memory_id} not found or access denied"
            )
        
        logger.info("Memory deleted",
                   memory_id=memory_id,
                   user_id=request.user_id)
        
        return {
            "status": "success",
            "message": "Memory deleted successfully",
            "memory_id": memory_id,
            "user_id": request.user_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete memory", error=str(e), memory_id=memory_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete memory: {str(e)}"
        )


@router.get("/stats")
async def get_memory_stats(
    user_id: Optional[str] = Query(None, description="User ID for user-specific stats")
):
    """
    Get usage and performance statistics
    
    If user_id is provided, returns stats for that user
    Otherwise returns system-wide statistics
    """
    try:
        from app.services.mem0_service import Mem0Service
        from app.core.database import AsyncSessionLocal
        from sqlalchemy import text
        
        stats = {
            "service": "I_MEMORY",
            "timestamp": datetime.now().isoformat()
        }
        
        # Get user-specific stats if user_id provided
        if user_id:
            mem0_service = Mem0Service()
            await mem0_service.initialize()
            
            user_stats = await mem0_service.get_user_stats(user_id)
            stats["user_stats"] = user_stats
            
            logger.info("Retrieved user stats", user_id=user_id)
        else:
            # Get system-wide stats
            try:
                async with AsyncSessionLocal() as db:
                    # Total memories in database
                    result = await db.execute(text("SELECT COUNT(*) FROM memories"))
                    total_memories = result.scalar()
                    
                    # Memory types distribution
                    result = await db.execute(
                        text("SELECT memory_type, COUNT(*) FROM memories GROUP BY memory_type")
                    )
                    memory_types = {row[0]: row[1] for row in result}
                    
                    stats["database_stats"] = {
                        "total_memories": total_memories,
                        "memory_types": memory_types
                    }
            except Exception as e:
                stats["database_stats"] = {"error": str(e)}
            
            # Get Mem0 service stats
            try:
                mem0_service = Mem0Service()
                await mem0_service.initialize()
                
                stats["mem0_stats"] = {
                    "initialized": mem0_service.initialized,
                    "redis_enabled": mem0_service.redis_client is not None
                }
            except Exception as e:
                stats["mem0_stats"] = {"error": str(e)}
            
            logger.info("Retrieved system stats")
        
        return {
            "status": "success",
            "stats": stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get memory stats", error=str(e), user_id=user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get memory stats: {str(e)}"
        )

