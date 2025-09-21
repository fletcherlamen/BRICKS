"""
Configuration settings for the I PROACTIVE BRICK Orchestration Intelligence.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = "I PROACTIVE BRICK Orchestration Intelligence"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API Keys - Multiple AI providers
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    MEM0_API_KEY: Optional[str] = None
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/brick_orchestration"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000"
    ]
    
    # CrewAI Configuration
    CREWAI_MAX_ITERATIONS: int = 10
    CREWAI_VERBOSE: bool = True
    
    # Mem0 Configuration
    MEM0_HOST: str = "https://api.mem0.ai"
    MEM0_PROJECT_ID: str = "brick-orchestration"
    
    # Orchestration
    MAX_CONCURRENT_TASKS: int = 5
    TASK_TIMEOUT: int = 300  # 5 minutes
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
