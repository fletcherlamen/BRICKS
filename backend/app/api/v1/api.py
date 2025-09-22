"""
API v1 Router Configuration
"""

from fastapi import APIRouter

from app.api.v1.endpoints import orchestration, bricks, memory, health

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    orchestration.router,
    prefix="/orchestration",
    tags=["orchestration"]
)

api_router.include_router(
    bricks.router,
    prefix="/bricks",
    tags=["bricks"]
)

api_router.include_router(
    memory.router,
    prefix="/memory",
    tags=["memory"]
)

api_router.include_router(
    health.router,
    prefix="/health",
    tags=["health"]
)
