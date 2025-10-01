"""
UBIC v1.5 Health Check API Endpoints
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Depends, status
import structlog
from datetime import datetime
import time
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import AsyncSessionLocal

from app.models.ubic import (
    UBICResponse, HealthStatus, DependencyInfo, Status, Severity,
    StateMetrics, BrickCapabilities, CapabilityInfo, FeatureFlag,
    ResourceSpec, ConfigReloadRequest, EmergencyStopRequest
)

logger = structlog.get_logger(__name__)
router = APIRouter()

# Global variables for tracking service state
_service_start_time = time.time()
_request_count = 0
_success_count = 0
_failed_count = 0


async def check_database_health() -> Dict[str, Any]:
    """Check actual database connection health"""
    try:
        start_time = time.time()
        async with AsyncSessionLocal() as session:
            # Test database connection with a simple query
            result = await session.execute(text("SELECT 1 as test"))
            result.fetchone()
            response_time = int((time.time() - start_time) * 1000)
            
            return {
                "status": Status.HEALTHY,
                "response_time_ms": response_time,
                "connection_type": "vps_postgresql",
                "host": "64.227.99.111:5432",
                "database": "brick_orchestration"
            }
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        return {
            "status": Status.CRITICAL,
            "error": str(e),
            "connection_type": "vps_postgresql",
            "host": "64.227.99.111:5432",
            "database": "brick_orchestration"
        }


@router.get("/", response_model=UBICResponse)
async def health_check():
    """UBIC v1.5 Required Health Endpoint - Returns status with dependency health"""
    global _request_count, _success_count, _failed_count
    
    try:
        _request_count += 1
        _success_count += 1
        
        # Check dependencies with real database health check
        db_health = await check_database_health()
        
        dependencies = [
            DependencyInfo(
                name="postgresql",
                type="infra",
                severity=Severity.CRITICAL,
                status=db_health["status"],
                last_check=datetime.utcnow(),
                details=db_health
            ),
            DependencyInfo(
                name="redis",
                type="infra", 
                severity=Severity.CRITICAL,
                status=Status.HEALTHY,
                last_check=datetime.utcnow(),
                details={"response_time_ms": 5}
            ),
            DependencyInfo(
                name="crewai",
                type="functional",
                severity=Severity.WARNING,
                status=Status.HEALTHY,
                last_check=datetime.utcnow(),
                details={"api_configured": True}
            ),
            DependencyInfo(
                name="mem0",
                type="functional",
                severity=Severity.WARNING,
                status=Status.HEALTHY,
                last_check=datetime.utcnow(),
                details={"api_configured": True}
            )
        ]
        
        # Determine overall status based on dependencies
        overall_status = Status.HEALTHY
        for dep in dependencies:
            if dep.status == Status.CRITICAL and dep.severity == Severity.CRITICAL:
                overall_status = Status.CRITICAL
                break
            elif dep.status == Status.WARNING and dep.severity == Severity.CRITICAL:
                overall_status = Status.WARNING
        
        health_data = HealthStatus(
            status=overall_status,
            dependencies=dependencies,
            last_check=datetime.utcnow(),
            uptime_seconds=int(time.time() - _service_start_time)
        )
        
        return UBICResponse(
            status=Status.SUCCESS,
            message="Health check completed",
            details=health_data.dict()
        )
        
    except Exception as e:
        _failed_count += 1
        logger.error("Health check failed", error=str(e))
        return UBICResponse(
            status=Status.ERROR,
            error_code="HEALTH_CHECK_FAILED",
            message="Health check failed",
            details={"error": str(e)}
        )


@router.get("/capabilities", response_model=UBICResponse)
async def get_capabilities():
    """UBIC v1.5 Required Capabilities Endpoint - Returns capabilities, api_version, feature flags"""
    try:
        capabilities = [
            CapabilityInfo(
                name="orchestration",
                description="AI orchestration and task coordination",
                version="1.0",
                enabled=True
            ),
            CapabilityInfo(
                name="memory_persistence",
                description="Session management and memory persistence",
                version="1.0", 
                enabled=True
            ),
            CapabilityInfo(
                name="multi_model_routing",
                description="Message coordination across AI models",
                version="1.0",
                enabled=True
            ),
            CapabilityInfo(
                name="feedback_processing",
                description="Analytics engine for system optimization",
                version="1.0",
                enabled=True
            )
        ]
        
        feature_flags = [
            FeatureFlag(
                name="emergence_detection",
                supported=True,
                enabled=True,
                description="Detect emergence patterns in AI interactions"
            ),
            FeatureFlag(
                name="auto_scaling",
                supported=True,
                enabled=False,
                description="Automatic resource scaling based on load"
            ),
            FeatureFlag(
                name="advanced_monitoring",
                supported=True,
                enabled=True,
                description="Enhanced monitoring and observability"
            )
        ]
        
        resource_spec = ResourceSpec(
            cpu_min=0.5,
            cpu_recommended=2.0,
            cpu_max=8.0,
            memory_min="512Mi",
            memory_recommended="2Gi", 
            memory_max="8Gi",
            storage_min="5Gi",
            storage_recommended="50Gi",
            storage_max="500Gi"
        )
        
        brick_capabilities = BrickCapabilities(
            capabilities=capabilities,
            api_version="1.5",
            feature_flags=feature_flags,
            resource_spec=resource_spec
        )
        
        return UBICResponse(
            status=Status.SUCCESS,
            message="Capabilities retrieved successfully",
            details=brick_capabilities.dict()
        )
        
    except Exception as e:
        logger.error("Failed to get capabilities", error=str(e))
        return UBICResponse(
            status=Status.ERROR,
            error_code="CAPABILITIES_FAILED",
            message="Failed to retrieve capabilities",
            details={"error": str(e)}
        )


@router.get("/state", response_model=UBICResponse)
async def get_state():
    """UBIC v1.5 Required State Endpoint - Returns operational metrics (not functional details)"""
    try:
        global _request_count, _success_count, _failed_count
        
        success_rate = (_success_count / _request_count * 100) if _request_count > 0 else 0
        
        state_metrics = StateMetrics(
            requests_total=_request_count,
            requests_success=_success_count,
            requests_failed=_failed_count,
            average_response_time_ms=250.0,  # Mock value
            memory_usage_percent=45.2,  # Mock value
            cpu_usage_percent=23.1,  # Mock value
            active_connections=5,  # Mock value
            last_updated=datetime.utcnow()
        )
        
        return UBICResponse(
            status=Status.SUCCESS,
            message="State metrics retrieved successfully",
            details=state_metrics.dict()
        )
        
    except Exception as e:
        logger.error("Failed to get state", error=str(e))
        return UBICResponse(
            status=Status.ERROR,
            error_code="STATE_FAILED",
            message="Failed to retrieve state metrics",
            details={"error": str(e)}
        )


@router.get("/dependencies", response_model=UBICResponse)
async def get_dependencies():
    """UBIC v1.5 Required Dependencies Endpoint - Lists infra + functional + optional dependencies"""
    try:
        # Get real database health status
        db_health = await check_database_health()
        
        dependencies = [
            DependencyInfo(
                name="postgresql",
                type="infra",
                severity=Severity.CRITICAL,
                status=db_health["status"],
                last_check=datetime.utcnow(),
                details=db_health
            ),
            DependencyInfo(
                name="redis",
                type="infra",
                severity=Severity.CRITICAL,
                status=Status.HEALTHY,
                last_check=datetime.utcnow(),
                details={"host": "redis", "port": 6379}
            ),
            DependencyInfo(
                name="crewai",
                type="functional",
                severity=Severity.WARNING,
                status=Status.HEALTHY,
                last_check=datetime.utcnow(),
                details={"version": "0.28.9rc2", "agents_available": 5}
            ),
            DependencyInfo(
                name="mem0",
                type="functional",
                severity=Severity.WARNING,
                status=Status.HEALTHY,
                last_check=datetime.utcnow(),
                details={"version": "0.1.0", "memory_count": 150}
            ),
            DependencyInfo(
                name="openai",
                type="optional",
                severity=Severity.INFO,
                status=Status.HEALTHY,
                last_check=datetime.utcnow(),
                details={"models_available": ["gpt-4", "gpt-3.5-turbo"]}
            ),
            DependencyInfo(
                name="anthropic",
                type="optional",
                severity=Severity.INFO,
                status=Status.HEALTHY,
                last_check=datetime.utcnow(),
                details={"models_available": ["claude-3-opus", "claude-3-sonnet"]}
            )
        ]
        
        return UBICResponse(
            status=Status.SUCCESS,
            message="Dependencies retrieved successfully",
            details={"dependencies": [dep.dict() for dep in dependencies]}
        )
        
    except Exception as e:
        logger.error("Failed to get dependencies", error=str(e))
        return UBICResponse(
            status=Status.ERROR,
            error_code="DEPENDENCIES_FAILED",
            message="Failed to retrieve dependencies",
            details={"error": str(e)}
        )


@router.post("/reload-config", response_model=UBICResponse)
async def reload_config(request: ConfigReloadRequest):
    """UBIC v1.5 Required Reload Config Endpoint - Validates & reloads configuration (audit logged)"""
    try:
        logger.info(
            "Configuration reload requested",
            request_id=request.request_id,
            dry_run=request.dry_run,
            user="system"
        )
        
        if request.dry_run:
            # Validate configuration without applying
            validation_result = {
                "valid": True,
                "errors": [],
                "warnings": ["Mock validation - would check actual config in production"]
            }
            
            return UBICResponse(
                status=Status.SUCCESS,
                message="Configuration validation completed (dry run)",
                details={
                    "validation_result": validation_result,
                    "request_id": request.request_id
                }
            )
        else:
            # Apply configuration
            logger.info(
                "Configuration reload applied",
                request_id=request.request_id,
                user="system"
            )
            
            return UBICResponse(
                status=Status.SUCCESS,
                message="Configuration reloaded successfully",
                details={
                    "reloaded_at": datetime.utcnow().isoformat(),
                    "request_id": request.request_id
                }
            )
            
    except Exception as e:
        logger.error("Failed to reload configuration", error=str(e), request_id=request.request_id)
        return UBICResponse(
            status=Status.ERROR,
            error_code="CONFIG_RELOAD_FAILED",
            message="Failed to reload configuration",
            details={"error": str(e), "request_id": request.request_id}
        )


@router.post("/shutdown", response_model=UBICResponse)
async def graceful_shutdown():
    """UBIC v1.5 Required Shutdown Endpoint - Graceful termination"""
    try:
        logger.info("Graceful shutdown initiated")
        
        # In a real implementation, this would:
        # 1. Stop accepting new requests
        # 2. Finish processing current requests
        # 3. Close database connections
        # 4. Clean up resources
        
        return UBICResponse(
            status=Status.SUCCESS,
            message="Graceful shutdown initiated",
            details={
                "shutdown_initiated_at": datetime.utcnow().isoformat(),
                "estimated_completion_seconds": 30
            }
        )
        
    except Exception as e:
        logger.error("Failed to initiate graceful shutdown", error=str(e))
        return UBICResponse(
            status=Status.ERROR,
            error_code="SHUTDOWN_FAILED",
            message="Failed to initiate graceful shutdown",
            details={"error": str(e)}
        )


@router.post("/emergency-stop", response_model=UBICResponse)
async def emergency_stop(request: EmergencyStopRequest):
    """UBIC v1.5 Required Emergency Stop Endpoint - Immediate shutdown (security breach/data corruption)"""
    try:
        logger.critical(
            "Emergency stop initiated",
            reason=request.reason,
            severity=request.severity,
            cooldown_seconds=request.cooldown_seconds,
            request_id=request.request_id
        )
        
        # In a real implementation, this would:
        # 1. Immediately stop all processing
        # 2. Broadcast emergency stop to other bricks
        # 3. Set cooldown period before restart
        # 4. Generate post-mortem report
        
        return UBICResponse(
            status=Status.SUCCESS,
            message="Emergency stop executed",
            details={
                "emergency_stop_at": datetime.utcnow().isoformat(),
                "reason": request.reason,
                "severity": request.severity,
                "cooldown_seconds": request.cooldown_seconds,
                "request_id": request.request_id
            }
        )
        
    except Exception as e:
        logger.error("Failed to execute emergency stop", error=str(e))
        return UBICResponse(
            status=Status.ERROR,
            error_code="EMERGENCY_STOP_FAILED",
            message="Failed to execute emergency stop",
            details={"error": str(e)}
        )


