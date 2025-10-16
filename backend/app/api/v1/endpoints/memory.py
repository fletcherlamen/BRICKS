"""
Trinity BRICKS I MEMORY - Memory API Endpoints
Uses ONLY real database data (no mock/hardcoded data)

All data comes from the memories table in the database.
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, status, Query, UploadFile, File
from pydantic import BaseModel, Field
import structlog
from datetime import datetime
import uuid
import io
import PyPDF2
import docx
import markdown
from bs4 import BeautifulSoup

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


# ============================================
# Document Upload & Processing Functions
# ============================================

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        logger.error("Failed to extract PDF text", error=str(e))
        raise HTTPException(status_code=400, detail=f"Failed to read PDF: {str(e)}")


def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(io.BytesIO(file_content))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        logger.error("Failed to extract DOCX text", error=str(e))
        raise HTTPException(status_code=400, detail=f"Failed to read DOCX: {str(e)}")


def extract_text_from_txt(file_content: bytes) -> str:
    """Extract text from TXT file"""
    try:
        return file_content.decode('utf-8').strip()
    except UnicodeDecodeError:
        # Try with different encoding
        try:
            return file_content.decode('latin-1').strip()
        except Exception as e:
            logger.error("Failed to extract TXT text", error=str(e))
            raise HTTPException(status_code=400, detail=f"Failed to read TXT: {str(e)}")


def extract_text_from_md(file_content: bytes) -> str:
    """Extract text from Markdown file"""
    try:
        md_text = file_content.decode('utf-8')
        # Convert markdown to HTML, then extract text
        html = markdown.markdown(md_text)
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text().strip()
    except Exception as e:
        logger.error("Failed to extract MD text", error=str(e))
        raise HTTPException(status_code=400, detail=f"Failed to read MD: {str(e)}")


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Chunk text into smaller pieces for better semantic search
    
    Args:
        text: The text to chunk
        chunk_size: Size of each chunk in characters
        overlap: Overlap between chunks
    
    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to break at sentence boundary
        if end < len(text):
            # Look for sentence ending in the last 100 characters
            sentence_end = text.rfind('.', end - 100, end)
            if sentence_end > start:
                end = sentence_end + 1
        
        chunks.append(text[start:end].strip())
        start = end - overlap
    
    return chunks


@router.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    user_id: str = Query(..., description="User identifier for isolation"),
    category: str = Query(default="document", description="Category for organization")
):
    """
    Upload and process document (PDF, DOCX, TXT, MD) for semantic search
    
    Trinity BRICKS I MEMORY - Document RAG System:
    - Extracts text from documents
    - Chunks text for better search
    - Stores chunks in I MEMORY with embeddings
    - Enables chat with document content
    
    This is what makes I CHAT work like a custom GPT!
    """
    try:
        # Validate file type
        filename = file.filename.lower()
        if not any(filename.endswith(ext) for ext in ['.pdf', '.docx', '.txt', '.md']):
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Supported: PDF, DOCX, TXT, MD"
            )
        
        # Read file content
        file_content = await file.read()
        
        # Extract text based on file type
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_content)
        elif filename.endswith('.docx'):
            text = extract_text_from_docx(file_content)
        elif filename.endswith('.txt'):
            text = extract_text_from_txt(file_content)
        elif filename.endswith('.md'):
            text = extract_text_from_md(file_content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        if not text:
            raise HTTPException(status_code=400, detail="No text content found in file")
        
        # Chunk the text
        chunks = chunk_text(text, chunk_size=1000, overlap=200)
        
        logger.info("Document processed", 
                   filename=file.filename,
                   text_length=len(text),
                   chunks=len(chunks))
        
        # Store each chunk in I MEMORY
        from app.services.mem0_service import Mem0Service
        mem0_service = Mem0Service()
        await mem0_service.initialize()
        
        stored_chunks = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"doc_{uuid.uuid4().hex[:12]}_chunk{i}"
            
            # Create content for this chunk
            chunk_content = {
                "type": "document_chunk",
                "filename": file.filename,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "text": chunk,
                "category": category
            }
            
            try:
                # Store in Mem0 for semantic search
                mem0_result = await mem0_service.add(
                    content=chunk_content,
                    user_id=user_id,
                    metadata={
                        "category": category,
                        "document": file.filename,
                        "chunk_index": i
                    }
                )
                
                memory_id = mem0_result.get("memory_id") if not mem0_result.get("mock") else chunk_id
                if not memory_id:
                    memory_id = chunk_id
                
                # Store in database
                async with AsyncSessionLocal() as db:
                    memory = Memory(
                        memory_id=memory_id,
                        user_id=user_id,
                        content=chunk_content,
                        memory_metadata={
                            "category": category,
                            "document": file.filename,
                            "chunk_index": i,
                            "total_chunks": len(chunks)
                        },
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    db.add(memory)
                    await db.commit()
                
                stored_chunks.append({
                    "chunk_id": memory_id,
                    "chunk_index": i,
                    "length": len(chunk)
                })
                
            except Exception as e:
                logger.warning(f"Failed to store chunk {i}", error=str(e))
                continue
        
        logger.info("Document uploaded and chunked",
                   user_id=user_id,
                   filename=file.filename,
                   chunks_stored=len(stored_chunks))
        
        return {
            "status": "success",
            "data": {
                "filename": file.filename,
                "text_length": len(text),
                "total_chunks": len(chunks),
                "chunks_stored": len(stored_chunks),
                "chunks": stored_chunks
            },
            "message": f"Document uploaded and split into {len(chunks)} searchable chunks. You can now chat about this document!",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to upload document", error=str(e), user_id=user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload document: {str(e)}"
        )
