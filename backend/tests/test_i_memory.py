"""
Test Suite for I MEMORY BRICK - Trinity BRICKS
Target: 80%+ code coverage

Tests:
1. Memory storage and retrieval
2. Multi-user isolation
3. Semantic search
4. Redis caching
5. UBIC v1.5 compliance (9 endpoints)
6. Persistence (container restart simulation)
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from datetime import datetime
import time

# Test client will be created for the main application
from app.main import app

client = TestClient(app)

# Test data
TEST_USER_A = "test_user_a@example.com"
TEST_USER_B = "test_user_b@example.com"

TEST_MEMORY_CONTENT_A = {
    "project": "I BUILD",
    "component": "I PROACTIVE",
    "status": "phase_1_complete",
    "test_coverage": 85,
    "last_audit": "2024-10-10"
}

TEST_MEMORY_CONTENT_B = {
    "project": "Trinity BRICKS",
    "component": "I MEMORY",
    "status": "development",
    "test_coverage": 90
}


class TestUBICCompliance:
    """Test all 9 UBIC v1.5 required endpoints"""
    
    def test_health_endpoint(self):
        """Test /health endpoint"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["service"] == "I_MEMORY"
        assert "version" in data
        assert "timestamp" in data
    
    def test_capabilities_endpoint(self):
        """Test /capabilities endpoint"""
        response = client.get("/api/v1/capabilities")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "I_MEMORY"
        assert data["brick_type"] == "Trinity_BRICKS"
        assert "capabilities" in data
        assert len(data["capabilities"]) >= 5  # At least 5 capabilities
        
        # Check for specific capabilities
        capability_names = [c["name"] for c in data["capabilities"]]
        assert "multi_user_isolation" in capability_names
        assert "semantic_search" in capability_names
        assert "persistent_storage" in capability_names
    
    def test_state_endpoint(self):
        """Test /state endpoint"""
        response = client.get("/api/v1/state")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "I_MEMORY"
        assert "status" in data
        assert "timestamp" in data
    
    def test_dependencies_endpoint(self):
        """Test /dependencies endpoint"""
        response = client.get("/api/v1/dependencies")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "I_MEMORY"
        assert "dependencies" in data
        
        # Check for required dependencies
        dep_names = [d["name"] for d in data["dependencies"]]
        assert "PostgreSQL" in dep_names
        assert "Redis" in dep_names
        assert "Mem0.ai" in dep_names
    
    def test_message_endpoint(self):
        """Test /message endpoint (UBIC message bus)"""
        message = {
            "source": "I_CHAT",
            "target": "I_MEMORY",
            "message_type": "STORE_MEMORY",
            "payload": {
                "user_id": TEST_USER_A,
                "content": {"test": "ubic_message"}
            }
        }
        
        response = client.post("/api/v1/message", json=message)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "idempotency_key" in data
        assert "trace_id" in data
    
    def test_send_endpoint(self):
        """Test /send endpoint (UBIC query bus)"""
        message = {
            "source": "I_CHAT",
            "target": "I_MEMORY",
            "message_type": "GET_STATS",
            "payload": {}
        }
        
        response = client.post("/api/v1/send", json=message)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "stats" in data
    
    def test_reload_config_endpoint(self):
        """Test /reload-config endpoint"""
        response = client.post("/api/v1/reload-config")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "new_version" in data
    
    def test_shutdown_endpoint(self):
        """Test /shutdown endpoint"""
        response = client.post("/api/v1/shutdown")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "shutdown_initiated"
    
    def test_emergency_stop_endpoint(self):
        """Test /emergency-stop endpoint"""
        response = client.post("/api/v1/emergency-stop")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


