"""
API v1 Router Configuration
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health, message_bus, metrics, memory, orchestration, chat, brick2_handshake, dashboard, database, strategic, revenue_integration, bricks, ubic

api_router = APIRouter()

# UBIC v1.5 Compliance Endpoints (CRITICAL)
api_router.include_router(
    ubic.router,
    prefix="",  # No prefix - UBIC endpoints at root level
    tags=["ubic-compliance"]
)

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

# System Chat Interface (Milestone 1 Completion)
api_router.include_router(
    chat.router,
    prefix="/chat",
    tags=["system-chat"]
)

# BRICK-2 Handshake Stub (Milestone 1 Completion)
api_router.include_router(
    brick2_handshake.router,
    prefix="/brick2",
    tags=["brick2-integration"]
)

# Unified Orchestration Dashboard (Phase 2 Completion)
api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["orchestration-dashboard"]
)

# Database Health and Diagnostics
api_router.include_router(
    database.router,
    prefix="/database",
    tags=["database-health"]
)

# Strategic Intelligence Layer (Phase 3 Completion)
api_router.include_router(
    strategic.router,
    prefix="/strategic",
    tags=["strategic-intelligence"]
)

# Revenue Integration Loop (Phase 4 Completion)
api_router.include_router(
    revenue_integration.router,
    prefix="/revenue",
    tags=["revenue-integration"]
)

# BRICKS Management (VPS Database)
api_router.include_router(
    bricks.router,
    prefix="/bricks",
    tags=["bricks-management"]
)
