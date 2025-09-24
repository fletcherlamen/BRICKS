"""
Simple FastAPI application for I PROACTIVE BRICK Orchestration Intelligence
This version runs without database dependencies for initial testing
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog
from app.api.v1.api import api_router
from app.models.ubic import UBICResponse, Status
from app.core.config import settings
from datetime import datetime
import asyncio

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="I PROACTIVE BRICK Orchestration Intelligence (UBIC v1.5)",
    description="AI-Powered Strategic Business Development Platform - Universal Brick Interface Contract v1.5",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Database initialization (temporarily disabled)
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        from app.core.database import init_db
        await init_db()
        print("✅ Database initialization completed")
    except Exception as e:
        print(f"⚠️ Database initialization failed: {e}")
        # Continue without database for now

# Configure CORS
app.add_middleware(
    CORSMiddleware,
     allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "I PROACTIVE BRICK Orchestration Intelligence API (UBIC v1.5)",
        "status": "operational",
        "version": "1.0.0",
        "ubic_version": "1.5"
    }

@app.get("/health", response_model=UBICResponse)
async def health_check():
    """UBIC v1.5 Root Health Endpoint"""
    logger.info("Health check requested")
    return UBICResponse(
        status=Status.SUCCESS,
        message="Service is healthy",
        details={
            "service": "I PROACTIVE BRICK Orchestration Intelligence",
            "ubic_version": "1.5",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.get("/api/v1/status")
async def api_status():
    """API status endpoint"""
    return {
        "api_version": "v1",
        "ubic_version": "1.5",
        "status": "operational",
        "required_endpoints": {
            "health": "GET /api/v1/health/",
            "capabilities": "GET /api/v1/health/capabilities",
            "state": "GET /api/v1/health/state",
            "dependencies": "GET /api/v1/health/dependencies",
            "message": "POST /api/v1/message-bus/message",
            "send": "POST /api/v1/message-bus/send",
            "reload_config": "POST /api/v1/health/reload-config",
            "shutdown": "POST /api/v1/health/shutdown",
            "emergency_stop": "POST /api/v1/health/emergency-stop"
        }
    }

@app.get("/api/v1/orchestration")
async def orchestration_status():
    """Orchestration status endpoint"""
    logger.info("Orchestration status requested")
    return {
        "status": "ready",
        "active_tasks": 0,
        "completed_tasks": 0,
        "ai_models": {
            "gpt4": "available",
            "claude": "available", 
            "gemini": "available"
        }
    }

@app.get("/api/v1/bricks")
async def bricks_status():
    """BRICKS status endpoint"""
    return {
        "total_bricks": 0,
        "active_bricks": 0,
        "strategic_components": []
    }

@app.get("/api/v1/memory")
async def memory_status():
    """Memory status endpoint"""
    return {
        "memory_system": "ready",
        "total_memories": 0,
        "last_sync": "2025-09-22T02:55:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting I PROACTIVE BRICK Orchestration Intelligence")
    uvicorn.run(app, host="0.0.0.0", port=8000)
