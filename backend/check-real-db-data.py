#!/usr/bin/env python3
import asyncio
import asyncpg

async def check_database_data():
    """Check what's actually in the VPS database"""
    print("🔍 Checking VPS Database Data")
    print("=" * 60)
    
    DATABASE_URL = "postgresql://user:password@64.227.99.111:5432/brick_orchestration"
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        print("✅ Connected to VPS database")
        print()
        
        # Check orchestration sessions
        print("📊 Orchestration Sessions Table:")
        print("-" * 60)
        sessions = await conn.fetch("SELECT * FROM orchestration_sessions ORDER BY created_at DESC LIMIT 5")
        
        for i, session in enumerate(sessions, 1):
            print(f"\nSession {i}:")
            for key, value in dict(session).items():
                print(f"  {key}: {value}")
        
        print()
        print("=" * 60)
        
        # Check memories
        print("📊 Memories Table:")
        print("-" * 60)
        memories = await conn.fetch("SELECT * FROM memories ORDER BY created_at DESC LIMIT 5")
        
        for i, memory in enumerate(memories, 1):
            print(f"\nMemory {i}:")
            for key, value in dict(memory).items():
                if len(str(value)) > 100:
                    print(f"  {key}: {str(value)[:100]}...")
                else:
                    print(f"  {key}: {value}")
        
        await conn.close()
        print()
        print("=" * 60)
        print("✅ Database check complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_database_data())
