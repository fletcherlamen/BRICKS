"""
Database health and diagnostic endpoints
"""

from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
import structlog
import asyncio
import asyncpg
from datetime import datetime

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.get("/health")
async def database_health_check():
    """Check database connection health"""
    try:
        async with AsyncSessionLocal() as session:
            # Test basic query
            result = await session.execute(text("SELECT 1 as test"))
            test_value = result.scalar()
            
            if test_value == 1:
                return {
                    "status": "healthy",
                    "message": "Database connection successful",
                    "timestamp": datetime.now().isoformat(),
                    "test_query": "SELECT 1",
                    "result": test_value
                }
            else:
                return {
                    "status": "unhealthy",
                    "message": "Database query returned unexpected result",
                    "timestamp": datetime.now().isoformat(),
                    "test_query": "SELECT 1",
                    "result": test_value
                }
                
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        return {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }


@router.get("/tables")
async def list_database_tables():
    """List all tables in the database"""
    try:
        async with AsyncSessionLocal() as session:
            # Query to get all tables
            result = await session.execute(text("""
                SELECT table_name, table_type
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            
            tables = [{"name": row[0], "type": row[1]} for row in result.fetchall()]
            
            return {
                "status": "success",
                "tables": tables,
                "count": len(tables),
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        logger.error("Failed to list database tables", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list database tables: {str(e)}"
        )


@router.get("/sessions-count")
async def get_sessions_count():
    """Get count of orchestration sessions"""
    try:
        async with AsyncSessionLocal() as session:
            # Check if orchestration_sessions table exists
            table_check = await session.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'orchestration_sessions'
                )
            """))
            
            table_exists = table_check.scalar()
            
            if not table_exists:
                return {
                    "status": "warning",
                    "message": "orchestration_sessions table does not exist",
                    "count": 0,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Get count
            result = await session.execute(text("SELECT COUNT(*) FROM orchestration_sessions"))
            count = result.scalar()
            
            return {
                "status": "success",
                "count": count,
                "table_exists": True,
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        logger.error("Failed to get sessions count", error=str(e))
        return {
            "status": "error",
            "message": f"Failed to get sessions count: {str(e)}",
            "count": 0,
            "timestamp": datetime.now().isoformat()
        }


@router.get("/memories-count")
async def get_memories_count():
    """Get count of memories"""
    try:
        async with AsyncSessionLocal() as session:
            # Check if memories table exists
            table_check = await session.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'memories'
                )
            """))
            
            table_exists = table_check.scalar()
            
            if not table_exists:
                return {
                    "status": "warning",
                    "message": "memories table does not exist",
                    "count": 0,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Get count
            result = await session.execute(text("SELECT COUNT(*) FROM memories"))
            count = result.scalar()
            
            return {
                "status": "success",
                "count": count,
                "table_exists": True,
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        logger.error("Failed to get memories count", error=str(e))
        return {
            "status": "error",
            "message": f"Failed to get memories count: {str(e)}",
            "count": 0,
            "timestamp": datetime.now().isoformat()
        }


@router.post("/test-connection")
async def test_database_connection():
    """Test direct database connection to VPS"""
    try:
        # Test direct connection to VPS
        conn = await asyncpg.connect(
            host='64.227.99.111',
            port=5432,
            user='user',
            password='password',
            database='brick_orchestration'
        )
        
        # Test basic query
        version = await conn.fetchval('SELECT version()')
        
        # Check tables
        tables = await conn.fetch('''
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        ''')
        
        await conn.close()
        
        return {
            "status": "success",
            "message": "Direct VPS database connection successful",
            "postgresql_version": version,
            "tables": [table['table_name'] for table in tables],
            "table_count": len(tables),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Direct VPS database connection failed", error=str(e))
        return {
            "status": "error",
            "message": f"Direct VPS database connection failed: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }
