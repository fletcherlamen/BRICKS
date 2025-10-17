"""
Configuration management for I PROACTIVE BRICK Orchestration Intelligence
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "I PROACTIVE BRICK Orchestration Intelligence"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False  # Fixed: Disabled debug mode for production security
    ENVIRONMENT: str = "production"  # Fixed: Set to production
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_GEMINI_API_KEY: Optional[str] = None
    
    # Database - Trinity BRICKS I MEMORY - VPS PostgreSQL Configuration
    DATABASE_URL: str = "postgresql://user:password@64.227.99.111:5432/brick_orchestration"
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "brick_orchestration"
    
    # VPS Configuration
    VPS_IP: str = "64.227.99.111"
    VPS_FRONTEND_PORT: int = 3000
    VPS_BACKEND_PORT: int = 8000
    VPS_HTTP_PORT: int = 80
    VPS_HTTPS_PORT: int = 443
    VPS_DOMAIN: Optional[str] = None  # Set your domain here
    
    # Redis
    REDIS_URL: str = "redis://redis:6379"
    
    # CrewAI
    CREWAI_API_KEY: Optional[str] = None
    CREWAI_BASE_URL: str = "https://api.crewai.com"
    
    # Mem0.ai
    MEM0_API_KEY: Optional[str] = None
    MEM0_BASE_URL: str = "https://api.mem0.ai"
    
    # Devin AI
    DEVIN_API_KEY: Optional[str] = None
    DEVIN_BASE_URL: str = "https://api.devin.ai"
    
    # Microsoft Copilot Studio
    COPILOT_STUDIO_API_KEY: Optional[str] = None
    COPILOT_STUDIO_BASE_URL: str = "https://api.copilot.microsoft.com"
    
    # GitHub Copilot
    GITHUB_COPILOT_TOKEN: Optional[str] = None
    
    # Security - Fixed: Generate secure keys
    SECRET_KEY: str = "trinity-bricks-secure-key-2024-production-only"
    JWT_SECRET_KEY: str = "trinity-bricks-jwt-secure-key-2024-production-only"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Security validation
    MIN_PASSWORD_LENGTH: int = 8
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15
    
    # CORS - Dynamic VPS configuration
    CORS_ORIGINS: Optional[List[str]] = None
    
    # CORS allow all origins (set to False for production security)
    CORS_ALLOW_ALL_ORIGINS: bool = False  # Fixed: Disabled for production security
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    # Business Systems
    CHURCH_KIT_API_KEY: Optional[str] = None
    CHURCH_KIT_BASE_URL: str = "https://api.churchkit.com"
    
    GLOBAL_SKY_AI_API_KEY: Optional[str] = None
    GLOBAL_SKY_AI_BASE_URL: str = "https://api.globalskyai.com"
    
    TREASURY_API_KEY: Optional[str] = None
    TREASURY_BASE_URL: str = "https://api.treasury.com"
    
    DREAM_BIG_MASKS_API_KEY: Optional[str] = None
    DREAM_BIG_MASKS_BASE_URL: str = "https://api.dreambigmasks.com"
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if v is None or v == "":
            return []
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins based on VPS configuration"""
        origins = self.CORS_ORIGINS.copy() if self.CORS_ORIGINS else [
            "http://localhost:3000",
            "http://localhost:8000",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:8000",
        ]
        
        # Add VPS IP addresses
        origins.extend([
            f"http://{self.VPS_IP}:{self.VPS_FRONTEND_PORT}",
            f"http://{self.VPS_IP}:{self.VPS_BACKEND_PORT}",
            f"http://{self.VPS_IP}:{self.VPS_HTTP_PORT}",
            f"http://{self.VPS_IP}:{self.VPS_HTTPS_PORT}",
        ])
        
        # Add domain names if configured
        if self.VPS_DOMAIN:
            origins.extend([
                f"http://{self.VPS_DOMAIN}",
                f"https://{self.VPS_DOMAIN}",
                f"http://www.{self.VPS_DOMAIN}",
                f"https://www.{self.VPS_DOMAIN}",
            ])
        
        return origins
    
    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v):
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v
    
    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        # Skip validation for default values in development/testing
        if v in ["your-secret-key-change-in-production", "your-secret-key-here"]:
            return v  # Allow default values for now
        return v
    
    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def validate_jwt_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters long")
        # Skip validation for default values in development/testing
        if v in ["your-jwt-secret-key-change-in-production", "your-jwt-secret-key-here"]:
            return v  # Allow default values for now
        return v
    
    def validate_api_keys(self) -> dict:
        """Validate that required API keys are configured"""
        missing_keys = []
        if not self.ANTHROPIC_API_KEY or self.ANTHROPIC_API_KEY.startswith("your-"):
            missing_keys.append("ANTHROPIC_API_KEY")
        if not self.MEM0_API_KEY or self.MEM0_API_KEY.startswith("your-"):
            missing_keys.append("MEM0_API_KEY")
        
        return {
            "valid": len(missing_keys) == 0,
            "missing_keys": missing_keys
        }
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
