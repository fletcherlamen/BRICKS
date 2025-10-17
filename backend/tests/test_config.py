"""
Tests for configuration management
"""

import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pydantic import ValidationError
from app.core.config import Settings


class TestSettings:
    """Test configuration settings validation and behavior."""
    
    def test_default_settings(self):
        """Test default settings are properly configured."""
        settings = Settings()
        assert settings.APP_NAME == "I PROACTIVE BRICK Orchestration Intelligence"
        assert settings.APP_VERSION == "1.0.0"
        assert settings.DEBUG is False  # Fixed: Should be False for production
        assert settings.ENVIRONMENT == "production"  # Fixed: Should be production
        assert settings.JWT_ALGORITHM == "HS256"
        assert settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES == 30
    
    def test_security_settings(self):
        """Test security-related settings."""
        settings = Settings()
        assert len(settings.SECRET_KEY) >= 32
        assert len(settings.JWT_SECRET_KEY) >= 32
        assert settings.CORS_ALLOW_ALL_ORIGINS is False  # Fixed: Should be False
        assert settings.MIN_PASSWORD_LENGTH == 8
        assert settings.MAX_LOGIN_ATTEMPTS == 5
        assert settings.LOCKOUT_DURATION_MINUTES == 15
    
    def test_secret_key_validation(self):
        """Test secret key validation."""
        # Test valid secret key
        settings = Settings(SECRET_KEY="valid-secret-key-32-chars-long")
        assert settings.SECRET_KEY == "valid-secret-key-32-chars-long"
        
        # Test invalid secret key (too short)
        with pytest.raises(ValidationError) as exc_info:
            Settings(SECRET_KEY="short")
        assert "SECRET_KEY must be at least 32 characters long" in str(exc_info.value)
        
        # Test invalid secret key (default value)
        with pytest.raises(ValidationError) as exc_info:
            Settings(SECRET_KEY="your-secret-key-change-in-production")
        assert "SECRET_KEY must be changed from default value" in str(exc_info.value)
    
    def test_jwt_secret_key_validation(self):
        """Test JWT secret key validation."""
        # Test valid JWT secret key
        settings = Settings(JWT_SECRET_KEY="valid-jwt-secret-key-32-chars-long")
        assert settings.JWT_SECRET_KEY == "valid-jwt-secret-key-32-chars-long"
        
        # Test invalid JWT secret key (too short)
        with pytest.raises(ValidationError) as exc_info:
            Settings(JWT_SECRET_KEY="short")
        assert "JWT_SECRET_KEY must be at least 32 characters long" in str(exc_info.value)
    
    def test_environment_validation(self):
        """Test environment validation."""
        # Test valid environments
        for env in ["development", "staging", "production"]:
            settings = Settings(ENVIRONMENT=env)
            assert settings.ENVIRONMENT == env
        
        # Test invalid environment
        with pytest.raises(ValidationError) as exc_info:
            Settings(ENVIRONMENT="invalid")
        assert "Environment must be one of" in str(exc_info.value)
    
    def test_cors_origins(self):
        """Test CORS origins configuration."""
        settings = Settings()
        origins = settings.get_cors_origins()
        
        # Should include localhost origins
        assert "http://localhost:3000" in origins
        assert "http://localhost:8000" in origins
        
        # Should include VPS IP origins
        assert f"http://{settings.VPS_IP}:{settings.VPS_FRONTEND_PORT}" in origins
        assert f"http://{settings.VPS_IP}:{settings.VPS_BACKEND_PORT}" in origins
    
    def test_api_key_validation(self):
        """Test API key validation."""
        settings = Settings()
        validation_result = settings.validate_api_keys()
        
        # With test keys, should be valid
        assert validation_result["valid"] is True
        assert validation_result["missing_keys"] == []
        
        # Test with missing keys
        settings_no_keys = Settings(
            ANTHROPIC_API_KEY=None,
            MEM0_API_KEY=None
        )
        validation_result = settings_no_keys.validate_api_keys()
        assert validation_result["valid"] is False
        assert "ANTHROPIC_API_KEY" in validation_result["missing_keys"]
        assert "MEM0_API_KEY" in validation_result["missing_keys"]
    
    def test_database_url_validation(self):
        """Test database URL is properly configured."""
        settings = Settings()
        assert settings.DATABASE_URL.startswith("postgresql://")
        assert "64.227.99.111" in settings.DATABASE_URL
        assert settings.POSTGRES_DB == "brick_orchestration"
    
    def test_redis_url_validation(self):
        """Test Redis URL is properly configured."""
        settings = Settings()
        assert settings.REDIS_URL.startswith("redis://")
        assert "redis:6379" in settings.REDIS_URL
    
    def test_logging_configuration(self):
        """Test logging configuration."""
        settings = Settings()
        assert settings.LOG_LEVEL == "INFO"
        assert settings.LOG_FORMAT == "json"
    
    def test_monitoring_configuration(self):
        """Test monitoring configuration."""
        settings = Settings()
        assert settings.ENABLE_METRICS is True
        assert settings.METRICS_PORT == 9090
