"""
Core orchestration service that coordinates multiple AI systems.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import structlog

import httpx

# AI libraries - import with fallback
try:
    from crewai import Agent, Task, Crew, Process
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    print("Warning: CrewAI not available, using mock implementation")

try:
    from mem0 import Memory
    MEM0_AVAILABLE = True
except ImportError:
    MEM0_AVAILABLE = False
    print("Warning: Mem0.ai not available, using local memory implementation")

from app.core.config import settings
from app.models.orchestration import OrchestrationSession, OrchestrationTask, AICollaboration
from app.models.analytics import PerformanceMetrics, SystemHealth
from app.core.database import AsyncSessionLocal

logger = structlog.get_logger()


class OrchestrationService:
    """Main orchestration service for coordinating AI systems."""
    
    def __init__(self):
        self.memory_client = None
        self.crewai_agents = {}
        self.active_sessions = {}
        self.system_health = {}
    
    async def initialize(self):
        """Initialize all AI systems and services."""
        try:
            # Initialize Mem0.ai
            await self._initialize_mem0()
            
            # Initialize CrewAI agents
            await self._initialize_crewai()
            
            # Initialize system health monitoring
            await self._initialize_health_monitoring()
            
            logger.info("Orchestration service initialized successfully")
            
        except Exception as e:
            logger.error("Failed to initialize orchestration service", error=str(e))
            raise
    
    async def _initialize_mem0(self):
        """Initialize Mem0.ai memory system."""
        if not MEM0_AVAILABLE:
            logger.warning("Mem0.ai not available, using local memory")
            self.memory_client = LocalMemory()
            return
            
        try:
            if settings.MEM0_API_KEY:
                self.memory_client = Memory(
                    api_key=settings.MEM0_API_KEY,
                    project_id=settings.MEM0_PROJECT_ID
                )
                logger.info("Mem0.ai initialized successfully")
            else:
                logger.warning("Mem0.ai API key not provided, using local memory")
                # Fallback to local memory implementation
                self.memory_client = LocalMemory()
                
        except Exception as e:
            logger.error("Failed to initialize Mem0.ai", error=str(e))
            self.memory_client = LocalMemory()  # Fallback
    
    async def _initialize_crewai(self):
        """Initialize CrewAI agents for different roles."""
        if not CREWAI_AVAILABLE:
            logger.warning("CrewAI not available, using mock agents")
            self.crewai_agents = {
                'strategic_analyst': MockAgent('Strategic BRICKS Analyst'),
                'technical_implementer': MockAgent('Technical Implementation Specialist'),
                'revenue_optimizer': MockAgent('Revenue Optimization Expert')
            }
            return
            
        try:
            # Strategic Analyst Agent
            self.crewai_agents['strategic_analyst'] = Agent(
                role='Strategic BRICKS Analyst',
                goal='Analyze BRICKS roadmap and identify strategic opportunities',
                backstory='You are an expert business strategist focused on BRICKS development and revenue optimization.',
                verbose=settings.CREWAI_VERBOSE,
                allow_delegation=False
            )
            
            # Technical Implementation Agent
            self.crewai_agents['technical_implementer'] = Agent(
                role='Technical Implementation Specialist',
                goal='Implement technical solutions and coordinate with development systems',
                backstory='You are a technical expert who bridges strategic vision with practical implementation.',
                verbose=settings.CREWAI_VERBOSE,
                allow_delegation=False
            )
            
            # Revenue Optimization Agent
            self.crewai_agents['revenue_optimizer'] = Agent(
                role='Revenue Optimization Expert',
                goal='Identify and maximize revenue opportunities from BRICKS development',
                backstory='You specialize in connecting technical capabilities to business value and revenue streams.',
                verbose=settings.CREWAI_VERBOSE,
                allow_delegation=False
            )
            
            logger.info("CrewAI agents initialized successfully")
            
        except Exception as e:
            logger.error("Failed to initialize CrewAI agents", error=str(e))
            raise
    
    async def _initialize_health_monitoring(self):
        """Initialize system health monitoring."""
        self.system_health = {
            'crewai': {'status': 'healthy', 'last_check': datetime.now()},
            'mem0': {'status': 'healthy', 'last_check': datetime.now()},
            'orchestrator': {'status': 'healthy', 'last_check': datetime.now()}
        }
    
    async def start_orchestration_session(self, session_name: str, context: Dict[str, Any]) -> str:
        """Start a new orchestration session."""
        try:
            # Create session in database
            async with AsyncSessionLocal() as db:
                session = OrchestrationSession(
                    session_name=session_name,
                    status="active"
                )
                db.add(session)
                await db.commit()
                await db.refresh(session)
                
                # Store context in memory
                await self._store_context(session.id, context)
                
                # Track in active sessions
                self.active_sessions[str(session.id)] = {
                    'session': session,
                    'context': context,
                    'started_at': datetime.now()
                }
                
                logger.info("Started orchestration session", session_id=str(session.id))
                return str(session.id)
                
        except Exception as e:
            logger.error("Failed to start orchestration session", error=str(e))
            raise
    
    async def execute_strategic_analysis(self, session_id: str, analysis_type: str) -> Dict[str, Any]:
        """Execute strategic analysis using CrewAI agents."""
        try:
            start_time = datetime.now()
            
            if not CREWAI_AVAILABLE:
                # Use mock analysis when CrewAI is not available
                result = await self.crewai_agents['strategic_analyst'].execute_task(
                    f"Perform {analysis_type} analysis for BRICKS development strategy"
                )
            else:
                # Create analysis task
                task = Task(
                    description=f"Perform {analysis_type} analysis for BRICKS development strategy",
                    agent=self.crewai_agents['strategic_analyst'],
                    expected_output="Detailed strategic analysis with actionable recommendations"
                )
                
                # Create crew for this analysis
                crew = Crew(
                    agents=[self.crewai_agents['strategic_analyst']],
                    tasks=[task],
                    process=Process.sequential,
                    verbose=settings.CREWAI_VERBOSE
                )
                
                # Execute the analysis
                result = crew.kickoff()
            
            end_time = datetime.now()
            
            # Log AI collaboration
            await self._log_ai_collaboration(
                session_id,
                "crewai",
                "orchestrator",
                "analysis_complete",
                f"Strategic analysis completed: {analysis_type}"
            )
            
            # Store result in memory
            await self._store_analysis_result(session_id, analysis_type, result)
            
            # Track performance metrics
            await self._track_performance_metric(
                "crewai",
                "analysis_duration",
                (end_time - start_time).total_seconds(),
                "seconds"
            )
            
            return {
                "session_id": session_id,
                "analysis_type": analysis_type,
                "result": result,
                "duration_seconds": (end_time - start_time).total_seconds(),
                "timestamp": end_time.isoformat()
            }
            
        except Exception as e:
            logger.error("Failed to execute strategic analysis", error=str(e))
            raise
    
    async def _store_context(self, session_id: str, context: Dict[str, Any]):
        """Store session context in memory."""
        if self.memory_client:
            try:
                await self.memory_client.add(
                    f"Session {session_id} context",
                    json.dumps(context)
                )
            except Exception as e:
                logger.error("Failed to store context in memory", error=str(e))
    
    async def _store_analysis_result(self, session_id: str, analysis_type: str, result: Any):
        """Store analysis result in memory."""
        if self.memory_client:
            try:
                await self.memory_client.add(
                    f"Session {session_id} {analysis_type} result",
                    str(result)
                )
            except Exception as e:
                logger.error("Failed to store analysis result in memory", error=str(e))
    
    async def _log_ai_collaboration(self, session_id: str, from_ai: str, to_ai: str, message_type: str, content: str):
        """Log AI-to-AI collaboration."""
        try:
            async with AsyncSessionLocal() as db:
                collaboration = AICollaboration(
                    session_id=session_id,
                    from_ai=from_ai,
                    to_ai=to_ai,
                    message_type=message_type,
                    content=content
                )
                db.add(collaboration)
                await db.commit()
                
        except Exception as e:
            logger.error("Failed to log AI collaboration", error=str(e))
    
    async def _track_performance_metric(self, system_name: str, metric_name: str, value: float, unit: str = None):
        """Track performance metrics."""
        try:
            async with AsyncSessionLocal() as db:
                metric = PerformanceMetrics(
                    system_name=system_name,
                    metric_name=metric_name,
                    metric_value=value,
                    unit=unit
                )
                db.add(metric)
                await db.commit()
                
        except Exception as e:
            logger.error("Failed to track performance metric", error=str(e))
    
    async def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get status of orchestration session."""
        try:
            async with AsyncSessionLocal() as db:
                session = await db.get(OrchestrationSession, session_id)
                if not session:
                    raise ValueError(f"Session {session_id} not found")
                
                # Get recent collaborations
                collaborations = await db.execute(
                    AICollaboration.__table__.select()
                    .where(AICollaboration.session_id == session_id)
                    .order_by(AICollaboration.timestamp.desc())
                    .limit(10)
                )
                
                return {
                    "session_id": str(session.id),
                    "session_name": session.session_name,
                    "status": session.status,
                    "created_at": session.created_at.isoformat(),
                    "updated_at": session.updated_at.isoformat() if session.updated_at else None,
                    "recent_collaborations": [
                        {
                            "from_ai": col.from_ai,
                            "to_ai": col.to_ai,
                            "message_type": col.message_type,
                            "content": col.content,
                            "timestamp": col.timestamp.isoformat()
                        }
                        for col in collaborations.fetchall()
                    ]
                }
                
        except Exception as e:
            logger.error("Failed to get session status", error=str(e))
            raise
    
    async def shutdown(self):
        """Shutdown orchestration service."""
        try:
            # Close active sessions
            for session_id in list(self.active_sessions.keys()):
                await self._close_session(session_id)
            
            logger.info("Orchestration service shutdown complete")
            
        except Exception as e:
            logger.error("Error during orchestration service shutdown", error=str(e))
    
    async def _close_session(self, session_id: str):
        """Close an orchestration session."""
        try:
            async with AsyncSessionLocal() as db:
                session = await db.get(OrchestrationSession, session_id)
                if session:
                    session.status = "completed"
                    session.completed_at = datetime.now()
                    await db.commit()
            
            # Remove from active sessions
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
                
        except Exception as e:
            logger.error("Failed to close session", session_id=session_id, error=str(e))


class LocalMemory:
    """Local memory implementation as fallback when Mem0.ai is not available."""
    
    def __init__(self):
        self.memory_store = {}
    
    async def add(self, key: str, content: str):
        """Add content to local memory."""
        self.memory_store[key] = {
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
    
    async def search(self, query: str):
        """Search local memory."""
        # Simple keyword matching for fallback
        results = []
        for key, value in self.memory_store.items():
            if query.lower() in key.lower() or query.lower() in value["content"].lower():
                results.append({"key": key, "content": value["content"]})
        return results


class MockAgent:
    """Mock agent implementation when CrewAI is not available."""
    
    def __init__(self, role: str):
        self.role = role
        self.goal = f"Mock implementation for {role}"
        self.backstory = f"Mock agent for {role}"
    
    async def execute_task(self, task_description: str):
        """Mock task execution."""
        return f"Mock analysis from {self.role}: {task_description} - This is a placeholder response while CrewAI is being set up."
