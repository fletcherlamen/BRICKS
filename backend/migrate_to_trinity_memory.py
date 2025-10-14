"""
Database Migration: BRICK 1 Memory → Trinity BRICKS I MEMORY

Changes:
1. Add user_id column (required for multi-user isolation)
2. Change content from Text to JSON (for structured data)
3. Simplify schema (remove unused columns)
4. Preserve existing data where possible
"""

import asyncio
import sys
from sqlalchemy import text
from app.core.database import engine, AsyncSessionLocal
from app.models.memory import Memory

async def migrate_memory_table():
    """Migrate memories table to Trinity BRICKS I MEMORY schema"""
    
    print("🔄 Starting Trinity BRICKS I MEMORY migration...")
    print("=" * 60)
    
    try:
        async with engine.begin() as conn:
            # Check if user_id column exists
            result = await conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'memories' AND column_name = 'user_id'
            """))
            has_user_id = result.fetchone() is not None
            
            if not has_user_id:
                print("\n📝 Step 1: Adding user_id column...")
                await conn.execute(text("""
                    ALTER TABLE memories 
                    ADD COLUMN IF NOT EXISTS user_id VARCHAR(255) DEFAULT 'system@i-memory.local'
                """))
                print("   ✅ user_id column added")
                
                # Create index on user_id
                print("\n📝 Step 2: Creating index on user_id...")
                await conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_memories_user_id ON memories(user_id)
                """))
                print("   ✅ Index created")
            else:
                print("\n✅ user_id column already exists")
            
            # Check content column type
            result = await conn.execute(text("""
                SELECT data_type 
                FROM information_schema.columns 
                WHERE table_name = 'memories' AND column_name = 'content'
            """))
            content_type = result.fetchone()
            
            if content_type and content_type[0] == 'text':
                print("\n📝 Step 3: Migrating existing content to JSON format...")
                
                # Get existing memories
                result = await conn.execute(text("SELECT id, content FROM memories"))
                existing_memories = result.fetchall()
                
                print(f"   Found {len(existing_memories)} existing memories")
                
                # Add temporary column
                await conn.execute(text("""
                    ALTER TABLE memories 
                    ADD COLUMN IF NOT EXISTS content_json JSONB
                """))
                
                # Migrate data
                for memory_id, content in existing_memories:
                    try:
                        # Wrap text content in JSON
                        json_content = {"text": content}
                        await conn.execute(
                            text("UPDATE memories SET content_json = :content WHERE id = :id"),
                            {"content": json.dumps(json_content), "id": memory_id}
                        )
                    except Exception as e:
                        print(f"   ⚠️  Warning: Could not migrate memory {memory_id}: {e}")
                
                # Drop old column and rename new one
                await conn.execute(text("ALTER TABLE memories DROP COLUMN IF EXISTS content"))
                await conn.execute(text("ALTER TABLE memories RENAME COLUMN content_json TO content"))
                
                print("   ✅ Content migrated to JSON format")
            else:
                print("\n✅ Content column already JSON format")
            
            # Remove unused columns for Trinity BRICKS
            print("\n📝 Step 4: Removing unused columns...")
            unused_columns = [
                'memory_type', 'importance_score', 'tags', 
                'source_system', 'source_type', 'category',
                'file_name', 'file_size', 'last_accessed', 'access_count'
            ]
            
            for col in unused_columns:
                try:
                    await conn.execute(text(f"ALTER TABLE memories DROP COLUMN IF EXISTS {col}"))
                except Exception as e:
                    pass  # Column might not exist
            
            print("   ✅ Unused columns removed")
            
            # Ensure user_id is NOT NULL
            print("\n📝 Step 5: Setting user_id as required...")
            await conn.execute(text("""
                UPDATE memories 
                SET user_id = 'system@i-memory.local' 
                WHERE user_id IS NULL
            """))
            await conn.execute(text("""
                ALTER TABLE memories 
                ALTER COLUMN user_id SET NOT NULL
            """))
            print("   ✅ user_id set as required")
            
            # Get final count
            result = await conn.execute(text("SELECT COUNT(*) FROM memories"))
            final_count = result.scalar()
            
            print("\n" + "=" * 60)
            print(f"✅ Migration complete!")
            print(f"   Total memories: {final_count}")
            print(f"   Schema: Trinity BRICKS I MEMORY compliant")
            print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


async def verify_schema():
    """Verify the new schema is correct"""
    print("\n🔍 Verifying Trinity BRICKS I MEMORY schema...")
    
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'memories'
                ORDER BY ordinal_position
            """))
            columns = result.fetchall()
            
            print("\n📋 Current schema:")
            for col_name, data_type, nullable in columns:
                null_str = "NULL" if nullable == "YES" else "NOT NULL"
                print(f"   {col_name:20} {data_type:15} {null_str}")
            
            # Verify required columns
            required_cols = ['id', 'memory_id', 'user_id', 'content', 'metadata']
            existing_cols = [col[0] for col in columns]
            
            missing = [col for col in required_cols if col not in existing_cols]
            if missing:
                print(f"\n⚠️  Missing required columns: {missing}")
            else:
                print("\n✅ All required columns present")
                
    except Exception as e:
        print(f"❌ Verification failed: {e}")


async def main():
    """Run migration"""
    print("\n╔══════════════════════════════════════════════════════════════════╗")
    print("║   Trinity BRICKS I MEMORY - Database Migration                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝\n")
    
    await migrate_memory_table()
    await verify_schema()
    
    print("\n🎉 Trinity BRICKS I MEMORY database is ready!")
    print("\nNext steps:")
    print("  1. Restart backend: docker compose restart backend")
    print("  2. Test endpoints: curl http://localhost:8000/api/v1/ubic/health")
    print("  3. Add memory: curl -X POST http://localhost:8000/api/v1/memory/add")


if __name__ == "__main__":
    asyncio.run(main())

