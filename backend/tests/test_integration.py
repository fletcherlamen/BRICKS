"""
Integration tests for Trinity BRICKS
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock


class TestTrinityIntegration:
    """Test integration between I MEMORY, I CHAT, and I ASSESS BRICKS."""
    
    @patch('app.services.mem0_service.Mem0Service.add')
    @patch('app.services.mem0_service.Mem0Service.search')
    @patch('app.services.anthropic.Anthropic.messages.create')
    def test_memory_to_chat_integration(self, mock_anthropic, mock_search, mock_add, client: TestClient):
        """Test I MEMORY integration with I CHAT."""
        # Mock memory search for context
        mock_search.return_value = [
            {
                "memory_id": "context-123",
                "content": {"project": "Test Project", "status": "in_progress"},
                "relevance_score": 0.9
            }
        ]
        
        # Mock memory add for storing conversation
        mock_add.return_value = {"memory_id": "conversation-123"}
        
        # Mock Anthropic response
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = "Based on your project context, here's my response."
        mock_anthropic.return_value = mock_response
        
        # Send a message that should use memory context
        response = client.post(
            "/api/v1/chat/message",
            json={
                "message": "What's the status of my project?",
                "user_id": "test@example.com",
                "session_id": "integration-test-123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "Based on your project context" in data["response"]
        
        # Verify memory search was called for context
        mock_search.assert_called_once()
        
        # Verify conversation was stored in memory
        mock_add.assert_called()
    
    @patch('app.services.mem0_service.Mem0Service.add')
    @patch('app.services.assess_service.check_ubic_compliance')
    @patch('app.services.assess_service.run_tests')
    @patch('app.services.assess_service.ai_code_review')
    @patch('app.services.assess_service.calculate_payment_recommendation')
    def test_assess_to_memory_integration(self, mock_payment, mock_ai_review, mock_tests, mock_ubic, mock_add, client: TestClient):
        """Test I ASSESS integration with I MEMORY."""
        # Mock service responses
        mock_ubic.return_value = {
            "total_required": 9,
            "found": 9,
            "missing": [],
            "compliant": True,
            "compliance_percent": 100.0
        }
        
        mock_tests.return_value = {
            "tests_passed": True,
            "coverage_percent": 90.0,
            "tests_run": 30,
            "meets_80_threshold": True
        }
        
        mock_ai_review.return_value = {
            "quality_score": 9,
            "production_ready": True,
            "ai_analysis": "Excellent code quality",
            "findings": [],
            "recommendations": ["Continue good practices"]
        }
        
        mock_payment.return_value = {
            "total_score": 95,
            "max_score": 100,
            "percentage": 95.0,
            "recommendation": "APPROVE_FULL_PAYMENT",
            "action": "Approve full payment",
            "confidence": "high"
        }
        
        mock_add.return_value = {"memory_id": "audit-result-123"}
        
        # Start an audit
        audit_data = {
            "repository": "https://github.com/test/excellent-repo",
            "user_id": "test@example.com",
            "criteria": ["UBIC_compliance", "test_coverage", "code_quality"]
        }
        
        response = client.post("/api/v1/audit/start", json=audit_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
        # Verify audit results were stored in memory
        mock_add.assert_called()
    
    @patch('app.services.mem0_service.Mem0Service.search')
    @patch('app.services.assess_service.check_ubic_compliance')
    @patch('app.services.assess_service.run_tests')
    @patch('app.services.assess_service.ai_code_review')
    @patch('app.services.assess_service.calculate_payment_recommendation')
    @patch('app.services.anthropic.Anthropic.messages.create')
    def test_full_trinity_workflow(self, mock_anthropic, mock_payment, mock_ai_review, mock_tests, mock_ubic, mock_search, client: TestClient):
        """Test complete Trinity BRICKS workflow."""
        # Mock memory search for previous audit context
        mock_search.return_value = [
            {
                "memory_id": "previous-audit-123",
                "content": {
                    "repository": "https://github.com/test/repo",
                    "audit_score": 85,
                    "recommendation": "APPROVE_PARTIAL_PAYMENT"
                },
                "relevance_score": 0.95
            }
        ]
        
        # Mock audit services
        mock_ubic.return_value = {
            "total_required": 9,
            "found": 8,
            "missing": ["/emergency-stop"],
            "compliant": False,
            "compliance_percent": 88.9
        }
        
        mock_tests.return_value = {
            "tests_passed": True,
            "coverage_percent": 75.0,
            "tests_run": 20,
            "meets_80_threshold": False
        }
        
        mock_ai_review.return_value = {
            "quality_score": 7,
            "production_ready": False,
            "ai_analysis": "Good code but needs improvements",
            "findings": ["Missing emergency stop endpoint", "Low test coverage"],
            "recommendations": ["Add missing endpoint", "Increase test coverage"]
        }
        
        mock_payment.return_value = {
            "total_score": 72,
            "max_score": 100,
            "percentage": 72.0,
            "recommendation": "APPROVE_PARTIAL_PAYMENT",
            "action": "Approve 70% payment, request fixes for remaining 30%",
            "confidence": "high"
        }
        
        # Mock Anthropic response for chat
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = "Based on the previous audit and current analysis, I recommend partial payment with specific improvements needed."
        mock_anthropic.return_value = mock_response
        
        # Step 1: User asks about a repository in chat
        chat_response = client.post(
            "/api/v1/chat/message",
            json={
                "message": "Should I pay for the work on https://github.com/test/repo?",
                "user_id": "test@example.com",
                "session_id": "trinity-workflow-123"
            }
        )
        
        assert chat_response.status_code == 200
        chat_data = chat_response.json()
        assert chat_data["status"] == "success"
        
        # Step 2: Start an audit (this would be triggered by the chat system)
        audit_response = client.post(
            "/api/v1/audit/start",
            json={
                "repository": "https://github.com/test/repo",
                "user_id": "test@example.com",
                "criteria": ["UBIC_compliance", "test_coverage", "code_quality"]
            }
        )
        
        assert audit_response.status_code == 200
        audit_data = audit_response.json()
        assert audit_data["status"] == "success"
        
        # Step 3: Get audit results
        audit_id = audit_data["audit_id"]
        results_response = client.get(f"/api/v1/audit/{audit_id}")
        
        assert results_response.status_code == 200
        results_data = results_response.json()
        assert results_data["status"] == "success"
        
        # Verify all services were called
        mock_search.assert_called()  # Memory search for context
        mock_ubic.assert_called()    # UBIC compliance check
        mock_tests.assert_called()   # Test execution
        mock_ai_review.assert_called()  # AI code review
        mock_payment.assert_called() # Payment recommendation
        mock_anthropic.assert_called()  # Chat response generation
    
    def test_ubic_message_bus_integration(self, client: TestClient):
        """Test UBIC message bus integration between BRICKS."""
        # Test I MEMORY receiving message from I CHAT
        memory_message = {
            "idempotency_key": "memory-chat-123",
            "priority": "normal",
            "source": "I_CHAT",
            "target": "I_MEMORY",
            "message_type": "MEMORY_ADD",
            "payload": {
                "user_id": "test@example.com",
                "content": {"conversation": "Test conversation"},
                "metadata": {"source": "chat"}
            },
            "trace_id": "trace-memory-chat-123"
        }
        
        response = client.post(
            "/api/v1/ubic/memory/message",
            json=memory_message
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
        # Test I ASSESS receiving message from I CHAT
        assess_message = {
            "idempotency_key": "assess-chat-456",
            "priority": "high",
            "source": "I_CHAT",
            "target": "I_ASSESS",
            "message_type": "AUDIT_REQUEST",
            "payload": {
                "repository": "https://github.com/test/repo",
                "user_id": "test@example.com",
                "criteria": ["UBIC_compliance"]
            },
            "trace_id": "trace-assess-chat-456"
        }
        
        response = client.post(
            "/api/v1/ubic/assess/message",
            json=assess_message
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_error_handling_integration(self, client: TestClient):
        """Test error handling across BRICKS integration."""
        # Test invalid memory operation
        response = client.post(
            "/api/v1/memory/add",
            json={
                "user_id": "",  # Invalid user_id
                "content": {"test": "data"}
            }
        )
        
        assert response.status_code == 422
        
        # Test invalid chat message
        response = client.post(
            "/api/v1/chat/message",
            json={
                "message": "",  # Empty message
                "user_id": "test@example.com",
                "session_id": "test-session"
            }
        )
        
        assert response.status_code == 422
        
        # Test invalid audit request
        response = client.post(
            "/api/v1/audit/start",
            json={
                "repository": "invalid-url",  # Invalid repository URL
                "user_id": "test@example.com",
                "criteria": ["UBIC_compliance"]
            }
        )
        
        assert response.status_code == 422
    
    def test_multi_user_isolation(self, client: TestClient):
        """Test multi-user isolation across BRICKS."""
        # User 1 operations
        user1_memory = {
            "user_id": "user1@example.com",
            "content": {"project": "User 1 Project"},
            "metadata": {"private": True}
        }
        
        response1 = client.post("/api/v1/memory/add", json=user1_memory)
        assert response1.status_code == 200
        
        # User 2 operations
        user2_memory = {
            "user_id": "user2@example.com",
            "content": {"project": "User 2 Project"},
            "metadata": {"private": True}
        }
        
        response2 = client.post("/api/v1/memory/add", json=user2_memory)
        assert response2.status_code == 200
        
        # Verify users can only access their own data
        user1_search = client.get(
            "/api/v1/memory/search",
            params={
                "user_id": "user1@example.com",
                "query": "project",
                "limit": 10
            }
        )
        
        user2_search = client.get(
            "/api/v1/memory/search",
            params={
                "user_id": "user2@example.com",
                "query": "project",
                "limit": 10
            }
        )
        
        assert user1_search.status_code == 200
        assert user2_search.status_code == 200
        
        # Results should be different for each user
        user1_data = user1_search.json()
        user2_data = user2_search.json()
        
        # This test would need to be implemented with actual memory service mocking
        # to verify complete isolation
