#!/usr/bin/env python3
import asyncio
import asyncpg
import sys
import time

async def test_vps_database():
    """Test VPS database connection and operations"""
    print("🔍 Testing VPS Database Connection...")
    print("=" * 50)
    
    # Test 1: Basic Connection
    try:
        print("1. Testing basic connection...")
        start_time = time.time()
        conn = await asyncpg.connect('postgresql://user:password@64.227.99.111:5432/brick_orchestration')
        connection_time = time.time() - start_time
        print(f"   ✅ Connected successfully in {connection_time:.2f}s")
        
        # Test 2: Simple Query
        print("2. Testing simple query...")
        result = await conn.fetchval('SELECT 1 as test_value')
        print(f"   ✅ Query result: {result}")
        
        # Test 3: Check if tables exist
        print("3. Checking database tables...")
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        print(f"   ✅ Found {len(tables)} tables:")
        for table in tables:
            print(f"      - {table['table_name']}")
        
        # Test 4: Check orchestration sessions
        print("4. Checking orchestration sessions...")
        session_count = await conn.fetchval('SELECT COUNT(*) FROM orchestration_sessions')
        print(f"   ✅ Orchestration sessions: {session_count}")
        
        # Test 5: Check memories
        print("5. Checking memories...")
        memory_count = await conn.fetchval('SELECT COUNT(*) FROM memories')
        print(f"   ✅ Memories: {memory_count}")
        
        # Test 6: Test a write operation
        print("6. Testing write operation...")
        test_id = f"test_{int(time.time())}"
        await conn.execute("""
            INSERT INTO orchestration_sessions 
            (session_id, run_id, goal, task_type, status, confidence, execution_time_ms, created_at, completed_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        """, test_id, test_id, "VPS Database Test", "test", "completed", 0.95, 100, 
        "2025-10-06T01:00:00Z", "2025-10-06T01:00:00Z")
        print(f"   ✅ Write test successful (session_id: {test_id})")
        
        # Clean up test data
        await conn.execute('DELETE FROM orchestration_sessions WHERE session_id = $1', test_id)
        print("   ✅ Test data cleaned up")
        
        await conn.close()
        print("   ✅ Connection closed successfully")
        
        print("\n🎉 VPS Database Test: ALL TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print(f"   ❌ Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_vps_database())
    sys.exit(0 if success else 1)
