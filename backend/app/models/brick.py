"""
BRICK (Business Resource Intelligence & Capability Kit) models
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Float, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Brick(Base):
    """BRICK (Business Resource Intelligence & Capability Kit)"""
    
    __tablename__ = "bricks"
    
    id = Column(Integer, primary_key=True, index=True)
    brick_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100), nullable=False)  # automation, analysis, integration, etc.
    status = Column(String(50), default="development")  # development, testing, production, deprecated
    priority = Column(Integer, default=5)  # 1-10 scale
    complexity = Column(Integer, default=5)  # 1-10 scale
    estimated_development_hours = Column(Integer)
    actual_development_hours = Column(Integer)
    revenue_potential = Column(Float)  # Estimated revenue impact
    dependencies = Column(JSON)  # Array of other brick IDs this depends on
    capabilities = Column(JSON)  # Array of capabilities this brick provides
    integration_points = Column(JSON)  # APIs, databases, services this connects to
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deployed_at = Column(DateTime(timezone=True))
    
    # Relationships
    developments = relationship("BrickDevelopment", back_populates="brick")
    analyses = relationship("BrickAnalysis", back_populates="brick")


class BrickDevelopment(Base):
    """Development progress tracking for BRICKs"""
    
    __tablename__ = "brick_developments"
    
    id = Column(Integer, primary_key=True, index=True)
    brick_id = Column(Integer, ForeignKey("bricks.id"))
    development_type = Column(String(50), nullable=False)  # planning, coding, testing, deployment
    description = Column(Text)
    progress_percentage = Column(Integer, default=0)  # 0-100
    ai_system_used = Column(String(50))  # Which AI system handled this development
    output = Column(JSON)  # Code, configurations, documentation
    time_spent_minutes = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    brick = relationship("Brick", back_populates="developments")


class BrickAnalysis(Base):
    """Strategic analysis of BRICKs"""
    
    __tablename__ = "brick_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    brick_id = Column(Integer, ForeignKey("bricks.id"))
    analysis_type = Column(String(50), nullable=False)  # strategic, technical, financial, market
    ai_system_used = Column(String(50))
    findings = Column(Text)
    recommendations = Column(Text)
    confidence_score = Column(Float)  # 0.0 to 1.0
    impact_assessment = Column(JSON)  # Revenue, efficiency, strategic value
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    brick = relationship("Brick", back_populates="analyses")