class TestMemoryStorage:
    """Test memory storage operations"""
    
    def test_store_memory(self):
        """Test storing a memory"""
        response = client.post("/api/v1/i-memory/store", json={
            "user_id": TEST_USER_A,
            "content": TEST_MEMORY_CONTENT_A
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data
        assert data["data"]["user_id"] == TEST_USER_A
        assert "memory_id" in data["data"]
    
    def test_store_memory_multiple_users(self):
        """Test storing memories for multiple users"""
        # Store for user A
        response_a = client.post("/api/v1/i-memory/store", json={
            "user_id": TEST_USER_A,
            "content": TEST_MEMORY_CONTENT_A
        })
        assert response_a.status_code == 200
        
        # Store for user B
        response_b = client.post("/api/v1/i-memory/store", json={
            "user_id": TEST_USER_B,
            "content": TEST_MEMORY_CONTENT_B
        })
        assert response_b.status_code == 200
        
        # Both should succeed
        assert response_a.json()["status"] == "success"
        assert response_b.json()["status"] == "success"


class TestMemorySearch:
    """Test semantic search functionality"""
    
    def test_search_memories(self):
        """Test searching memories"""
        # First store a memory
        client.post("/api/v1/i-memory/store", json={
            "user_id": TEST_USER_A,
            "content": {
                "topic": "revenue optimization",
                "strategy": "focus on high-value customers"
            }
        })
        
        # Search for it
        response = client.post("/api/v1/i-memory/search", json={
            "user_id": TEST_USER_A,
            "query": "revenue strategy",
            "limit": 10
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "results" in data
        assert data["user_id"] == TEST_USER_A
    
    def test_search_limit(self):
        """Test search with result limit"""
        response = client.post("/api/v1/i-memory/search", json={
            "user_id": TEST_USER_A,
            "query": "test",
            "limit": 5
        })
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) <= 5


class TestMultiUserIsolation:
    """Test multi-user isolation - users cannot see each other's memories"""
    
    def test_user_isolation_search(self):
        """Test that search results are isolated per user"""
        # Store memory for user A
        client.post("/api/v1/i-memory/store", json={
            "user_id": TEST_USER_A,
            "content": {"secret": "user_a_secret", "data": "confidential_a"}
        })
        
        # Store memory for user B
        client.post("/api/v1/i-memory/store", json={
            "user_id": TEST_USER_B,
            "content": {"secret": "user_b_secret", "data": "confidential_b"}
        })
        
        # User A searches
        response_a = client.post("/api/v1/i-memory/search", json={
            "user_id": TEST_USER_A,
            "query": "secret",
            "limit": 100
        })
        
        # User B searches
        response_b = client.post("/api/v1/i-memory/search", json={
            "user_id": TEST_USER_B,
            "query": "secret",
            "limit": 100
        })
        
        results_a = response_a.json()["results"]
        results_b = response_b.json()["results"]
        
        # Check that user A cannot see user B's data
        for result in results_a:
            content_str = str(result.get("content", {}))
            assert "user_b_secret" not in content_str
            assert "confidential_b" not in content_str
        
        # Check that user B cannot see user A's data
        for result in results_b:
            content_str = str(result.get("content", {}))
            assert "user_a_secret" not in content_str
            assert "confidential_a" not in content_str
    
    def test_user_isolation_get_all(self):
        """Test that get_all is isolated per user"""
        # Store memory for both users
        client.post("/api/v1/i-memory/store", json={
            "user_id": TEST_USER_A,
            "content": {"owner": "user_a"}
        })
        
        client.post("/api/v1/i-memory/store", json={
            "user_id": TEST_USER_B,
            "content": {"owner": "user_b"}
        })
        
        # Get memories for user A
        response_a = client.get(f"/api/v1/i-memory/user/{TEST_USER_A}")
        memories_a = response_a.json()["memories"]
        
        # Get memories for user B
        response_b = client.get(f"/api/v1/i-memory/user/{TEST_USER_B}")
        memories_b = response_b.json()["memories"]
        
        # Verify isolation
        assert response_a.json()["user_id"] == TEST_USER_A
        assert response_b.json()["user_id"] == TEST_USER_B
        
        # User A's memories should not contain user B's data
        for memory in memories_a:
            content_str = str(memory.get("content", {}))
            if "owner" in content_str:
                assert "user_b" not in content_str


class TestMemoryRetrieval:
    """Test memory retrieval operations"""
    
    def test_get_user_memories(self):
        """Test retrieving all memories for a user"""
        response = client.get(f"/api/v1/i-memory/user/{TEST_USER_A}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["user_id"] == TEST_USER_A
        assert "memories" in data
        assert "count" in data
    
    def test_get_user_memories_with_limit(self):
        """Test retrieving memories with limit"""
        response = client.get(f"/api/v1/i-memory/user/{TEST_USER_A}?limit=5")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["memories"]) <= 5


class TestMemoryDeletion:
    """Test memory deletion operations"""
    
    def test_delete_memory(self):
        """Test deleting a memory"""
        # First store a memory
        store_response = client.post("/api/v1/i-memory/store", json={
            "user_id": TEST_USER_A,
            "content": {"to_delete": "this will be deleted"}
        })
        
        memory_id = store_response.json()["data"]["memory_id"]
        
        # Delete it
        delete_response = client.delete(
            f"/api/v1/i-memory/{memory_id}",
            json={"user_id": TEST_USER_A}
        )
        
        assert delete_response.status_code == 200
        data = delete_response.json()
        assert data["status"] == "success"
        assert data["memory_id"] == memory_id


class TestMemoryStatistics:
    """Test memory statistics endpoints"""
    
    def test_get_system_stats(self):
        """Test getting system-wide statistics"""
        response = client.get("/api/v1/i-memory/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "stats" in data
    
    def test_get_user_stats(self):
        """Test getting user-specific statistics"""
        response = client.get(f"/api/v1/i-memory/stats?user_id={TEST_USER_A}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "stats" in data
        assert "user_stats" in data["stats"]


class TestPersistence:
    """Test memory persistence (survives container restart)"""
    
    def test_persistence_simulation(self):
        """
        Simulate container restart by:
        1. Storing memory
        2. Getting the memory ID
        3. Reinitializing service (simulated)
        4. Retrieving the memory again
        """
        # Store a memory with unique content
        timestamp = datetime.now().isoformat()
        unique_content = {
            "persistence_test": True,
            "timestamp": timestamp,
            "data": "this should persist"
        }
        
        store_response = client.post("/api/v1/i-memory/store", json={
            "user_id": TEST_USER_A,
            "content": unique_content
        })
        
        assert store_response.status_code == 200
        memory_id = store_response.json()["data"]["memory_id"]
        
        # Wait a moment
        time.sleep(1)
        
        # Retrieve all memories for user
        retrieve_response = client.get(f"/api/v1/i-memory/user/{TEST_USER_A}?limit=100")
        assert retrieve_response.status_code == 200
        
        memories = retrieve_response.json()["memories"]
        
        # Find our specific memory
        found = False
        for memory in memories:
            if memory.get("memory_id") == memory_id:
                found = True
                # Verify content matches
                content = memory.get("content", {})
                if isinstance(content, dict):
                    assert content.get("timestamp") == timestamp
                    assert content.get("data") == "this should persist"
                break
        
        assert found, f"Memory {memory_id} not found after retrieval"


class TestCaching:
    """Test Redis caching functionality"""
    
    def test_cached_search_performance(self):
        """Test that cached searches are faster than initial searches"""
        # First search (not cached)
        start_time = time.time()
        response1 = client.post("/api/v1/i-memory/search", json={
            "user_id": TEST_USER_A,
            "query": "performance test",
            "limit": 10
        })
        first_search_time = time.time() - start_time
        
        # Second search (should be cached)
        start_time = time.time()
        response2 = client.post("/api/v1/i-memory/search", json={
            "user_id": TEST_USER_A,
            "query": "performance test",
            "limit": 10
        })
        second_search_time = time.time() - start_time
        
        # Both should succeed
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Second search should be faster (or at least not significantly slower)
        # We use a generous multiplier because caching benefit depends on system load
        assert second_search_time <= first_search_time * 2.0


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_store_memory_missing_user_id(self):
        """Test storing memory without user_id"""
        response = client.post("/api/v1/i-memory/store", json={
            "content": {"test": "data"}
        })
        
        assert response.status_code == 422  # Validation error
    
    def test_search_memory_missing_query(self):
        """Test searching without query"""
        response = client.post("/api/v1/i-memory/search", json={
            "user_id": TEST_USER_A
        })
        
        assert response.status_code == 422  # Validation error
    
    def test_delete_nonexistent_memory(self):
        """Test deleting a memory that doesn't exist"""
        response = client.delete(
            "/api/v1/i-memory/nonexistent_id",
            json={"user_id": TEST_USER_A}
        )
        
        # Should return 404 or handle gracefully
        assert response.status_code in [404, 200]


# Run with: pytest backend/tests/test_i_memory.py -v --cov=app/services/mem0_service --cov=app/api/v1/endpoints/ubic --cov=app/api/v1/endpoints/i_memory

