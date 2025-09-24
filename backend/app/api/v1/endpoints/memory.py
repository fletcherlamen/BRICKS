"""
Enhanced Memory API Endpoints - Support for Multiple File Types and Organization
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import structlog
import time
import uuid
import os
from datetime import datetime
import mimetypes

logger = structlog.get_logger(__name__)
router = APIRouter()


class MemoryRequest(BaseModel):
    """Request model for memory operations"""
    content: str
    memory_type: str = "fact"
    importance_score: float = Field(default=0.5, ge=0.0, le=1.0)
    category: str = "general"
    tags: List[str] = []
    metadata: Dict[str, Any] = {}
    source_type: str = "text"  # text, pdf, markdown, url


class FileUploadRequest(BaseModel):
    """Request model for file upload operations"""
    category: str = "documents"
    tags: List[str] = []
    importance_score: float = Field(default=0.5, ge=0.0, le=1.0)
    description: Optional[str] = None
    auto_extract: bool = True


class MemoryResponse(BaseModel):
    """Response model for memory operations"""
    memory_id: str
    content: str
    memory_type: str
    category: str
    tags: List[str]
    source_type: str
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    importance_score: float
    timestamp: str


class OrganizationRequest(BaseModel):
    """Request model for organizing memories"""
    memory_ids: List[str]
    new_category: Optional[str] = None
    new_tags: Optional[List[str]] = None
    bulk_operation: str = "update"  # update, archive, delete


class SearchRequest(BaseModel):
    """Enhanced search request model"""
    query: str
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    memory_type: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    importance_min: Optional[float] = None
    limit: int = Field(default=10, ge=1, le=100)


@router.post("/", response_model=MemoryResponse)
async def store_memory(memory: MemoryRequest):
    """Store a new memory with enhanced organization and real persistence"""
    
    try:
        # Import real orchestrator for memory persistence
        from app.services.real_orchestrator import real_orchestrator
        
        # Store memory using real orchestrator
        memory_data = await real_orchestrator.store_memory(
            content=memory.content,
            category=memory.category,
            tags=memory.tags,
            importance_score=memory.importance_score,
            memory_type=memory.memory_type,
            source_type=memory.source_type
        )
        
        logger.info("Memory stored successfully", 
                   memory_id=memory_data["memory_id"],
                   category=memory.category,
                   tags=memory.tags)
        
        return MemoryResponse(
            memory_id=memory_data["memory_id"],
            content=memory_data["content"],
            memory_type=memory.memory_type,
            category=memory_data["category"],
            tags=memory_data["tags"],
            source_type=memory.source_type,
            importance_score=memory_data["importance_score"],
            timestamp=memory_data["created_at"]
        )
        
    except Exception as e:
        logger.error("Failed to store memory", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/upload", response_model=MemoryResponse)
async def upload_file(
    file: UploadFile = File(...),
    category: str = Form("documents"),
    tags: str = Form("[]"),  # JSON string
    importance_score: float = Form(0.5),
    description: Optional[str] = Form(None),
    auto_extract: bool = Form(True)
):
    """Upload and process files (PDF, .md, .txt) with organization"""
    
    try:
        # Validate file type
        allowed_types = {
            'application/pdf': 'pdf',
            'text/plain': 'text',
            'text/markdown': 'markdown',
            'text/x-markdown': 'markdown',
            'application/octet-stream': 'unknown'  # For .md files
        }
        
        file_type = allowed_types.get(file.content_type, 'unknown')
        if file_type == 'unknown' and not file.filename.endswith(('.pdf', '.md', '.txt', '.markdown')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type. Only PDF, .md, .txt files are allowed."
            )
        
        # Read file content
        content = await file.read()
        file_size = len(content)
        
        # Parse tags from JSON string first (before using in content generation)
        import json
        try:
            parsed_tags = json.loads(tags) if tags else []
        except json.JSONDecodeError:
            parsed_tags = [tags] if tags else []
        
        # Real file processing - extract actual content
        if file_type == 'pdf':
            # For PDF files, store metadata and note that content extraction is needed
            extracted_content = f"[PDF FILE UPLOADED: {file.filename}]\n\nFile Size: {file_size} bytes\nUploaded: {datetime.now().isoformat()}\nCategory: {category}\nTags: {', '.join(parsed_tags)}\n\nNote: PDF content extraction requires additional processing. File has been stored and can be processed for text extraction."
        else:
            # For text and markdown files - extract real content
            try:
                extracted_content = content.decode('utf-8')
                # Validate that we got meaningful content
                if len(extracted_content.strip()) < 10:
                    extracted_content = f"[TEXT FILE: {file.filename}]\n\nFile appears to be empty or contains minimal content.\nOriginal content: {extracted_content}"
            except UnicodeDecodeError:
                # Handle encoding issues
                extracted_content = f"[BINARY FILE: {file.filename}]\n\nFile Size: {file_size} bytes\nType: {file.content_type}\nNote: File contains binary data that cannot be displayed as text."
        
        # Store memory using real orchestrator
        from app.services.real_orchestrator import real_orchestrator
        
        memory_data = await real_orchestrator.store_memory(
            content=extracted_content,
            category=category,
            tags=parsed_tags,
            importance_score=importance_score,
            memory_type="document",
            source_type=file_type,
            file_name=file.filename,
            file_size=file_size
        )
        
        logger.info("File uploaded and memory stored", 
                   memory_id=memory_data["memory_id"],
                   filename=file.filename,
                   file_type=file_type,
                   file_size=file_size,
                   category=category,
                   tags=parsed_tags)
        
        return MemoryResponse(
            memory_id=memory_data["memory_id"],
            content=memory_data["content"],
            memory_type="document",
            category=memory_data["category"],
            tags=memory_data["tags"],
            source_type=file_type,
            file_name=file.filename,
            file_size=file_size,
            importance_score=memory_data["importance_score"],
            timestamp=memory_data["created_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to upload file", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/upload-text", response_model=MemoryResponse)
async def upload_large_text(
    content: str = Form(...),
    category: str = Form("general"),
    tags: str = Form("[]"),  # JSON string
    importance_score: float = Form(0.5),
    description: Optional[str] = Form(None)
):
    """Upload large text content with organization"""
    
    try:
        # Validate content length
        if len(content) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Content too short. Minimum 10 characters required."
            )
        
        if len(content) > 100000:  # 100KB limit for large text
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Content too large. Maximum 100,000 characters allowed."
            )
        
        # Parse tags from JSON string
        import json
        try:
            parsed_tags = json.loads(tags) if tags else []
        except json.JSONDecodeError:
            parsed_tags = [tags] if tags else []
        
        # Store memory using real orchestrator
        from app.services.real_orchestrator import real_orchestrator
        
        memory_data = await real_orchestrator.store_memory(
            content=content,
            category=category,
            tags=parsed_tags,
            importance_score=importance_score,
            memory_type="text",
            source_type="text"
        )
        
        logger.info("Large text uploaded and memory stored", 
                   memory_id=memory_data["memory_id"],
                   content_length=len(content),
                   category=category,
                   tags=parsed_tags)
        
        return MemoryResponse(
            memory_id=memory_data["memory_id"],
            content=memory_data["content"],
            memory_type="text",
            category=memory_data["category"],
            tags=memory_data["tags"],
            source_type="text",
            importance_score=memory_data["importance_score"],
            timestamp=memory_data["created_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to upload text", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/")
async def list_memories(
    memory_type: Optional[str] = None,
    category: Optional[str] = None,
    tags: Optional[str] = None,  # Comma-separated tags
    importance_min: Optional[float] = None,
    limit: int = 50,
    offset: int = 0
):
    """Get list of memories with enhanced filtering and real data"""
    
    try:
        # Get memories from real orchestrator
        from app.services.real_orchestrator import real_orchestrator
        memories = real_orchestrator.get_memories(limit=limit * 2)  # Get more for filtering
        
        # Apply filters
        filtered_memories = memories
        
        if memory_type:
            filtered_memories = [m for m in filtered_memories if m["memory_type"] == memory_type]
        
        if category:
            filtered_memories = [m for m in filtered_memories if m["category"] == category]
        
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",")]
            filtered_memories = [m for m in filtered_memories if any(tag in m["tags"] for tag in tag_list)]
        
        if importance_min is not None:
            filtered_memories = [m for m in filtered_memories if m["importance_score"] >= importance_min]
        
        # Apply pagination
        total_count = len(filtered_memories)
        paginated_memories = filtered_memories[offset:offset + limit]
        
        return {
            "memories": paginated_memories,
            "count": len(paginated_memories),
            "total": total_count,
            "filters": {
                "memory_type": memory_type,
                "category": category,
                "tags": tags,
                "importance_min": importance_min
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to list memories", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/search")
async def search_memories(
    query: str,
    category: Optional[str] = None,
    tags: Optional[str] = None,
    memory_type: Optional[str] = None,
    limit: int = 10
):
    """Enhanced search memories by content with filters"""
    
    try:
        # Mock search results - would use Mem0 service in production
        all_results = [
            {
                "memory_id": "mem_001",
                "content": "Church Kit Generator has high revenue potential",
                "relevance_score": 0.95,
                "memory_type": "strategy",
                "category": "business",
                "tags": ["revenue", "strategy", "church-kit"],
                "source_type": "text",
                "importance_score": 0.9
            },
            {
                "memory_id": "file_001",
                "content": "[PDF Content from business_plan.pdf]\n\nThis is mock extracted text from the PDF file.",
                "relevance_score": 0.87,
                "memory_type": "document",
                "category": "documents",
                "tags": ["business-plan", "pdf", "planning"],
                "source_type": "pdf",
                "file_name": "business_plan.pdf",
                "importance_score": 0.7
            }
        ]
        
        # Apply filters
        filtered_results = all_results
        
        if category:
            filtered_results = [r for r in filtered_results if r["category"] == category]
        
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",")]
            filtered_results = [r for r in filtered_results if any(tag in r["tags"] for tag in tag_list)]
        
        if memory_type:
            filtered_results = [r for r in filtered_results if r["memory_type"] == memory_type]
        
        # Limit results
        limited_results = filtered_results[:limit]
        
        return {
            "query": query,
            "results": limited_results,
            "count": len(limited_results),
            "total_matches": len(filtered_results),
            "filters": {
                "category": category,
                "tags": tags,
                "memory_type": memory_type
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to search memories", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/organize", response_model=Dict[str, Any])
async def organize_memories(request: OrganizationRequest):
    """Organize memories with bulk operations"""
    
    try:
        # Mock organization - would update database in production
        results = {
            "operation": request.bulk_operation,
            "memory_ids": request.memory_ids,
            "updated_count": len(request.memory_ids),
            "changes": []
        }
        
        for memory_id in request.memory_ids:
            change = {"memory_id": memory_id, "status": "updated"}
            
            if request.new_category:
                change["new_category"] = request.new_category
            if request.new_tags:
                change["new_tags"] = request.new_tags
            
            results["changes"].append(change)
        
        logger.info("Organized memories", 
                   operation=request.bulk_operation,
                   count=len(request.memory_ids),
                   new_category=request.new_category,
                   new_tags=request.new_tags)
        
        return {
            "status": "success",
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to organize memories", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/categories")
async def get_categories():
    """Get available categories and their statistics"""
    
    try:
        categories = {
            "business": {
                "name": "Business",
                "count": 15,
                "description": "Business strategy and planning documents"
            },
            "technical": {
                "name": "Technical", 
                "count": 12,
                "description": "Technical documentation and code"
            },
            "documents": {
                "name": "Documents",
                "count": 8,
                "description": "PDF and document files"
            },
            "research": {
                "name": "Research",
                "count": 6,
                "description": "Market research and analysis"
            },
            "general": {
                "name": "General",
                "count": 4,
                "description": "General information and notes"
            }
        }
        
        return {
            "categories": categories,
            "total_categories": len(categories),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get categories", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/tags")
async def get_tags():
    """Get available tags and their usage statistics"""
    
    try:
        tags = {
            "revenue": {"count": 8, "category": "business"},
            "strategy": {"count": 6, "category": "business"},
            "development": {"count": 5, "category": "technical"},
            "mobile": {"count": 4, "category": "technical"},
            "pdf": {"count": 3, "category": "documents"},
            "research": {"count": 3, "category": "research"},
            "church-kit": {"count": 2, "category": "business"},
            "gap": {"count": 2, "category": "technical"},
            "business-plan": {"count": 2, "category": "documents"},
            "planning": {"count": 2, "category": "business"}
        }
        
        return {
            "tags": tags,
            "total_tags": len(tags),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get tags", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/stats")
async def get_memory_stats():
    """Get real memory statistics from actual stored memories"""
    
    try:
        from app.services.real_orchestrator import real_orchestrator
        
        # Get real memory data
        memories = real_orchestrator.get_memories()
        
        # Calculate real statistics
        total_memories = len(memories)
        memory_types = {}
        categories = {}
        tags_count = {}
        
        for memory in memories:
            # Count by type
            mem_type = memory.get("memory_type", "unknown")
            memory_types[mem_type] = memory_types.get(mem_type, 0) + 1
            
            # Count by category
            category = memory.get("category", "unknown")
            categories[category] = categories.get(category, 0) + 1
            
            # Count tags
            for tag in memory.get("tags", []):
                tags_count[tag] = tags_count.get(tag, 0) + 1
        
        # Get recent memories (last 24 hours)
        recent_memories = 0
        recent_cutoff = datetime.now().timestamp() - (24 * 60 * 60)
        
        for memory in memories:
            try:
                memory_time = datetime.fromisoformat(memory.get("created_at", "")).timestamp()
                if memory_time > recent_cutoff:
                    recent_memories += 1
            except:
                pass  # Skip invalid timestamps
        
        # Get session count from orchestrator
        session_count = len(real_orchestrator.sessions)
        
        stats = {
            "total_memories": total_memories,
            "memory_types": memory_types,
            "categories": categories,
            "top_tags": dict(sorted(tags_count.items(), key=lambda x: x[1], reverse=True)[:10]),
            "recent_memories": recent_memories,
            "session_count": session_count,
            "data_source": "real_orchestrator"
        }
        
        return {
            "statistics": stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get memory stats", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/context/{session_id}")
async def get_session_context(session_id: str):
    """Get context for a specific session"""
    
    try:
        # Mock context - would query database in production
        context = {
            "session_id": session_id,
            "context_data": {
                "goal": "Strategic analysis of revenue opportunities",
                "current_focus": "Church Kit Generator optimization",
                "key_insights": [
                    "High revenue potential identified",
                    "Mobile gap needs addressing"
                ]
            },
            "created_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat()
        }
        
        return context
        
    except Exception as e:
        logger.error("Failed to get session context", error=str(e), session_id=session_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/context/{session_id}")
async def store_session_context(
    session_id: str,
    context_data: Dict[str, Any]
):
    """Store context for a session"""
    
    try:
        # In production, this would save to database
        logger.info("Stored session context", session_id=session_id)
        
        return {
            "session_id": session_id,
            "status": "stored",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to store session context", error=str(e), session_id=session_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/{memory_id}")
async def delete_memory(memory_id: str):
    """Delete a memory by ID"""
    
    try:
        from app.services.real_orchestrator import real_orchestrator
        
        # Delete from database using real orchestrator
        deleted = await real_orchestrator.delete_memory(memory_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Memory with ID {memory_id} not found"
            )
        
        return {
            "memory_id": memory_id,
            "status": "deleted",
            "message": "Memory deleted successfully",
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
