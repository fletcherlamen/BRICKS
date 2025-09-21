"""
Database models for analytics and performance tracking.
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class PerformanceMetrics(Base):
    """Track performance metrics for AI systems and orchestration."""
    
    __tablename__ = "performance_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    system_name = Column(String(100), nullable=False)  # crewai, mem0, orchestrator
    metric_name = Column(String(100), nullable=False)  # response_time, accuracy, cost
    metric_value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=True)  # seconds, percentage, dollars
    meta_data = Column(JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class RevenueOpportunity(Base):
    """Track identified revenue opportunities and their implementation status."""
    
    __tablename__ = "revenue_opportunities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    opportunity_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    estimated_revenue = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)  # 0.0 to 1.0
    brick_related = Column(String(255), nullable=True)  # Which BRICK this relates to
    status = Column(String(50), nullable=False, default="identified")  # identified, in_progress, implemented
    implementation_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    implemented_at = Column(DateTime(timezone=True), nullable=True)


class SystemHealth(Base):
    """Monitor health and status of integrated AI systems."""
    
    __tablename__ = "system_health"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    system_name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)  # healthy, degraded, down
    response_time = Column(Float, nullable=True)
    error_rate = Column(Float, nullable=True)
    last_successful_call = Column(DateTime(timezone=True), nullable=True)
    last_error = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(String(500), nullable=True)
    meta_data = Column(JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
