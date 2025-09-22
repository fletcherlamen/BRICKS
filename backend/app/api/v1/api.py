"""
API v1 Router Configuration
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health, message_bus, metrics

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
