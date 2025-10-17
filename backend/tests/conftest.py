"""
Pytest configuration and fixtures for Trinity BRICKS
"""

import pytest
import asyncio
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from main import app
from app.core.database import get_db, Base
from app.core.config import Settings

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session) -> Generator[TestClient, None, None]:
    """Create a test client with database dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_settings():
    """Create test settings with safe defaults."""
    return Settings(
        DEBUG=False,
        ENVIRONMENT="testing",
        SECRET_KEY="test-secret-key-32-chars-long",
        JWT_SECRET_KEY="test-jwt-secret-key-32-chars-long",
        DATABASE_URL=SQLALCHEMY_DATABASE_URL,
        REDIS_URL="redis://localhost:6379/1",  # Use different Redis DB for tests
        ANTHROPIC_API_KEY="test-anthropic-key",
        MEM0_API_KEY="test-mem0-key",
    )


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "user_id": "test@example.com",
        "email": "test@example.com",
        "name": "Test User",
        "role": "developer"
    }


@pytest.fixture
def sample_memory_data():
    """Sample memory data for testing."""
    return {
        "content": {
            "project": "Test Project",
            "status": "testing",
            "phase": 1
        },
        "metadata": {
            "category": "test",
            "priority": "high"
        }
    }


@pytest.fixture
def sample_audit_data():
    """Sample audit data for testing."""
    return {
        "repository": "https://github.com/test/repo",
        "user_id": "test@example.com",
        "criteria": ["UBIC_compliance", "test_coverage", "code_quality"]
    }
