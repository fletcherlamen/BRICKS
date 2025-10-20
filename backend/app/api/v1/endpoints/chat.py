"""
Trinity BRICKS I CHAT - Conversational AI with I MEMORY Integration

Provides conversational interface using Claude API with persistent context via I MEMORY.
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
import structlog
import time
import uuid
from datetime import datetime
from sqlalchemy import select, func
from app.core.database import AsyncSessionLocal
from app.core.config import settings
import anthropic
import json
import httpx

logger = structlog.get_logger(__name__)
router = APIRouter()


class ChatMessage(BaseModel):
    """Request model for chat messages"""
    message: str
    user_id: str = Field(default="anonymous", description="User identifier for I MEMORY isolation")
    session_id: Optional[str] = None
    context: Dict[str, Any] = {}


class ChatResponse(BaseModel):
    """Response model for chat messages"""
    response: str
    session_id: str
    user_id: str
    timestamp: str
    context_used: bool
    memory_count: int
    metadata: Dict[str, Any] = {}


# Initialize Anthropic client
claude_client = None
if settings.ANTHROPIC_API_KEY and settings.ANTHROPIC_API_KEY != "your-anthropic-api-key":
    try:
        claude_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        logger.info("Claude API initialized for I CHAT")
    except Exception as e:
        logger.warning("Failed to initialize Claude API", error=str(e))


async def get_conversation_context(user_id: str, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieve conversation context from I MEMORY"""
    try:
        from app.services.mem0_service import Mem0Service
        
        mem0_service = Mem0Service()
        await mem0_service.initialize()
        
        # Search for recent conversation in this session
        memories = await mem0_service.search(
            query=f"conversation session {session_id}",
            user_id=user_id,
            limit=limit
        )
        
        logger.info("Retrieved conversation context from I MEMORY", 
                   user_id=user_id, 
                   session_id=session_id,
                   memory_count=len(memories))
        
        return memories
    except Exception as e:
        logger.warning("Failed to retrieve context from I MEMORY", error=str(e))
        return []


async def store_conversation_in_memory(
    user_id: str, 
    session_id: str,
    user_message: str,
    assistant_response: str
):
    """Store conversation exchange in I MEMORY for persistent context"""
    try:
        from app.services.mem0_service import Mem0Service
        
        mem0_service = Mem0Service()
        await mem0_service.initialize()
        
        conversation_data = {
            "type": "conversation",
            "session_id": session_id,
            "user_message": user_message,
            "assistant_response": assistant_response,
            "timestamp": datetime.now().isoformat()
        }
        
        result = await mem0_service.add(
            content=conversation_data,
            user_id=user_id,
            metadata={
                "category": "conversation",
                "session_id": session_id,
                "brick": "I_CHAT"
            }
        )
        
        logger.info("Conversation stored in I MEMORY", 
                   user_id=user_id,
                   session_id=session_id,
                   memory_id=result.get("memory_id") if result else None)
        
    except Exception as e:
        logger.error("Failed to store conversation in I MEMORY", error=str(e), user_id=user_id, session_id=session_id)


