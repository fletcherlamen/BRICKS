"""
Tests for I ASSESS BRICK endpoints
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import tempfile
import os


class TestAssessEndpoints:
    """Test I ASSESS BRICK API endpoints."""
    
    def test_health_endpoint(self, client: TestClient):
        """Test health endpoint returns 200."""
        response = client.get("/api/v1/ubic/assess/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_capabilities_endpoint(self, client: TestClient):
        """Test capabilities endpoint returns assess operations."""
        response = client.get("/api/v1/ubic/assess/capabilities")
        assert response.status_code == 200
        data = response.json()
        assert "assess_operations" in data
        assert "audit_repository" in data["assess_operations"]
        assert "check_ubic_compliance" in data["assess_operations"]
        assert "run_tests" in data["assess_operations"]
        assert "ai_code_review" in data["assess_operations"]
    
    def test_state_endpoint(self, client: TestClient):
        """Test state endpoint returns assess statistics."""
        response = client.get("/api/v1/ubic/assess/state")
        assert response.status_code == 200
        data = response.json()
        assert "active_audits" in data
        assert "completed_audits" in data
        assert "average_score" in data
    
    def test_dependencies_endpoint(self, client: TestClient):
        """Test dependencies endpoint returns service status."""
        response = client.get("/api/v1/ubic/assess/dependencies")
        assert response.status_code == 200
        data = response.json()
        assert "anthropic" in data
        assert "i_memory" in data
        assert "git" in data
        assert "pytest" in data
    
    @patch('app.services.assess_service.check_ubic_compliance')
    @patch('app.services.assess_service.run_tests')
    @patch('app.services.assess_service.ai_code_review')
    @patch('app.services.assess_service.calculate_payment_recommendation')
    def test_start_audit_endpoint(self, mock_payment, mock_ai_review, mock_tests, mock_ubic, client: TestClient, sample_audit_data):
        """Test start audit endpoint."""
        # Mock service responses
        mock_ubic.return_value = {
            "total_required": 9,
            "found": 8,
            "missing": ["/emergency-stop"],
            "compliant": False,
            "compliance_percent": 88.9
        }
        
        mock_tests.return_value = {
            "tests_passed": True,
            "coverage_percent": 85.5,
            "tests_run": 25,
            "meets_80_threshold": True
        }
        
        mock_ai_review.return_value = {
            "quality_score": 8,
            "production_ready": True,
            "ai_analysis": "Code quality is good",
            "findings": ["Minor issues found"],
            "recommendations": ["Add more tests"]
        }
        
        mock_payment.return_value = {
            "total_score": 85,
            "max_score": 100,
            "percentage": 85.0,
            "recommendation": "APPROVE_PARTIAL_PAYMENT",
            "action": "Approve with minor fixes",
            "confidence": "high"
        }
        
        response = client.post(
            "/api/v1/audit/start",
            json=sample_audit_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "audit_id" in data
        assert data["audit_status"] == "queued"
        assert data["repository"] == sample_audit_data["repository"]
        assert data["user_id"] == sample_audit_data["user_id"]
    
    def test_start_audit_validation(self, client: TestClient):
        """Test start audit endpoint validation."""
        # Test missing required fields
        response = client.post("/api/v1/audit/start", json={})
        assert response.status_code == 422
        
        # Test invalid repository URL
        response = client.post(
            "/api/v1/audit/start",
            json={
                "repository": "not-a-valid-url",
                "user_id": "test@example.com",
                "criteria": ["UBIC_compliance"]
            }
        )
        assert response.status_code == 422
    
    def test_get_audit_endpoint(self, client: TestClient):
        """Test get audit results endpoint."""
        # First create an audit
        audit_data = {
            "repository": "https://github.com/test/repo",
            "user_id": "test@example.com",
            "criteria": ["UBIC_compliance", "test_coverage"]
        }
        
        create_response = client.post("/api/v1/audit/start", json=audit_data)
        assert create_response.status_code == 200
        audit_id = create_response.json()["audit_id"]
        
        # Then get the audit
        response = client.get(f"/api/v1/audit/{audit_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "audit" in data
        assert data["audit"]["audit_id"] == audit_id
    
    def test_get_audit_not_found(self, client: TestClient):
        """Test get audit with non-existent ID."""
        response = client.get("/api/v1/audit/non-existent-id")
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_explain_audit_endpoint(self, client: TestClient):
        """Test explain audit endpoint."""
        # First create an audit
        audit_data = {
            "repository": "https://github.com/test/repo",
            "user_id": "test@example.com",
            "criteria": ["UBIC_compliance"]
        }
        
        create_response = client.post("/api/v1/audit/start", json=audit_data)
        audit_id = create_response.json()["audit_id"]
        
        # Then explain the audit
        response = client.post(
            f"/api/v1/audit/{audit_id}/explain",
            json={"question": "What is the overall quality score?"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "explanation" in data
    
    def test_get_user_audits_endpoint(self, client: TestClient):
        """Test get user audits endpoint."""
        response = client.get(
            "/api/v1/audit/user/test@example.com"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "audits" in data
    
    def test_rerun_audit_endpoint(self, client: TestClient):
        """Test rerun audit endpoint."""
        # First create an audit
        audit_data = {
            "repository": "https://github.com/test/repo",
            "user_id": "test@example.com",
            "criteria": ["UBIC_compliance"]
        }
        
        create_response = client.post("/api/v1/audit/start", json=audit_data)
        audit_id = create_response.json()["audit_id"]
        
        # Then rerun the audit
        response = client.post(f"/api/v1/audit/{audit_id}/rerun")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "new_audit_id" in data
    
    def test_ubic_compliance_check(self, client: TestClient):
        """Test UBIC compliance check functionality."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a mock repository structure
            os.makedirs(os.path.join(temp_dir, "app"))
            
            # Create a mock FastAPI app file
            app_file = os.path.join(temp_dir, "app", "main.py")
            with open(app_file, "w") as f:
                f.write("""
from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/capabilities")
def capabilities():
    return {"capabilities": []}

@app.get("/state")
def state():
    return {"state": "running"}

@app.get("/dependencies")
def dependencies():
    return {"dependencies": []}

@app.post("/message")
def message():
    return {"status": "received"}

@app.post("/send")
def send():
    return {"status": "sent"}

@app.post("/reload-config")
def reload_config():
    return {"status": "reloaded"}

@app.post("/shutdown")
def shutdown():
    return {"status": "shutdown"}

@app.post("/emergency-stop")
def emergency_stop():
    return {"status": "stopped"}
""")
            
            # Test UBIC compliance check
            response = client.post(
                "/api/v1/ubic/assess/check-ubic",
                json={"repository_path": temp_dir}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "compliance" in data
            assert data["compliance"]["total_required"] == 9
            assert data["compliance"]["found"] == 9
            assert data["compliance"]["compliant"] is True
    
    def test_ubic_message_endpoint(self, client: TestClient):
        """Test UBIC message endpoint."""
        message_data = {
            "idempotency_key": "assess-test-123",
            "priority": "normal",
            "source": "I_CHAT",
            "target": "I_ASSESS",
            "message_type": "AUDIT_REQUEST",
            "payload": {
                "repository": "https://github.com/test/repo",
                "user_id": "test@example.com",
                "criteria": ["UBIC_compliance"]
            },
            "trace_id": "trace-assess-123"
        }
        
        response = client.post(
            "/api/v1/ubic/assess/message",
            json=message_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_ubic_send_endpoint(self, client: TestClient):
        """Test UBIC send endpoint."""
        message_data = {
            "idempotency_key": "assess-send-456",
            "priority": "high",
            "source": "I_MEMORY",
            "target": "I_ASSESS",
            "message_type": "AUDIT_RESULT",
            "payload": {
                "audit_id": "test-audit-456",
                "results": {"score": 85, "recommendation": "APPROVE"}
            },
            "trace_id": "trace-send-456"
        }
        
        response = client.post(
            "/api/v1/ubic/assess/send",
            json=message_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
