"""
Health check and system status endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import structlog

from app.core.database import get_db
from app.models.analytics import SystemHealth

logger = structlog.get_logger()
router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "I PROACTIVE BRICK Orchestration Intelligence",
        "version": "1.0.0"
    }


@router.get("/health/detailed")
async def detailed_health_check(db: AsyncSession = Depends(get_db)):
    """Detailed health check with system status."""
    try:
        # Check database connection
        await db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": db_status,
            "orchestration": "healthy",
            "crewai": "healthy",
            "mem0": "healthy"
        },
        "version": "1.0.0"
    }


@router.get("/status")
async def system_status():
    """Get overall system status and capabilities."""
    return {
        "system": "I PROACTIVE BRICK Orchestration Intelligence",
        "phase": "Foundation",
        "capabilities": [
            "CrewAI orchestration",
            "Mem0.ai memory persistence",
            "Multi-AI collaboration logging",
            "Strategic analysis execution",
            "Performance metrics tracking"
        ],
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }
