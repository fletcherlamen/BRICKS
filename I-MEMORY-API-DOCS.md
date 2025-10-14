# I MEMORY BRICK - API Documentation

Complete API reference for I MEMORY endpoints

---

## Base URL

```
http://localhost:8000/api/v1
```

For production:
```
https://your-domain.com/api/v1
```

---

## UBIC v1.5 Compliant Endpoints

### 1. GET /health

**System health status**

Returns comprehensive health information including database, Redis, and Mem0.ai status.

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "I_MEMORY",
  "version": "1.0.0",
  "brick_type": "Trinity_BRICKS",
  "timestamp": "2024-10-14T12:00:00Z",
  "uptime_since": "2024-10-14T10:00:00Z",
  "database": "connected",
  "mem0": {
    "status": "healthy",
    "mode": "real_ai",
    "api_key_configured": true
  },
  "redis_cache": "enabled"
}
```

---

### 2. GET /capabilities

**Memory operations available**

Lists all capabilities this BRICK provides.

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/capabilities
```

**Response:**
```json
{
  "service": "I_MEMORY",
  "brick_type": "Trinity_BRICKS",
  "version": "1.0.0",
  "capabilities": [
    {
      "name": "multi_user_isolation",
      "description": "Each user has private memory namespace",
      "status": "available"
    },
    {
      "name": "semantic_search",
      "description": "Natural language memory search",
      "status": "available"
    },
    {
      "name": "persistent_storage",
      "description": "Memories persist across container restarts",
      "status": "available"
    },
    {
      "name": "redis_caching",
      "description": "Redis caching layer for performance",
      "status": "available"
    }
  ],
  "limitations": [
    "Mem0.ai requires valid API key for full functionality",
    "Redis optional but recommended for performance"
  ],
  "ubic_compliance": "v1.5"
}
```

---

### 3. GET /state

**Current memory usage metrics**

Returns runtime state and performance metrics.

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/state
```

**Response:**
```json
{
  "service": "I_MEMORY",
  "status": "running",
  "config_version": "1.0.0",
  "timestamp": "2024-10-14T12:00:00Z",
  "database_memories": 150,
  "mem0_initialized": true,
  "redis_enabled": true
}
```

---

### 4. GET /dependencies

**Mem0.ai, PostgreSQL, Redis status**

Returns status of all external dependencies.

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/dependencies
```

**Response:**
```json
{
  "service": "I_MEMORY",
  "timestamp": "2024-10-14T12:00:00Z",
  "dependencies": [
    {
      "name": "PostgreSQL",
      "type": "database",
      "status": "healthy",
      "version": "PostgreSQL 15.4",
      "required": true
    },
    {
      "name": "Redis",
      "type": "cache",
      "status": "healthy",
      "version": "7.2.0",
      "required": false
    },
    {
      "name": "Mem0.ai",
      "type": "ai_service",
      "status": "healthy",
      "mode": "real_ai",
      "api_key_configured": true,
      "required": true
    }
  ]
}
```

---

### 5. POST /message

**Store memory via message bus**

UBIC standard message bus endpoint for storing memories.

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/message \
  -H "Content-Type: application/json" \
  -d '{
    "idempotency_key": "550e8400-e29b-41d4-a716-446655440000",
    "priority": "normal",
    "source": "I_CHAT",
    "target": "I_MEMORY",
    "message_type": "STORE_MEMORY",
    "payload": {
      "user_id": "user@example.com",
      "content": {
        "key": "value"
      }
    },
    "trace_id": "trace-123-456-789"
  }'
```

**Response:**
```json
{
  "idempotency_key": "550e8400-e29b-41d4-a716-446655440000",
  "trace_id": "trace-123-456-789",
  "status": "success",
  "result": {
    "memory_id": "mem_abc123",
    "user_id": "user@example.com",
    "timestamp": "2024-10-14T12:00:00Z"
  }
}
```

---

### 6. POST /send

**Query memory via message bus**

UBIC standard message bus endpoint for querying memories.

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/send \
  -H "Content-Type: application/json" \
  -d '{
    "source": "I_CHAT",
    "target": "I_MEMORY",
    "message_type": "GET_USER_MEMORIES",
    "payload": {
      "user_id": "user@example.com",
      "limit": 50
    }
  }'
```

