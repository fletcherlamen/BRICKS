"""
Analytics endpoints for monitoring AI collaboration and performance.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Dict, Any
from datetime import datetime, timedelta
import structlog

from app.core.database import get_db
from app.models.analytics import PerformanceMetrics, SystemHealth, RevenueOpportunity
from app.models.orchestration import AICollaboration, OrchestrationSession

logger = structlog.get_logger()
router = APIRouter()


@router.get("/analytics/performance")
async def get_performance_metrics(
    db: AsyncSession = Depends(get_db),
    hours: int = 24
):
    """Get performance metrics for AI systems."""
    try:
        since = datetime.now() - timedelta(hours=hours)
        
        # Get performance metrics
        metrics_query = select(PerformanceMetrics).where(
            PerformanceMetrics.timestamp >= since
        ).order_by(desc(PerformanceMetrics.timestamp))
        
        result = await db.execute(metrics_query)
        metrics = result.scalars().all()
        
        # Group metrics by system and metric name
        grouped_metrics = {}
        for metric in metrics:
            if metric.system_name not in grouped_metrics:
                grouped_metrics[metric.system_name] = {}
            
            if metric.metric_name not in grouped_metrics[metric.system_name]:
                grouped_metrics[metric.system_name][metric.metric_name] = []
            
            grouped_metrics[metric.system_name][metric.metric_name].append({
                "value": metric.metric_value,
                "unit": metric.unit,
                "timestamp": metric.timestamp.isoformat(),
                "metadata": metric.meta_data
            })
        
        return {
            "time_range_hours": hours,
            "metrics": grouped_metrics,
            "summary": {
                "total_metrics": len(metrics),
                "systems_monitored": len(grouped_metrics)
            }
        }
        
    except Exception as e:
        logger.error("Failed to get performance metrics", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/collaboration")
async def get_ai_collaboration_logs(
    db: AsyncSession = Depends(get_db),
    hours: int = 24,
    limit: int = 100
):
    """Get AI-to-AI collaboration logs."""
    try:
        since = datetime.now() - timedelta(hours=hours)
        
        # Get collaboration logs
        collaboration_query = select(AICollaboration).where(
            AICollaboration.timestamp >= since
        ).order_by(desc(AICollaboration.timestamp)).limit(limit)
        
        result = await db.execute(collaboration_query)
        collaborations = result.scalars().all()
        
        # Format collaboration data
        collaboration_logs = []
        for col in collaborations:
            collaboration_logs.append({
                "id": str(col.id),
                "session_id": str(col.session_id),
                "from_ai": col.from_ai,
                "to_ai": col.to_ai,
                "message_type": col.message_type,
                "content": col.content,
                "timestamp": col.timestamp.isoformat(),
                "metadata": col.meta_data
            })
        
        # Get collaboration statistics
        stats_query = select(
            AICollaboration.from_ai,
            AICollaboration.to_ai,
            func.count(AICollaboration.id).label('count')
        ).where(
            AICollaboration.timestamp >= since
        ).group_by(
            AICollaboration.from_ai,
            AICollaboration.to_ai
        )
        
        stats_result = await db.execute(stats_query)
        collaboration_stats = [
            {
                "from_ai": row.from_ai,
                "to_ai": row.to_ai,
                "interaction_count": row.count
            }
            for row in stats_result.fetchall()
        ]
        
        return {
            "time_range_hours": hours,
            "collaboration_logs": collaboration_logs,
            "collaboration_stats": collaboration_stats,
            "summary": {
                "total_interactions": len(collaboration_logs),
                "unique_ai_pairs": len(collaboration_stats)
            }
        }
        
    except Exception as e:
        logger.error("Failed to get collaboration logs", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/revenue-opportunities")
async def get_revenue_opportunities(
    db: AsyncSession = Depends(get_db),
    status: str = None
):
    """Get identified revenue opportunities."""
    try:
        query = select(RevenueOpportunity)
        
        if status:
            query = query.where(RevenueOpportunity.status == status)
        
        query = query.order_by(desc(RevenueOpportunity.created_at))
        
        result = await db.execute(query)
        opportunities = result.scalars().all()
        
        # Format opportunity data
        opportunity_data = []
        total_estimated_revenue = 0
        
        for opp in opportunities:
            opportunity_data.append({
                "id": str(opp.id),
                "opportunity_name": opp.opportunity_name,
                "description": opp.description,
                "estimated_revenue": opp.estimated_revenue,
                "confidence_score": opp.confidence_score,
                "brick_related": opp.brick_related,
                "status": opp.status,
                "implementation_notes": opp.implementation_notes,
                "created_at": opp.created_at.isoformat(),
                "updated_at": opp.updated_at.isoformat() if opp.updated_at else None,
                "implemented_at": opp.implemented_at.isoformat() if opp.implemented_at else None
            })
            
            if opp.status == "identified":
                total_estimated_revenue += opp.estimated_revenue
        
        return {
            "opportunities": opportunity_data,
            "summary": {
                "total_opportunities": len(opportunities),
                "total_estimated_revenue": total_estimated_revenue,
                "opportunities_by_status": {
                    status: len([o for o in opportunity_data if o["status"] == status])
                    for status in ["identified", "in_progress", "implemented"]
                }
            }
        }
        
    except Exception as e:
        logger.error("Failed to get revenue opportunities", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/sessions")
async def get_session_analytics(
    db: AsyncSession = Depends(get_db),
    hours: int = 24
):
    """Get orchestration session analytics."""
    try:
        since = datetime.now() - timedelta(hours=hours)
        
        # Get session statistics
        session_query = select(OrchestrationSession).where(
            OrchestrationSession.created_at >= since
        )
        
        result = await db.execute(session_query)
        sessions = result.scalars().all()
        
        # Calculate session statistics
        total_sessions = len(sessions)
        active_sessions = len([s for s in sessions if s.status == "active"])
        completed_sessions = len([s for s in sessions if s.status == "completed"])
        failed_sessions = len([s for s in sessions if s.status == "failed"])
        
        # Calculate average session duration
        completed_with_duration = [
            s for s in sessions 
            if s.status == "completed" and s.completed_at and s.created_at
        ]
        
        if completed_with_duration:
            total_duration = sum([
                (s.completed_at - s.created_at).total_seconds()
                for s in completed_with_duration
            ])
            avg_duration = total_duration / len(completed_with_duration)
        else:
            avg_duration = 0
        
        return {
            "time_range_hours": hours,
            "session_statistics": {
                "total_sessions": total_sessions,
                "active_sessions": active_sessions,
                "completed_sessions": completed_sessions,
                "failed_sessions": failed_sessions,
                "average_duration_seconds": avg_duration
            },
            "recent_sessions": [
                {
                    "id": str(s.id),
                    "session_name": s.session_name,
                    "status": s.status,
                    "created_at": s.created_at.isoformat(),
                    "completed_at": s.completed_at.isoformat() if s.completed_at else None
                }
                for s in sessions[-10:]  # Last 10 sessions
            ]
        }
        
    except Exception as e:
        logger.error("Failed to get session analytics", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/dashboard")
async def get_analytics_dashboard(db: AsyncSession = Depends(get_db)):
    """Get comprehensive analytics dashboard data."""
    try:
        # Get data for the last 24 hours
        since = datetime.now() - timedelta(hours=24)
        
        # Get session count
        session_count = await db.scalar(
            select(func.count(OrchestrationSession.id)).where(
                OrchestrationSession.created_at >= since
            )
        )
        
        # Get collaboration count
        collaboration_count = await db.scalar(
            select(func.count(AICollaboration.id)).where(
                AICollaboration.timestamp >= since
            )
        )
        
        # Get revenue opportunities
        revenue_opportunities = await db.scalar(
            select(func.count(RevenueOpportunity.id)).where(
                RevenueOpportunity.status == "identified"
            )
        )
        
        # Get total estimated revenue
        total_revenue = await db.scalar(
            select(func.sum(RevenueOpportunity.estimated_revenue)).where(
                RevenueOpportunity.status == "identified"
            )
        ) or 0
        
        return {
            "dashboard_data": {
                "sessions_24h": session_count,
                "collaborations_24h": collaboration_count,
                "revenue_opportunities": revenue_opportunities,
                "total_estimated_revenue": float(total_revenue),
                "system_health": "operational",
                "last_updated": datetime.now().isoformat()
            },
            "quick_stats": {
                "active_sessions": session_count,
                "ai_interactions": collaboration_count,
                "strategic_analyses": revenue_opportunities
            }
        }
        
    except Exception as e:
        logger.error("Failed to get analytics dashboard", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
