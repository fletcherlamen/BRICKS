"""
Database models for Strategic Intelligence Layer
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class BRICKEcosystem(Base):
    """BRICKS ecosystem model - stores BRICK definitions and relationships"""
    __tablename__ = "brick_ecosystem"
    
    id = Column(Integer, primary_key=True, index=True)
    brick_id = Column(String, unique=True, index=True, nullable=False)
    brick_name = Column(String, nullable=False)
    brick_type = Column(String, nullable=False)  # existing, potential
    status = Column(String, nullable=False)  # production, development, concept, mvp
    revenue_stream = Column(String)
    monthly_revenue = Column(Float, default=0.0)
    user_base = Column(Integer, default=0)
    technology_stack = Column(JSON)
    integration_points = Column(JSON)
    expansion_potential = Column(String)
    strategic_value = Column(String)
    revenue_potential = Column(String)
    dependencies = Column(JSON)
    value_proposition = Column(Text)
    target_market = Column(String)
    estimated_dev_time = Column(String)
    brick_metadata = Column(JSON)  # Renamed from metadata to avoid SQLAlchemy reserved name
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class RevenueOpportunity(Base):
    """Revenue opportunities model - stores identified revenue opportunities"""
    __tablename__ = "revenue_opportunities"
    
    id = Column(Integer, primary_key=True, index=True)
    opportunity_id = Column(String, unique=True, index=True, nullable=False)
    opportunity_type = Column(String, nullable=False)  # cross_selling, upselling, new_brick, etc.
    name = Column(String, nullable=False)
    description = Column(Text)
    potential_revenue = Column(Float, nullable=False)
    probability = Column(Float, default=0.5)
    effort_level = Column(String)
    time_to_revenue = Column(String)
    action_items = Column(JSON)
    status = Column(String, default="identified")  # identified, in_progress, completed, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class StrategicGap(Base):
    """Strategic gaps model - stores identified strategic gaps"""
    __tablename__ = "strategic_gaps"
    
    id = Column(Integer, primary_key=True, index=True)
    gap_id = Column(String, unique=True, index=True, nullable=False)
    gap_category = Column(String, nullable=False)  # capability, market, revenue, technology, competitive
    gap_name = Column(String, nullable=False)
    description = Column(Text)
    importance = Column(String)
    priority = Column(String)
    severity = Column(String)
    impact = Column(String)
    coverage_level = Column(Float)
    missing_capabilities = Column(JSON)
    market_segment = Column(String)
    current_penetration = Column(Float)
    market_size = Column(Integer)
    revenue_potential = Column(Float)
    competition_level = Column(String)
    examples = Column(JSON)
    mitigation_strategy = Column(Text)
    status = Column(String, default="open")  # open, in_progress, resolved, accepted
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class BRICKPriority(Base):
    """BRICK priority model - stores BRICK priority scores and rankings"""
    __tablename__ = "brick_priorities"
    
    id = Column(Integer, primary_key=True, index=True)
    brick_id = Column(String, index=True, nullable=False)
    brick_name = Column(String, nullable=False)
    priority_score = Column(Float, nullable=False)
    priority_level = Column(String, nullable=False)  # critical, high, medium, low
    component_scores = Column(JSON)  # Individual scoring components
    recommendation = Column(Text)
    estimated_timeline = Column(JSON)
    dependencies_met = Column(Boolean, default=False)
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ConstraintPrediction(Base):
    """Constraint predictions model - stores predicted constraints for BRICKs"""
    __tablename__ = "constraint_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(String, unique=True, index=True, nullable=False)
    brick_id = Column(String, index=True, nullable=False)
    brick_name = Column(String, nullable=False)
    constraint_type = Column(String, nullable=False)  # resource, technical, business, operational
    constraint_description = Column(Text)
    severity = Column(String)
    impact = Column(String)
    probability = Column(Float)
    mitigation_strategy = Column(Text)
    mitigation_actions = Column(JSON)
    predicted_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime(timezone=True))


class IncomeStream(Base):
    """Income streams model - stores revenue stream data"""
    __tablename__ = "income_streams"
    
    id = Column(Integer, primary_key=True, index=True)
    stream_id = Column(String, unique=True, index=True, nullable=False)
    brick_id = Column(String, index=True, nullable=False)
    stream_type = Column(String, nullable=False)  # subscription, service_fee, transaction_fee, etc.
    current_monthly = Column(Float, nullable=False)
    projected_annual = Column(Float)
    customers = Column(Integer)
    avg_revenue_per_customer = Column(Float)
    churn_rate = Column(Float)
    growth_rate = Column(Float)
    recurring = Column(Boolean, default=False)
    predictability = Column(String)
    margin = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
