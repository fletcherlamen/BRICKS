#!/usr/bin/env python3
import asyncio
import asyncpg
import sys

async def test_vps_database_connection():
    """Test direct connection to VPS database"""
    print("🔍 Testing VPS Database Connection")
    print("=" * 50)
    
    # VPS Database Configuration
    DATABASE_URL = "postgresql://user:password@64.227.99.111:5432/brick_orchestration"
    
    try:
        print("Connecting to VPS database...")
        print(f"URL: {DATABASE_URL}")
        
        # Test connection
        conn = await asyncpg.connect(DATABASE_URL)
        print("✅ Connected to VPS database successfully!")
        
        # Test query
        result = await conn.fetchval('SELECT 1 as test')
        print(f"✅ Test query result: {result}")
        
        # Check if orchestration_sessions table exists
        table_exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'orchestration_sessions'
            )
        """)
        
        if table_exists:
            print("✅ orchestration_sessions table exists")
            
            # Get session count
            session_count = await conn.fetchval('SELECT COUNT(*) FROM orchestration_sessions')
            print(f"✅ Found {session_count} orchestration sessions")
            
            # Get a sample session
            sample_session = await conn.fetchrow('SELECT * FROM orchestration_sessions LIMIT 1')
            if sample_session:
                print(f"✅ Sample session: {dict(sample_session)}")
        else:
            print("❌ orchestration_sessions table does not exist")
        
        # Check if memories table exists
        memories_exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'memories'
            )
        """)
        
        if memories_exists:
            print("✅ memories table exists")
            
            # Get memory count
            memory_count = await conn.fetchval('SELECT COUNT(*) FROM memories')
            print(f"✅ Found {memory_count} memories")
        else:
            print("❌ memories table does not exist")
        
        await conn.close()
        print("✅ Connection closed successfully")
        
        print("\n🎉 VPS Database Connection Test: SUCCESS!")
        print("The VPS database is accessible and working correctly.")
        print("The issue is that the VPS backend is not configured to use this database URL.")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_vps_database_connection())
    sys.exit(0 if success else 1)
