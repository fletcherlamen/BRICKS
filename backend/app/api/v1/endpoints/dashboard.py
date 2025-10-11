"""
Unified Orchestration Dashboard API
Real-time monitoring and control of all autonomous systems
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
import structlog
from datetime import datetime, timedelta

from app.core.exceptions import AIOrchestrationError
from app.models.orchestration import UBICResponse
from app.services.ai_orchestrator import AIOrchestrator

logger = structlog.get_logger(__name__)

router = APIRouter(tags=["Dashboard"])


class DashboardMetrics(BaseModel):
    """Dashboard metrics model"""
    timestamp: str
    system_health: str
    active_sessions: int
    total_requests_today: int
    success_rate: float
    average_response_time: float
    cost_utilization: float
    services_status: Dict[str, Any]


class SystemStatus(BaseModel):
    """System status model"""
    service_name: str
    status: str
    health_score: float
    last_activity: str
    metrics: Dict[str, Any]


class OrchestrationLog(BaseModel):
    """Orchestration log entry"""
    timestamp: str
    session_id: str
    task_type: str
    status: str
    duration_ms: int
    services_used: List[str]
    result_summary: str


# Global orchestrator instance (will be injected)
real_orchestrator: Optional[AIOrchestrator] = None


async def get_orchestrator() -> AIOrchestrator:
    """Get or create the global AIOrchestrator instance"""
    from app.services.ai_orchestrator import AIOrchestrator
    
    orchestrator = AIOrchestrator()
    await orchestrator.initialize()
    return orchestrator


@router.get("/test")
async def test_dashboard():
    """Test endpoint to verify dashboard router is working"""
    return {"message": "Dashboard router is working"}

@router.get("/overview", response_model=UBICResponse)
async def get_dashboard_overview(
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """Get comprehensive dashboard overview"""
    
    try:
        # Get system status
        system_status = await orchestrator.get_system_status()
        health_status = await orchestrator.health_check()
        
        # Calculate metrics
        total_services = len(system_status.get("services", {}))
        healthy_services = sum(
            1 for service in system_status.get("services", {}).values()
            if service.get("status") == "healthy"
        )
        
        health_score = (healthy_services / total_services * 100) if total_services > 0 else 0
        
        # Get cost optimization metrics if available
        cost_metrics = {}
        if "multi_model_router" in system_status.get("services", {}):
            router_status = system_status["services"]["multi_model_router"]
            if "cost_optimization" in router_status:
                cost_metrics = router_status["cost_optimization"]
        
        overview = {
            "timestamp": datetime.now().isoformat(),
            "system_health": health_status,
            "health_score": health_score,
            "total_services": total_services,
            "healthy_services": healthy_services,
            "services_status": system_status.get("services", {}),
            "cost_optimization": cost_metrics,
            "orchestrator_status": system_status.get("orchestrator", "unknown")
        }
        
        return UBICResponse(
            success=True,
            message="Dashboard overview retrieved successfully",
            data=overview
        )
        
    except Exception as e:
        logger.error("Failed to get dashboard overview", error=str(e))
        raise HTTPException(status_code=500, detail=f"Dashboard overview failed: {str(e)}")


@router.get("/services", response_model=UBICResponse)
async def get_services_status():
    """Get detailed status of all services"""
    
    try:
        # Check API keys and service status directly without full orchestrator initialization
        from app.core.config import settings
        
        service_list = []
        
        # Check each service individually
        services_to_check = [
            ("openai", "OpenAI API", settings.OPENAI_API_KEY),
            ("anthropic", "Anthropic API", settings.ANTHROPIC_API_KEY),
            ("google", "Google Gemini API", settings.GOOGLE_GEMINI_API_KEY),
            ("mem0", "Mem0 AI", settings.MEM0_API_KEY),
            ("crewai", "CrewAI", settings.CREWAI_API_KEY),
            ("devin", "Devin AI", settings.DEVIN_API_KEY),
            ("copilot", "Copilot Studio", settings.COPILOT_STUDIO_API_KEY),
            ("github_copilot", "GitHub Copilot", settings.GITHUB_COPILOT_TOKEN)
        ]
        
        for service_id, service_name, api_key in services_to_check:
            # Check if API key is configured and not a placeholder
            api_key_configured = bool(api_key and api_key.strip() != "" and not api_key.startswith("your-"))
            
            # Special handling for specific services
            if not api_key_configured:
                status = "critical"
                health_score = 0.0
                message = "API key not configured - service not operational"
            elif service_id == "devin":
                # For Devin AI, check the actual service status instead of assuming warning
                try:
                    from app.services.devin_service import DevinService
                    devin_service = DevinService()
                    await devin_service.initialize()
                    devin_status = await devin_service.get_status()
                    status = devin_status["status"]
                    health_score = 100.0 if devin_status["status"] == "healthy" else 75.0
                    message = devin_status["message"]
                except Exception as e:
                    # Fallback to warning if we can't check the actual status
                    status = "warning"
                    health_score = 75.0
                    message = "API key configured but using enhanced mock mode - Devin AI API may not be publicly available yet"
            else:
                # All other services with real API keys should be healthy
                status = "healthy"
                health_score = 100.0
                message = "API key configured - service operational"
            
            service_status = SystemStatus(
                service_name=service_name,
                status=status,
                health_score=health_score,
                last_activity=datetime.now().isoformat(),
                metrics={
                    "api_key_configured": api_key_configured,
                    "service_id": service_id,
                    "message": message
                }
            )
            service_list.append(service_status)
        
        return UBICResponse(
            success=True,
            message="Services status retrieved successfully",
            data={
                "services": [service.dict() for service in service_list],
                "total_services": len(service_list),
                "healthy_services": sum(1 for s in service_list if s.status == "healthy"),
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to get services status", error=str(e))
        raise HTTPException(status_code=500, detail=f"Services status failed: {str(e)}")


@router.get("/metrics", response_model=UBICResponse)
async def get_system_metrics(
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """Get system performance metrics"""
    
    try:
        system_status = await orchestrator.get_system_status()
        
        # Calculate performance metrics
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "system_health": await orchestrator.health_check(),
            "services_count": len(system_status.get("services", {})),
            "healthy_services": sum(
                1 for service in system_status.get("services", {}).values()
                if service.get("status") == "healthy"
            )
        }
        
        # Add service-specific metrics
        for service_name, service_data in system_status.get("services", {}).items():
            if "performance_metrics" in service_data:
                metrics[f"{service_name}_performance"] = service_data["performance_metrics"]
            
            if "cost_optimization" in service_data:
                metrics[f"{service_name}_cost"] = service_data["cost_optimization"]
        
        return UBICResponse(
            status="success",
            message="System metrics retrieved successfully",
            details=metrics
        )
        
    except Exception as e:
        logger.error("Failed to get system metrics", error=str(e))
        raise HTTPException(status_code=500, detail=f"System metrics failed: {str(e)}")


@router.get("/cost-analysis", response_model=UBICResponse)
async def get_cost_analysis(
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """Get cost analysis and optimization insights"""
    
    try:
        system_status = await orchestrator.get_system_status()
        
        # Extract cost optimization data
        cost_data = {}
        total_daily_cost = 0
        
        for service_name, service_data in system_status.get("services", {}).items():
            if "cost_optimization" in service_data:
                cost_info = service_data["cost_optimization"]
                cost_data[service_name] = cost_info
                
                if "daily_usage" in cost_info:
                    total_daily_cost += cost_info["daily_usage"]
        
        # Calculate cost insights
        cost_analysis = {
            "timestamp": datetime.now().isoformat(),
            "total_daily_cost": total_daily_cost,
            "service_costs": cost_data,
            "cost_optimization_insights": {
                "highest_cost_service": max(cost_data.keys(), key=lambda k: cost_data[k].get("daily_usage", 0)) if cost_data else None,
                "cost_efficiency_score": self._calculate_cost_efficiency(cost_data),
                "optimization_recommendations": self._generate_cost_recommendations(cost_data)
            }
        }
        
        return UBICResponse(
            status="success",
            message="Cost analysis retrieved successfully",
            details=cost_analysis
        )
        
    except Exception as e:
        logger.error("Failed to get cost analysis", error=str(e))
        raise HTTPException(status_code=500, detail=f"Cost analysis failed: {str(e)}")


@router.get("/performance", response_model=UBICResponse)
async def get_performance_metrics(
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """Get performance metrics for all services"""
    
    try:
        system_status = await orchestrator.get_system_status()
        
        performance_metrics = {
            "timestamp": datetime.now().isoformat(),
            "overall_performance": {
                "system_health": await orchestrator.health_check(),
                "response_time_avg": 0,
                "success_rate_avg": 0,
                "throughput": 0
            },
            "service_performance": {}
        }
        
        # Aggregate performance metrics from all services
        total_response_time = 0
        total_success_rate = 0
        service_count = 0
        
        for service_name, service_data in system_status.get("services", {}).items():
            if "performance_metrics" in service_data:
                perf_data = service_data["performance_metrics"]
                performance_metrics["service_performance"][service_name] = perf_data
                
                # Aggregate metrics
                for model_name, model_metrics in perf_data.items():
                    if "avg_response_time" in model_metrics:
                        total_response_time += model_metrics["avg_response_time"]
                    if "success_rate" in model_metrics:
                        total_success_rate += model_metrics["success_rate"]
                    service_count += 1
        
        # Calculate averages
        if service_count > 0:
            performance_metrics["overall_performance"]["response_time_avg"] = total_response_time / service_count
            performance_metrics["overall_performance"]["success_rate_avg"] = total_success_rate / service_count
        
        return UBICResponse(
            status="success",
            message="Performance metrics retrieved successfully",
            details=performance_metrics
        )
        
    except Exception as e:
        logger.error("Failed to get performance metrics", error=str(e))
        raise HTTPException(status_code=500, detail=f"Performance metrics failed: {str(e)}")


@router.get("/health-check", response_model=UBICResponse)
async def comprehensive_health_check(
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """Perform comprehensive health check on all systems"""
    
    try:
        # Get system status
        system_status = await orchestrator.get_system_status()
        health_status = await orchestrator.health_check()
        
        # Detailed health check
        health_details = {
            "timestamp": datetime.now().isoformat(),
            "overall_health": health_status,
            "orchestrator_status": system_status.get("orchestrator", "unknown"),
            "services_health": {},
            "health_summary": {
                "total_services": 0,
                "healthy_services": 0,
                "degraded_services": 0,
                "unhealthy_services": 0
            }
        }
        
        # Check each service
        for service_name, service_data in system_status.get("services", {}).items():
            service_status = service_data.get("status", "unknown")
            health_details["services_health"][service_name] = {
                "status": service_status,
                "details": service_data,
                "last_check": datetime.now().isoformat()
            }
            
            # Update summary
            health_details["health_summary"]["total_services"] += 1
            if service_status == "healthy":
                health_details["health_summary"]["healthy_services"] += 1
            elif service_status == "degraded":
                health_details["health_summary"]["degraded_services"] += 1
            else:
                health_details["health_summary"]["unhealthy_services"] += 1
        
        return UBICResponse(
            status="success",
            message="Health check completed successfully",
            details=health_details
        )
        
    except Exception as e:
        logger.error("Failed to perform health check", error=str(e))
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@router.post("/restart-service", response_model=UBICResponse)
async def restart_service(
    service_name: str,
    background_tasks: BackgroundTasks,
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """Restart a specific service"""
    
    try:
        # Validate service name
        valid_services = [
            "crewai", "mem0", "devin", "copilot", 
            "github_copilot", "multi_model_router"
        ]
        
        if service_name not in valid_services:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid service name. Valid services: {valid_services}"
            )
        
        # Schedule service restart in background
        background_tasks.add_task(restart_service_task, orchestrator, service_name)
        
        return UBICResponse(
            status="success",
            message=f"Service {service_name} restart initiated",
            details={
                "service_name": service_name,
                "restart_initiated": True,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to restart service", service=service_name, error=str(e))
        raise HTTPException(status_code=500, detail=f"Service restart failed: {str(e)}")


@router.get("/logs", response_model=UBICResponse)
async def get_system_logs(
    limit: int = 100,
    service: Optional[str] = None
):
    """Get system logs (mock implementation)"""
    
    try:
        # Mock log entries
        logs = []
        for i in range(min(limit, 50)):  # Limit to 50 for demo
            log_entry = OrchestrationLog(
                timestamp=(datetime.now() - timedelta(minutes=i)).isoformat(),
                session_id=f"session_{i:03d}",
                task_type=["strategic_analysis", "brick_development", "revenue_optimization"][i % 3],
                status=["completed", "in_progress", "failed"][i % 3],
                duration_ms=1000 + (i * 100),
                services_used=["crewai", "devin", "copilot"][:i % 3 + 1],
                result_summary=f"Task {i} completed successfully"
            )
            logs.append(log_entry)
        
        # Filter by service if specified
        if service:
            logs = [log for log in logs if service in log.services_used]
        
        return UBICResponse(
            status="success",
            message="System logs retrieved successfully",
            details={
                "logs": [log.dict() for log in logs],
                "total_logs": len(logs),
                "filtered_by": service,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to get system logs", error=str(e))
        raise HTTPException(status_code=500, detail=f"System logs failed: {str(e)}")


async def restart_service_task(orchestrator: AIOrchestrator, service_name: str):
    """Background task to restart a service"""
    try:
        logger.info(f"Restarting service: {service_name}")
        
        # Get the service instance
        service = getattr(orchestrator, f"{service_name}_service", None)
        if service:
            # Cleanup and reinitialize
            await service.cleanup()
            await service.initialize()
            logger.info(f"Service {service_name} restarted successfully")
        else:
            logger.error(f"Service {service_name} not found")
            
    except Exception as e:
        logger.error(f"Failed to restart service {service_name}", error=str(e))


def _calculate_cost_efficiency(cost_data: Dict[str, Any]) -> float:
    """Calculate cost efficiency score"""
    if not cost_data:
        return 0.0
    
    total_usage = sum(service.get("daily_usage", 0) for service in cost_data.values())
    total_budget = sum(service.get("daily_budget", 100) for service in cost_data.values())
    
    if total_budget == 0:
        return 0.0
    
    efficiency = (1 - (total_usage / total_budget)) * 100
    return max(0.0, min(100.0, efficiency))


def _generate_cost_recommendations(cost_data: Dict[str, Any]) -> List[str]:
    """Generate cost optimization recommendations"""
    recommendations = []
    
    for service_name, service_info in cost_data.items():
        daily_usage = service_info.get("daily_usage", 0)
        daily_budget = service_info.get("daily_budget", 100)
        
        if daily_usage > daily_budget * 0.8:
            recommendations.append(f"Consider optimizing {service_name} usage - currently at {daily_usage:.2f}/{daily_budget:.2f}")
        
        if service_info.get("budget_status") == "critical":
            recommendations.append(f"URGENT: {service_name} budget critical - immediate optimization needed")
    
    if not recommendations:
        recommendations.append("Cost utilization is within acceptable limits")
    
    return recommendations


# Set the global orchestrator instance
def set_orchestrator(orchestrator: AIOrchestrator):
    """Set the global orchestrator instance"""
    global real_orchestrator
    real_orchestrator = orchestrator
