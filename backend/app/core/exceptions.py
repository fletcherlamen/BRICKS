"""
Custom exceptions for I PROACTIVE BRICK Orchestration Intelligence
"""

from fastapi import HTTPException, status
from typing import Any, Dict, Optional


class BrickOrchestrationException(HTTPException):
    """Base exception for Brick Orchestration system"""
    
    def __init__(
        self,
        detail: str = "Brick Orchestration error",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class AIOrchestrationError(BrickOrchestrationException):
    """Exception for AI orchestration failures"""
    
    def __init__(self, detail: str = "AI orchestration failed"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


class CrewAIError(AIOrchestrationError):
    """Exception for CrewAI integration failures"""
    
    def __init__(self, detail: str = "CrewAI integration failed"):
        super().__init__(detail=f"CrewAI Error: {detail}")


class Mem0Error(AIOrchestrationError):
    """Exception for Mem0.ai integration failures"""
    
    def __init__(self, detail: str = "Mem0.ai integration failed"):
        super().__init__(detail=f"Mem0 Error: {detail}")


class DevinAIError(AIOrchestrationError):
    """Exception for Devin AI integration failures"""
    
    def __init__(self, detail: str = "Devin AI integration failed"):
        super().__init__(detail=f"Devin AI Error: {detail}")


class BusinessSystemError(BrickOrchestrationException):
    """Exception for business system integration failures"""
    
    def __init__(self, detail: str = "Business system integration failed"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_502_BAD_GATEWAY
        )


class ConfigurationError(BrickOrchestrationException):
    """Exception for configuration errors"""
    
    def __init__(self, detail: str = "Configuration error"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class ValidationError(BrickOrchestrationException):
    """Exception for validation errors"""
    
    def __init__(self, detail: str = "Validation error"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


class AuthenticationError(BrickOrchestrationException):
    """Exception for authentication errors"""
    
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class AuthorizationError(BrickOrchestrationException):
    """Exception for authorization errors"""
    
    def __init__(self, detail: str = "Authorization failed"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_403_FORBIDDEN
        )
