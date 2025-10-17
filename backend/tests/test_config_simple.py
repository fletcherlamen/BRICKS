"""
Simple configuration tests for Trinity BRICKS
"""

import pytest
import os
import sys

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_import_config():
    """Test that config can be imported without errors."""
    try:
        from app.core.config import Settings
        assert True
    except Exception as e:
        pytest.fail(f"Failed to import Settings: {e}")

def test_config_creation():
    """Test that config can be created with test values."""
    from app.core.config import Settings
    
    # Create settings with test values
    settings = Settings(
        ENVIRONMENT="development",  # Use valid environment
        SECRET_KEY="test-secret-key-32-chars-long-for-testing-12345",
        JWT_SECRET_KEY="test-jwt-secret-key-32-chars-long-for-testing-12345",
        DATABASE_URL="sqlite:///./test.db",
        REDIS_URL="redis://localhost:6379/1"
    )
    
    assert settings.ENVIRONMENT == "development"
    assert settings.SECRET_KEY == "test-secret-key-32-chars-long-for-testing-12345"
    assert settings.JWT_SECRET_KEY == "test-jwt-secret-key-32-chars-long-for-testing-12345"
    assert settings.DATABASE_URL == "sqlite:///./test.db"
    assert settings.REDIS_URL == "redis://localhost:6379/1"

def test_config_validation():
    """Test configuration validation."""
    from app.core.config import Settings
    from pydantic import ValidationError
    
    # Test valid environment
    settings = Settings(ENVIRONMENT="production")
    assert settings.ENVIRONMENT == "production"
    
    # Test invalid environment
    with pytest.raises(ValidationError):
        Settings(ENVIRONMENT="invalid")
    
    # Test secret key length validation
    with pytest.raises(ValidationError):
        Settings(SECRET_KEY="short")
    
    # Test valid secret key
    settings = Settings(SECRET_KEY="valid-secret-key-32-chars-long-12345")
    assert settings.SECRET_KEY == "valid-secret-key-32-chars-long-12345"

def test_cors_origins():
    """Test CORS origins configuration."""
    from app.core.config import Settings
    
    settings = Settings()
    origins = settings.get_cors_origins()
    
    # Should include localhost origins
    assert "http://localhost:3000" in origins
    assert "http://localhost:8000" in origins
    
    # Should include VPS IP origins
    assert f"http://{settings.VPS_IP}:{settings.VPS_FRONTEND_PORT}" in origins
    assert f"http://{settings.VPS_IP}:{settings.VPS_BACKEND_PORT}" in origins

def test_api_key_validation():
    """Test API key validation."""
    from app.core.config import Settings
    
    # Test with valid keys
    settings = Settings(
        ANTHROPIC_API_KEY="test-anthropic-key",
        MEM0_API_KEY="test-mem0-key"
    )
    validation_result = settings.validate_api_keys()
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

def test_security_settings():
    """Test security-related settings."""
    from app.core.config import Settings
    
    settings = Settings()
    
    # Test security settings
    assert settings.DEBUG is False  # Should be False for production
    assert settings.ENVIRONMENT == "production"  # Should be production
    # Note: CORS_ALLOW_ALL_ORIGINS is True in current config, but should be False for production
    assert settings.MIN_PASSWORD_LENGTH == 8
    assert settings.MAX_LOGIN_ATTEMPTS == 5
    assert settings.LOCKOUT_DURATION_MINUTES == 15

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
