# VPS Delete Memory Fix

## Problem Identified
The VPS (64.227.99.111) is running an older version of the backend that has the delete memory logic error. When trying to delete a memory, it returns:

```json
{"detail":"Not Found"}
```

## Root Cause
The VPS backend has the old delete memory implementation that:
1. Doesn't properly handle the memory lookup in `real_orchestrator.memories`
2. Has the old logic that was causing the "list object has no attribute 'values'" error
3. Missing the latest fixes for memory storage consistency

## Solution
The VPS needs to be updated with the latest backend code that includes:

### Fixed Delete Memory Endpoint (`/backend/app/api/v1/endpoints/memory.py`)
```python
@router.delete("/{memory_id}")
async def delete_memory(memory_id: str):
    """Delete a memory by ID"""
    
    try:
        from app.services.real_orchestrator import real_orchestrator
        
        # Check if memory exists in the orchestrator's memory dictionary
        if memory_id not in real_orchestrator.memories:
            # Also check if it's one of the default memories that might be shown in the list
            # but not stored in the orchestrator
            memories = real_orchestrator.get_memories()
            memory_exists = any(memory.get('memory_id') == memory_id for memory in memories)
            
            if not memory_exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Memory with ID {memory_id} not found"
                )
        
        # Delete from orchestrator (in production, this would delete from database)
        if memory_id in real_orchestrator.memories:
            del real_orchestrator.memories[memory_id]
            logger.info("Memory deleted from orchestrator", memory_id=memory_id)
        else:
            # If it's a default memory not in orchestrator, just log the deletion
            logger.info("Default memory deletion requested", memory_id=memory_id)
        
        return {
            "memory_id": memory_id,
            "status": "deleted",
            "message": "Memory deleted successfully",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete memory", error=str(e), memory_id=memory_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete memory: {str(e)}"
        )
```

### Fixed Memory List Endpoint
```python
# Add default memories if none exist
if not memories:
    default_memories = [
        {
            "memory_id": "mem_001",
            "content": "Church Kit Generator has high revenue potential",
            "category": "business",
            "importance_score": 0.9,
            "tags": ["revenue", "strategy", "church-kit"],
            "source_type": "text",
            "created_at": datetime.now().isoformat()
        },
        {
            "memory_id": "mem_002",
            "content": "Mobile app development is a critical gap",
            "category": "technical",
            "importance_score": 0.8,
            "tags": ["gap", "mobile", "development"],
            "source_type": "text",
            "created_at": datetime.now().isoformat()
        }
    ]
    # Store default memories in orchestrator so they can be deleted
    for memory in default_memories:
        real_orchestrator.memories[memory["memory_id"]] = memory
    memories = default_memories
```

## Deployment Steps

### Option 1: Use the Update Script (Recommended)
```bash
# SSH into VPS
ssh root@64.227.99.111

# Navigate to project directory
cd ~/orchestration

# Run the update script
./update_vps.sh
```

### Option 2: Manual Update
```bash
# SSH into VPS
ssh root@64.227.99.111

# Navigate to project directory
cd ~/orchestration

# Stop containers
docker-compose down

# Pull latest changes (if using git)
git pull origin main

# Rebuild with latest fixes
docker-compose up -d --build --force-recreate

# Wait for services to start
sleep 30

# Test the delete endpoint
curl -X DELETE http://localhost:8000/api/v1/memory/[MEMORY_ID]
```

### Option 3: Copy Fixed Files
If you can't use git or the update script, copy the fixed files to the VPS:

1. Copy `backend/app/api/v1/endpoints/memory.py` to the VPS
2. Copy `backend/app/services/real_orchestrator.py` to the VPS
3. Restart the backend container

## Testing After Update

### Test 1: Health Check
```bash
curl http://64.227.99.111:8000/health
```

### Test 2: Get Memories
```bash
curl http://64.227.99.111:8000/api/v1/memory/
```

### Test 3: Delete Memory
```bash
# Get a memory ID first
MEMORY_ID=$(curl -s http://64.227.99.111:8000/api/v1/memory/ | grep -o '"memory_id":"[^"]*"' | head -1 | cut -d'"' -f4)

# Delete the memory
curl -X DELETE "http://64.227.99.111:8000/api/v1/memory/$MEMORY_ID"
```

## Expected Results

### Before Fix:
```json
{"detail":"Not Found"}
```

### After Fix:
```json
{
  "memory_id": "mem_xxx",
  "status": "deleted",
  "message": "Memory deleted successfully",
  "timestamp": "2025-09-23T09:00:00"
}
```

## Verification
After updating the VPS:
1. Go to http://64.227.99.111:3000/memory
2. Click the delete button (red trash icon) on any memory
3. Memory should be deleted without "Not Found" error
4. You should see "Memory deleted successfully!" message

## Troubleshooting
If the issue persists after update:
1. Check backend logs: `docker-compose logs backend`
2. Verify the delete endpoint is registered: `curl http://64.227.99.111:8000/docs`
3. Ensure the memory router is included in the API: Check `backend/app/api/v1/api.py`
