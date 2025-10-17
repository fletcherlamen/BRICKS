"""
Tests for I MEMORY BRICK endpoints
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock


class TestMemoryEndpoints:
    """Test I MEMORY BRICK API endpoints."""
    
    def test_health_endpoint(self, client: TestClient):
        """Test health endpoint returns 200."""
        response = client.get("/api/v1/ubic/memory/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_capabilities_endpoint(self, client: TestClient):
        """Test capabilities endpoint returns memory operations."""
        response = client.get("/api/v1/ubic/memory/capabilities")
        assert response.status_code == 200
        data = response.json()
        assert "memory_operations" in data
        assert "add" in data["memory_operations"]
        assert "search" in data["memory_operations"]
        assert "get_all" in data["memory_operations"]
    
    def test_state_endpoint(self, client: TestClient):
        """Test state endpoint returns memory statistics."""
        response = client.get("/api/v1/ubic/memory/state")
        assert response.status_code == 200
        data = response.json()
        assert "memory_count" in data
        assert "active_users" in data
        assert "memory_usage_mb" in data
    
    def test_dependencies_endpoint(self, client: TestClient):
        """Test dependencies endpoint returns service status."""
        response = client.get("/api/v1/ubic/memory/dependencies")
        assert response.status_code == 200
        data = response.json()
        assert "mem0" in data
        assert "postgresql" in data
        assert "redis" in data
    
    @patch('app.services.mem0_service.Mem0Service.add')
    def test_add_memory_endpoint(self, mock_add, client: TestClient, sample_memory_data):
        """Test add memory endpoint."""
        mock_add.return_value = {"memory_id": "test-memory-123"}
        
        response = client.post(
            "/api/v1/memory/add",
            json={
                "user_id": "test@example.com",
                "content": sample_memory_data["content"],
                "metadata": sample_memory_data["metadata"]
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "memory_id" in data
        mock_add.assert_called_once()
    
    @patch('app.services.mem0_service.Mem0Service.search')
    def test_search_memory_endpoint(self, mock_search, client: TestClient):
        """Test search memory endpoint."""
        mock_search.return_value = [
            {
                "memory_id": "test-123",
                "content": {"project": "Test Project"},
                "relevance_score": 0.95
            }
        ]
        
        response = client.get(
            "/api/v1/memory/search",
            params={
                "user_id": "test@example.com",
                "query": "test project",
                "limit": 5
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "memories" in data
        assert len(data["memories"]) == 1
        mock_search.assert_called_once()
    
    @patch('app.services.mem0_service.Mem0Service.get_all')
    def test_get_all_memories_endpoint(self, mock_get_all, client: TestClient):
        """Test get all memories endpoint."""
        mock_get_all.return_value = [
            {
                "memory_id": "test-1",
                "content": {"project": "Project 1"},
                "created_at": "2024-01-01T00:00:00Z"
            },
            {
                "memory_id": "test-2", 
                "content": {"project": "Project 2"},
                "created_at": "2024-01-02T00:00:00Z"
            }
        ]
        
        response = client.get(
            "/api/v1/memory/get-all",
            params={"user_id": "test@example.com"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "memories" in data
        assert len(data["memories"]) == 2
        mock_get_all.assert_called_once()
    
    def test_add_memory_validation(self, client: TestClient):
        """Test add memory endpoint validation."""
        # Test missing required fields
        response = client.post("/api/v1/memory/add", json={})
        assert response.status_code == 422
        
        # Test invalid user_id
        response = client.post(
            "/api/v1/memory/add",
            json={
                "user_id": "",  # Empty user_id
                "content": {"test": "data"}
            }
        )
        assert response.status_code == 422
    
    def test_search_memory_validation(self, client: TestClient):
        """Test search memory endpoint validation."""
        # Test missing required parameters
        response = client.get("/api/v1/memory/search")
        assert response.status_code == 422
        
        # Test invalid limit
        response = client.get(
            "/api/v1/memory/search",
            params={
                "user_id": "test@example.com",
                "query": "test",
                "limit": -1  # Invalid limit
            }
        )
        assert response.status_code == 422
    
    @patch('app.services.mem0_service.Mem0Service.delete')
    def test_delete_memory_endpoint(self, mock_delete, client: TestClient):
        """Test delete memory endpoint."""
        mock_delete.return_value = True
        
        response = client.delete(
            "/api/v1/memory/delete",
            params={
                "user_id": "test@example.com",
                "memory_id": "test-memory-123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        mock_delete.assert_called_once()
    
    def test_memory_stats_endpoint(self, client: TestClient):
        """Test memory statistics endpoint."""
        response = client.get("/api/v1/memory/stats")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "stats" in data
        assert "user_stats" in data["stats"]
        assert "system_stats" in data["stats"]
    
    def test_ubic_message_endpoint(self, client: TestClient):
        """Test UBIC message endpoint."""
        message_data = {
            "idempotency_key": "test-123",
            "priority": "normal",
            "source": "I_CHAT",
            "target": "I_MEMORY",
            "message_type": "MEMORY_ADD",
            "payload": {
                "user_id": "test@example.com",
                "content": {"test": "data"}
            },
            "trace_id": "trace-123"
        }
        
        response = client.post(
            "/api/v1/ubic/memory/message",
            json=message_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_ubic_send_endpoint(self, client: TestClient):
        """Test UBIC send endpoint."""
        message_data = {
            "idempotency_key": "test-456",
            "priority": "high",
            "source": "I_ASSESS",
            "target": "I_MEMORY",
            "message_type": "MEMORY_SEARCH",
            "payload": {
                "user_id": "test@example.com",
                "query": "test search"
            },
            "trace_id": "trace-456"
        }
        
        response = client.post(
            "/api/v1/ubic/memory/send",
            json=message_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
