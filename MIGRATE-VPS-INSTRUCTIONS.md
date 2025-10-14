# Trinity BRICKS I MEMORY - VPS Database Migration Instructions

## Current Situation

You're currently using the **local PostgreSQL container** (`postgres:5432`).

To use the **VPS database** (64.227.99.111:5432), you need to:
1. Provide the correct VPS database credentials
2. Update the `.env` file
3. Run the migration script

---

## Option 1: Provide VPS Database Credentials

Please provide the following information:

```bash
VPS_DATABASE_HOST=64.227.99.111
VPS_DATABASE_PORT=5432
VPS_DATABASE_NAME=brick_orchestration
VPS_DATABASE_USER=?  # What is the username?
VPS_DATABASE_PASSWORD=?  # What is the password?
```

Once you provide these, I can:
1. Update the `.env` file
2. Run the Trinity BRICKS I MEMORY migration on VPS
3. Update the application to use VPS database

---

## Option 2: Use Local Database (Current Setup)

If you want to continue with the **local PostgreSQL container**, the Trinity BRICKS I MEMORY is already working:

✅ Database: `postgresql://user:password@postgres:5432/brick_orchestration`  
✅ Trinity BRICKS schema: Already created  
✅ Sample data: Already added  
✅ All endpoints: Working  

---

## Option 3: Manual VPS Migration

If you have direct access to the VPS database, you can run this SQL manually:

```sql
-- Connect to VPS database
psql -h 64.227.99.111 -U <username> -d brick_orchestration

-- Drop old table
DROP TABLE IF EXISTS memories CASCADE;

-- Create Trinity BRICKS I MEMORY table
CREATE TABLE memories (
    id SERIAL PRIMARY KEY,
    memory_id VARCHAR(100) UNIQUE NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    content JSONB NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_memories_user_id ON memories(user_id);
CREATE INDEX idx_memories_memory_id ON memories(memory_id);
CREATE INDEX idx_memories_created_at ON memories(created_at DESC);

-- Add sample data
INSERT INTO memories (memory_id, user_id, content, metadata) VALUES
(
    'mem_trinity_001',
    'james@fullpotential.com',
    '{"developer": "Fletcher", "brick": "I PROACTIVE", "phase": 1, "status": "verified_working", "verified_by": "Vahit", "payment_recommended": 280}'::jsonb,
    '{"category": "developer_assessment"}'::jsonb
),
(
    'mem_trinity_002',
    'james@fullpotential.com',
    '{"project": "I BUILD", "revenue_target": 6000, "current_gap": 6000, "priority": "developer_verification"}'::jsonb,
    '{"category": "project_context"}'::jsonb
);

-- Verify
SELECT COUNT(*) FROM memories;
SELECT * FROM memories LIMIT 3;
```

---

## Current Status

✅ **Local Database**: Trinity BRICKS I MEMORY working perfectly  
⏳ **VPS Database**: Waiting for credentials or manual migration  

---

## What to Do Next

**Choose one:**

1. **Provide VPS credentials** → I'll migrate automatically
2. **Keep local database** → Already working, no changes needed
3. **Manual migration** → Use SQL script above

Let me know which option you prefer!

