"""
Orchestration models for tracking AI system interactions
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime
from app.core.database import Base


class OrchestrationSession(Base):
    """Orchestration session tracking"""
    
    __tablename__ = "orchestration_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(Integer, nullable=True)  # Removed foreign key constraint
    status = Column(String(50), default="active")  # active, completed, failed, cancelled
    goal = Column(Text)  # High-level goal description
    context = Column(JSON)  # Session context and parameters
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    # user = relationship("User", back_populates="orchestration_sessions")  # Temporarily disabled
    tasks = relationship("OrchestrationTask", back_populates="session")


class OrchestrationTask(Base):
    """Individual tasks within orchestration sessions"""
    
    __tablename__ = "orchestration_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(100), unique=True, index=True, nullable=False)
    session_id = Column(Integer, ForeignKey("orchestration_sessions.id"))
    ai_system = Column(String(50), nullable=False)  # crewai, mem0, devin, copilot, etc.
    task_type = Column(String(50), nullable=False)  # analysis, generation, execution, etc.
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    input_data = Column(JSON)
    output_data = Column(JSON)
    error_message = Column(Text)
    execution_time_ms = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    session = relationship("OrchestrationSession", back_populates="tasks")
    logs = relationship("TaskLog", back_populates="task")


class TaskLog(Base):
    """Detailed logs for orchestration tasks"""
    
    __tablename__ = "task_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("orchestration_tasks.id"))
    log_level = Column(String(20), nullable=False)  # info, warning, error, debug
    message = Column(Text, nullable=False)
    task_metadata = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    task = relationship("OrchestrationTask", back_populates="logs")


class AIInteraction(Base):
    """AI-to-AI interaction logs"""
    
    __tablename__ = "ai_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("orchestration_sessions.id"))
    from_ai_system = Column(String(50), nullable=False)
    to_ai_system = Column(String(50), nullable=False)
    interaction_type = Column(String(50), nullable=False)  # request, response, collaboration
    message = Column(Text, nullable=False)
    task_metadata = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("OrchestrationSession")


class ChatMessage(Base):
    """Chat messages model - stores chat conversation history"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String, unique=True, index=True, nullable=False)
    session_id = Column(String, index=True, nullable=False)
    message_type = Column(String(20), nullable=False)  # user or system
    content = Column(Text, nullable=False)
    message_metadata = Column(JSON)  # renamed from 'metadata' (SQLAlchemy reserved)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class ChatSession(Base):
    """Chat sessions model - stores chat session metadata"""
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    message_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# Pydantic models for API responses
class UBICResponse(BaseModel):
    """Unified Brick Intelligence Communication Response"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.now()
    session_id: Optional[str] = None
    task_id: Optional[str] = None
