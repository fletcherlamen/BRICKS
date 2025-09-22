"""
UBIC v1.5 Models - Universal Brick Interface Contract
"""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
from enum import Enum
import uuid
from datetime import datetime


class Priority(str, Enum):
    """Message priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    EMERGENCY = "emergency"


class Status(str, Enum):
    """Standard status values"""
    SUCCESS = "success"
    ERROR = "error"
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"


class Severity(str, Enum):
    """Dependency severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class UBICResponse(BaseModel):
    """UBIC v1.5 Standard API Response Format"""
    status: Status = Field(..., description="Response status")
    error_code: Optional[str] = Field(None, description="Error code if applicable")
    message: str = Field(..., description="Response message")
    details: Dict[str, Any] = Field(default_factory=dict, description="Additional details")


class EmergenceSignal(BaseModel):
    """Emergence detection signal"""
    signal: bool = Field(..., description="Whether emergence is detected")
    type: Optional[str] = Field(None, description="Type of emergence")
    confidence: float = Field(0.0, description="Confidence level 0-1")
    threshold_metrics: Dict[str, Any] = Field(default_factory=dict, description="Boundary conditions")


class UBICMessage(BaseModel):
    """UBIC v1.5 Standard Message Format"""
    idempotency_key: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique message identifier")
    priority: Priority = Field(Priority.NORMAL, description="Message priority")
    source: str = Field(..., description="Source brick name")
    target: str = Field(..., description="Target brick name")
    message_type: str = Field(..., description="Type of message")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Message payload")
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Request trace identifier")
    emergence: Optional[EmergenceSignal] = Field(None, description="Emergence detection data")


class DependencyInfo(BaseModel):
    """Dependency information"""
    name: str = Field(..., description="Dependency name")
    type: str = Field(..., description="Dependency type (infra/functional/optional)")
    severity: Severity = Field(Severity.INFO, description="Dependency severity")
    status: Status = Field(..., description="Dependency status")
    last_check: datetime = Field(default_factory=datetime.utcnow, description="Last health check")
    details: Dict[str, Any] = Field(default_factory=dict, description="Additional dependency info")


class CapabilityInfo(BaseModel):
    """Brick capabilities information"""
    name: str = Field(..., description="Capability name")
    description: str = Field(..., description="Capability description")
    version: str = Field(..., description="Capability version")
    enabled: bool = Field(True, description="Whether capability is enabled")


class FeatureFlag(BaseModel):
    """Feature flag definition"""
    name: str = Field(..., description="Feature flag name")
    supported: bool = Field(..., description="Whether feature is supported")
    enabled: bool = Field(False, description="Whether feature is enabled")
    description: Optional[str] = Field(None, description="Feature description")


class ResourceSpec(BaseModel):
    """Resource specification"""
    cpu_min: float = Field(0.1, description="Minimum CPU cores")
    cpu_recommended: float = Field(1.0, description="Recommended CPU cores")
    cpu_max: float = Field(4.0, description="Maximum CPU cores")
    memory_min: str = Field("256Mi", description="Minimum memory")
    memory_recommended: str = Field("1Gi", description="Recommended memory")
    memory_max: str = Field("4Gi", description="Maximum memory")
    storage_min: str = Field("1Gi", description="Minimum storage")
    storage_recommended: str = Field("10Gi", description="Recommended storage")
    storage_max: str = Field("100Gi", description="Maximum storage")


class HealthStatus(BaseModel):
    """Health status with dependencies"""
    status: Status = Field(..., description="Overall health status")
    dependencies: List[DependencyInfo] = Field(default_factory=list, description="Dependency health")
    last_check: datetime = Field(default_factory=datetime.utcnow, description="Last health check")
    uptime_seconds: int = Field(0, description="Service uptime in seconds")


class StateMetrics(BaseModel):
    """Operational state metrics"""
    requests_total: int = Field(0, description="Total requests processed")
    requests_success: int = Field(0, description="Successful requests")
    requests_failed: int = Field(0, description="Failed requests")
    average_response_time_ms: float = Field(0.0, description="Average response time")
    memory_usage_percent: float = Field(0.0, description="Memory usage percentage")
    cpu_usage_percent: float = Field(0.0, description="CPU usage percentage")
    active_connections: int = Field(0, description="Active connections")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last metrics update")


class BrickCapabilities(BaseModel):
    """Brick capabilities response"""
    capabilities: List[CapabilityInfo] = Field(default_factory=list, description="Available capabilities")
    api_version: str = Field("1.5", description="UBIC API version")
    feature_flags: List[FeatureFlag] = Field(default_factory=list, description="Feature flags")
    resource_spec: ResourceSpec = Field(default_factory=ResourceSpec, description="Resource specification")


class ConfigReloadRequest(BaseModel):
    """Configuration reload request"""
    dry_run: bool = Field(True, description="Whether to perform dry run validation")
    config_data: Dict[str, Any] = Field(..., description="Configuration data to reload")
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Request identifier")


class RateLimitInfo(BaseModel):
    """Rate limiting information"""
    requests_per_minute: int = Field(60, description="Requests allowed per minute")
    requests_per_hour: int = Field(1000, description="Requests allowed per hour")
    burst_limit: int = Field(10, description="Burst request limit")
    current_usage: int = Field(0, description="Current usage count")
    reset_time: datetime = Field(default_factory=datetime.utcnow, description="Usage reset time")


class EmergencyStopRequest(BaseModel):
    """Emergency stop request"""
    reason: str = Field(..., description="Reason for emergency stop")
    severity: Severity = Field(Severity.CRITICAL, description="Emergency severity")
    cooldown_seconds: int = Field(300, description="Cooldown period before restart")
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Request identifier")


class AuditLogEntry(BaseModel):
    """Audit log entry"""
    request_id: str = Field(..., description="Request identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")
    action: str = Field(..., description="Action performed")
    user: Optional[str] = Field(None, description="User identifier")
    details: Dict[str, Any] = Field(default_factory=dict, description="Action details")
    result: Status = Field(..., description="Action result")
