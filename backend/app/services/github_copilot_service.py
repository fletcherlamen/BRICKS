"""
GitHub Copilot Workspace Service Integration
Handles development pipeline automation and code generation
"""

from typing import Dict, List, Optional, Any
import structlog
import httpx
import asyncio
from datetime import datetime
import json

from app.core.config import settings
from app.core.exceptions import BusinessSystemError

logger = structlog.get_logger(__name__)


class GitHubCopilotService:
    """GitHub Copilot Workspace service for development pipeline automation"""
    
    def __init__(self):
        self.initialized = False
        self.client = None
        self.api_key = None
        self.base_url = "https://api.github.com"
        
    async def initialize(self):
        """Initialize GitHub Copilot Workspace service"""
        try:
            if not settings.GITHUB_COPILOT_TOKEN:
                logger.warning("GitHub Copilot token not configured, using enhanced mock service")
                self.client = EnhancedMockGitHubCopilotClient()
            else:
                self.api_key = settings.GITHUB_COPILOT_TOKEN
                self.client = RealGitHubCopilotClient(self.api_key, self.base_url)
                await self.client.initialize()
            
            self.initialized = True
            logger.info("GitHub Copilot Workspace service initialized successfully")
            
        except Exception as e:
            logger.error("Failed to initialize GitHub Copilot service", error=str(e))
            raise BusinessSystemError(f"GitHub Copilot initialization failed: {str(e)}")
    
    async def generate_code(
        self,
        prompt: str,
        context: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Generate code using GitHub Copilot Workspace"""
        
        if not self.initialized:
            raise BusinessSystemError("GitHub Copilot service not initialized")
        
        try:
            result = await self.client.generate_code(
                prompt=prompt,
                context=context,
                session_id=session_id
            )
            
            logger.info("Code generation completed", session_id=session_id)
            
            return {
                "generated_code": result,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "service": "github_copilot"
            }
            
        except Exception as e:
            logger.error("Code generation failed", error=str(e), session_id=session_id)
            raise BusinessSystemError(f"Code generation failed: {str(e)}")
    
    async def create_repository(
        self,
        repo_config: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Create a new repository with Copilot assistance"""
        
        if not self.initialized:
            raise BusinessSystemError("GitHub Copilot service not initialized")
        
        try:
            result = await self.client.create_repository(
                repo_config=repo_config,
                session_id=session_id
            )
            
            logger.info("Repository created", repo_name=repo_config.get("name"), session_id=session_id)
            
            return {
                "repository_result": result,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "service": "github_copilot"
            }
            
        except Exception as e:
            logger.error("Repository creation failed", error=str(e), session_id=session_id)
            raise BusinessSystemError(f"Repository creation failed: {str(e)}")
    
    async def setup_ci_cd(
        self,
        repo_name: str,
        ci_config: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Setup CI/CD pipeline with Copilot assistance"""
        
        if not self.initialized:
            raise BusinessSystemError("GitHub Copilot service not initialized")
        
        try:
            result = await self.client.setup_ci_cd(
                repo_name=repo_name,
                ci_config=ci_config,
                session_id=session_id
            )
            
            logger.info("CI/CD pipeline setup completed", repo_name=repo_name, session_id=session_id)
            
            return {
                "ci_cd_result": result,
                "repo_name": repo_name,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "service": "github_copilot"
            }
            
        except Exception as e:
            logger.error("CI/CD setup failed", error=str(e), session_id=session_id)
            raise BusinessSystemError(f"CI/CD setup failed: {str(e)}")
    
    async def get_status(self) -> Dict[str, Any]:
        """Get GitHub Copilot service status"""
        
        if not settings.GITHUB_COPILOT_TOKEN:
            return {
                "status": "critical",
                "mode": "mock",
                "api_key_configured": False,
                "message": "API token not configured - service not operational",
                "error": "Missing GITHUB_COPILOT_TOKEN"
            }
        
        if not self.initialized:
            return {
                "status": "error",
                "mode": "failed",
                "api_key_configured": True,
                "message": "Service initialization failed",
                "error": "Failed to initialize GitHub Copilot"
            }
        
        try:
            status = await self.client.get_status()
            
            return {
                "status": "healthy",
                "mode": "real_ai",
                "api_key_configured": True,
                "service_status": status
            }
            
        except Exception as e:
            logger.error("GitHub Copilot health check failed", error=str(e))
            return {
                "status": "error",
                "mode": "failed",
                "api_key_configured": True,
                "error": str(e)
            }
    
    async def cleanup(self):
        """Cleanup GitHub Copilot resources"""
        try:
            self.client = None
            self.initialized = False
            logger.info("GitHub Copilot service cleaned up")
        except Exception as e:
            logger.error("Error cleaning up GitHub Copilot service", error=str(e))


class RealGitHubCopilotClient:
    """Real GitHub Copilot Workspace client for production use"""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.http_client = None
        
    async def initialize(self):
        """Initialize HTTP client"""
        self.http_client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"token {self.api_key}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
        
    async def generate_code(self, prompt: str, context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Generate code using real GitHub Copilot API"""
        try:
            payload = {
                "prompt": prompt,
                "context": context,
                "session_id": session_id
            }
            
            response = await self.http_client.post("/copilot/generate", json=payload)
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error("GitHub Copilot API error", error=str(e))
            raise BusinessSystemError(f"GitHub Copilot API error: {str(e)}")
    
    async def create_repository(self, repo_config: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Create repository using real GitHub API"""
        try:
            response = await self.http_client.post("/user/repos", json=repo_config)
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error("GitHub repository creation error", error=str(e))
            raise BusinessSystemError(f"GitHub repository creation error: {str(e)}")
    
    async def setup_ci_cd(self, repo_name: str, ci_config: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Setup CI/CD using real GitHub API"""
        try:
            # Create .github/workflows directory and CI file
            workflow_content = self._generate_workflow_content(ci_config)
            
            payload = {
                "message": "Add CI/CD workflow",
                "content": workflow_content,
                "path": ".github/workflows/ci.yml"
            }
            
            response = await self.http_client.put(f"/repos/{repo_name}/contents/.github/workflows/ci.yml", json=payload)
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error("GitHub CI/CD setup error", error=str(e))
            raise BusinessSystemError(f"GitHub CI/CD setup error: {str(e)}")
    
    def _generate_workflow_content(self, ci_config: Dict[str, Any]) -> str:
        """Generate GitHub Actions workflow content"""
        return f"""name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest tests/ -v
    - name: Run linting
      run: |
        black --check .
        isort --check-only .
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
"""
    
    async def get_status(self) -> Dict[str, Any]:
        """Get real GitHub Copilot service status"""
        try:
            response = await self.http_client.get("/user")
            response.raise_for_status()
            user_data = response.json()
            
            return {
                "status": "operational",
                "user": user_data.get("login"),
                "rate_limit": "available"
            }
        except httpx.HTTPError as e:
            logger.error("GitHub status check error", error=str(e))
            return {"status": "error", "error": str(e)}


class EnhancedMockGitHubCopilotClient:
    """Enhanced mock GitHub Copilot client with realistic development capabilities"""
    
    def __init__(self):
        self.repositories = {}
        self.code_templates = {
            "api": self._get_api_template(),
            "frontend": self._get_frontend_template(),
            "database": self._get_database_template(),
            "microservice": self._get_microservice_template()
        }
        
    async def generate_code(self, prompt: str, context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Enhanced mock code generation with realistic output"""
        
        # Determine code type from prompt
        code_type = self._determine_code_type(prompt)
        template = self.code_templates.get(code_type, self._get_generic_template())
        
        # Generate code based on prompt and context
        generated_code = self._generate_code_from_template(template, prompt, context)
        
        return {
            "code": generated_code,
            "language": self._determine_language(prompt),
            "framework": self._determine_framework(prompt),
            "dependencies": self._identify_dependencies(prompt),
            "documentation": self._generate_documentation(prompt, generated_code),
            "tests": self._generate_tests(generated_code),
            "deployment_instructions": self._generate_deployment_instructions(prompt),
            "code_quality_score": 8.5,
            "complexity_analysis": self._analyze_complexity(generated_code),
            "security_considerations": self._identify_security_issues(generated_code),
            "performance_notes": self._generate_performance_notes(generated_code),
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }
    
    async def create_repository(self, repo_config: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Enhanced mock repository creation with realistic setup"""
        
        repo_name = repo_config.get("name", f"brick-repo-{len(self.repositories) + 1}")
        
        repository = {
            "id": len(self.repositories) + 1,
            "name": repo_name,
            "full_name": f"brick-orchestration/{repo_name}",
            "description": repo_config.get("description", "BRICK orchestration repository"),
            "private": repo_config.get("private", False),
            "html_url": f"https://github.com/brick-orchestration/{repo_name}",
            "clone_url": f"https://github.com/brick-orchestration/{repo_name}.git",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "language": repo_config.get("language", "Python"),
            "topics": repo_config.get("topics", ["brick", "orchestration", "ai"]),
            "default_branch": "main"
        }
        
        self.repositories[repo_name] = repository
        
        # Generate initial files
        initial_files = self._generate_initial_files(repo_config)
        
        return {
            "repository": repository,
            "initial_files": initial_files,
            "setup_instructions": self._generate_setup_instructions(repo_name),
            "ci_cd_ready": True,
            "documentation_generated": True,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }
    
    async def setup_ci_cd(self, repo_name: str, ci_config: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Enhanced mock CI/CD setup with comprehensive pipeline"""
        
        workflow_files = {
            "ci.yml": self._generate_ci_workflow(ci_config),
            "cd.yml": self._generate_cd_workflow(ci_config),
            "security.yml": self._generate_security_workflow(),
            "performance.yml": self._generate_performance_workflow()
        }
        
        return {
            "workflow_files": workflow_files,
            "pipeline_configuration": {
                "trigger_branches": ["main", "develop"],
                "test_environments": ["unit", "integration", "e2e"],
                "deployment_environments": ["staging", "production"],
                "security_checks": ["dependabot", "codeql", "secret-scanning"],
                "performance_monitoring": True,
                "notifications": ["slack", "email"]
            },
            "setup_status": "completed",
            "estimated_setup_time": "5 minutes",
            "next_steps": [
                "Review workflow configurations",
                "Test CI/CD pipeline",
                "Configure deployment secrets",
                "Set up monitoring and alerts"
            ],
            "repo_name": repo_name,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_status(self) -> Dict[str, Any]:
        """Enhanced mock status with development metrics"""
        return {
            "status": "operational",
            "version": "2.1.0",
            "repositories_managed": len(self.repositories),
            "code_generation_requests_today": 89,
            "success_rate": "97.8%",
            "average_response_time": "2.1s",
            "features": [
                "code_generation",
                "repository_management",
                "ci_cd_automation",
                "documentation_generation",
                "testing_framework",
                "deployment_automation"
            ],
            "integrations": {
                "github": "connected",
                "docker": "connected",
                "kubernetes": "connected",
                "aws": "connected",
                "azure": "connected"
            },
            "last_updated": datetime.now().isoformat()
        }
    
    def _determine_code_type(self, prompt: str) -> str:
        """Determine code type from prompt"""
        prompt_lower = prompt.lower()
        if "api" in prompt_lower or "endpoint" in prompt_lower:
            return "api"
        elif "frontend" in prompt_lower or "ui" in prompt_lower or "react" in prompt_lower:
            return "frontend"
        elif "database" in prompt_lower or "model" in prompt_lower or "schema" in prompt_lower:
            return "database"
        elif "microservice" in prompt_lower or "service" in prompt_lower:
            return "microservice"
        else:
            return "generic"
    
    def _get_api_template(self) -> str:
        """Get API code template"""
        return '''"""
API Implementation
Generated by GitHub Copilot - I PROACTIVE BRICK Orchestration
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import structlog

logger = structlog.get_logger(__name__)

app = FastAPI(title="BRICK API")

class {name}Request(BaseModel):
    """Request model"""
    data: str
    context: Optional[dict] = None

class {name}Response(BaseModel):
    """Response model"""
    result: str
    status: str
    timestamp: str

@app.post("/{endpoint}", response_model={name}Response)
async def process_{name}(
    request: {name}Request
):
    """Process {name} request"""
    try:
        logger.info("Processing {name} request", data=request.data)
        
        # Implementation logic here
        result = f"Processed: {{request.data}}"
        
        return {name}Response(
            result=result,
            status="success",
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error("Error processing {name}", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
'''
    
    def _get_frontend_template(self) -> str:
        """Get frontend code template"""
        return '''/**
 * Frontend Component
 * Generated by GitHub Copilot - I PROACTIVE BRICK Orchestration
 */

import React, {{ useState, useEffect }} from 'react';
import {{ Card, Button, Input, Alert }} from 'antd';

const {name}Component = () => {{
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (formData) => {{
        setLoading(true);
        setError(null);
        
        try {{
            const response = await fetch('/api/{endpoint}', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(formData)
            }});
            
            if (!response.ok) throw new Error('Request failed');
            
            const result = await response.json();
            setData(result);
        }} catch (err) {{
            setError(err.message);
        }} finally {{
            setLoading(false);
        }}
    }};

    return (
        <Card title="{name}" className="w-full max-w-2xl mx-auto">
            {{error && <Alert message={{error}} type="error" className="mb-4" />}}
            
            <div className="space-y-4">
                <Input
                    placeholder="Enter data for {name}"
                    onChange={{e => setData({{...data, input: e.target.value}})}}
                />
                
                <Button
                    type="primary"
                    loading={{loading}}
                    onClick={{() => handleSubmit(data)}}
                    className="w-full"
                >
                    Process {name}
                </Button>
                
                {{data && (
                    <div className="mt-4 p-4 bg-gray-50 rounded">
                        <h3>Result:</h3>
                        <pre>{{JSON.stringify(data, null, 2)}}</pre>
                    </div>
                )}}
            </div>
        </Card>
    );
}};

export default {name}Component;
'''
    
    def _get_database_template(self) -> str:
        """Get database code template"""
        return '''"""
Database Model
Generated by GitHub Copilot - I PROACTIVE BRICK Orchestration
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class {name}(Base):
    """Database model for {name}"""
    
    __tablename__ = '{table_name}'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    data = Column(Text, nullable=True)
    status = Column(String(50), default='active', index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True, index=True)
    
    def __repr__(self):
        return f"<{name}(id={{self.id}}, name='{{self.name}}')>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {{
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'data': self.data,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }}
'''
    
    def _get_microservice_template(self) -> str:
        """Get microservice code template"""
        return '''"""
Microservice Implementation
Generated by GitHub Copilot - I PROACTIVE BRICK Orchestration
"""

import asyncio
import structlog
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException

logger = structlog.get_logger(__name__)

app = FastAPI(title="{name} Microservice")

class {name}Service:
    """Main service class for {name}"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {{}}
        self.initialized = False
        
    async def initialize(self):
        """Initialize the {name} service"""
        try:
            logger.info("Initializing {name} service")
            # Initialization logic here
            self.initialized = True
            logger.info("{name} service initialized successfully")
        except Exception as e:
            logger.error("Failed to initialize {name} service", error=str(e))
            raise
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data for {name}"""
        if not self.initialized:
            raise RuntimeError("{name} service not initialized")
            
        try:
            logger.info("Processing {name} data", data_keys=list(data.keys()))
            
            # Processing logic here
            result = {{
                "processed_data": data,
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "service": "{name}"
            }}
            
            logger.info("{name} processing completed")
            return result
            
        except Exception as e:
            logger.error("Error processing {name}", error=str(e))
            raise
    
    async def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up {name} service")
        self.initialized = False

# Global service instance
service = {name}Service()

@app.on_event("startup")
async def startup_event():
    await service.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    await service.cleanup()

@app.post("/process")
async def process_data(data: Dict[str, Any]):
    """Process data endpoint"""
    try:
        result = await service.process(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {{"status": "healthy", "service": "{name}"}}
'''
    
    def _get_generic_template(self) -> str:
        """Get generic code template"""
        return '''"""
Generic Implementation
Generated by GitHub Copilot - I PROACTIVE BRICK Orchestration
"""

import asyncio
import structlog
from datetime import datetime
from typing import Dict, Any, Optional

logger = structlog.get_logger(__name__)

class {name}:
    """Main class for {name} functionality"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {{}}
        self.initialized = False
        
    async def initialize(self):
        """Initialize the {name} system"""
        try:
            logger.info("Initializing {name}")
            # Initialization logic here
            self.initialized = True
            logger.info("{name} initialized successfully")
        except Exception as e:
            logger.error("Failed to initialize {name}", error=str(e))
            raise
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data for {name}"""
        if not self.initialized:
            raise RuntimeError("{name} not initialized")
            
        try:
            logger.info("Processing {name} data", data_keys=list(data.keys()))
            
            # Processing logic here
            result = {{
                "processed_data": data,
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "name": "{name}"
            }}
            
            logger.info("{name} processing completed")
            return result
            
        except Exception as e:
            logger.error("Error processing {name}", error=str(e))
            raise
    
    async def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up {name}")
        self.initialized = False

# Factory function
async def create_{name.lower()}(config: Optional[Dict[str, Any]] = None):
    """Factory function to create {name} instance"""
    instance = {name}(config)
    await instance.initialize()
    return instance
'''
    
    def _generate_code_from_template(self, template: str, prompt: str, context: Dict[str, Any]) -> str:
        """Generate code from template with prompt context"""
        # Extract name and endpoint from prompt
        name = self._extract_name_from_prompt(prompt)
        endpoint = name.lower().replace(' ', '-')
        table_name = name.lower().replace(' ', '_')
        
        # Replace placeholders in template
        code = template.format(
            name=name,
            endpoint=endpoint,
            table_name=table_name
        )
        
        return code
    
    def _extract_name_from_prompt(self, prompt: str) -> str:
        """Extract name from prompt"""
        # Simple extraction - in real implementation, this would be more sophisticated
        words = prompt.split()
        if len(words) > 0:
            return words[0].title()
        return "GeneratedComponent"
    
    def _determine_language(self, prompt: str) -> str:
        """Determine programming language from prompt"""
        prompt_lower = prompt.lower()
        if "python" in prompt_lower or "fastapi" in prompt_lower:
            return "Python"
        elif "javascript" in prompt_lower or "react" in prompt_lower or "node" in prompt_lower:
            return "JavaScript"
        elif "typescript" in prompt_lower:
            return "TypeScript"
        elif "java" in prompt_lower:
            return "Java"
        elif "go" in prompt_lower or "golang" in prompt_lower:
            return "Go"
        else:
            return "Python"  # Default
    
    def _determine_framework(self, prompt: str) -> str:
        """Determine framework from prompt"""
        prompt_lower = prompt.lower()
        if "fastapi" in prompt_lower:
            return "FastAPI"
        elif "react" in prompt_lower:
            return "React"
        elif "django" in prompt_lower:
            return "Django"
        elif "flask" in prompt_lower:
            return "Flask"
        elif "express" in prompt_lower:
            return "Express.js"
        else:
            return "FastAPI"  # Default
    
    def _identify_dependencies(self, prompt: str) -> List[str]:
        """Identify required dependencies"""
        deps = []
        prompt_lower = prompt.lower()
        
        if "api" in prompt_lower:
            deps.extend(["fastapi", "uvicorn", "pydantic"])
        if "database" in prompt_lower:
            deps.extend(["sqlalchemy", "asyncpg", "alembic"])
        if "frontend" in prompt_lower or "react" in prompt_lower:
            deps.extend(["react", "antd", "axios"])
        if "ai" in prompt_lower or "ml" in prompt_lower:
            deps.extend(["openai", "anthropic", "crewai"])
        if "monitoring" in prompt_lower:
            deps.extend(["prometheus-client", "structlog"])
        
        return deps
    
    def _generate_documentation(self, prompt: str, code: str) -> str:
        """Generate documentation for code"""
        return f'''# Generated Code Documentation

## Overview
This code was generated based on the prompt: "{prompt}"

## Features
- Automated code generation
- Best practices implementation
- Error handling
- Logging and monitoring
- Type hints and validation

## Usage
```python
# Example usage
instance = create_{self._extract_name_from_prompt(prompt).lower()}()
result = await instance.process({{"data": "example"}})
```

## API Endpoints
- POST /process - Process data
- GET /health - Health check

## Configuration
Set environment variables for configuration:
- DATABASE_URL
- API_KEY
- LOG_LEVEL

## Testing
Run tests with:
```bash
pytest tests/ -v
```

## Deployment
Deploy using Docker:
```bash
docker build -t {self._extract_name_from_prompt(prompt).lower()} .
docker run -p 8000:8000 {self._extract_name_from_prompt(prompt).lower()}
```
'''
    
    def _generate_tests(self, code: str) -> str:
        """Generate tests for code"""
        return f'''"""
Tests for generated code
"""

import pytest
import asyncio
from unittest.mock import Mock, patch

class TestGeneratedCode:
    """Test suite for generated code"""
    
    @pytest.mark.asyncio
    async def test_initialization(self):
        """Test proper initialization"""
        # Test implementation here
        assert True
    
    @pytest.mark.asyncio
    async def test_processing(self):
        """Test data processing"""
        # Test implementation here
        assert True
    
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling"""
        # Test implementation here
        assert True
    
    @pytest.mark.asyncio
    async def test_cleanup(self):
        """Test cleanup functionality"""
        # Test implementation here
        assert True
'''
    
    def _generate_deployment_instructions(self, prompt: str) -> str:
        """Generate deployment instructions"""
        return f'''
Deployment Instructions:

1. **Environment Setup**:
   - Python 3.11+
   - Docker and Docker Compose
   - Required environment variables

2. **Build and Deploy**:
   ```bash
   docker build -t generated-app .
   docker-compose up -d
   ```

3. **Health Check**:
   ```bash
   curl http://localhost:8000/health
   ```

4. **Monitoring**:
   - Check logs: docker-compose logs -f
   - Monitor metrics: http://localhost:9090/metrics
'''
    
    def _analyze_complexity(self, code: str) -> Dict[str, Any]:
        """Analyze code complexity"""
        lines = code.count('\n')
        functions = code.count('def ')
        classes = code.count('class ')
        
        return {
            "lines_of_code": lines,
            "functions": functions,
            "classes": classes,
            "complexity_score": min(10, (lines / 50) + (functions / 5) + (classes / 2)),
            "maintainability": "good" if lines < 200 else "moderate"
        }
    
    def _identify_security_issues(self, code: str) -> List[str]:
        """Identify potential security issues"""
        issues = []
        
        if "sql" in code.lower() and "parameterized" not in code.lower():
            issues.append("Potential SQL injection vulnerability")
        if "password" in code.lower() and "hash" not in code.lower():
            issues.append("Password should be hashed")
        if "api" in code.lower() and "authentication" not in code.lower():
            issues.append("API should include authentication")
        
        return issues
    
    def _generate_performance_notes(self, code: str) -> str:
        """Generate performance notes"""
        return """
Performance Considerations:

1. **Database Queries**:
   - Use connection pooling
   - Implement query optimization
   - Add proper indexing

2. **API Performance**:
   - Implement caching
   - Use async/await patterns
   - Add rate limiting

3. **Memory Management**:
   - Monitor memory usage
   - Implement garbage collection
   - Use efficient data structures

4. **Monitoring**:
   - Track response times
   - Monitor resource usage
   - Set up alerts
"""
    
    def _generate_initial_files(self, repo_config: Dict[str, Any]) -> Dict[str, str]:
        """Generate initial repository files"""
        return {
            "README.md": f"# {repo_config.get('name', 'BRICK Repository')}\n\nGenerated by GitHub Copilot Workspace",
            "requirements.txt": "fastapi==0.104.1\nuvicorn[standard]==0.24.0\npydantic==2.5.0",
            "Dockerfile": "FROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]",
            "docker-compose.yml": "version: '3.8'\nservices:\n  app:\n    build: .\n    ports:\n      - '8000:8000'\n    environment:\n      - ENVIRONMENT=production",
            ".gitignore": "*.pyc\n__pycache__/\n.env\n.venv/\nnode_modules/\n*.log"
        }
    
    def _generate_setup_instructions(self, repo_name: str) -> str:
        """Generate setup instructions for repository"""
        return f"""
Setup Instructions for {repo_name}:

1. **Clone Repository**:
   ```bash
   git clone https://github.com/brick-orchestration/{repo_name}.git
   cd {repo_name}
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run Application**:
   ```bash
   uvicorn main:app --reload
   ```

5. **Access Application**:
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
"""
    
    def _generate_ci_workflow(self, ci_config: Dict[str, Any]) -> str:
        """Generate CI workflow"""
        return """name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest tests/ -v
    - name: Run linting
      run: |
        black --check .
        isort --check-only .
    - name: Security scan
      run: |
        bandit -r . -f json -o bandit-report.json
"""
    
    def _generate_cd_workflow(self, ci_config: Dict[str, Any]) -> str:
        """Generate CD workflow"""
        return """name: CD Pipeline

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    needs: test
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to staging
      run: |
        echo "Deploying to staging environment..."
    - name: Run integration tests
      run: |
        echo "Running integration tests..."
    - name: Deploy to production
      if: success()
      run: |
        echo "Deploying to production environment..."
"""
    
    def _generate_security_workflow(self) -> str:
        """Generate security workflow"""
        return """name: Security Scan

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  push:
    branches: [ main ]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Run security scan
      run: |
        bandit -r . -f json -o bandit-report.json
    - name: Dependency check
      run: |
        safety check
    - name: Upload security report
      uses: actions/upload-artifact@v3
      with:
        name: security-report
        path: bandit-report.json
"""
    
    def _generate_performance_workflow(self) -> str:
        """Generate performance workflow"""
        return """name: Performance Test

on:
  schedule:
    - cron: '0 3 * * *'  # Daily at 3 AM

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run performance tests
      run: |
        pytest tests/performance/ -v
    - name: Generate performance report
      run: |
        echo "Performance test completed"
"""
