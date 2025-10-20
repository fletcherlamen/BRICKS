"""
Comprehensive service tests to increase code coverage
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.services.mem0_service import Mem0Service
from app.services.assess_service import AssessService
from app.core.exceptions import Mem0Error


class TestMem0ServiceCoverage:
    """Test Mem0 service for better coverage"""
    
    @pytest.mark.asyncio
    async def test_mem0_initialization(self):
        """Test Mem0 service initializes correctly"""
        service = Mem0Service()
        await service.initialize()
        assert service.initialized is True
    
    @pytest.mark.asyncio
    async def test_mem0_add_memory_success(self):
        """Test adding memory successfully"""
        service = Mem0Service()
        await service.initialize()
        
        result = await service.add(
            content={"test_key": "test_value"},
            user_id="test_user",
            metadata={"category": "test"}
        )
        assert result is not None
        assert "id" in result or "memory_id" in result
    
    @pytest.mark.asyncio
    async def test_mem0_search_memory(self):
        """Test searching memories"""
        service = Mem0Service()
        await service.initialize()
        
        # Add a memory first
        await service.add(
            content={"topic": "testing"},
            user_id="test_user",
            metadata={"category": "test"}
        )
        
        # Search for it
        results = await service.search(
            query="testing",
            user_id="test_user",
            limit=10
        )
        assert isinstance(results, list)
    
    @pytest.mark.asyncio
    async def test_mem0_get_all_memories(self):
        """Test getting all memories for a user"""
        service = Mem0Service()
        await service.initialize()
        
        results = await service.get_all(
            user_id="test_user",
            limit=100
        )
        assert isinstance(results, list)
    
    @pytest.mark.asyncio
    async def test_mem0_error_handling(self):
        """Test Mem0 error handling"""
        service = Mem0Service()
        
        # Test without initialization
        with pytest.raises(Exception):
            await service.add(
                content={},
                user_id=None,  # Invalid user_id
                metadata={}
            )


class TestAssessServiceCoverage:
    """Test Assess service for better coverage"""
    
    def test_assess_service_creation(self):
        """Test AssessService can be instantiated"""
        service = AssessService()
        assert service is not None
    
    @pytest.mark.asyncio
    async def test_check_ubic_compliance(self):
        """Test UBIC compliance checking"""
        service = AssessService()
        
        # Test with local repository (the current project)
        result = await service.check_ubic_compliance("/app")
        
        assert "compliant" in result
        assert "found" in result
        assert "total_required" in result
        assert result["total_required"] == 9  # 9 required endpoints per BRICK
    
    @pytest.mark.asyncio
    async def test_run_tests_no_framework(self):
        """Test run_tests with no test framework"""
        service = AssessService()
        
        # Create a temp directory with no tests
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            result = await service.run_tests(tmpdir)
            
            assert "tests_passed" in result
            assert "coverage_percent" in result
            assert result["has_test_framework"] is False
    
    def test_payment_recommendation_full_compliance(self):
        """Test payment recommendation with full UBIC compliance"""
        service = AssessService()
        
        audit_results = {
            "ubic": {
                "compliant": True,
                "found": 9,
                "total_required": 9,
                "missing": []
            },
            "tests": {
                "coverage_percent": 85,
                "test_success_rate": 95,
                "meets_80_threshold": True,
                "has_test_framework": True
            },
            "ai_review": {
                "quality_score": 9
            }
        }
        
        result = service.calculate_payment_recommendation(audit_results)
        
        assert "total_score" in result
        assert "recommendation" in result
        assert result["total_score"] >= 80  # Should be high
    
    def test_payment_recommendation_partial_compliance(self):
        """Test payment recommendation with partial compliance"""
        service = AssessService()
        
        audit_results = {
            "ubic": {
                "compliant": False,
                "found": 6,
                "total_required": 9,
                "missing": ["state", "dependencies", "reload"]
            },
            "tests": {
                "coverage_percent": 45,
                "test_success_rate": 70,
                "meets_80_threshold": False,
                "has_test_framework": True
            },
            "ai_review": {
                "quality_score": 6
            }
        }
        
        result = service.calculate_payment_recommendation(audit_results)
        
        assert "total_score" in result
        assert "recommendation" in result
        assert result["total_score"] < 80  # Should be lower
    
    def test_extract_score_various_formats(self):
        """Test score extraction from different text formats"""
        service = AssessService()
        
        # Test decimal score (it rounds to nearest int)
        score1 = service._extract_score("Quality: 8.5/10")
        assert score1 in [8, 9]  # Could round either way
        
        score2 = service._extract_score("Score: 7.2/10")
        assert score2 == 7  # Rounded down
        
        # Test integer score
        assert service._extract_score("score 8 / 10") == 8
        
        # Test default
        assert service._extract_score("No score here") == 7  # Default
    
    def test_extract_list_from_text(self):
        """Test extracting lists from AI response"""
        service = AssessService()
        
        text = """
        Recommendations:
        1. Add more tests
        2. Improve documentation
        3. Fix security issues
        
        Other section:
        - Something else
        """
        
        result = service._extract_list(text, "recommendations")
        assert len(result) >= 3
        assert "Add more tests" in result[0]
    
    def test_generate_reasoning(self):
        """Test payment reasoning generation"""
        service = AssessService()
        
        audit_results = {
            "ubic": {
                "compliant": True,
                "found": 9,
                "missing": []
            },
            "tests": {
                "coverage_percent": 82,
                "test_success_rate": 90,
                "tests_passed_count": 90,
                "tests_run": 100
            },
            "ai_review": {
                "quality_score": 8
            }
        }
        
        breakdown = {
            "ubic": 40,
            "ai_quality": 24,
            "coverage": 20,
            "tests_pass": 9
        }
        
        reasoning = service._generate_reasoning(audit_results, 93, breakdown)
        
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0
        assert "✅" in reasoning or "⚠️" in reasoning or "❌" in reasoning


class TestCacheModule:
    """Test cache module exists"""
    
    def test_cache_module_exists(self):
        """Test cache module can be imported"""
        try:
            from app.core import cache
            assert cache is not None
        except ImportError:
            pytest.skip("Cache module not available")


class TestMetricsModule:
    """Test metrics module exists"""
    
    def test_metrics_module_exists(self):
        """Test metrics module can be imported"""
        try:
            from app.core import metrics
            assert metrics is not None
        except ImportError:
            pytest.skip("Metrics module not available")


class TestMultiModelRouter:
    """Test multi-model router for coverage"""
    
    def test_router_import(self):
        """Test router can be imported"""
        from app.services.multi_model_router import MultiModelRouter
        assert MultiModelRouter is not None
    
    def test_router_initialization(self):
        """Test router initializes"""
        from app.services.multi_model_router import MultiModelRouter
        router = MultiModelRouter()
        assert router is not None
        assert hasattr(router, 'route_request')


class TestAIOrchestrator:
    """Test AI orchestrator for coverage"""
    
    def test_orchestrator_import(self):
        """Test orchestrator can be imported"""
        from app.services.ai_orchestrator import AIOrchestrator
        assert AIOrchestrator is not None
    
    @pytest.mark.asyncio
    async def test_orchestrator_initialization(self):
        """Test orchestrator initializes"""
        from app.services.ai_orchestrator import AIOrchestrator
        orchestrator = AIOrchestrator()
        await orchestrator.initialize()
        assert orchestrator.initialized is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

