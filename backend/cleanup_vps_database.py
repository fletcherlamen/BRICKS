#!/usr/bin/env python3
"""
VPS Database Cleanup Script for Trinity BRICKS

This script removes legacy tables from the old BRICK 1 system
while preserving essential Trinity BRICKS data.

Essential Tables (KEEP):
- memories (I MEMORY BRICK)
- orchestration_sessions (I CHAT BRICK)
- chat_sessions (I CHAT BRICK)
- chat_messages (I CHAT BRICK)
- users (Authentication)
- alembic_version (Database migrations)

Legacy Tables (REMOVE):
- All other tables from old BRICK 1 system
"""

import psycopg2
import sys
from datetime import datetime

# VPS Database Configuration
VPS_CONFIG = {
    'host': '64.227.99.111',
    'port': 5432,
    'database': 'brick_orchestration',
    'user': 'user',
    'password': 'password'
}

# Essential tables to keep
ESSENTIAL_TABLES = [
    'memories',
    'orchestration_sessions', 
    'chat_sessions',
    'chat_messages',
    'users',
    'alembic_version'
]

def connect_to_database():
    """Connect to VPS database"""
    try:
        conn = psycopg2.connect(**VPS_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        return None

def get_all_tables(conn):
    """Get all tables in the database"""
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = [row[0] for row in cur.fetchall()]
    cur.close()
    return tables

def get_table_row_count(conn, table_name):
    """Get row count for a table"""
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cur.fetchone()[0]
        return count
    except Exception as e:
        print(f"⚠️  Could not get count for {table_name}: {e}")
        return 0
    finally:
        cur.close()

def backup_table_data(conn, table_name):
    """Create a backup of table data before deletion"""
    cur = conn.cursor()
    try:
        # Create backup table
        backup_table = f"{table_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        cur.execute(f"CREATE TABLE {backup_table} AS SELECT * FROM {table_name};")
        conn.commit()
        print(f"✅ Created backup: {backup_table}")
        return backup_table
    except Exception as e:
        print(f"⚠️  Could not backup {table_name}: {e}")
        return None
    finally:
        cur.close()

def drop_table(conn, table_name):
    """Safely drop a table"""
    cur = conn.cursor()
    try:
        cur.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
        conn.commit()
        print(f"✅ Dropped table: {table_name}")
        return True
    except Exception as e:
        print(f"❌ Failed to drop {table_name}: {e}")
        return False
    finally:
        cur.close()

def main():
    """Main cleanup function"""
    print("🧹 VPS Database Cleanup for Trinity BRICKS")
    print("=" * 60)
    
    # Connect to database
    conn = connect_to_database()
    if not conn:
        sys.exit(1)
    
    try:
        # Get all tables
        all_tables = get_all_tables(conn)
        print(f"📊 Found {len(all_tables)} tables in database")
        
        # Identify tables to remove
        tables_to_remove = [t for t in all_tables if t not in ESSENTIAL_TABLES]
        essential_tables = [t for t in all_tables if t in ESSENTIAL_TABLES]
        
        print(f"\n✅ Essential tables (keeping): {len(essential_tables)}")
        for table in essential_tables:
            count = get_table_row_count(conn, table)
            print(f"  - {table}: {count} rows")
        
        print(f"\n🗑️  Legacy tables (removing): {len(tables_to_remove)}")
        for table in tables_to_remove:
            count = get_table_row_count(conn, table)
            print(f"  - {table}: {count} rows")
        
        # Confirm before proceeding
        print(f"\n⚠️  WARNING: This will remove {len(tables_to_remove)} legacy tables!")
        print("Essential Trinity BRICKS data will be preserved.")
        
        response = input("\nProceed with cleanup? (yes/no): ").lower().strip()
        if response != 'yes':
            print("❌ Cleanup cancelled by user")
            return
        
        print(f"\n🧹 Starting cleanup of {len(tables_to_remove)} legacy tables...")
        
        # Remove legacy tables
        removed_count = 0
        failed_count = 0
        
        for table in tables_to_remove:
            count = get_table_row_count(conn, table)
            
            # Create backup if table has data
            if count > 0:
                backup_table = backup_table_data(conn, table)
                if not backup_table:
                    print(f"⚠️  Skipping {table} due to backup failure")
                    failed_count += 1
                    continue
            
            # Drop the table
            if drop_table(conn, table):
                removed_count += 1
            else:
                failed_count += 1
        
        print(f"\n📊 Cleanup Summary:")
        print(f"✅ Successfully removed: {removed_count} tables")
        print(f"❌ Failed to remove: {failed_count} tables")
        
        # Verify essential tables are still there
        print(f"\n🔍 Verifying essential tables...")
        remaining_tables = get_all_tables(conn)
        missing_essential = [t for t in ESSENTIAL_TABLES if t not in remaining_tables]
        
        if missing_essential:
            print(f"❌ ERROR: Missing essential tables: {missing_essential}")
        else:
            print(f"✅ All essential tables preserved")
        
        # Show final table count
        final_count = len(remaining_tables)
        print(f"\n📈 Database cleanup complete!")
        print(f"Before: {len(all_tables)} tables")
        print(f"After: {final_count} tables")
        print(f"Removed: {len(all_tables) - final_count} legacy tables")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
