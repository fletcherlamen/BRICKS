#!/usr/bin/env python3
import asyncio
import asyncpg

async def check_schema():
    conn = await asyncpg.connect('postgresql://user:password@64.227.99.111:5432/brick_orchestration')
    
    print("📋 Orchestration Sessions Table Schema:")
    print("=" * 50)
    
    columns = await conn.fetch("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'orchestration_sessions'
        ORDER BY ordinal_position
    """)
    
    for col in columns:
        print(f"  {col['column_name']}: {col['data_type']} {'NULL' if col['is_nullable'] == 'YES' else 'NOT NULL'}")
    
    print("\n📋 Memories Table Schema:")
    print("=" * 50)
    
    columns = await conn.fetch("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'memories'
        ORDER BY ordinal_position
    """)
    
    for col in columns:
        print(f"  {col['column_name']}: {col['data_type']} {'NULL' if col['is_nullable'] == 'YES' else 'NOT NULL'}")
    
    await conn.close()

asyncio.run(check_schema())
