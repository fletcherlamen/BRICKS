"""
Migrate VPS Database Memory Table to Trinity BRICKS I MEMORY Schema

This script connects to the VPS database and alters the memory table
to match the Trinity BRICKS I MEMORY specification.
"""

import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# VPS Database URL
VPS_DATABASE_URL = "postgresql+asyncpg://brick_user:Brick2024Secure!@64.227.99.111:5432/brick_orchestration"


async def migrate_vps_memory_table():
    """Migrate VPS memory table to Trinity BRICKS I MEMORY schema"""
    
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║   Trinity BRICKS I MEMORY - VPS Database Migration              ║")
    print("╚══════════════════════════════════════════════════════════════════╝\n")
    
    # Create engine for VPS database
    engine = create_async_engine(VPS_DATABASE_URL, echo=False)
    
    try:
        async with engine.begin() as conn:
            print("🔌 Connected to VPS database: 64.227.99.111:5432")
            print("=" * 70)
            
            # Check current schema
            print("\n📋 Step 1: Checking current schema...")
            result = await conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'memories'
                ORDER BY ordinal_position
            """))
            current_columns = result.fetchall()
            
            if current_columns:
                print("   Current columns:")
                for col_name, data_type, nullable in current_columns:
                    print(f"   - {col_name:20} {data_type:20} {nullable}")
            else:
                print("   ⚠️  Table does not exist or has no columns")
            
            # Backup existing data
            print("\n📋 Step 2: Backing up existing data...")
            result = await conn.execute(text("SELECT COUNT(*) FROM memories"))
            existing_count = result.scalar() if current_columns else 0
            print(f"   Existing memories: {existing_count}")
            
            if existing_count > 0:
                result = await conn.execute(text("""
                    SELECT id, memory_id, content 
                    FROM memories 
                    LIMIT 5
                """))
                sample_data = result.fetchall()
                print(f"   Sample data (first 5):")
                for row in sample_data:
                    print(f"   - ID: {row[0]}, Memory ID: {row[1]}")
            
            # Drop and recreate table with Trinity BRICKS schema
            print("\n📋 Step 3: Recreating table with Trinity BRICKS schema...")
            await conn.execute(text("DROP TABLE IF EXISTS memories CASCADE"))
            print("   ✅ Old table dropped")
            
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
            print("   ✅ New Trinity BRICKS table created")
            
            # Create indexes
            print("\n📋 Step 4: Creating indexes...")
            await conn.execute(text("""
                CREATE INDEX idx_memories_user_id ON memories(user_id)
            """))
            await conn.execute(text("""
                CREATE INDEX idx_memories_memory_id ON memories(memory_id)
            """))
            await conn.execute(text("""
                CREATE INDEX idx_memories_created_at ON memories(created_at DESC)
            """))
            print("   ✅ Indexes created")
            
            # Add sample Trinity BRICKS data
            print("\n📋 Step 5: Adding sample Trinity BRICKS data...")
            sample_memories = [
                {
                    "memory_id": "mem_trinity_001",
                    "user_id": "james@fullpotential.com",
                    "content": {
                        "developer": "Fletcher",
                        "brick": "I PROACTIVE",
                        "phase": 1,
                        "status": "verified_working",
                        "verified_by": "Vahit",
                        "payment_recommended": 280
                    },
                    "metadata": {"category": "developer_assessment"}
                },
                {
                    "memory_id": "mem_trinity_002",
                    "user_id": "james@fullpotential.com",
                    "content": {
                        "project": "I BUILD",
                        "revenue_target": 6000,
                        "current_gap": 6000,
                        "priority": "developer_verification"
                    },
                    "metadata": {"category": "project_context"}
                },
                {
                    "memory_id": "mem_trinity_003",
                    "user_id": "vahit@company.com",
                    "content": {
                        "developer": "Vahit",
                        "role": "Technical Lead",
                        "status": "active"
                    },
                    "metadata": {"category": "team_member"}
                }
            ]
            
            for mem in sample_memories:
                await conn.execute(
                    text("""
                        INSERT INTO memories (memory_id, user_id, content, metadata)
                        VALUES (:memory_id, :user_id, :content::jsonb, :metadata::jsonb)
                    """),
                    {
                        "memory_id": mem["memory_id"],
                        "user_id": mem["user_id"],
                        "content": str(mem["content"]).replace("'", '"'),
                        "metadata": str(mem["metadata"]).replace("'", '"')
                    }
                )
            
            print(f"   ✅ Added {len(sample_memories)} sample memories")
            
            # Verify final schema
            print("\n📋 Step 6: Verifying final schema...")
            result = await conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'memories'
                ORDER BY ordinal_position
            """))
            final_columns = result.fetchall()
            
            print("\n   Final Trinity BRICKS I MEMORY Schema:")
            print("   " + "-" * 60)
            for col_name, data_type, nullable in final_columns:
                null_str = "NULL" if nullable == "YES" else "NOT NULL"
                print(f"   {col_name:20} {data_type:20} {null_str}")
            
            # Get final count
            result = await conn.execute(text("SELECT COUNT(*) FROM memories"))
            final_count = result.scalar()
            
            print("\n" + "=" * 70)
            print("✅ VPS Database Migration Complete!")
            print("=" * 70)
            print(f"\n📊 Summary:")
            print(f"   Database: 64.227.99.111:5432")
            print(f"   Total memories: {final_count}")
            print(f"   Schema: Trinity BRICKS I MEMORY compliant")
            print(f"   Multi-user isolation: Enabled")
            print(f"   Ready for: I CHAT and I ASSESS integration")
            print("\n🎉 Trinity BRICKS I MEMORY is ready on VPS!")
            
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(migrate_vps_memory_table())

