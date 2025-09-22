"""
I PROACTIVE BRICK Orchestration Intelligence
FastAPI Main Application Entry Point
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import structlog
import uvicorn

from app.core.config import settings
from app.core.database import init_db
from app.core.logging import setup_logging
from app.api.v1.api import api_router
from app.core.exceptions import BrickOrchestrationException


# Setup structured logging
setup_logging()
logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting I PROACTIVE BRICK Orchestration Intelligence")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized successfully")
    
    # Initialize AI services
    try:
        from app.services.ai_orchestrator import AIOrchestrator
        orchestrator = AIOrchestrator()
        await orchestrator.initialize()
        app.state.orchestrator = orchestrator
        logger.info("AI Orchestrator initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize AI Orchestrator", error=str(e))
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down I PROACTIVE BRICK Orchestration Intelligence")
    if hasattr(app.state, 'orchestrator'):
        await app.state.orchestrator.cleanup()


# Create FastAPI application
app = FastAPI(
    title="I PROACTIVE BRICK Orchestration Intelligence",
    description="Revolutionary orchestration intelligence that coordinates multiple production-ready autonomous AI systems for strategic BRICKS development and revenue generation.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"]
)


# Global exception handler
@app.exception_handler(BrickOrchestrationException)
async def brick_orchestration_exception_handler(request, exc: BrickOrchestrationException):
    """Handle custom Brick Orchestration exceptions"""
    logger.error(
        "Brick Orchestration Exception",
        error=exc.detail,
        status_code=exc.status_code,
        path=request.url.path
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "brick_orchestration_error"}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.error(
        "HTTP Exception",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "http_error"}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle general exceptions"""
    logger.error(
        "Unhandled Exception",
        error=str(exc),
        path=request.url.path,
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "type": "internal_error"
        }
    )


# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "I PROACTIVE BRICK Orchestration Intelligence API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        from app.core.database import get_db
        db = next(get_db())
        
        # Check Redis connection
        from app.core.cache import get_redis
        redis = await get_redis()
        await redis.ping()
        
        # Check AI orchestrator status
        orchestrator_status = "healthy"
        if hasattr(app.state, 'orchestrator'):
            orchestrator_status = await app.state.orchestrator.health_check()
        
        return {
            "status": "healthy",
            "database": "connected",
            "redis": "connected",
            "ai_orchestrator": orchestrator_status,
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unhealthy"
        )


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    if not settings.ENABLE_METRICS:
        raise HTTPException(status_code=404, detail="Metrics disabled")
    
    try:
        from app.core.metrics import generate_metrics
        return generate_metrics()
    except Exception as e:
        logger.error("Failed to generate metrics", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate metrics")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_config=None  # Use our structured logging
    )
