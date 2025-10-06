#!/usr/bin/env python3
import asyncio
import asyncpg
import sys

async def test_connection():
    try:
        print("Testing VPS database connection...")
        conn = await asyncpg.connect('postgresql://user:password@64.227.99.111:5432/brick_orchestration')
        print("✅ Connected successfully to VPS database!")
        
        # Test a simple query
        result = await conn.fetchval('SELECT 1')
        print(f"✅ Test query result: {result}")
        
        await conn.close()
        print("✅ Connection closed successfully")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    sys.exit(0 if success else 1)
