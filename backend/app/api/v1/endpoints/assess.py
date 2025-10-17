"""
Trinity BRICKS I ASSESS - Code Auditing API Endpoints

Provides automated code quality audits with payment recommendations.
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, status, Query, BackgroundTasks
from pydantic import BaseModel, Field
import structlog
from datetime import datetime
import uuid
import json

from app.core.database import AsyncSessionLocal
from app.services.assess_service import AssessService
from sqlalchemy import select, desc

logger = structlog.get_logger(__name__)
router = APIRouter()

# In-memory audit storage (will be moved to database/I MEMORY)
audits_storage = {}


class AuditStartRequest(BaseModel):
    """Request to start a new audit"""
    repository: str = Field(..., description="GitHub repository URL")
    user_id: str = Field(..., description="User identifier")
    criteria: Optional[List[str]] = Field(default=None, description="Audit criteria")


class AuditExplainRequest(BaseModel):
    """Request to explain audit results"""
    question: str = Field(..., description="Question about the audit")


async def perform_audit_task(
    audit_id: str,
    repository: str,
    user_id: str,
    criteria: List[str] = None
):
    """Background task to perform actual audit"""
    assess_service = AssessService()
    repo_path = None
    
    try:
        # Update status
        audits_storage[audit_id]["status"] = "cloning"
        
        # Clone repository
        repo_path = await assess_service.clone_repository(repository)
        
        audits_storage[audit_id]["status"] = "analyzing"
        
        # Run checks
        ubic_results = await assess_service.check_ubic_compliance(repo_path)
        test_results = await assess_service.run_tests(repo_path)
        ai_review = await assess_service.ai_code_review(repo_path, ubic_results, test_results)
        
        # Calculate payment recommendation
        audit_results = {
            "ubic": ubic_results,
            "tests": test_results,
            "ai_review": ai_review
        }
        
        payment_rec = assess_service.calculate_payment_recommendation(audit_results)
        
        # Store complete audit results
        audits_storage[audit_id].update({
            "status": "completed",
            "ubic_compliance": ubic_results,
            "test_results": test_results,
            "ai_review": ai_review,
            "payment_recommendation": payment_rec,
            "completed_at": datetime.now().isoformat()
        })
        
        # Store in I MEMORY
        try:
            from app.services.mem0_service import Mem0Service
            mem0 = Mem0Service()
            await mem0.initialize()
            
            await mem0.add(
                content={
                    "type": "audit_result",
                    "audit_id": audit_id,
                    "repository": repository,
                    "ubic_score": ubic_results["compliance_percent"],
                    "test_coverage": test_results["coverage_percent"],
                    "quality_score": ai_review["quality_score"],
                    "payment_recommendation": payment_rec["recommendation"],
                    "total_score": payment_rec["total_score"]
                },
                user_id=user_id,
                metadata={
                    "category": "audit",
                    "audit_id": audit_id,
                    "brick": "I_ASSESS"
                }
            )
            
            logger.info("Audit stored in I MEMORY",
                       audit_id=audit_id,
                       user_id=user_id)
                       
        except Exception as e:
            logger.warning("Failed to store audit in I MEMORY", error=str(e))
        
        logger.info("Audit completed successfully",
                   audit_id=audit_id,
                   score=payment_rec["total_score"])
        
    except Exception as e:
        logger.error("Audit failed", audit_id=audit_id, error=str(e))
        audits_storage[audit_id].update({
            "status": "failed",
            "error": str(e),
            "completed_at": datetime.now().isoformat()
        })
    
    finally:
        # Cleanup
        if repo_path:
            assess_service.cleanup_repository(repo_path)


@router.post("/start")
async def start_audit(request: AuditStartRequest, background_tasks: BackgroundTasks):
    """
    Start a new code audit
    
    Trinity BRICKS I ASSESS:
    - Clones repository
    - Checks UBIC compliance
    - Runs tests and coverage
    - AI code review
    - Payment recommendation
    """
    try:
        audit_id = f"audit_{uuid.uuid4().hex[:16]}"
        
        # Initialize audit record
        audits_storage[audit_id] = {
            "audit_id": audit_id,
            "repository": request.repository,
            "user_id": request.user_id,
            "status": "queued",
            "started_at": datetime.now().isoformat(),
            "criteria": request.criteria or ["UBIC_compliance", "test_coverage", "code_quality"]
        }
        
        # Schedule background task
        background_tasks.add_task(
            perform_audit_task,
            audit_id,
            request.repository,
            request.user_id,
            request.criteria
        )
        
        logger.info("Audit queued",
                   audit_id=audit_id,
                   repository=request.repository)
        
        return {
            "status": "success",
            "audit_id": audit_id,
            "audit_status": "queued",
            "repository": request.repository,
            "user_id": request.user_id,
            "message": "Audit started. Check /audit/{id} for results.",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to start audit", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start audit: {str(e)}"
        )


@router.get("/{audit_id}")
async def get_audit_results(audit_id: str):
    """
    Get audit results by ID
    
    Trinity BRICKS I ASSESS
    """
    try:
        if audit_id not in audits_storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Audit {audit_id} not found"
            )
        
        audit = audits_storage[audit_id]
        
        return {
            "status": "success",
            "audit": audit,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get audit results", error=str(e), audit_id=audit_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get audit results: {str(e)}"
        )


@router.post("/{audit_id}/explain")
async def explain_audit(audit_id: str, request: AuditExplainRequest):
    """
    Ask questions about audit results using Claude AI
    
    Trinity BRICKS I ASSESS - Conversational Audit Explanations
    """
    try:
        if audit_id not in audits_storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Audit {audit_id} not found"
            )
        
        audit = audits_storage[audit_id]
        
        if audit["status"] != "completed":
            return {
                "status": "pending",
                "message": f"Audit is {audit['status']}. Please wait for completion.",
                "audit_status": audit["status"]
            }
        
        # Use Claude to answer question
        assess_service = AssessService()
        
        if not assess_service.claude_client:
            # Fallback response
            return {
                "status": "success",
                "answer": f"Audit {audit_id} scored {audit.get('payment_recommendation', {}).get('total_score', 0)}/100. {audit.get('payment_recommendation', {}).get('action', 'Review needed.')}",
                "mock": True
            }
        
        try:
            response = assess_service.claude_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": f"""Audit Results:
{json.dumps(audit, indent=2, default=str)}

