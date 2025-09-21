"""
Database models for orchestration tracking and AI collaboration logs.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class OrchestrationSession(Base):
    """Track orchestration sessions between AI systems."""
    
    __tablename__ = "orchestration_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="active")  # active, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    tasks = relationship("OrchestrationTask", back_populates="session")
    collaborations = relationship("AICollaboration", back_populates="session")


class OrchestrationTask(Base):
    """Track individual tasks within orchestration sessions."""
    
    __tablename__ = "orchestration_tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("orchestration_sessions.id"))
    task_name = Column(String(255), nullable=False)
    task_type = Column(String(100), nullable=False)  # crewai, mem0, analysis, etc.
    status = Column(String(50), nullable=False, default="pending")  # pending, running, completed, failed
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("OrchestrationSession", back_populates="tasks")


class AICollaboration(Base):
    """Log AI-to-AI collaboration and communication."""
    
    __tablename__ = "ai_collaborations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("orchestration_sessions.id"))
    from_ai = Column(String(100), nullable=False)  # crewai, mem0, orchestrator, etc.
    to_ai = Column(String(100), nullable=False)
    message_type = Column(String(50), nullable=False)  # request, response, notification
    content = Column(Text, nullable=False)
    meta_data = Column(JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("OrchestrationSession", back_populates="collaborations")


class StrategicAnalysis(Base):
    """Store strategic BRICKS analysis and recommendations."""
    
    __tablename__ = "strategic_analyses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_type = Column(String(100), nullable=False)  # bricks_roadmap, revenue_opportunity, gap_detection
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    recommendations = Column(JSON, nullable=True)
    priority_score = Column(Integer, default=0)
    revenue_impact = Column(Integer, nullable=True)  # Estimated revenue impact
    status = Column(String(50), nullable=False, default="draft")  # draft, reviewed, approved, implemented
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
