"""
Tests for I CHAT BRICK endpoints
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock


class TestChatEndpoints:
    """Test I CHAT BRICK API endpoints."""
    
    def test_health_endpoint(self, client: TestClient):
        """Test health endpoint returns 200."""
        response = client.get("/api/v1/ubic/chat/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_capabilities_endpoint(self, client: TestClient):
        """Test capabilities endpoint returns chat operations."""
        response = client.get("/api/v1/ubic/chat/capabilities")
        assert response.status_code == 200
        data = response.json()
        assert "capabilities" in data
        assert "service" in data
        assert data["service"] == "I_CHAT"
        assert len(data["capabilities"]) > 0
    
    def test_state_endpoint(self, client: TestClient):
        """Test state endpoint returns chat statistics."""
        response = client.get("/api/v1/ubic/chat/state")
        assert response.status_code == 200
        data = response.json()
        assert "active_sessions" in data
        assert "total_messages" in data
        assert "conversation_count" in data
    
    def test_dependencies_endpoint(self, client: TestClient):
        """Test dependencies endpoint returns service status."""
        response = client.get("/api/v1/ubic/chat/dependencies")
        assert response.status_code == 200
        data = response.json()
        assert "anthropic" in data
        assert "i_memory" in data
        assert "redis" in data
    
    @patch('app.services.anthropic.Anthropic.messages.create')
    @patch('app.services.mem0_service.Mem0Service.search')
    def test_send_message_endpoint(self, mock_search, mock_anthropic, client: TestClient):
        """Test send message endpoint."""
        # Mock memory search
        mock_search.return_value = [
            {
                "memory_id": "test-123",
                "content": {"context": "Previous conversation about testing"},
                "relevance_score": 0.9
            }
        ]
        
        # Mock Anthropic response
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = "This is a test response from Claude."
        mock_anthropic.return_value = mock_response
        
        response = client.post(
            "/api/v1/chat/message",
            json={
                "message": "Hello, can you help me test?",
                "user_id": "test@example.com",
                "session_id": "test-session-123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "response" in data
        assert "session_id" in data
        assert data["response"] == "This is a test response from Claude."
        mock_search.assert_called_once()
        mock_anthropic.assert_called_once()
    
    def test_send_message_validation(self, client: TestClient):
        """Test send message endpoint validation."""
        # Test missing required fields
        response = client.post("/api/v1/chat/message", json={})
        assert response.status_code == 422
        
        # Test empty message
        response = client.post(
            "/api/v1/chat/message",
            json={
                "message": "",
                "user_id": "test@example.com",
                "session_id": "test-session"
            }
        )
        assert response.status_code == 422
    
    @patch('app.services.mem0_service.Mem0Service.add')
    def test_store_conversation_in_memory(self, mock_add, client: TestClient):
        """Test conversation storage in memory."""
        mock_add.return_value = {"memory_id": "conversation-123"}
        
        response = client.post(
            "/api/v1/chat/message",
            json={
                "message": "Test message",
                "user_id": "test@example.com",
                "session_id": "test-session-123"
            }
        )
        
        # Should call memory add to store conversation
        mock_add.assert_called()
    
    def test_get_conversation_history_endpoint(self, client: TestClient):
        """Test get conversation history endpoint."""
        response = client.get(
            "/api/v1/chat/conversation/test-session-123",
            params={"user_id": "test@example.com"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "conversation" in data
    
    def test_get_active_sessions_endpoint(self, client: TestClient):
        """Test get active sessions endpoint."""
        response = client.get(
            "/api/v1/chat/active-sessions",
            params={"user_id": "test@example.com"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "sessions" in data
    
    def test_ubic_message_endpoint(self, client: TestClient):
        """Test UBIC message endpoint."""
        message_data = {
            "idempotency_key": "chat-test-123",
            "priority": "normal",
            "source": "I_MEMORY",
            "target": "I_CHAT",
            "message_type": "CHAT_MESSAGE",
            "payload": {
                "user_id": "test@example.com",
                "message": "Test message via UBIC",
                "session_id": "ubic-session-123"
            },
            "trace_id": "trace-chat-123"
        }
        
        response = client.post(
            "/api/v1/ubic/chat/message",
            json=message_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_ubic_send_endpoint(self, client: TestClient):
        """Test UBIC send endpoint."""
        message_data = {
            "idempotency_key": "chat-send-456",
            "priority": "high",
            "source": "I_ASSESS",
            "target": "I_CHAT",
            "message_type": "CHAT_QUERY",
            "payload": {
                "user_id": "test@example.com",
                "query": "What is the status of the audit?",
                "session_id": "assess-session-456"
            },
            "trace_id": "trace-send-456"
        }
        
        response = client.post(
            "/api/v1/ubic/chat/send",
            json=message_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_reload_config_endpoint(self, client: TestClient):
        """Test reload config endpoint."""
        response = client.post("/api/v1/ubic/chat/reload-config")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "message" in data
    
    def test_shutdown_endpoint(self, client: TestClient):
        """Test shutdown endpoint."""
        response = client.post("/api/v1/ubic/chat/shutdown")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "message" in data
    
    def test_emergency_stop_endpoint(self, client: TestClient):
        """Test emergency stop endpoint."""
        response = client.post("/api/v1/ubic/chat/emergency-stop")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "message" in data