**Response:**
```json
{
  "idempotency_key": "auto-generated-uuid",
  "trace_id": "auto-generated-trace",
  "status": "success",
  "memories": [...],
  "count": 25
}
```

---

### 7. POST /reload-config

**Reload configuration**

Reload service configuration without restart.

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/reload-config
```

**Response:**
```json
{
  "status": "success",
  "message": "Configuration reloaded",
  "old_version": "1.0.0",
  "new_version": "1.0.1",
  "timestamp": "2024-10-14T12:00:00Z"
}
```

---

### 8. POST /shutdown

**Graceful shutdown**

Initiate graceful shutdown process.

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/shutdown
```

**Response:**
```json
{
  "status": "shutdown_initiated",
  "message": "Graceful shutdown in progress",
  "timestamp": "2024-10-14T12:00:00Z"
}
```

---

### 9. POST /emergency-stop

**Immediate shutdown**

Emergency stop - immediate shutdown without cleanup.

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/emergency-stop
```

**Response:**
```json
{
  "status": "emergency_stopped",
  "message": "Service stopped immediately",
  "timestamp": "2024-10-14T12:00:00Z"
}
```

---

## Custom Memory Endpoints

### 1. POST /i-memory/store

**Direct memory storage**

Store memory with user isolation.

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/i-memory/store \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user@example.com",
    "content": {
      "project": "I BUILD",
      "component": "I PROACTIVE",
      "status": "phase_1_complete",
      "test_coverage": 85,
      "last_audit": "2024-10-10"
    }
  }'
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "memory_id": "mem_abc123",
    "user_id": "user@example.com",
    "content": {...},
    "timestamp": "2024-10-14T12:00:00Z"
  }
}
```

**Parameters:**
- `user_id` (string, required): User identifier for isolation
- `content` (object, required): Memory content as dictionary

---

### 2. POST /i-memory/search

**Semantic search across memories**

Natural language memory search with user isolation.

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/i-memory/search \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user@example.com",
    "query": "What is the status of I PROACTIVE?",
    "limit": 10
  }'
```

**Response:**
```json
{
  "status": "success",
  "query": "What is the status of I PROACTIVE?",
  "user_id": "user@example.com",
  "results": [
    {
      "memory_id": "mem_abc123",
      "content": {
        "project": "I BUILD",
        "component": "I PROACTIVE",
        "status": "phase_1_complete"
      },
      "relevance_score": 0.95,
      "user_id": "user@example.com",
      "metadata": {...}
    }
  ],
  "count": 1,
  "timestamp": "2024-10-14T12:00:00Z"
}
```

**Parameters:**
- `user_id` (string, required): User identifier for isolation
- `query` (string, required): Natural language search query
- `limit` (integer, optional): Maximum results (default: 10, max: 100)

---

### 3. GET /i-memory/user/{user_id}

**Retrieve all user memories**

Get all memories for a specific user.

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/i-memory/user/user@example.com?limit=50"
```

**Response:**
```json
{
  "status": "success",
  "user_id": "user@example.com",
  "memories": [
    {
      "memory_id": "mem_abc123",
      "content": {...},
      "timestamp": "2024-10-14T12:00:00Z",
      "metadata": {...}
    }
  ],
  "count": 25,
  "limit": 50,
  "timestamp": "2024-10-14T12:05:00Z"
}
```

**Path Parameters:**
- `user_id` (string, required): User identifier

**Query Parameters:**
- `limit` (integer, optional): Maximum memories to return (default: 50, max: 1000)

---

### 4. DELETE /i-memory/{memory_id}

**Delete specific memory**

Delete a memory with ownership verification.

**Request:**
```bash
curl -X DELETE http://localhost:8000/api/v1/i-memory/mem_abc123 \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user@example.com"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Memory deleted successfully",
  "memory_id": "mem_abc123",
  "user_id": "user@example.com",
  "timestamp": "2024-10-14T12:00:00Z"
}
```

**Path Parameters:**
- `memory_id` (string, required): Memory identifier

**Body Parameters:**
- `user_id` (string, required): User identifier for ownership verification

---

### 5. GET /i-memory/stats

**Usage and performance statistics**

Get system-wide or user-specific statistics.

**System-wide stats:**
```bash
curl -X GET http://localhost:8000/api/v1/i-memory/stats
```

**User-specific stats:**
```bash
curl -X GET "http://localhost:8000/api/v1/i-memory/stats?user_id=user@example.com"
```