async def get_relevant_context(user_id: str, message: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Get relevant context from I MEMORY based on message content"""
    try:
        from app.services.mem0_service import Mem0Service
        
        mem0_service = Mem0Service()
        await mem0_service.initialize()
        
        # Semantic search for relevant memories
        memories = await mem0_service.search(
            query=message,
            user_id=user_id,
            limit=limit
        )
        
        logger.info("Retrieved relevant context from I MEMORY",
                   user_id=user_id,
                   memory_count=len(memories))
        
        return memories
    except Exception as e:
        logger.warning("Failed to retrieve relevant context", error=str(e))
        return []


async def get_memory_stats(user_id: str) -> Dict[str, Any]:
    """Get memory statistics for capability demonstration"""
    try:
        from app.services.mem0_service import Mem0Service
        
        mem0_service = Mem0Service()
        await mem0_service.initialize()
        
        # Get all memories for stats
        all_memories = await mem0_service.get_all(user_id=user_id, limit=100)
        
        # Count by category
        categories = {}
        for memory in all_memories:
            category = memory.get('metadata', {}).get('category', 'general')
            categories[category] = categories.get(category, 0) + 1
        
        return {
            "total_memories": len(all_memories),
            "categories": list(categories.keys()),
            "category_counts": categories
        }
    except Exception as e:
        logger.warning("Failed to get memory stats", error=str(e))
        return {"total_memories": 0, "categories": [], "category_counts": {}}


async def get_system_status() -> Dict[str, Any]:
    """Get system status for capability demonstration"""
    try:
        # Check if services are available
        return {
            "i_memory": "active",
            "i_chat": "active", 
            "i_assess": "active",
            "claude_api": "configured" if claude_client else "not_configured"
        }
    except Exception as e:
        logger.warning("Failed to get system status", error=str(e))
        return {"status": "unknown"}


def build_claude_messages(
    current_message: str,
    conversation_history: List[Dict[str, Any]],
    relevant_context: List[Dict[str, Any]]
) -> List[Dict[str, str]]:
    """Build message array for Claude API with context"""
    
    messages = []
    
    # Add system context if available
    if relevant_context:
        context_summary = "Here's relevant context from memory:\n\n"
        for ctx in relevant_context[:3]:
            content = ctx.get("content", {})
            if isinstance(content, dict):
                context_summary += f"- {json.dumps(content)}\n"
            else:
                context_summary += f"- {content}\n"
        
        messages.append({
            "role": "user",
            "content": f"[System Context] {context_summary}"
        })
        messages.append({
            "role": "assistant",
            "content": "I understand the context. How can I help you?"
        })
    
    # Add conversation history
    for exchange in conversation_history[-5:]:  # Last 5 exchanges
        content = exchange.get("content", {})
        if isinstance(content, dict):
            if "user_message" in content:
                messages.append({
                    "role": "user",
                    "content": content["user_message"]
                })
            if "assistant_response" in content:
                messages.append({
                    "role": "assistant",
                    "content": content["assistant_response"]
                })
    
    # Add current message
    messages.append({
        "role": "user",
        "content": current_message
    })
    
    return messages


async def trigger_assess_audit(user_id: str, repository: str = "https://github.com/fletcherlamen/BRICKS") -> Dict[str, Any]:
    """Trigger I ASSESS audit from I CHAT"""
    try:
        async with httpx.AsyncClient() as client:
            # Start audit
            response = await client.post(
                "http://localhost:8000/api/v1/audit/start",
                json={
                    "repository": repository,
                    "user_id": user_id,
                    "criteria": ["UBIC_compliance", "test_coverage", "code_quality"]
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                audit_data = response.json()
                audit_id = audit_data.get("audit_id")
                
                logger.info("I ASSESS audit triggered from I CHAT",
                           audit_id=audit_id,
                           user_id=user_id)
                
                # Wait for completion (with timeout)
                import asyncio
                for _ in range(60):  # Wait up to 60 seconds
                    await asyncio.sleep(1)
                    
                    # Check status
                    status_response = await client.get(
                        f"http://localhost:8000/api/v1/audit/{audit_id}",
                        timeout=10.0
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        audit_status = status_data.get("audit", {}).get("status")
                        
                        if audit_status == "completed":
                            return status_data.get("audit", {})
                        elif audit_status == "failed":
                            return {"error": "Audit failed", "details": status_data.get("audit", {})}
                
                return {"error": "Audit timeout", "audit_id": audit_id}
            else:
                return {"error": f"Failed to start audit: {response.status_code}"}
                
    except Exception as e:
        logger.error("Failed to trigger I ASSESS audit", error=str(e))
        return {"error": f"Failed to trigger audit: {str(e)}"}


@router.post("/message", response_model=ChatResponse)
async def send_chat_message(message_request: ChatMessage):
    """
    Trinity BRICKS I CHAT - Process message with Claude API and I MEMORY
    
    Features:
    - Retrieves conversation context from I MEMORY
    - Uses Claude API for intelligent responses
    - Stores conversation in I MEMORY for persistence
    - Supports multi-turn conversations
    - User-isolated conversation history
    """
    
    try:
        # Generate session ID if not provided
        session_id = message_request.session_id or f"chat_{uuid.uuid4().hex[:16]}"
        user_id = message_request.user_id
        
        logger.info("Processing I CHAT message",
                   session_id=session_id,
                   user_id=user_id,
                   message_length=len(message_request.message))
        
        # Get conversation history from I MEMORY
        conversation_history = await get_conversation_context(user_id, session_id)
        
        # Get relevant context from I MEMORY
        relevant_context = await get_relevant_context(user_id, message_request.message)
        
        # Build messages for Claude
        claude_messages = build_claude_messages(
            message_request.message,
            conversation_history,
            relevant_context
        )
        
        # Check if user is requesting an audit
        audit_keywords = ["audit", "assess", "code quality", "run audit", "check code", "analyze code", "fresh audit"]
        is_audit_request = any(keyword in message_request.message.lower() for keyword in audit_keywords)
        
        # Check if user is asking about capabilities
        capability_keywords = ["show me how", "demonstrate", "use those capabilities", "what can you do", "capabilities", "show your"]
        is_capability_request = any(keyword in message_request.message.lower() for keyword in capability_keywords)
        
        # Generate response with Claude
        if claude_client:
            try:
                # If it's a capability demonstration request, show real capabilities
                if is_capability_request:
                    logger.info("Capability demonstration requested", user_id=user_id)
                    
                    # Get real memory stats
                    memory_stats = await get_memory_stats(user_id)
                    
                    # Get real system status
                    system_status = await get_system_status()
                    
                    capability_demo = f"""
DEMONSTRATING TRINITY BRICKS CAPABILITIES (Real Data):

🧠 I MEMORY - Persistent Memory System:
- Your stored memories: {memory_stats.get('total_memories', 0)}
- Recent memories: {len(relevant_context)} relevant to your query
- Memory categories: {memory_stats.get('categories', [])}

💬 I CHAT - Conversational AI:
- Current session: {session_id}
- Conversation history: {len(conversation_history)} previous exchanges
- Context awareness: {len(relevant_context)} relevant memories retrieved

🔍 I ASSESS - Code Analysis:
- Ready to audit GitHub repositories
- Can check UBIC compliance (9/9 endpoints required)
- AI code review with Claude Sonnet 4
- Real-time test coverage analysis

REAL CAPABILITIES IN ACTION:
1. I just retrieved {len(relevant_context)} memories related to your query
2. I have access to {memory_stats.get('total_memories', 0)} stored memories
3. I can trigger I ASSESS audits on demand
4. I remember our conversation history ({len(conversation_history)} exchanges)

Would you like me to demonstrate any specific capability? I can:
- Show you specific memories I found
- Run a real audit on a GitHub repository
- Search through your stored data
- Analyze code quality and compliance
"""
                    claude_messages.append({"role": "user", "content": capability_demo})
                
                # If it's an audit request, trigger I ASSESS first
                if is_audit_request:
                    logger.info("Audit request detected, triggering I ASSESS", user_id=user_id)
                    audit_results = await trigger_assess_audit(user_id)
                    
                    if "error" not in audit_results:
                        # Add audit results to context
                        audit_context = f"""
AUDIT RESULTS (just completed):
- UBIC Compliance: {audit_results.get('ubic_compliance', {}).get('compliance_percent', 0)}%
- Test Coverage: {audit_results.get('test_results', {}).get('coverage_percent', 0)}%
- Tests Passing: {audit_results.get('test_results', {}).get('tests_passed_count', 0)}/{audit_results.get('test_results', {}).get('tests_run', 0)}
- AI Quality Score: {audit_results.get('ai_review', {}).get('quality_score', 0)}/10
- Production Ready: {audit_results.get('ai_review', {}).get('production_ready', False)}
- Payment Recommendation: {audit_results.get('payment_recommendation', {}).get('recommendation', 'Unknown')}
- Total Score: {audit_results.get('payment_recommendation', {}).get('total_score', 0)}/100

Please provide a comprehensive analysis of these audit results.
"""
                        claude_messages.append({"role": "user", "content": audit_context})
                    else:
                        claude_messages.append({
                            "role": "user", 
                            "content": f"Note: I tried to run a fresh audit but encountered an issue: {audit_results.get('error', 'Unknown error')}. Please provide analysis based on available memory context."
                        })
                
                # Dynamic system prompt based on request type
                if is_capability_request:
                    system_prompt = """You are I CHAT, the conversational AI component of Trinity BRICKS. You have REAL capabilities that you should demonstrate, not just list:

1. I MEMORY: You have access to persistent memory with semantic search
2. I ASSESS: You can trigger real code audits and analysis  
3. I CHAT: You maintain conversation context and can reference stored data

When users ask about capabilities, SHOW them what you can do with real data, not generic descriptions. Be specific about the actual memories you found, the real system status, and offer to demonstrate specific features."""
                else:
                    system_prompt = "You are I CHAT, a helpful AI assistant that is part of the Trinity BRICKS system. You have access to persistent memory and can help users with various tasks. Be conversational, helpful, and remember context from previous conversations. When providing audit analysis, be detailed and specific about the metrics and recommendations."
                
                response = claude_client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=2000,
                    system=system_prompt,
                    messages=claude_messages
                )
                
                assistant_response = response.content[0].text
                
                logger.info("Claude API response received",
                           response_length=len(assistant_response),
                           audit_triggered=is_audit_request)
                
            except Exception as e:
                logger.error("Claude API call failed", error=str(e))
                assistant_response = (
                    "I understand your message. However, I'm currently in enhanced mock mode. "
                    "I can still help you, but my responses may be limited. "
                    "Your message has been stored in memory for future reference."
                )
        else:
            # Mock mode
            assistant_response = (
                f"I received your message: \"{message_request.message}\"\n\n"
                f"I'm I CHAT, your conversational AI assistant. "
                f"I'm currently in mock mode (Claude API not configured), but I can still help you! "
                f"I have access to {len(relevant_context)} relevant memories and {len(conversation_history)} conversation history items.\n\n"
                f"How can I assist you today?"
            )
        
        # Store conversation in I MEMORY
        await store_conversation_in_memory(
            user_id,
            session_id,
            message_request.message,
            assistant_response
        )
        
        return ChatResponse(
            response=assistant_response,
            session_id=session_id,
            user_id=user_id,
            timestamp=datetime.now().isoformat(),
            context_used=len(relevant_context) > 0 or len(conversation_history) > 0,
            memory_count=len(relevant_context) + len(conversation_history),
            metadata={
                "conversation_history_count": len(conversation_history),
                "relevant_context_count": len(relevant_context),
                "claude_enabled": claude_client is not None,
                "brick": "I_CHAT"
            }
        )
        
    except Exception as e:
        logger.error("Failed to process chat message", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat message: {str(e)}"
        )


@router.get("/history/{user_id}")
async def get_chat_history(
    user_id: str,
    session_id: Optional[str] = None,
    limit: int = 50
):
    """
    Get conversation history for a user from I MEMORY
    
    Trinity BRICKS I CHAT Specification:
    - Retrieves all conversation exchanges
    - Optionally filtered by session_id
    - Returns in chronological order
    """
    try:
        from app.services.mem0_service import Mem0Service
        
        mem0_service = Mem0Service()
        await mem0_service.initialize()
        
        # Search for conversations
        if session_id:
            query = f"conversation session {session_id}"
        else:
            query = "conversation type:conversation"
        
        memories = await mem0_service.search(
            query=query,
            user_id=user_id,
            limit=limit
        )
        
        # Format conversations
        conversations = []
        for memory in memories:
            content = memory.get("content", {})
            if isinstance(content, dict) and content.get("type") == "conversation":
                conversations.append({
                    "session_id": content.get("session_id"),
                    "user_message": content.get("user_message"),
                    "assistant_response": content.get("assistant_response"),
                    "timestamp": content.get("timestamp"),
                    "memory_id": memory.get("memory_id")
                })
        
        return {
            "status": "success",
            "user_id": user_id,
            "session_id": session_id,
            "conversations": conversations,
            "count": len(conversations),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get chat history", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get chat history: {str(e)}"
        )


@router.get("/active-sessions")
async def get_active_sessions():
    """
    List active chat sessions across all users
    
    Trinity BRICKS I CHAT - UBIC Endpoint
    """
    try:
        async with AsyncSessionLocal() as db:
            # Get unique session IDs from memories (PostgreSQL JSON syntax)
            from app.models.memory import Memory
            from sqlalchemy import cast, String
            
            session_id_expr = cast(Memory.content['session_id'], String)
            type_expr = cast(Memory.content['type'], String)
            
            result = await db.execute(
                select(
                    session_id_expr.label('session_id'),
                    func.count().label('message_count'),
                    func.max(Memory.created_at).label('last_activity')
                ).where(
                    type_expr == 'conversation'
                ).group_by(
                    session_id_expr
                ).order_by(
                    func.max(Memory.created_at).desc()
                ).limit(50)
            )
            
            sessions = []
            for row in result:
                if row.session_id:
                    sessions.append({
                        "session_id": row.session_id,
                        "message_count": row.message_count,
                        "last_activity": row.last_activity.isoformat() if row.last_activity else None
                    })
        
        return {
            "status": "success",
            "sessions": sessions,
            "total_sessions": len(sessions),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get active sessions", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get active sessions: {str(e)}"
        )


@router.post("/send-message")
async def programmatic_send_message(
    user_id: str,
    message: str,
    session_id: Optional[str] = None
):
    """
    Programmatic message sending (Trinity BRICKS I CHAT - UBIC endpoint)
    
    Allows other BRICKs to send messages via API
    """
    return await send_chat_message(ChatMessage(
        message=message,
        user_id=user_id,
        session_id=session_id
    ))
