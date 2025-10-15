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
    Store new memory with REAL semantic search via Mem0.ai
    
    Trinity BRICKS I MEMORY Specification:
    - Stores in database for persistence
    - Stores in Mem0.ai for semantic search
    """
    try:
        from app.services.mem0_service import Mem0Service
        import json
        
        # Generate memory ID
        memory_id = f"mem_{uuid.uuid4().hex[:16]}"
        
        # Store in Mem0.ai for semantic search (with real API)
        mem0_service = Mem0Service()
        await mem0_service.initialize()
        
        try:
            # Store in Mem0 with user isolation
            mem0_result = await mem0_service.add(
                content=request.content,
                user_id=request.user_id,
                metadata=request.metadata
            )
            # Use Mem0's memory ID if available and not None
            if not mem0_result.get("mock") and mem0_result.get("memory_id"):
                memory_id = mem0_result.get("memory_id")
            
            logger.info("Memory stored in Mem0.ai", 
                       user_id=request.user_id,
                       mem0_initialized=mem0_service.initialized)
        except Exception as e:
            logger.warning("Mem0 storage failed, continuing with database only", error=str(e))
        
        # Store in database for persistence
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
        
        logger.info("Memory added to database with semantic search",
                   user_id=request.user_id,
                   memory_id=memory_id,
                   mem0_enabled=mem0_service.initialized)
        
        return {
            "status": "success",
            "data": {
                "memory_id": memory_id,
                "user_id": request.user_id,
                "content": request.content,
                "metadata": request.metadata,
                "timestamp": datetime.now().isoformat(),
                "source": "database",
                "semantic_search_enabled": mem0_service.initialized
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
    query: str = Query(..., description="Natural language search query"),
    limit: int = Query(default=10, ge=1, le=100, description="Maximum results")
):
    """
    REAL Semantic Search using Mem0.ai with AI embeddings
    
    Trinity BRICKS I MEMORY Specification:
    - Uses Mem0.ai for semantic understanding
    - Falls back to database text search if Mem0 unavailable
    - Returns relevance-scored results
    
    Example queries:
    - "What's Fletcher's status?"
    - "Show me developer assessments"
    - "Find payment recommendations"
    """
    try:
        from app.services.mem0_service import Mem0Service
        
        mem0_service = Mem0Service()
        await mem0_service.initialize()
        
        results = []
        search_method = "text_matching"
        
        # Try semantic search with Mem0.ai first (REAL AI)
        if mem0_service.initialized:
            try:
                # REAL semantic search with AI embeddings
                mem0_results = await mem0_service.search(
                    query=query,
                    user_id=user_id,
                    limit=limit
                )
                
                # Mem0 returns semantic results with relevance scores
                for mem in mem0_results:
                    if not mem.get("mock"):  # Only use real results
                        results.append({
                            "memory_id": mem.get("memory_id"),
                            "content": mem.get("content"),
                            "relevance_score": mem.get("relevance_score", 0),
                            "user_id": user_id,
                            "metadata": mem.get("metadata", {}),
                            "timestamp": mem.get("timestamp"),
                            "source": "mem0_semantic"
                        })
                
                if results:
                    search_method = "semantic_ai"
                    logger.info("Semantic search completed with Mem0.ai",
                               user_id=user_id,
                               query=query,
                               results_count=len(results))
                
            except Exception as e:
                logger.warning("Mem0 semantic search failed, falling back to database", error=str(e))
        
        # Fallback: Database text search if Mem0 not available or no results
        if not results:
            async with AsyncSessionLocal() as db:
                from sqlalchemy import cast, String
                result = await db.execute(
                    select(Memory)
                    .where(Memory.user_id == user_id)
                    .where(cast(Memory.content, String).ilike(f'%{query}%'))
                    .order_by(Memory.created_at.desc())
                    .limit(limit)
                )
                db_memories = result.scalars().all()
            
            for db_mem in db_memories:
                results.append({
                    "memory_id": db_mem.memory_id,
                    "content": db_mem.content,
                    "relevance_score": 0.8,  # Lower score for text matching
                    "user_id": db_mem.user_id,
                    "metadata": db_mem.memory_metadata or {},
                    "timestamp": db_mem.created_at.isoformat() if db_mem.created_at else None,
                    "source": "database_text"
                })
            
            logger.info("Text search completed from database",
                       user_id=user_id,
                       query=query,
                       results_count=len(results))
        
        return {
            "status": "success",
            "query": query,
            "user_id": user_id,
            "results": results,
            "count": len(results),
            "search_method": search_method,
            "semantic_enabled": mem0_service.initialized,
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
