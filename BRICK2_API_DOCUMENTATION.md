# BRICK 2 Automation API Documentation

## Overview
Enhanced orchestration API endpoints designed specifically for BRICK 2 automation with structured JSON responses, programmatic triggers, and comprehensive session management.

## API Base URL
- **Local**: `http://localhost:8000/api/v1/orchestration`
- **VPS**: `http://64.227.99.111:8000/api/v1/orchestration`
- **Production**: `http://64.227.99.111:8000/api/v1/orchestration`

---

## 🔄 Core Endpoints

### 1. Execute Orchestration (Enhanced)
**POST** `/execute`

Execute orchestration with enhanced structured responses for BRICK 2 automation.

#### Request Body
```json
{
  "task_type": "strategic_analysis|brick_development|revenue_optimization|gap_analysis",
  "goal": "Your orchestration goal",
  "context": {
    "user_id": "optional_user_id",
    "priority": "high|normal|low",
    "custom_data": "any_additional_context"
  },
  "session_id": "optional_existing_session_id",
  "priority": "high|normal|low",
  "automation_mode": true
}
```

#### Response Structure
```json
{
  "status": "success",
  "message": "Orchestration completed successfully - BRICK 2 automation ready",
  "details": {
    "run_id": "unique_run_id",
    "session_id": "unique_session_id",
    "task_type": "strategic_analysis",
    "status": "completed",
    "confidence": 0.95,
    "execution_time_ms": 2500,
    "priority": "normal",
    "automation_mode": true,
    "context": {...},
    "results": {...},
    "automation_ready": true,
    "structured_outputs": {
      "recommendations": [...],
      "key_insights": [...],
      "risk_assessment": {...},
      "revenue_potential": {...},
      "systems_built": {...},
      "generated_apps": [...],
      "deployment_files": {...},
      "ai_systems_used": [...],
      "confidence_score": 0.95
    },
    "timestamp": "2024-01-01T12:00:00Z"
  }
}
```

---

### 2. Programmatic Trigger (New)
**POST** `/trigger`

Dedicated endpoint for programmatic orchestration triggers optimized for BRICK 2 automation.

#### Request Body
```json
{
  "task_type": "strategic_analysis|brick_development|revenue_optimization|gap_analysis",
  "goal": "Your automation goal",
  "context": {
    "automation": true,
    "brick2_integration": true,
    "custom_parameters": {...}
  },
  "session_id": "optional_session_id",
  "priority": "high|normal|low",
  "automation_mode": true
}
```

#### Response Structure
```json
{
  "status": "success",
  "message": "Programmatic orchestration completed - BRICK 2 automation ready",
  "details": {
    "success": true,
    "run_id": "unique_run_id",
    "session_id": "unique_session_id",
    "task_type": "brick_development",
    "status": "completed",
    "confidence": 0.92,
    "execution_time_ms": 3200,
    "priority": "normal",
    "automation_mode": true,
    "context": {...},
    "goal": "Build automation-ready system",
    "structured_data": {
      "recommendations": [...],
      "key_insights": [...],
      "risk_assessment": {...},
      "revenue_potential": {...},
      "systems_built": {...},
      "generated_applications": [...],
      "deployment_artifacts": {...},
      "ai_systems_used": [...],
      "confidence_score": 0.92,
      "automation_ready": true,
      "brick2_compatible": true
    },
    "timestamp": "2024-01-01T12:00:00Z",
    "api_version": "1.0",
    "automation_endpoint": true
  }
}
```

---

### 3. Get Orchestration Sessions (Enhanced)
**GET** `/sessions`

Retrieve orchestration sessions with complete status, goal, and outputs for BRICK 2 automation.

#### Query Parameters
- `limit`: Number of sessions to return (default: 10)
- `status_filter`: Filter by status (completed, failed, running)
- `task_type_filter`: Filter by task type (strategic_analysis, brick_development, etc.)

#### Example Request
```
GET /api/v1/orchestration/sessions?limit=20&status_filter=completed&task_type_filter=brick_development
```

