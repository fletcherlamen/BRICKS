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
    
    # Database - VPS Configuration
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
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_SECRET_KEY: str = "your-jwt-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS - Dynamic VPS configuration
    CORS_ORIGINS: List[str] = [
        # Local development
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    # CORS allow all origins (set to False for production security)
    CORS_ALLOW_ALL_ORIGINS: bool = True
    
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
    
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins based on VPS configuration"""
        origins = self.CORS_ORIGINS.copy()
        
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
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
