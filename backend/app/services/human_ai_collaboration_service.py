"""
Human-AI Collaboration Interface Service
Enables human oversight, approval, and feedback for AI decisions
"""

import structlog
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

logger = structlog.get_logger(__name__)


class HumanAICollaborationService:
    """Service for managing human-AI collaboration and approval workflows"""
    
    def __init__(self):
        self.pending_approvals = {}
        self.approval_history = []
        self.collaboration_sessions = {}
        logger.info("Human-AI Collaboration Service initialized")
    
    async def submit_for_approval(
        self,
        decision_type: str,
        ai_recommendation: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
        priority: str = "medium"
    ) -> Dict[str, Any]:
        """Submit an AI recommendation for human approval"""
        try:
            approval_id = f"approval_{int(datetime.now().timestamp()*1000)}_{uuid.uuid4().hex[:8]}"
            
            approval_request = {
                "approval_id": approval_id,
                "decision_type": decision_type,
                "ai_recommendation": ai_recommendation,
                "context": context or {},
                "priority": priority,
                "status": "pending",
                "submitted_at": datetime.now().isoformat(),
                "expires_at": self._calculate_expiry(priority),
                "human_feedback": None,
                "approved": None,
                "reviewed_by": None,
                "reviewed_at": None
            }
            
            self.pending_approvals[approval_id] = approval_request
            
            logger.info("AI recommendation submitted for approval",
                       approval_id=approval_id,
                       decision_type=decision_type,
                       priority=priority)
            
            return {
                "status": "success",
                "approval_id": approval_id,
                "message": "AI recommendation submitted for human review",
                "approval_request": approval_request
            }
        
        except Exception as e:
            logger.error("Failed to submit for approval", error=str(e))
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def get_pending_approvals(
        self,
        decision_type: Optional[str] = None,
        priority: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get pending approval requests"""
        try:
            approvals = list(self.pending_approvals.values())
            
            # Filter by decision type
            if decision_type:
                approvals = [a for a in approvals if a["decision_type"] == decision_type]
            
            # Filter by priority
            if priority:
                approvals = [a for a in approvals if a["priority"] == priority]
            
            # Sort by priority and submission time
            priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            approvals.sort(key=lambda x: (
                priority_order.get(x["priority"], 2),
                x["submitted_at"]
            ))
            
            return {
                "status": "success",
                "pending_approvals": approvals,
                "total_pending": len(approvals),
                "by_priority": {
                    "critical": sum(1 for a in approvals if a["priority"] == "critical"),
                    "high": sum(1 for a in approvals if a["priority"] == "high"),
                    "medium": sum(1 for a in approvals if a["priority"] == "medium"),
                    "low": sum(1 for a in approvals if a["priority"] == "low")
                }
            }
        
        except Exception as e:
            logger.error("Failed to get pending approvals", error=str(e))
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def process_approval(
        self,
        approval_id: str,
        approved: bool,
        feedback: Optional[str] = None,
        reviewed_by: str = "human_reviewer"
    ) -> Dict[str, Any]:
        """Process human approval/rejection of AI recommendation"""
        try:
            if approval_id not in self.pending_approvals:
                return {
                    "status": "error",
                    "message": f"Approval request {approval_id} not found"
                }
            
            approval_request = self.pending_approvals[approval_id]
            
            # Update approval status
            approval_request["status"] = "approved" if approved else "rejected"
            approval_request["approved"] = approved
            approval_request["human_feedback"] = feedback
            approval_request["reviewed_by"] = reviewed_by
            approval_request["reviewed_at"] = datetime.now().isoformat()
            
            # Move to history
            self.approval_history.append(approval_request)
            del self.pending_approvals[approval_id]
            
            logger.info("Approval processed",
                       approval_id=approval_id,
                       approved=approved,
                       reviewed_by=reviewed_by)
            
            return {
                "status": "success",
                "approval_id": approval_id,
                "approved": approved,
                "message": f"Recommendation {'approved' if approved else 'rejected'}",
                "ai_recommendation": approval_request["ai_recommendation"],
                "human_feedback": feedback
            }
        
        except Exception as e:
            logger.error("Failed to process approval", error=str(e))
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def create_collaboration_session(
        self,
        session_name: str,
        participants: List[str],
        topic: str
    ) -> Dict[str, Any]:
        """Create a human-AI collaboration session"""
        try:
            session_id = f"collab_{int(datetime.now().timestamp()*1000)}_{uuid.uuid4().hex[:8]}"
            
            session = {
                "session_id": session_id,
                "session_name": session_name,
                "participants": participants,
                "topic": topic,
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "messages": [],
                "decisions": [],
                "action_items": []
            }
            
            self.collaboration_sessions[session_id] = session
            
            logger.info("Collaboration session created",
                       session_id=session_id,
                       topic=topic)
            
            return {
                "status": "success",
                "session_id": session_id,
                "message": "Collaboration session created",
                "session": session
            }
        
        except Exception as e:
            logger.error("Failed to create collaboration session", error=str(e))
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def add_collaboration_message(
        self,
        session_id: str,
        sender: str,
        message: str,
        sender_type: str = "human"
    ) -> Dict[str, Any]:
        """Add a message to a collaboration session"""
        try:
            if session_id not in self.collaboration_sessions:
                return {
                    "status": "error",
                    "message": f"Collaboration session {session_id} not found"
                }
            
            message_entry = {
                "message_id": f"msg_{int(datetime.now().timestamp()*1000)}",
                "sender": sender,
                "sender_type": sender_type,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
            
            self.collaboration_sessions[session_id]["messages"].append(message_entry)
            
            return {
                "status": "success",
                "message_id": message_entry["message_id"],
                "session_id": session_id
            }
        
        except Exception as e:
            logger.error("Failed to add collaboration message", error=str(e))
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def record_decision(
        self,
        session_id: str,
        decision: str,
        decision_maker: str,
        rationale: Optional[str] = None
    ) -> Dict[str, Any]:
        """Record a decision made in collaboration session"""
        try:
            if session_id not in self.collaboration_sessions:
                return {
                    "status": "error",
                    "message": f"Collaboration session {session_id} not found"
                }
            
            decision_entry = {
                "decision_id": f"decision_{int(datetime.now().timestamp()*1000)}",
                "decision": decision,
                "decision_maker": decision_maker,
                "rationale": rationale,
                "timestamp": datetime.now().isoformat()
            }
            
            self.collaboration_sessions[session_id]["decisions"].append(decision_entry)
            
            return {
                "status": "success",
                "decision_id": decision_entry["decision_id"],
                "session_id": session_id
            }
        
        except Exception as e:
            logger.error("Failed to record decision", error=str(e))
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def get_approval_statistics(self) -> Dict[str, Any]:
        """Get statistics about approval workflows"""
        try:
            total_approvals = len(self.approval_history)
            approved_count = sum(1 for a in self.approval_history if a["approved"])
            rejected_count = total_approvals - approved_count
            
            # Calculate approval rate by decision type
            by_decision_type = {}
            for approval in self.approval_history:
                dt = approval["decision_type"]
                if dt not in by_decision_type:
                    by_decision_type[dt] = {"total": 0, "approved": 0}
                by_decision_type[dt]["total"] += 1
                if approval["approved"]:
                    by_decision_type[dt]["approved"] += 1
            
            # Calculate average response time
            response_times = []
            for approval in self.approval_history:
                if approval.get("reviewed_at") and approval.get("submitted_at"):
                    submitted = datetime.fromisoformat(approval["submitted_at"])
                    reviewed = datetime.fromisoformat(approval["reviewed_at"])
                    response_times.append((reviewed - submitted).total_seconds())
            
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            return {
                "status": "success",
                "total_approvals_processed": total_approvals,
                "approved_count": approved_count,
                "rejected_count": rejected_count,
                "approval_rate": approved_count / total_approvals if total_approvals > 0 else 0,
                "pending_approvals": len(self.pending_approvals),
                "by_decision_type": by_decision_type,
                "avg_response_time_seconds": round(avg_response_time, 2),
                "active_collaboration_sessions": len([
                    s for s in self.collaboration_sessions.values()
                    if s["status"] == "active"
                ])
            }
        
        except Exception as e:
            logger.error("Failed to get approval statistics", error=str(e))
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _calculate_expiry(self, priority: str) -> str:
        """Calculate expiry time based on priority"""
        hours_mapping = {
            "critical": 4,
            "high": 24,
            "medium": 72,
            "low": 168  # 1 week
        }
        
        hours = hours_mapping.get(priority, 72)
        expiry_time = datetime.now() + timedelta(hours=hours)
        return expiry_time.isoformat()
    
    async def get_status(self) -> Dict[str, Any]:
        """Get service status"""
        return {
            "service": "human_ai_collaboration",
            "status": "operational",
            "pending_approvals": len(self.pending_approvals),
            "total_approvals_processed": len(self.approval_history),
            "active_sessions": len([
                s for s in self.collaboration_sessions.values()
                if s["status"] == "active"
            ])
        }


# Import timedelta
from datetime import timedelta