**Response (system-wide):**
```json
{
  "status": "success",
  "stats": {
    "service": "I_MEMORY",
    "timestamp": "2024-10-14T12:00:00Z",
    "database_stats": {
      "total_memories": 150,
      "memory_types": {
        "fact": 50,
        "strategy": 30,
        "context": 70
      }
    },
    "mem0_stats": {
      "initialized": true,
      "redis_enabled": true
    }
  }
}
```

**Response (user-specific):**
```json
{
  "status": "success",
  "stats": {
    "user_stats": {
      "total_memories": 25,
      "user_id": "user@example.com",
      "oldest_memory": "2024-10-01T10:00:00Z",
      "newest_memory": "2024-10-14T12:00:00Z",
      "cache_enabled": true
    }
  }
}
```

**Query Parameters:**
- `user_id` (string, optional): User identifier for user-specific stats

---

## Error Responses

All endpoints may return error responses in this format:

**400 Bad Request:**
```json
{
  "detail": "Invalid request parameters"
}
```

**404 Not Found:**
```json
{
  "detail": "Memory mem_abc123 not found or access denied"
}
```

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "user_id"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Failed to store memory: [error details]"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production deployment, consider adding rate limiting middleware.

---

## Authentication

Currently no authentication is required. For production deployment, implement authentication and use `user_id` from verified JWT tokens.

---

## Caching

### Cache Behavior

- **Search Results**: Cached for 3 minutes
- **User Memories**: Cached for 5 minutes
- **Cache Invalidation**: Automatic on store/delete operations

### Cache Keys

```
mem0:{user_namespace}:search:{query}:{limit}
mem0:{user_namespace}:all_memories
```

---

## UBIC Message Types

### Supported Message Types

**For /message endpoint:**
- `STORE_MEMORY`: Store a new memory
- `SEARCH_MEMORY`: Search for memories

**For /send endpoint:**
- `GET_USER_MEMORIES`: Retrieve all user memories
- `GET_STATS`: Get statistics

### Priority Levels

- `normal`: Standard operations
- `high`: User-initiated requests
- `emergency`: System failures, security issues

---

## Examples

### Python Client

```python
import requests

class IMemoryClient:
    def __init__(self, base_url="http://localhost:8000/api/v1"):
        self.base_url = base_url
    
    def store(self, user_id, content):
        response = requests.post(
            f"{self.base_url}/i-memory/store",
            json={"user_id": user_id, "content": content}
        )
        return response.json()
    
    def search(self, user_id, query, limit=10):
        response = requests.post(
            f"{self.base_url}/i-memory/search",
            json={"user_id": user_id, "query": query, "limit": limit}
        )
        return response.json()
    
    def get_memories(self, user_id, limit=50):
        response = requests.get(
            f"{self.base_url}/i-memory/user/{user_id}",
            params={"limit": limit}
        )
        return response.json()

# Usage
client = IMemoryClient()

# Store memory
result = client.store("user@example.com", {
    "project": "I BUILD",
    "status": "complete"
})

# Search
results = client.search("user@example.com", "project status")

# Get all memories
memories = client.get_memories("user@example.com")
```

### JavaScript Client

```javascript
class IMemoryClient {
  constructor(baseUrl = 'http://localhost:8000/api/v1') {
    this.baseUrl = baseUrl;
  }
  
  async store(userId, content) {
    const response = await fetch(`${this.baseUrl}/i-memory/store`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({user_id: userId, content})
    });
    return response.json();
  }
  
  async search(userId, query, limit = 10) {
    const response = await fetch(`${this.baseUrl}/i-memory/search`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({user_id: userId, query, limit})
    });
    return response.json();
  }
  
  async getMemories(userId, limit = 50) {
    const response = await fetch(
      `${this.baseUrl}/i-memory/user/${userId}?limit=${limit}`
    );
    return response.json();
  }
}

// Usage
const client = new IMemoryClient();

// Store memory
const result = await client.store('user@example.com', {
  project: 'I BUILD',
  status: 'complete'
});

// Search
const results = await client.search('user@example.com', 'project status');
```

---

## Testing

Test all endpoints using the provided test suite:

```bash
pytest backend/tests/test_i_memory.py -v
```

---

Built with ❤️ as part of the Trinity BRICKS - I BUILD project

