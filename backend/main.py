"""
I PROACTIVE BRICK Orchestration Intelligence - FastAPI Backend
Main application entry point for the orchestration control plane.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
import structlog
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_db
from app.api.routes import orchestration, health, analytics
from app.services.orchestrator import OrchestrationService

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

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting I PROACTIVE BRICK Orchestration Intelligence")
    await init_db()
    logger.info("Database initialized")
    
    # Initialize orchestration service
    app.state.orchestrator = OrchestrationService()
    await app.state.orchestrator.initialize()
    logger.info("Orchestration service initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down orchestration service")
    await app.state.orchestrator.shutdown()
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="I PROACTIVE BRICK Orchestration Intelligence",
    description="Orchestrates multiple AI systems for strategic BRICKS development",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include API routes
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(orchestration.router, prefix="/api/v1", tags=["orchestration"])
app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"])


@app.get("/")
async def root():
    """Root endpoint with system information."""
    return {
        "message": "I PROACTIVE BRICK Orchestration Intelligence",
        "version": "1.0.0",
        "status": "operational",
        "phase": "Foundation"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
