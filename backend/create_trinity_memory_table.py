"""
Create Trinity BRICKS I MEMORY table in database
According to Trinity BRICKS specification
"""

import asyncio
from sqlalchemy import text
from app.core.database import engine

async def create_trinity_memory_table():
    """Create Trinity BRICKS I MEMORY table"""
    
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║   Creating Trinity BRICKS I MEMORY Table                        ║")
    print("╚══════════════════════════════════════════════════════════════════╝\n")
    
    try:
        async with engine.begin() as conn:
            # Drop existing table if it exists
            print("📝 Step 1: Dropping old memories table (if exists)...")
            await conn.execute(text("DROP TABLE IF EXISTS memories CASCADE"))
            print("   ✅ Old table dropped\n")
            
            # Create Trinity BRICKS I MEMORY table
            print("📝 Step 2: Creating Trinity BRICKS I MEMORY table...")
            await conn.execute(text("""
                CREATE TABLE memories (
                    id SERIAL PRIMARY KEY,
                    memory_id VARCHAR(100) UNIQUE NOT NULL,
                    user_id VARCHAR(255) NOT NULL,
                    content JSONB NOT NULL,
                    metadata JSONB DEFAULT '{}'::jsonb,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                )
            """))
            print("   ✅ Table created\n")
            
            # Create indexes
            print("📝 Step 3: Creating indexes...")
            await conn.execute(text("""
                CREATE INDEX idx_memories_user_id ON memories(user_id)
            """))
            await conn.execute(text("""
                CREATE INDEX idx_memories_memory_id ON memories(memory_id)
            """))
            await conn.execute(text("""
                CREATE INDEX idx_memories_created_at ON memories(created_at DESC)
            """))
            print("   ✅ Indexes created\n")
            
            # Verify table structure
            print("📝 Step 4: Verifying table structure...")
            result = await conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'memories'
                ORDER BY ordinal_position
            """))
            columns = result.fetchall()
            
            print("\n   Trinity BRICKS I MEMORY Schema:")
            print("   " + "-" * 60)
            for col_name, data_type, nullable in columns:
                null_str = "NULL" if nullable == "YES" else "NOT NULL"
                print(f"   {col_name:20} {data_type:20} {null_str}")
            
            print("\n" + "=" * 70)
            print("✅ Trinity BRICKS I MEMORY table created successfully!")
            print("=" * 70)
            print("\n📋 Table Features:")
            print("   ✅ user_id (NOT NULL, indexed) - Multi-user isolation")
            print("   ✅ content (JSONB) - Structured data storage")
            print("   ✅ metadata (JSONB) - Flexible metadata")
            print("   ✅ Timestamps - created_at, updated_at")
            print("   ✅ Indexes - user_id, memory_id, created_at")
            print("\n🎉 Ready for Trinity BRICKS I MEMORY operations!")
            
    except Exception as e:
        print(f"\n❌ Failed to create table: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    asyncio.run(create_trinity_memory_table())

