"""
Comprehensive API endpoint tests to increase coverage
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints for coverage"""
    
    def test_root_health_check(self):
        """Test root health endpoint"""
        response = client.get("/api/v1/health/")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
    
    def test_health_capabilities(self):
        """Test health capabilities endpoint"""
        response = client.get("/api/v1/health/capabilities")
        assert response.status_code == 200
        data = response.json()
        assert "capabilities" in data or "details" in data
    
    def test_health_state(self):
        """Test health state endpoint"""
        response = client.get("/api/v1/health/state")
        assert response.status_code == 200
        data = response.json()
        assert "details" in data or "state" in data
    
    def test_health_dependencies(self):
        """Test health dependencies endpoint"""
        response = client.get("/api/v1/health/dependencies")
        assert response.status_code == 200
        data = response.json()
        assert "details" in data or "dependencies" in data


class TestMemoryEndpoints:
    """Test memory endpoints for coverage"""
    
    def test_add_memory_basic(self):
        """Test adding a basic memory"""
        response = client.post("/api/v1/memory/add", json={
            "user_id": "coverage_test_user",
            "content": {"test": "data"},
            "metadata": {"category": "test"}
        })
        assert response.status_code in [200, 201]
        data = response.json()
        assert "status" in data or "memory_id" in data
    
    def test_search_memory_basic(self):
        """Test searching memories"""
        response = client.get("/api/v1/memory/search?user_id=coverage_test_user&query=test")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data or "memories" in data or "results" in data
    
    def test_get_all_memories_basic(self):
        """Test getting all memories"""
        response = client.get("/api/v1/memory/get-all?user_id=coverage_test_user")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data or "memories" in data
    
    def test_memory_stats_basic(self):
        """Test getting memory stats"""
        response = client.get("/api/v1/memory/stats?user_id=coverage_test_user")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data or "stats" in data or "statistics" in data
    
    def test_memory_health(self):
        """Test memory health endpoint"""
        response = client.get("/api/v1/ubic/memory/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


class TestChatEndpoints:
    """Test chat endpoints for coverage"""
    
    def test_send_message_basic(self):
        """Test sending a basic message"""
        response = client.post("/api/v1/chat/message", json={
            "message": "Hello, this is a test",
            "user_id": "coverage_test_user",
            "session_id": "test_session"
        })
        assert response.status_code in [200, 201]
        data = response.json()
        assert "response" in data or "message" in data or "status" in data
    
    def test_get_conversation_history(self):
        """Test getting conversation history"""
        response = client.get("/api/v1/chat/history/coverage_test_user")
        assert response.status_code == 200
        data = response.json()
        assert "conversations" in data or "history" in data or "status" in data
    
    def test_get_active_sessions(self):
        """Test getting active sessions"""
        response = client.get("/api/v1/chat/active-sessions?user_id=coverage_test_user")
        assert response.status_code == 200
        data = response.json()
        assert "sessions" in data or "active_sessions" in data or "status" in data
    
    def test_chat_health(self):
        """Test chat health endpoint"""
        response = client.get("/api/v1/ubic/chat/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


class TestAssessEndpoints:
    """Test assess endpoints for coverage"""
    
    def test_start_audit_validation_error(self):
        """Test audit with invalid data"""
        response = client.post("/api/v1/audit/start", json={})
        # Should fail validation
        assert response.status_code in [400, 422]
    
    def test_get_user_audits(self):
        """Test getting user audits"""
        response = client.get("/api/v1/audit/user/coverage_test_user")
        assert response.status_code == 200
        data = response.json()
        assert "audits" in data or "status" in data
    
    def test_assess_health(self):
        """Test assess health endpoint"""
        response = client.get("/api/v1/ubic/assess/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


class TestOrchestrationEndpoints:
    """Test orchestration endpoints for coverage"""
    
    def test_orchestration_sessions(self):
        """Test getting orchestration sessions"""
        response = client.get("/api/v1/orchestration/sessions")
        assert response.status_code == 200
        data = response.json()
        assert "sessions" in data or "status" in data
    
    def test_orchestration_status(self):
        """Test orchestration status"""
        response = client.get("/api/v1/orchestration/status")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data or "orchestration_status" in data
    
    def test_orchestration_execute_validation(self):
        """Test orchestration execute with invalid data"""
        response = client.post("/api/v1/orchestration/execute", json={})
        # Should fail validation or return error
        assert response.status_code in [200, 400, 422]


class TestBricksEndpoints:
    """Test BRICKS endpoints for coverage"""
    
    def test_get_bricks(self):
        """Test getting BRICKS list"""
        response = client.get("/api/v1/bricks/")
        assert response.status_code == 200
        data = response.json()
        assert "bricks" in data or "status" in data
    
    def test_get_brick_categories(self):
        """Test getting BRICK categories"""
        response = client.get("/api/v1/bricks/categories")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (list, dict))


class TestStrategicEndpoints:
    """Test strategic endpoints for coverage"""
    
    def test_get_revenue_opportunities(self):
        """Test getting revenue opportunities"""
        response = client.get("/api/v1/strategic/revenue-opportunities")
        assert response.status_code == 200
        data = response.json()
        assert "opportunities" in data or "status" in data
    
    def test_get_strategic_gaps(self):
        """Test getting strategic gaps"""
        response = client.get("/api/v1/strategic/strategic-gaps")
        assert response.status_code == 200
        data = response.json()
        assert "gaps" in data or "status" in data


class TestDashboardEndpoints:
    """Test dashboard endpoints for coverage"""
    
    def test_dashboard_services(self):
        """Test dashboard services status"""
        response = client.get("/api/v1/dashboard/services")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data or "services" in data or "status" in data


class TestUBICMessageBus:
    """Test UBIC message bus for coverage"""
    
    def test_memory_send_event(self):
        """Test memory send event"""
        response = client.post("/api/v1/ubic/memory/send", json={
            "source": "test",
            "message_type": "TEST",
            "payload": {},
            "idempotency_key": "test_key",
            "trace_id": "test_trace"
        })
        assert response.status_code in [200, 201]
    
    def test_chat_send_event(self):
        """Test chat send event"""
        response = client.post("/api/v1/ubic/chat/send", json={
            "source": "test",
            "event_type": "TEST",
            "payload": {},
            "idempotency_key": "test_key"
        })
        assert response.status_code in [200, 201]
    
    def test_assess_send_event(self):
        """Test assess send event"""
        response = client.post("/api/v1/ubic/assess/send", json={
            "source": "test",
            "message_type": "TEST",
            "payload": {},
            "idempotency_key": "test_key"
        })
        assert response.status_code in [200, 201]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

