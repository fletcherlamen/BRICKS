"""
API v1 Router Configuration
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health, message_bus, metrics, memory, orchestration

api_router = APIRouter()

# UBIC v1.5 Required Endpoints Only
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["ubic-health"]
)

api_router.include_router(
    message_bus.router,
    prefix="/message-bus",
    tags=["ubic-message-bus"]
)

api_router.include_router(
    metrics.router,
    prefix="/metrics",
    tags=["ubic-metrics"]
)

# Enhanced Memory System (Client Requested)
api_router.include_router(
    memory.router,
    prefix="/memory",
    tags=["enhanced-memory"]
)

# Real Orchestration System (Client Requested)
api_router.include_router(
    orchestration.router,
    prefix="/orchestration",
    tags=["real-orchestration"]
)
