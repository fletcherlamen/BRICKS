"""
Trinity BRICKS I MEMORY - Memory API Endpoints
Uses ONLY real database data (no mock/hardcoded data)

All data comes from the memories table in the database.
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel, Field
import structlog
from datetime import datetime
import uuid

from app.core.database import AsyncSessionLocal
from app.models.memory import Memory
from sqlalchemy import select, delete as sql_delete, func

logger = structlog.get_logger(__name__)
router = APIRouter()


# ============================================
# Trinity BRICKS I MEMORY - Request Models
# ============================================

class MemoryAddRequest(BaseModel):
    """Add memory request - Trinity BRICKS specification"""
    user_id: str = Field(..., description="User identifier for isolation")
    content: Dict[str, Any] = Field(..., description="Memory content as JSON")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional metadata")


# ============================================
# Trinity BRICKS I MEMORY - Endpoints
# ============================================

@router.post("/add")
async def add_memory(request: MemoryAddRequest):
    """
    Store new memory - ONLY uses database (no mock data)
    
    Trinity BRICKS I MEMORY Specification Example:
        await memory.add(
            content={
                "developer": "Fletcher",
                "brick": "I PROACTIVE",
                "status": "verified_working",
                "payment_recommended": 280
            },
            user_id="james@fullpotential.com",
            metadata={"category": "developer_assessment"}
        )
    """
    try:
        # Generate memory ID
        memory_id = f"mem_{uuid.uuid4().hex[:16]}"
        
        # Store in database
        async with AsyncSessionLocal() as db:
            memory = Memory(
                memory_id=memory_id,
                user_id=request.user_id,
                content=request.content,
                memory_metadata=request.metadata or {},
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(memory)
            await db.commit()
            await db.refresh(memory)
        
        logger.info("Memory added to database",
                   user_id=request.user_id,
                   memory_id=memory_id)
        
        return {
            "status": "success",
            "data": {
                "memory_id": memory_id,
                "user_id": request.user_id,
                "content": request.content,
                "metadata": request.metadata,
                "timestamp": datetime.now().isoformat(),
                "source": "database"
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to add memory", error=str(e), user_id=request.user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add memory: {str(e)}"
        )


@router.get("/search")
async def search_memories(
    user_id: str = Query(..., description="User identifier for isolation"),
    query: str = Query(..., description="Search query"),
    limit: int = Query(default=10, ge=1, le=100, description="Maximum results")
):
    """
    Search memories - Uses database with simple text matching
    
    Trinity BRICKS I MEMORY Specification:
    Semantic search powered by database queries
    """
    try:
        # Search in database
        async with AsyncSessionLocal() as db:
            # Simple text search in content
            from sqlalchemy import cast, String
            result = await db.execute(
                select(Memory)
                .where(Memory.user_id == user_id)
                .where(cast(Memory.content, String).ilike(f'%{query}%'))
                .order_by(Memory.created_at.desc())
                .limit(limit)
            )
            db_memories = result.scalars().all()
        
        # Format results
        results = []
        for db_mem in db_memories:
            results.append({
                "memory_id": db_mem.memory_id,
                "content": db_mem.content,
                "relevance_score": 0.9,  # Placeholder for now
                "user_id": db_mem.user_id,
                "metadata": db_mem.memory_metadata or {},
                "timestamp": db_mem.created_at.isoformat() if db_mem.created_at else None,
                "source": "database"
            })
        
        logger.info("Memory search completed from database",
                   user_id=user_id,
                   query=query,
                   results_count=len(results))
        
        return {
            "status": "success",
            "query": query,
            "user_id": user_id,
            "results": results,
            "count": len(results),
            "data_source": "database",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to search memories", error=str(e), user_id=user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search memories: {str(e)}"
        )


@router.get("/get-all")
async def get_all_memories(
    user_id: str = Query(..., description="User identifier for isolation"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum memories")
):
    """
    Get all memories for user - ONLY from database (no mock data)
    
    Trinity BRICKS I MEMORY Specification:
    Multi-user isolation ensures users only see their own memories.
    """
    try:
        # Get from database ONLY
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Memory)
                .where(Memory.user_id == user_id)
                .order_by(Memory.created_at.desc())
                .limit(limit)
            )
            db_memories = result.scalars().all()
        
        # Format memories
        memories = []
        for db_mem in db_memories:
            memories.append({
                "memory_id": db_mem.memory_id,
                "user_id": db_mem.user_id,
                "content": db_mem.content,
                "metadata": db_mem.memory_metadata or {},
                "timestamp": db_mem.created_at.isoformat() if db_mem.created_at else None,
                "source": "database"
            })
        
        logger.info("Retrieved all memories from database",
                   user_id=user_id,
                   count=len(memories))
        
        return {
            "status": "success",
            "user_id": user_id,
            "memories": memories,
            "count": len(memories),
            "limit": limit,
            "data_source": "database",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get all memories", error=str(e), user_id=user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get all memories: {str(e)}"
        )


@router.delete("/delete")
async def delete_memory(
    memory_id: str = Query(..., description="Memory identifier"),
    user_id: str = Query(..., description="User identifier for ownership verification")
):
    """
    Delete memory - from database only
    
    Trinity BRICKS I MEMORY Specification:
    User ID required for ownership verification
    """
    try:
        # Delete from database
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                sql_delete(Memory)
                .where(Memory.memory_id == memory_id)
                .where(Memory.user_id == user_id)
            )
            await db.commit()
            deleted = result.rowcount > 0
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Memory {memory_id} not found or access denied"
            )
        
        logger.info("Memory deleted from database",
                   memory_id=memory_id,
                   user_id=user_id)
        
        return {
            "status": "success",
            "message": "Memory deleted successfully",
            "memory_id": memory_id,
            "user_id": user_id,
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
    Memory statistics - from database only
    
    Trinity BRICKS I MEMORY Specification
    """
    try:
        stats = {
            "service": "I_MEMORY",
            "data_source": "database",
            "timestamp": datetime.now().isoformat()
        }
        
        if user_id:
            # User-specific stats from database
            async with AsyncSessionLocal() as db:
                result = await db.execute(
                    select(func.count(Memory.id))
                    .where(Memory.user_id == user_id)
                )
                user_count = result.scalar()
                
                # Get oldest and newest
                result = await db.execute(
                    select(Memory.created_at)
                    .where(Memory.user_id == user_id)
                    .order_by(Memory.created_at.asc())
                    .limit(1)
                )
                oldest = result.scalar()
                
                result = await db.execute(
                    select(Memory.created_at)
                    .where(Memory.user_id == user_id)
                    .order_by(Memory.created_at.desc())
                    .limit(1)
                )
                newest = result.scalar()
            
            stats["user_stats"] = {
                "user_id": user_id,
                "total_memories": user_count,
                "oldest_memory": oldest.isoformat() if oldest else None,
                "newest_memory": newest.isoformat() if newest else None
            }
            
            logger.info("Retrieved user stats from database", user_id=user_id)
        else:
            # System-wide stats from database
            async with AsyncSessionLocal() as db:
                # Total memories
                result = await db.execute(select(func.count(Memory.id)))
                total_memories = result.scalar()
                
                # Unique users
                result = await db.execute(
                    select(func.count(func.distinct(Memory.user_id)))
                )
                unique_users = result.scalar()
                
                # Recent memories (last 24 hours)
                from sqlalchemy import text
                result = await db.execute(
                    text("SELECT COUNT(*) FROM memories WHERE created_at > NOW() - INTERVAL '24 hours'")
                )
                recent_memories = result.scalar()
            
            stats["system_stats"] = {
                "total_memories": total_memories,
                "unique_users": unique_users,
                "recent_memories_24h": recent_memories
            }
            
            logger.info("Retrieved system stats from database")
        
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
