"""
Tests for core modules (database, logging, exceptions)
"""

import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.core.database import get_db, init_db, Base
from app.core.logging import setup_logging, get_logger
from app.core.exceptions import (
    BrickOrchestrationException, AIOrchestrationError, CrewAIError, Mem0Error,
    DevinAIError, BusinessSystemError, ConfigurationError, ValidationError,
    AuthenticationError, AuthorizationError
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


class TestDatabase:
    """Test database functionality."""
    
    def test_database_imports(self):
        """Test database module imports correctly."""
        from app.core.database import get_db, init_db, Base
        assert get_db is not None
        assert init_db is not None
        assert Base is not None
    
    def test_database_engine_creation(self):
        """Test database engine creation."""
        from app.core.database import create_engine
        engine = create_engine("sqlite:///./test.db", poolclass=StaticPool)
        assert engine is not None
    
    def test_database_session_creation(self):
        """Test database session creation."""
        from app.core.database import create_engine, sessionmaker
        engine = create_engine("sqlite:///./test.db", poolclass=StaticPool)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        assert session is not None
        session.close()


class TestLogging:
    """Test logging functionality."""
    
    def test_logging_imports(self):
        """Test logging module imports correctly."""
        from app.core.logging import setup_logging, get_logger
        assert setup_logging is not None
        assert get_logger is not None
    
    def test_logger_creation(self):
        """Test logger creation."""
        logger = get_logger("test")
        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'warning')
        assert hasattr(logger, 'debug')
    
    def test_logger_binding(self):
        """Test logger binding with context."""
        logger = get_logger("test")
        bound_logger = logger.bind(user_id="test@example.com")
        assert bound_logger is not None
        assert bound_logger._context["user_id"] == "test@example.com"


class TestExceptions:
    """Test custom exceptions."""
    
    def test_base_exception(self):
        """Test base BrickOrchestrationException."""
        error = BrickOrchestrationException("Test error")
        assert error.detail == "Test error"
        assert isinstance(error, Exception)
    
    def test_ai_orchestration_error(self):
        """Test AIOrchestrationError exception."""
        error = AIOrchestrationError("AI operation failed")
        assert "AI operation failed" in error.detail
        assert isinstance(error, BrickOrchestrationException)
    
    def test_mem0_error(self):
        """Test Mem0Error exception."""
        error = Mem0Error("Memory operation failed")
        assert "Mem0 Error: Memory operation failed" in error.detail
        assert isinstance(error, AIOrchestrationError)
    
    def test_crewai_error(self):
        """Test CrewAIError exception."""
        error = CrewAIError("CrewAI operation failed")
        assert "CrewAI Error: CrewAI operation failed" in error.detail
        assert isinstance(error, AIOrchestrationError)
    
    def test_devin_ai_error(self):
        """Test DevinAIError exception."""
        error = DevinAIError("Devin AI operation failed")
        assert "Devin AI Error: Devin AI operation failed" in error.detail
        assert isinstance(error, AIOrchestrationError)
    
    def test_validation_error(self):
        """Test ValidationError exception."""
        error = ValidationError("Invalid input")
        assert error.detail == "Invalid input"
        assert isinstance(error, BrickOrchestrationException)
    
    def test_authentication_error(self):
        """Test AuthenticationError exception."""
        error = AuthenticationError("Authentication failed")
        assert error.detail == "Authentication failed"
        assert isinstance(error, BrickOrchestrationException)
    
    def test_authorization_error(self):
        """Test AuthorizationError exception."""
        error = AuthorizationError("Access denied")
        assert error.detail == "Access denied"
        assert isinstance(error, BrickOrchestrationException)
    
    def test_business_system_error(self):
        """Test BusinessSystemError exception."""
        error = BusinessSystemError("Business system down")
        assert error.detail == "Business system down"
        assert isinstance(error, BrickOrchestrationException)
    
    def test_configuration_error(self):
        """Test ConfigurationError exception."""
        error = ConfigurationError("Invalid configuration")
        assert error.detail == "Invalid configuration"
        assert isinstance(error, BrickOrchestrationException)


