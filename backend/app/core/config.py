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
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_GEMINI_API_KEY: Optional[str] = None
    
    # Database
    DATABASE_URL: str = "postgresql://brick_user:brick_password@postgres:5432/brick_orchestration"
    POSTGRES_USER: str = "brick_user"
    POSTGRES_PASSWORD: str = "brick_password"
    POSTGRES_DB: str = "brick_orchestration"
    
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
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_SECRET_KEY: str = "your-jwt-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS - VPS deployment configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000", 
        "http://localhost:8000",
        "http://localhost:3001",
        "http://localhost:8080",
        "http://64.227.99.111:3000",
        "http://64.227.99.111:8000",
        "https://64.227.99.111:3000",
        "https://64.227.99.111:8000",
        "http://64.227.99.111",
        "https://64.227.99.111",
        "http://64.227.99.111:80",
        "https://64.227.99.111:443",
        "*"  # Allow all origins for VPS deployment
    ]
    
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
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v):
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
