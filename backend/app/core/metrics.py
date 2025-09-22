"""
Prometheus metrics collection
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import structlog

logger = structlog.get_logger(__name__)

# Request metrics
REQUEST_COUNT = Counter(
    'brick_orchestration_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'brick_orchestration_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

# AI System metrics
AI_REQUESTS = Counter(
    'brick_orchestration_ai_requests_total',
    'Total AI system requests',
    ['ai_system', 'task_type', 'status']
)

AI_RESPONSE_TIME = Histogram(
    'brick_orchestration_ai_response_time_seconds',
    'AI system response time',
    ['ai_system', 'task_type']
)

# Orchestration metrics
ORCHESTRATION_SESSIONS = Gauge(
    'brick_orchestration_active_sessions',
    'Number of active orchestration sessions'
)

ORCHESTRATION_TASKS = Counter(
    'brick_orchestration_tasks_total',
    'Total orchestration tasks',
    ['task_type', 'status']
)

# Business metrics
BRICK_ANALYSES = Counter(
    'brick_orchestration_brick_analyses_total',
    'Total BRICK analyses performed'
)

REVENUE_OPPORTUNITIES = Gauge(
    'brick_orchestration_revenue_opportunities_identified',
    'Number of revenue opportunities identified'
)

STRATEGIC_GAPS = Gauge(
    'brick_orchestration_strategic_gaps_identified',
    'Number of strategic gaps identified'
)


def generate_metrics():
    """Generate Prometheus metrics"""
    try:
        return generate_latest()
    except Exception as e:
        logger.error("Failed to generate metrics", error=str(e))
        raise


def record_request(method: str, endpoint: str, status_code: int, duration: float):
    """Record request metrics"""
    try:
        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            status=status_code
        ).inc()
        
        REQUEST_DURATION.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)
        
    except Exception as e:
        logger.error("Failed to record request metrics", error=str(e))


def record_ai_request(ai_system: str, task_type: str, status: str, duration: float):
    """Record AI system request metrics"""
    try:
        AI_REQUESTS.labels(
            ai_system=ai_system,
            task_type=task_type,
            status=status
        ).inc()
        
        AI_RESPONSE_TIME.labels(
            ai_system=ai_system,
            task_type=task_type
        ).observe(duration)
        
    except Exception as e:
        logger.error("Failed to record AI request metrics", error=str(e))


def record_orchestration_session(active_sessions: int):
    """Record orchestration session metrics"""
    try:
        ORCHESTRATION_SESSIONS.set(active_sessions)
    except Exception as e:
        logger.error("Failed to record orchestration session metrics", error=str(e))


def record_orchestration_task(task_type: str, status: str):
    """Record orchestration task metrics"""
    try:
        ORCHESTRATION_TASKS.labels(
            task_type=task_type,
            status=status
        ).inc()
    except Exception as e:
        logger.error("Failed to record orchestration task metrics", error=str(e))


def record_brick_analysis():
    """Record BRICK analysis metrics"""
    try:
        BRICK_ANALYSES.inc()
    except Exception as e:
        logger.error("Failed to record BRICK analysis metrics", error=str(e))


def record_revenue_opportunities(count: int):
    """Record revenue opportunities metrics"""
    try:
        REVENUE_OPPORTUNITIES.set(count)
    except Exception as e:
        logger.error("Failed to record revenue opportunities metrics", error=str(e))


def record_strategic_gaps(count: int):
    """Record strategic gaps metrics"""
    try:
        STRATEGIC_GAPS.set(count)
    except Exception as e:
        logger.error("Failed to record strategic gaps metrics", error=str(e))