#### Response Structure
```json
{
  "sessions": [
    {
      "session_id": "session_123",
      "run_id": "run_456",
      "goal": "Build complete e-commerce platform",
      "task_type": "brick_development",
      "status": "completed",
      "confidence": 0.94,
      "execution_time_ms": 4500,
      "created_at": "2024-01-01T12:00:00Z",
      "completed_at": "2024-01-01T12:00:05Z",
      "context": {...},
      "outputs": {
        "recommendations": [...],
        "key_insights": [...],
        "risk_assessment": {...},
        "revenue_potential": {...},
        "systems_built": {...},
        "generated_apps": [...],
        "ai_systems_used": [...],
        "confidence_score": 0.94
      },
      "automation_ready": true
    }
  ],
  "total_count": 15,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

---

### 4. Get Specific Session (Enhanced)
**GET** `/sessions/{session_id}`

Retrieve detailed information about a specific orchestration session with complete outputs.

#### Response Structure
```json
{
  "session_id": "session_123",
  "run_id": "run_456",
  "goal": "Build complete e-commerce platform with payment processing",
  "task_type": "brick_development",
  "status": "completed",
  "confidence": 0.94,
  "execution_time_ms": 4500,
  "created_at": "2024-01-01T12:00:00Z",
  "completed_at": "2024-01-01T12:00:05Z",
  "context": {
    "user_id": "user_789",
    "priority": "high",
    "automation": true
  },
  "outputs": {
    "recommendations": [
      "Implement secure payment gateway integration",
      "Create responsive product catalog",
      "Set up inventory management system"
    ],
    "key_insights": [
      "E-commerce platform requires robust security measures",
      "Mobile-first design is essential for user engagement",
      "Payment processing integration is critical for success"
    ],
    "risk_assessment": {
      "security": "high",
      "scalability": "medium",
      "compliance": "high"
    },
    "revenue_potential": {
      "estimated_monthly_revenue": "$50,000",
      "growth_potential": "high",
      "break_even_time": "6_months"
    },
    "systems_built": {
      "ai_powered": true,
      "systems_built": true,
      "working_prototypes": true,
      "deployable_ready": true,
      "actual_code_generated": true,
      "production_ready": true
    },
    "generated_apps": [
      {
        "name": "Real E-Commerce Platform Application",
        "type": "production_ready_application",
        "status": "built_and_deployed",
        "generated_files": {
          "app_directory": "/app/generated_apps/e_commerce_platform_1234567890",
          "backend_files": ["main.py", "requirements.txt", "Dockerfile"],
          "frontend_files": ["App.js", "package.json"],
          "database_files": ["schema.sql"],
          "deployment_files": ["docker-compose.yml"],
          "total_files_created": 7,
          "deployment_ready": true
        }
      }
    ],
    "ai_systems_used": ["openai", "anthropic", "google_gemini"],
    "confidence_score": 0.94
  },
  "automation_ready": true
}
```

---

## 🔧 BRICK 2 Integration Examples

### Python Integration Example
```python
import requests
import json

# BRICK 2 Automation Integration
API_BASE = "http://localhost:8000/api/v1/orchestration"

