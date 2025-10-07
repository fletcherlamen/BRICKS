"""
Chat API Endpoints - System Chat Interface
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
import structlog
import time
import uuid
from datetime import datetime
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.orchestration import ChatMessage as ChatMessageModel, ChatSession as ChatSessionModel

logger = structlog.get_logger(__name__)
router = APIRouter()


class ChatMessage(BaseModel):
    """Request model for chat messages"""
    message: str
    session_id: Optional[str] = None
    context: Dict[str, Any] = {}


class ChatResponse(BaseModel):
    """Response model for chat messages"""
    response: str
    session_id: str
    timestamp: str
    metadata: Dict[str, Any] = {}


class ChatSession(BaseModel):
    """Chat session information"""
    session_id: str
    created_at: str
    message_count: int
    last_activity: str


# In-memory chat storage (combined with VPS database persistence)
chat_sessions = {}
chat_messages = {}


async def _save_message_to_db(message_id: str, session_id: str, message_type: str, content: str, metadata: Dict[str, Any] = None):
    """Save chat message to VPS database"""
    async with AsyncSessionLocal() as db:
        try:
            db_message = ChatMessageModel(
                message_id=message_id,
                session_id=session_id,
                message_type=message_type,
                content=content,
                message_metadata=metadata or {}
            )
            
            db.add(db_message)
            await db.commit()
            logger.info("Chat message saved to VPS database", message_id=message_id, session_id=session_id)
            
        except Exception as e:
            logger.error("Failed to save chat message to VPS database", error=str(e))
            await db.rollback()


async def _update_session_in_db(session_id: str):
    """Update or create chat session in VPS database"""
    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(
                select(ChatSessionModel).where(ChatSessionModel.session_id == session_id)
            )
            db_session = result.scalar_one_or_none()
            
            if db_session:
                db_session.message_count += 1
                db_session.last_activity = datetime.now()
            else:
                db_session = ChatSessionModel(
                    session_id=session_id,
                    message_count=1
                )
                db.add(db_session)
            
            await db.commit()
            logger.info("Chat session updated in VPS database", session_id=session_id)
            
        except Exception as e:
            logger.error("Failed to update chat session in VPS database", error=str(e))
            await db.rollback()


@router.post("/message", response_model=ChatResponse)
async def send_chat_message(message_request: ChatMessage):
    """Process chat message and return orchestrated response"""
    
    try:
        # Generate session ID if not provided
        session_id = message_request.session_id or f"chat_{int(time.time() * 1000)}"
        
        # Initialize session if new
        if session_id not in chat_sessions:
            chat_sessions[session_id] = {
                "session_id": session_id,
                "created_at": datetime.now().isoformat(),
                "message_count": 0,
                "last_activity": datetime.now().isoformat()
            }
            chat_messages[session_id] = []
        
        # Store user message in VPS database
        user_message_id = f"user_{int(time.time() * 1000)}"
        await _save_message_to_db(user_message_id, session_id, "user", message_request.message)
        
        # Store user message in memory
        user_message = {
            "id": user_message_id,
            "type": "user",
            "content": message_request.message,
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id
        }
        chat_messages[session_id].append(user_message)
        
        # Update session in VPS database and memory
        await _update_session_in_db(session_id)
        chat_sessions[session_id]["message_count"] += 1
        chat_sessions[session_id]["last_activity"] = datetime.now().isoformat()
        
        # Process message through orchestration system
        response_content, metadata = await process_chat_message(
            message_request.message,
            session_id,
            message_request.context
        )
        
        # Store system response in VPS database
        system_message_id = f"system_{int(time.time() * 1000)}"
        await _save_message_to_db(system_message_id, session_id, "system", response_content, metadata)
        
        # Store system response in memory
        system_message = {
            "id": system_message_id,
            "type": "system",
            "content": response_content,
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "metadata": metadata
        }
        chat_messages[session_id].append(system_message)
        
        logger.info("Chat message processed", 
                   session_id=session_id,
                   message_length=len(message_request.message),
                   response_length=len(response_content))
        
        return ChatResponse(
            response=response_content,
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            metadata=metadata
        )
        
    except Exception as e:
        logger.error("Failed to process chat message", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def process_chat_message(message: str, session_id: str, context: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
    """Process chat message through orchestration system"""
    
    # Import real orchestrator
    from app.services.real_orchestrator import real_orchestrator
    
    # Analyze the message to determine intent
    message_lower = message.lower()
    
    # Determine response based on message content - Improved logic
    if any(word in message_lower for word in ['brick', 'development', 'build', 'create', 'develop', 'project', 'app', 'application', 'system', 'platform', 'orchestration', 'campaign', 'streaming', 'processing', 'batch', 'real-time', 'api', 'service', 'microservice']):
        # BRICK development request
        try:
            results = await real_orchestrator.execute_brick_development(
                goal=message,
                context=context,
                session_id=session_id
            )
            
            response = f"I'll help you with BRICK development!\n\n"
            response += f"**BRICK Development Plan:**\n"
            response += f"• **BRICK Name:** {results['development_plan']['brick_name']}\n"
            response += f"• **Priority:** {results['development_plan']['priority']}\n"
            response += f"• **Estimated Hours:** {results['development_plan']['estimated_hours']}\n\n"
            response += f"**Key Components:**\n"
            for component in results['development_plan']['components'][:3]:
                response += f"• {component}\n"
            response += f"\n**Next Steps:**\n"
            for step in results['next_steps'][:3]:
                response += f"• {step}\n"
            response += f"\nWould you like me to elaborate on any of these components or help you get started?"
            
            metadata = {
                "orchestration_type": "brick_development",
                "run_id": results.get("run_id"),
                "confidence": results.get("confidence"),
                "execution_time_ms": results.get("execution_time_ms")
            }
            
        except Exception as e:
            logger.error("BRICK development orchestration failed", error=str(e))
            response = f"I understand you want to work on development. Let me help you with that!\n\n"
            response += f"Could you provide more details about what you'd like to develop? "
            response += f"For example, what functionality should it have or what problem should it solve?"
            metadata = {"error": str(e), "fallback": True}
    
    elif any(word in message_lower for word in ['analyze', 'analysis', 'strategy', 'strategic', 'plan', 'planning', 'business', 'market', 'revenue', 'optimize', 'insight', 'recommend', 'decision', 'choice', 'compare', 'evaluate', 'assess']):
        # Strategic analysis request
        try:
            results = await real_orchestrator.execute_strategic_analysis(
                goal=message,
                context=context,
                session_id=session_id
            )
            
            response = f"I'll analyze this strategically for you!\n\n"
            response += f"**Strategic Analysis Results:**\n\n"
            response += f"**Key Insights:**\n"
            for insight in results['analysis']['key_insights'][:3]:
                response += f"• {insight}\n"
            response += f"\n**Recommendations:**\n"
            for rec in results['analysis']['recommendations'][:3]:
                response += f"• {rec}\n"
            response += f"\n**Revenue Potential:**\n"
            for opp, value in list(results['analysis']['revenue_potential'].items())[:3]:
                response += f"• {opp}: ${value:,}\n"
            response += f"\nWould you like me to dive deeper into any of these areas?"
            
            metadata = {
                "orchestration_type": "strategic_analysis",
                "run_id": results.get("run_id"),
                "confidence": results.get("confidence"),
                "execution_time_ms": results.get("execution_time_ms")
            }
            
        except Exception as e:
            logger.error("Strategic analysis orchestration failed", error=str(e))
            response = f"I'd be happy to help with strategic analysis! "
            response += f"Could you provide more context about what you'd like me to analyze? "
            response += f"For example, a business goal, market opportunity, or strategic challenge?"
            metadata = {"error": str(e), "fallback": True}
    
    elif any(word in message_lower for word in ['memory', 'remember', 'store', 'save']):
        # Memory-related request
        response = f"I can help you with memory management! "
        response += f"You can:\n"
        response += f"• Upload files (PDF, .md, .txt) in the Memory page\n"
        response += f"• Store large text content for future reference\n"
        response += f"• Organize information with categories and tags\n"
        response += f"• Search through stored memories\n\n"
        response += f"Would you like me to help you store some information or retrieve something from memory?"
        
        metadata = {
            "orchestration_type": "memory_management",
            "session_id": session_id
        }
    
    elif any(word in message_lower for word in ['help', 'what can you do', 'capabilities']):
        # Help request
        response = f"I'm the I PROACTIVE BRICK Orchestration Intelligence! I can help you with:\n\n"
        response += f"🤖 **AI Orchestration:**\n"
        response += f"• Strategic analysis and planning\n"
        response += f"• BRICK development and architecture\n"
        response += f"• Revenue optimization strategies\n"
        response += f"• Gap analysis and recommendations\n\n"
        response += f"💾 **Memory Management:**\n"
        response += f"• Store and organize project documents\n"
        response += f"• Process large text content and files\n"
        response += f"• Maintain context across sessions\n\n"
        response += f"🔧 **System Integration:**\n"
        response += f"• Coordinate multiple AI systems\n"
        response += f"• Track development progress\n"
        response += f"• Generate actionable insights\n\n"
        response += f"What would you like to work on today?"
        
        metadata = {
            "orchestration_type": "help",
            "session_id": session_id
        }
    
    else:
        # General conversation - Try to route through orchestration anyway
        try:
            # For any other message, try strategic analysis first as it's most general
            results = await real_orchestrator.execute_strategic_analysis(
                goal=message,
                context=context,
                session_id=session_id
            )
            
            response = f"I understand you're asking about: \"{message}\"\n\n"
            response += f"Let me provide some strategic insights on this:\n\n"
            response += f"**Key Insights:**\n"
            for insight in results['analysis']['key_insights'][:2]:
                response += f"• {insight}\n"
            response += f"\n**Recommendations:**\n"
            for rec in results['analysis']['recommendations'][:2]:
                response += f"• {rec}\n"
            response += f"\nWould you like me to dive deeper into this topic or help you with something specific?"
            
            metadata = {
                "orchestration_type": "strategic_analysis",
                "run_id": results.get("run_id"),
                "confidence": results.get("confidence"),
                "execution_time_ms": results.get("execution_time_ms"),
                "auto_routed": True
            }
            
        except Exception as e:
            logger.error("Auto-routing orchestration failed", error=str(e))
            # Fallback to generic response
            response = f"I understand you're asking about: \"{message}\"\n\n"
            response += f"Let me help you with that! I can assist with:\n"
            response += f"• Strategic analysis and planning\n"
            response += f"• BRICK development and architecture\n"
            response += f"• Memory management and document processing\n"
            response += f"• Revenue optimization strategies\n\n"
            response += f"Could you provide more specific details about what you'd like me to help you with?"
            
            metadata = {
                "orchestration_type": "general_conversation",
                "session_id": session_id,
                "message_intent": "clarification_needed",
                "auto_routing_failed": str(e)
            }
    
    return response, metadata


@router.get("/sessions")
async def get_chat_sessions():
    """Get list of chat sessions"""
    
    try:
        sessions = list(chat_sessions.values())
        sessions.sort(key=lambda x: x['last_activity'], reverse=True)
        
        return {
            "sessions": sessions,
            "total_sessions": len(sessions),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get chat sessions", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/sessions/{session_id}/messages")
async def get_session_messages(session_id: str):
    """Get messages for a specific session"""
    
    try:
        if session_id not in chat_messages:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session {session_id} not found"
            )
        
        messages = chat_messages[session_id]
        
        return {
            "session_id": session_id,
            "messages": messages,
            "message_count": len(messages),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get session messages", error=str(e), session_id=session_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/sessions/{session_id}")
async def clear_chat_session(session_id: str):
    """Clear a chat session"""
    
    try:
        if session_id in chat_sessions:
            del chat_sessions[session_id]
        if session_id in chat_messages:
            del chat_messages[session_id]
        
        logger.info("Chat session cleared", session_id=session_id)
        
        return {
            "session_id": session_id,
            "status": "cleared",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to clear chat session", error=str(e), session_id=session_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