User Question: {request.question}

Provide a clear, conversational answer based on the audit data."""
                }]
            )
            
            return {
                "status": "success",
                "question": request.question,
                "answer": response.content[0].text,
                "audit_id": audit_id,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error("Claude explain failed", error=str(e))
            # Fallback
            return {
                "status": "success",
                "answer": f"Based on the audit, this repository scored {audit.get('payment_recommendation', {}).get('total_score', 0)}/100. Recommendation: {audit.get('payment_recommendation', {}).get('action', 'Review needed.')}",
                "fallback": True
            }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to explain audit", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to explain audit: {str(e)}"
        )


@router.get("/user/{user_id}")
async def get_user_audits(
    user_id: str,
    limit: int = Query(default=10, ge=1, le=100)
):
    """
    Get audit history for a user
    
    Trinity BRICKS I ASSESS
    """
    try:
        # Filter audits by user
        user_audits = [
            audit for audit in audits_storage.values()
            if audit.get("user_id") == user_id
        ]
        
        # Sort by started_at descending
        user_audits.sort(
            key=lambda x: x.get("started_at", ""),
            reverse=True
        )
        
        return {
            "status": "success",
            "user_id": user_id,
            "audits": user_audits[:limit],
            "total_count": len(user_audits),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get user audits", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user audits: {str(e)}"
        )


@router.post("/{audit_id}/rerun")
async def rerun_audit(audit_id: str, background_tasks: BackgroundTasks):
    """
    Re-run an existing audit
    
    Trinity BRICKS I ASSESS
    """
    try:
        if audit_id not in audits_storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Audit {audit_id} not found"
            )
        
        old_audit = audits_storage[audit_id]
        
        # Create new audit with same parameters
        new_audit_id = f"audit_{uuid.uuid4().hex[:16]}"
        
        audits_storage[new_audit_id] = {
            "audit_id": new_audit_id,
            "repository": old_audit["repository"],
            "user_id": old_audit["user_id"],
            "status": "queued",
            "started_at": datetime.now().isoformat(),
            "rerun_of": audit_id
        }
        
        # Schedule background task
        background_tasks.add_task(
            perform_audit_task,
            new_audit_id,
            old_audit["repository"],
            old_audit["user_id"],
            old_audit.get("criteria")
        )
        
        return {
            "status": "success",
            "new_audit_id": new_audit_id,
            "original_audit_id": audit_id,
            "message": "Audit re-queued",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to rerun audit", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to rerun audit: {str(e)}"
        )