def trigger_brick_orchestration(goal, task_type="brick_development", context=None):
    """Trigger orchestration programmatically for BRICK 2"""
    
    payload = {
        "task_type": task_type,
        "goal": goal,
        "context": context or {},
        "automation_mode": True,
        "priority": "high"
    }
    
    response = requests.post(f"{API_BASE}/trigger", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        if data["details"]["success"]:
            return {
                "success": True,
                "session_id": data["details"]["session_id"],
                "structured_data": data["details"]["structured_data"],
                "automation_ready": data["details"]["structured_data"]["brick2_compatible"]
            }
    
    return {"success": False, "error": response.text}

def get_orchestration_sessions(limit=10, status_filter=None):
    """Get orchestration sessions for BRICK 2"""
    
    params = {"limit": limit}
    if status_filter:
        params["status_filter"] = status_filter
    
    response = requests.get(f"{API_BASE}/sessions", params=params)
    
    if response.status_code == 200:
        return response.json()["sessions"]
    
    return []

# Usage Example
result = trigger_brick_orchestration(
    goal="Build automated testing system",
    task_type="brick_development",
    context={"brick2_integration": True, "automation_level": "full"}
)

if result["success"]:
    print(f"Session ID: {result['session_id']}")
    print(f"Automation Ready: {result['automation_ready']}")
    print(f"Generated Apps: {len(result['structured_data']['generated_applications'])}")
```

### JavaScript/Node.js Integration Example
```javascript
const axios = require('axios');

const API_BASE = 'http://localhost:8000/api/v1/orchestration';

class Brick2OrchestrationClient {
    constructor(baseUrl = API_BASE) {
        this.baseUrl = baseUrl;
    }

    async triggerOrchestration(goal, taskType = 'brick_development', context = {}) {
        try {
            const response = await axios.post(`${this.baseUrl}/trigger`, {
                task_type: taskType,
                goal: goal,
                context: {
                    ...context,
                    brick2_integration: true,
                    automation: true
                },
                automation_mode: true,
                priority: 'high'
            });

            if (response.data.details.success) {
                return {
                    success: true,
                    sessionId: response.data.details.session_id,
                    structuredData: response.data.details.structured_data,
                    automationReady: response.data.details.structured_data.brick2_compatible
                };
            }
        } catch (error) {
            console.error('Orchestration failed:', error.message);
            return { success: false, error: error.message };
        }
    }

    async getSessions(limit = 10, statusFilter = null) {
        try {
            const params = { limit };
            if (statusFilter) params.status_filter = statusFilter;

            const response = await axios.get(`${this.baseUrl}/sessions`, { params });
            return response.data.sessions;
        } catch (error) {
            console.error('Failed to get sessions:', error.message);
            return [];
        }
    }

    async getSessionDetails(sessionId) {
        try {
            const response = await axios.get(`${this.baseUrl}/sessions/${sessionId}`);
            return response.data;
        } catch (error) {
            console.error('Failed to get session details:', error.message);
            return null;
        }
    }
}

// Usage Example
const client = new Brick2OrchestrationClient();

async function runAutomation() {
    const result = await client.triggerOrchestration(
        'Build automated deployment pipeline',
        'brick_development',
        { automation_level: 'full', environment: 'production' }
    );

    if (result.success) {
        console.log(`Session ID: ${result.sessionId}`);
        console.log(`Automation Ready: ${result.automationReady}`);
        console.log(`Generated Applications: ${result.structuredData.generated_applications.length}`);
        
        // Process the structured data for BRICK 2
        const recommendations = result.structuredData.recommendations;
        const generatedApps = result.structuredData.generated_applications;
        
        // Use the structured data for further automation
        return { recommendations, generatedApps, sessionId: result.sessionId };
    }
}

runAutomation().then(result => {
    if (result) {
        console.log('BRICK 2 automation completed successfully');
        console.log('Recommendations:', result.recommendations);
        console.log('Generated Apps:', result.generatedApps.length);
    }
});
```

---

## 🎯 Key Features for BRICK 2

### 1. **Structured JSON Responses**
- All endpoints return consistent, structured JSON
- Nested data organization for easy parsing
- Automation-ready data formats

### 2. **Programmatic Triggers**
- Dedicated `/trigger` endpoint for automation
- Non-UI optimized responses
- BRICK 2 compatibility flags

### 3. **Session Management**
- Complete session history with outputs
- Filtering by status and task type
- Detailed session information retrieval

### 4. **Automation Indicators**
- `automation_ready`: Boolean flag indicating automation compatibility
- `brick2_compatible`: Specific BRICK 2 integration flag
- `automation_mode`: Context for automation requests

### 5. **Rich Output Data**
- Generated applications with file structures
- Deployment artifacts and configurations
- AI system usage tracking
- Confidence scores and risk assessments

---

## 🔍 Error Handling

All endpoints return consistent error responses:

```json
{
  "status": "error",
  "error_code": "AUTOMATION_ERROR",
  "message": "Programmatic orchestration failed",
  "details": {
    "error": "Detailed error message",
    "automation_mode": true,
    "success": false,
    "brick2_compatible": false
  }
}
```

---

## 📊 Status Codes

- **200**: Success
- **404**: Session not found
- **422**: Validation error
- **500**: Internal server error

---

## 🚀 Getting Started

1. **Test the API**: Use the examples above to test integration
2. **Check Sessions**: Verify session history with `/sessions`
3. **Trigger Automation**: Use `/trigger` for programmatic orchestration
4. **Process Results**: Parse structured outputs for BRICK 2 automation

The API is now fully optimized for BRICK 2 automation with clear structured responses, programmatic triggers, and comprehensive session management.
