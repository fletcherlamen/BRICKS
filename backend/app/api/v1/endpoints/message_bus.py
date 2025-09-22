"""
UBIC v1.5 Message Bus API Endpoints
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Depends, status
import structlog
from datetime import datetime, timedelta
import uuid
import json

from app.models.ubic import (
    UBICResponse, UBICMessage, Priority, Status, EmergenceSignal,
    RateLimitInfo
)

logger = structlog.get_logger(__name__)
router = APIRouter()

# In-memory message storage (in production, use Redis or database)
_message_queue = {
    Priority.LOW: [],
    Priority.NORMAL: [],
    Priority.HIGH: [],
    Priority.EMERGENCY: []
}

_dead_letter_queue = []
_processed_messages = set()  # Track processed idempotency keys
_message_retention_days = 7


def _cleanup_old_messages():
    """Clean up messages older than retention period"""
    cutoff_date = datetime.utcnow() - timedelta(days=_message_retention_days)
    
    for priority in _message_queue:
        _message_queue[priority] = [
            msg for msg in _message_queue[priority]
            if msg.get('timestamp', datetime.utcnow()) > cutoff_date
        ]
    
    _dead_letter_queue[:] = [
        msg for msg in _dead_letter_queue
        if msg.get('timestamp', datetime.utcnow()) > cutoff_date
    ]


def _is_idempotent(message: UBICMessage) -> bool:
    """Check if message is idempotent (already processed)"""
    return message.idempotency_key in _processed_messages


def _add_to_queue(message: UBICMessage) -> str:
    """Add message to appropriate priority queue"""
    global _message_queue
    
    message_data = {
        'idempotency_key': message.idempotency_key,
        'priority': message.priority,
        'source': message.source,
        'target': message.target,
        'message_type': message.message_type,
        'payload': message.payload,
        'trace_id': message.trace_id,
        'emergence': message.emergence.dict() if message.emergence else None,
        'timestamp': datetime.utcnow(),
        'status': 'queued'
    }
    
    # Add to appropriate priority queue
    _message_queue[message.priority].append(message_data)
    
    # Mark as processed for idempotency
    _processed_messages.add(message.idempotency_key)
    
    return message.idempotency_key


@router.post("/message", response_model=UBICResponse)
async def accept_message(message: UBICMessage):
    """UBIC v1.5 Required Message Endpoint - Accepts messages with idempotency & priority"""
    try:
        # Clean up old messages
        _cleanup_old_messages()
        
        # Check idempotency
        if _is_idempotent(message):
            return UBICResponse(
                status=Status.SUCCESS,
                message="Message already processed (idempotent)",
                details={
                    "idempotency_key": message.idempotency_key,
                    "status": "duplicate"
                }
            )
        
        # Validate message
        if not message.source or not message.target:
            return UBICResponse(
                status=Status.ERROR,
                error_code="INVALID_MESSAGE",
                message="Source and target are required",
                details={"source": message.source, "target": message.target}
            )
        
        # Check emergence signals
        emergence_detected = False
        if message.emergence and message.emergence.signal:
            emergence_detected = True
            logger.warning(
                "Emergence signal detected",
                idempotency_key=message.idempotency_key,
                emergence_type=message.emergence.type,
                confidence=message.emergence.confidence,
                threshold_metrics=message.emergence.threshold_metrics
            )
        
        # Add to queue
        message_id = _add_to_queue(message)
        
        # Log message processing
        logger.info(
            "Message accepted",
            idempotency_key=message_id,
            priority=message.priority,
            source=message.source,
            target=message.target,
            message_type=message.message_type,
            trace_id=message.trace_id,
            emergence_detected=emergence_detected
        )
        
        return UBICResponse(
            status=Status.SUCCESS,
            message="Message accepted successfully",
            details={
                "idempotency_key": message_id,
                "priority": message.priority,
                "queue_position": len(_message_queue[message.priority]),
                "emergence_detected": emergence_detected,
                "trace_id": message.trace_id
            }
        )
        
    except Exception as e:
        logger.error("Failed to accept message", error=str(e))
        return UBICResponse(
            status=Status.ERROR,
            error_code="MESSAGE_ACCEPT_FAILED",
            message="Failed to accept message",
            details={"error": str(e)}
        )


@router.post("/send", response_model=UBICResponse)
async def send_message(message: UBICMessage):
    """UBIC v1.5 Required Send Endpoint - Sends messages to bus with metadata"""
    try:
        # Clean up old messages
        _cleanup_old_messages()
        
        # Check idempotency
        if _is_idempotent(message):
            return UBICResponse(
                status=Status.SUCCESS,
                message="Message already sent (idempotent)",
                details={
                    "idempotency_key": message.idempotency_key,
                    "status": "duplicate"
                }
            )
        
        # Validate message
        if not message.source or not message.target:
            return UBICResponse(
                status=Status.ERROR,
                error_code="INVALID_MESSAGE",
                message="Source and target are required",
                details={"source": message.source, "target": message.target}
            )
        
        # Add message metadata
        message_metadata = {
            "sent_at": datetime.utcnow().isoformat(),
            "sender_ip": "127.0.0.1",  # Mock value
            "message_size_bytes": len(json.dumps(message.dict())),
            "retry_count": 0
        }
        
        # Add to queue with metadata
        message_data = {
            'idempotency_key': message.idempotency_key,
            'priority': message.priority,
            'source': message.source,
            'target': message.target,
            'message_type': message.message_type,
            'payload': message.payload,
            'trace_id': message.trace_id,
            'emergence': message.emergence.dict() if message.emergence else None,
            'timestamp': datetime.utcnow(),
            'status': 'sent',
            'metadata': message_metadata
        }
        
        _message_queue[message.priority].append(message_data)
        _processed_messages.add(message.idempotency_key)
        
        # Log message sending
        logger.info(
            "Message sent to bus",
            idempotency_key=message.idempotency_key,
            priority=message.priority,
            source=message.source,
            target=message.target,
            message_type=message.message_type,
            trace_id=message.trace_id,
            metadata=message_metadata
        )
        
        return UBICResponse(
            status=Status.SUCCESS,
            message="Message sent to bus successfully",
            details={
                "idempotency_key": message.idempotency_key,
                "priority": message.priority,
                "queue_position": len(_message_queue[message.priority]),
                "metadata": message_metadata,
                "trace_id": message.trace_id
            }
        )
        
    except Exception as e:
        logger.error("Failed to send message", error=str(e))
        return UBICResponse(
            status=Status.ERROR,
            error_code="MESSAGE_SEND_FAILED",
            message="Failed to send message to bus",
            details={"error": str(e)}
        )


@router.get("/queue-status", response_model=UBICResponse)
async def get_queue_status():
    """Get current message queue status"""
    try:
        _cleanup_old_messages()
        
        queue_status = {
            "priority_queues": {
                priority: {
                    "count": len(queue),
                    "oldest_message": queue[0]['timestamp'].isoformat() if queue else None,
                    "newest_message": queue[-1]['timestamp'].isoformat() if queue else None
                }
                for priority, queue in _message_queue.items()
            },
            "dead_letter_queue": {
                "count": len(_dead_letter_queue),
                "oldest_message": _dead_letter_queue[0]['timestamp'].isoformat() if _dead_letter_queue else None
            },
            "processed_messages": len(_processed_messages),
            "retention_days": _message_retention_days,
            "last_cleanup": datetime.utcnow().isoformat()
        }
        
        return UBICResponse(
            status=Status.SUCCESS,
            message="Queue status retrieved successfully",
            details=queue_status
        )
        
    except Exception as e:
        logger.error("Failed to get queue status", error=str(e))
        return UBICResponse(
            status=Status.ERROR,
            error_code="QUEUE_STATUS_FAILED",
            message="Failed to get queue status",
            details={"error": str(e)}
        )


@router.get("/rate-limits", response_model=UBICResponse)
async def get_rate_limits():
    """UBIC v1.5 Required Rate Limits Endpoint - Returns discoverable rate limits"""
    try:
        rate_limits = RateLimitInfo(
            requests_per_minute=60,
            requests_per_hour=1000,
            burst_limit=10,
            current_usage=5,  # Mock value
            reset_time=datetime.utcnow() + timedelta(minutes=1)
        )
        
        return UBICResponse(
            status=Status.SUCCESS,
            message="Rate limits retrieved successfully",
            details=rate_limits.dict()
        )
        
    except Exception as e:
        logger.error("Failed to get rate limits", error=str(e))
        return UBICResponse(
            status=Status.ERROR,
            error_code="RATE_LIMITS_FAILED",
            message="Failed to get rate limits",
            details={"error": str(e)}
        )


@router.post("/emergence-report", response_model=UBICResponse)
async def report_emergence(emergence: EmergenceSignal):
    """Report emergence detection (UBIC v1.5 requirement)"""
    try:
        # Log emergence with flagged but indistinguishable format
        logger.info(
            "Emergence pattern detected",
            signal=emergence.signal,
            emergence_type=emergence.type,
            confidence=emergence.confidence,
            threshold_metrics=emergence.threshold_metrics,
            timestamp=datetime.utcnow().isoformat()
        )
        
        # Store emergence data for analysis
        emergence_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "signal": emergence.signal,
            "type": emergence.type,
            "confidence": emergence.confidence,
            "threshold_metrics": emergence.threshold_metrics
        }
        
        return UBICResponse(
            status=Status.SUCCESS,
            message="Emergence reported successfully",
            details=emergence_data
        )
        
    except Exception as e:
        logger.error("Failed to report emergence", error=str(e))
        return UBICResponse(
            status=Status.ERROR,
            error_code="EMERGENCE_REPORT_FAILED",
            message="Failed to report emergence",
            details={"error": str(e)}
        )
