"""
Tests for database functionality
"""

import pytest
from sqlalchemy.orm import Session
from app.core.database import get_db, init_db
from app.models.memory import Memory
from app.models.orchestration import OrchestrationSession


class TestDatabase:
    """Test database operations and models."""
    
    def test_get_db_session(self, db_session: Session):
        """Test database session creation."""
        assert db_session is not None
        assert hasattr(db_session, 'query')
    
    def test_memory_model(self, db_session: Session, sample_memory_data):
        """Test Memory model operations."""
        # Create memory
        memory = Memory(
            user_id="test@example.com",
            content=sample_memory_data["content"],
            metadata=sample_memory_data["metadata"]
        )
        
        db_session.add(memory)
        db_session.commit()
        db_session.refresh(memory)
        
        # Verify memory was created
        assert memory.id is not None
        assert memory.user_id == "test@example.com"
        assert memory.content == sample_memory_data["content"]
        assert memory.metadata == sample_memory_data["metadata"]
        assert memory.created_at is not None
        assert memory.updated_at is not None
    
    def test_memory_retrieval(self, db_session: Session, sample_memory_data):
        """Test memory retrieval by user."""
        # Create multiple memories for different users
        memory1 = Memory(
            user_id="user1@example.com",
            content={"project": "Project 1"},
            metadata={"category": "test"}
        )
        memory2 = Memory(
            user_id="user2@example.com",
            content={"project": "Project 2"},
            metadata={"category": "test"}
        )
        
        db_session.add_all([memory1, memory2])
        db_session.commit()
        
        # Test user isolation
        user1_memories = db_session.query(Memory).filter(
            Memory.user_id == "user1@example.com"
        ).all()
        user2_memories = db_session.query(Memory).filter(
            Memory.user_id == "user2@example.com"
        ).all()
        
        assert len(user1_memories) == 1
        assert len(user2_memories) == 1
        assert user1_memories[0].content["project"] == "Project 1"
        assert user2_memories[0].content["project"] == "Project 2"
    
    def test_orchestration_session_model(self, db_session: Session):
        """Test OrchestrationSession model operations."""
        session_data = {
            "user_id": "test@example.com",
            "session_type": "revenue_optimization",
            "status": "completed",
            "results": {"revenue": 1000, "opportunities": 5},
            "metadata": {"duration": 120}
        }
        
        session = OrchestrationSession(**session_data)
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)
        
        # Verify session was created
        assert session.id is not None
        assert session.user_id == "test@example.com"
        assert session.session_type == "revenue_optimization"
        assert session.status == "completed"
        assert session.results == {"revenue": 1000, "opportunities": 5}
        assert session.metadata == {"duration": 120}
        assert session.created_at is not None
        assert session.updated_at is not None
    
    def test_database_constraints(self, db_session: Session):
        """Test database constraints and validations."""
        # Test required fields
        with pytest.raises(Exception):  # Should raise due to missing required fields
            memory = Memory()
            db_session.add(memory)
            db_session.commit()
    
    def test_memory_content_json_handling(self, db_session: Session):
        """Test JSON content handling in Memory model."""
        complex_content = {
            "nested": {
                "data": [1, 2, 3],
                "boolean": True,
                "null_value": None
            },
            "array": ["a", "b", "c"],
            "number": 42.5
        }
        
        memory = Memory(
            user_id="test@example.com",
            content=complex_content,
            metadata={"test": "json_handling"}
        )
        
        db_session.add(memory)
        db_session.commit()
        db_session.refresh(memory)
        
        # Verify JSON content is preserved
        assert memory.content == complex_content
        assert memory.content["nested"]["data"] == [1, 2, 3]
        assert memory.content["nested"]["boolean"] is True
        assert memory.content["nested"]["null_value"] is None
        assert memory.content["array"] == ["a", "b", "c"]
        assert memory.content["number"] == 42.5
    
    def test_memory_timestamps(self, db_session: Session):
        """Test automatic timestamp handling."""
        memory = Memory(
            user_id="test@example.com",
            content={"test": "timestamps"},
            metadata={}
        )
        
        db_session.add(memory)
        db_session.commit()
        db_session.refresh(memory)
        
        # Verify timestamps are set
        assert memory.created_at is not None
        assert memory.updated_at is not None
        assert memory.created_at == memory.updated_at
        
        # Update memory and check updated_at changes
        original_updated = memory.updated_at
        memory.content = {"test": "updated"}
        db_session.commit()
        db_session.refresh(memory)
        
        assert memory.updated_at > original_updated
