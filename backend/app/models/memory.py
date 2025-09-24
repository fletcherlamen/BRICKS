"""
Memory models for persistent AI memory and context
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Float, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class Memory(Base):
    """Persistent memory storage"""
    
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key=True, index=True)
    memory_id = Column(String(100), unique=True, index=True, nullable=False)
    content = Column(Text, nullable=False)
    memory_type = Column(String(50), nullable=False)  # fact, experience, strategy, context
    importance_score = Column(Float, default=0.5)  # 0.0 to 1.0
    tags = Column(JSON)  # Array of tags for categorization
    source_system = Column(String(50))  # Which AI system created this memory
    memory_metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_accessed = Column(DateTime(timezone=True))
    access_count = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<Memory(id={self.id}, type='{self.memory_type}', importance={self.importance_score})>"


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
    memory_metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<KnowledgeGraph({self.source_entity} -> {self.relationship} -> {self.target_entity})>"
