"""
Memory models for persistent AI memory and context
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Float, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class Memory(Base):
    """
    Trinity BRICKS I MEMORY - Persistent memory storage with multi-user isolation
    
    Schema aligned with Trinity BRICKS specification
    """
    
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key=True, index=True)
    memory_id = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(String(255), nullable=False, index=True)  # Trinity BRICKS: Multi-user isolation
    content = Column(JSON, nullable=False)  # Trinity BRICKS: Store as JSONB for structured data
    memory_metadata = Column("metadata", JSON)  # Trinity BRICKS: Flexible metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Memory(id={self.id}, user='{self.user_id}', memory_id='{self.memory_id}')>"


class Context(Base):
    """Contextual information for sessions and tasks"""
    
    __tablename__ = "contexts"
    
    id = Column(Integer, primary_key=True, index=True)
    context_id = Column(String(100), unique=True, index=True, nullable=False)
    session_id = Column(String(100), index=True)
    context_type = Column(String(50), nullable=False)  # session, task, user, business
    content = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Context(id={self.id}, type='{self.context_type}', session='{self.session_id}')>"


class KnowledgeGraph(Base):
    """Knowledge graph for relationships between concepts"""
    
    __tablename__ = "knowledge_graph"
    
    id = Column(Integer, primary_key=True, index=True)
    source_entity = Column(String(200), nullable=False, index=True)
    relationship = Column(String(100), nullable=False)
    target_entity = Column(String(200), nullable=False, index=True)
    strength = Column(Float, default=1.0)  # Relationship strength
    memory_metadata = Column("metadata", JSON)  # Map to 'metadata' column in database
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<KnowledgeGraph({self.source_entity} -> {self.relationship} -> {self.target_entity})>"