class TestModels:
    """Test data models."""
    
    def test_memory_model_import(self):
        """Test Memory model import."""
        from app.models.memory import Memory
        assert Memory is not None
    
    def test_orchestration_model_import(self):
        """Test OrchestrationSession model import."""
        from app.models.orchestration import OrchestrationSession
        assert OrchestrationSession is not None
    
    def test_ubic_model_import(self):
        """Test UBIC model import."""
        from app.models.ubic import UBICMessage
        assert UBICMessage is not None
    
    def test_memory_model_creation(self):
        """Test Memory model creation."""
        from app.models.memory import Memory
        
        memory = Memory(
            user_id="test@example.com",
            content={"test": "data"},
            metadata={"category": "test"}
        )
        
        assert memory.user_id == "test@example.com"
        assert memory.content == {"test": "data"}
        assert memory.metadata == {"category": "test"}
    
    def test_orchestration_model_creation(self):
        """Test OrchestrationSession model creation."""
        from app.models.orchestration import OrchestrationSession
        
        session = OrchestrationSession(
            session_id="test-session-123",
            user_id=1,  # Integer, not string
            status="active",
            goal="Test orchestration",
            context={"test": "result"}
        )
        
        assert session.session_id == "test-session-123"
        assert session.user_id == 1
        assert session.status == "active"
        assert session.goal == "Test orchestration"
        assert session.context == {"test": "result"}
    
    def test_ubic_message_creation(self):
        """Test UBICMessage model creation."""
        from app.models.ubic import UBICMessage
        
        message = UBICMessage(
            idempotency_key="test-123",
            priority="normal",
            source="I_MEMORY",
            target="I_CHAT",
            message_type="TEST_MESSAGE",
            payload={"test": "data"},
            trace_id="trace-123"
        )
        
        assert message.idempotency_key == "test-123"
        assert message.priority == "normal"
        assert message.source == "I_MEMORY"
        assert message.target == "I_CHAT"
        assert message.message_type == "TEST_MESSAGE"
        assert message.payload == {"test": "data"}
        assert message.trace_id == "trace-123"


class TestAPIEndpoints:
    """Test API endpoint imports and basic functionality."""
    
    def test_memory_endpoints_import(self):
        """Test memory endpoints import."""
        from app.api.v1.endpoints import memory
        assert memory is not None
        assert hasattr(memory, 'router')
    
    def test_chat_endpoints_import(self):
        """Test chat endpoints import."""
        from app.api.v1.endpoints import chat
        assert chat is not None
        assert hasattr(chat, 'router')
    
    def test_assess_endpoints_import(self):
        """Test assess endpoints import."""
        from app.api.v1.endpoints import assess
        assert assess is not None
        assert hasattr(assess, 'router')
    
    def test_ubic_endpoints_import(self):
        """Test UBIC endpoints import."""
        from app.api.v1.endpoints import ubic_memory, ubic_chat, ubic_assess
        assert ubic_memory is not None
        assert ubic_chat is not None
        assert ubic_assess is not None
        assert hasattr(ubic_memory, 'router')
        assert hasattr(ubic_chat, 'router')
        assert hasattr(ubic_assess, 'router')


class TestServices:
    """Test service imports."""
    
    def test_mem0_service_import(self):
        """Test Mem0Service import."""
        from app.services.mem0_service import Mem0Service
        assert Mem0Service is not None
    
    def test_assess_service_import(self):
        """Test AssessService import."""
        from app.services.assess_service import AssessService
        assert AssessService is not None
        
        # Test service instantiation
        service = AssessService()
        assert service is not None
        assert hasattr(service, 'start_audit')
        assert hasattr(service, 'check_ubic_compliance')
        assert hasattr(service, 'run_tests')
        assert hasattr(service, 'ai_code_review')
        assert hasattr(service, 'calculate_payment_recommendation')
        assert hasattr(service, 'claude_client')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
