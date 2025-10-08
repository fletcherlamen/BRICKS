"""
CrewAI Service Integration
Handles multi-agent orchestration using CrewAI framework
"""

from typing import Dict, List, Optional, Any
import structlog
from datetime import datetime

from app.core.config import settings
from app.core.exceptions import CrewAIError

logger = structlog.get_logger(__name__)


class CrewAIService:
    """CrewAI service for multi-agent orchestration"""
    
    def __init__(self):
        self.initialized = False
        self.crew = None
        self.agents = {}
        
    async def initialize(self):
        """Initialize CrewAI service"""
        try:
            # Import CrewAI components
            try:
                from crewai import Agent, Task, Crew, Process
                from crewai.tools import BaseTool
            except ImportError as e:
                logger.warning("CrewAI not available, running in mock mode", error=str(e))
                self.initialized = False
                return
            
            # Check if API key is configured (optional for mock mode)
            if not settings.CREWAI_API_KEY:
                logger.warning("CrewAI API key not configured, running in mock mode")
                self.initialized = False
                return
            
            # Create specialized agents for BRICK orchestration
            await self._create_agents()
            await self._create_crew()
            
            self.initialized = True
            logger.info("CrewAI service initialized successfully")
            
        except Exception as e:
            logger.warning("Failed to initialize CrewAI service, running in mock mode", error=str(e))
            self.initialized = False
    
    async def _create_agents(self):
        """Create specialized agents for different roles"""
        
        from crewai import Agent
        
        # Strategic Analyst Agent
        self.agents["strategic_analyst"] = Agent(
            role="Strategic Business Analyst",
            goal="Analyze business opportunities and provide strategic insights for BRICK development",
            backstory="""You are an expert strategic business analyst with deep experience in 
            technology ecosystems and revenue optimization. You excel at identifying opportunities 
            and gaps in business capabilities.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Technical Architect Agent
        self.agents["technical_architect"] = Agent(
            role="Technical Architecture Specialist",
            goal="Design and plan technical implementations for BRICK systems",
            backstory="""You are a senior technical architect with expertise in system design, 
            API integration, and scalable software architecture. You focus on creating robust, 
            maintainable technical solutions.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Revenue Optimization Agent
        self.agents["revenue_optimizer"] = Agent(
            role="Revenue Optimization Specialist",
            goal="Identify and analyze revenue opportunities in business systems",
            backstory="""You are a business intelligence expert specializing in revenue optimization 
            and financial analysis. You excel at connecting technical capabilities to business value 
            and revenue streams.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Integration Specialist Agent
        self.agents["integration_specialist"] = Agent(
            role="System Integration Specialist",
            goal="Plan and execute integrations between different systems and services",
            backstory="""You are an expert in system integration with deep knowledge of APIs, 
            data flows, and service orchestration. You ensure seamless connectivity between 
            different business systems.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Quality Assurance Agent
        self.agents["qa_specialist"] = Agent(
            role="Quality Assurance Specialist",
            goal="Ensure high quality and reliability of BRICK implementations",
            backstory="""You are a meticulous quality assurance expert with experience in testing, 
            validation, and quality control. You ensure that all implementations meet high standards 
            of reliability and performance.""",
            verbose=True,
            allow_delegation=False
        )
    
    async def _create_crew(self):
        """Create the main crew with all agents"""
        
        from crewai import Crew, Process
        
        self.crew = Crew(
            agents=list(self.agents.values()),
            process=Process.sequential,
            verbose=True,
            memory=True
        )
    
    async def analyze_strategic_opportunity(
        self,
        goal: str,
        context: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Analyze strategic opportunities using CrewAI"""
        
        if not self.initialized:
            # Return mock response when CrewAI is not available
            return {
                "analysis": f"Mock strategic analysis for: {goal}\n\nContext: {context}\n\nThis is a mock response since CrewAI is not available. In a real implementation, this would provide comprehensive strategic analysis with actionable recommendations.",
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "agent_used": "strategic_analyst_mock",
                "mock": True
            }
        
        try:
            from crewai import Task
            
            # Create strategic analysis task
            strategic_task = Task(
                description=f"""
                Analyze the strategic opportunity: {goal}
                
                Context: {context}
                
                Please provide:
                1. Strategic analysis of the opportunity
                2. Potential revenue impact
                3. Required resources and timeline
                4. Risk assessment
                5. Implementation recommendations
                """,
                agent=self.agents["strategic_analyst"],
                expected_output="Comprehensive strategic analysis with actionable recommendations"
            )
            
            # Execute the task
            result = self.crew.kickoff(inputs={"goal": goal, "context": str(context)})
            
            return {
                "analysis": str(result),
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "agent_used": "strategic_analyst"
            }
            
        except Exception as e:
            logger.error("Strategic analysis failed", error=str(e), session_id=session_id)
            raise CrewAIError(f"Strategic analysis failed: {str(e)}")
    
    async def plan_brick_development(
        self,
        goal: str,
        context: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Plan BRICK development using CrewAI"""
        
        if not self.initialized:
            # Return mock response when CrewAI is not available
            return {
                "development_plan": f"Mock development plan for: {goal}\n\nContext: {context}\n\nThis is a mock response since CrewAI is not available. In a real implementation, this would provide detailed development plan with technical specifications.",
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "agent_used": "technical_architect_mock",
                "mock": True
            }
        
        try:
            from crewai import Task
            
            # Create development planning task
            planning_task = Task(
                description=f"""
                Plan the development of a BRICK for: {goal}
                
                Context: {context}
                
                Please provide:
                1. Technical architecture design
                2. Development phases and timeline
                3. Required integrations
                4. Testing strategy
                5. Deployment plan
                """,
                agent=self.agents["technical_architect"],
                expected_output="Detailed development plan with technical specifications"
            )
            
            # Execute the task
            result = self.crew.kickoff(inputs={"goal": goal, "context": str(context)})
            
            return {
                "development_plan": str(result),
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "agent_used": "technical_architect"
            }
            
        except Exception as e:
            logger.error("Development planning failed", error=str(e), session_id=session_id)
            raise CrewAIError(f"Development planning failed: {str(e)}")
    
    async def analyze_revenue_opportunities(
        self,
        goal: str,
        context: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Analyze revenue opportunities using CrewAI"""
        
        if not self.initialized:
            # Return mock response when CrewAI is not available
            return {
                "revenue_analysis": f"Mock revenue analysis for: {goal}\n\nContext: {context}\n\nThis is a mock response since CrewAI is not available. In a real implementation, this would provide comprehensive revenue opportunity analysis with financial projections.",
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "agent_used": "revenue_optimizer_mock",
                "mock": True
            }
        
        try:
            from crewai import Task
            
            # Create revenue analysis task
            revenue_task = Task(
                description=f"""
                Analyze revenue opportunities for: {goal}
                
                Context: {context}
                
                Please provide:
                1. Revenue potential analysis
                2. Market opportunity assessment
                3. Pricing strategy recommendations
                4. Revenue stream identification
                5. Financial projections
                """,
                agent=self.agents["revenue_optimizer"],
                expected_output="Comprehensive revenue opportunity analysis with financial projections"
            )
            
            # Execute the task
            result = self.crew.kickoff(inputs={"goal": goal, "context": str(context)})
            
            return {
                "revenue_analysis": str(result),
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "agent_used": "revenue_optimizer"
            }
            
        except Exception as e:
            logger.error("Revenue analysis failed", error=str(e), session_id=session_id)
            raise CrewAIError(f"Revenue analysis failed: {str(e)}")
    
    async def identify_strategic_gaps(
        self,
        goal: str,
        context: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Identify strategic gaps using CrewAI"""
        
        if not self.initialized:
            # Return mock response when CrewAI is not available
            return {
                "gap_analysis": f"Mock gap analysis for: {goal}\n\nContext: {context}\n\nThis is a mock response since CrewAI is not available. In a real implementation, this would provide strategic gap analysis with prioritized recommendations.",
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "agent_used": "strategic_analyst_mock",
                "mock": True
            }
        
        try:
            from crewai import Task
            
            # Create gap analysis task
            gap_task = Task(
                description=f"""
                Identify strategic gaps for: {goal}
                
                Context: {context}
                
                Please provide:
                1. Current capability assessment
                2. Identified gaps and weaknesses
                3. Priority ranking of gaps
                4. Recommended solutions
                5. Implementation roadmap
                """,
                agent=self.agents["strategic_analyst"],
                expected_output="Strategic gap analysis with prioritized recommendations"
            )
            
            # Execute the task
            result = self.crew.kickoff(inputs={"goal": goal, "context": str(context)})
            
            return {
                "gap_analysis": str(result),
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "agent_used": "strategic_analyst"
            }
            
        except Exception as e:
            logger.error("Gap analysis failed", error=str(e), session_id=session_id)
            raise CrewAIError(f"Gap analysis failed: {str(e)}")
    
    async def generic_analysis(
        self,
        goal: str,
        context: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Perform generic analysis using CrewAI"""
        
        if not self.initialized:
            # Return mock response when CrewAI is not available
            return {
                "analysis": f"Mock generic analysis for: {goal}\n\nContext: {context}\n\nThis is a mock response since CrewAI is not available. In a real implementation, this would provide comprehensive analysis and recommendations.",
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "agent_used": "strategic_analyst_mock",
                "mock": True
            }
        
        try:
            from crewai import Task
            
            # Create generic analysis task
            analysis_task = Task(
                description=f"""
                Perform comprehensive analysis for: {goal}
                
                Context: {context}
                
                Please provide detailed analysis and recommendations.
                """,
                agent=self.agents["strategic_analyst"],
                expected_output="Comprehensive analysis and recommendations"
            )
            
            # Execute the task
            result = self.crew.kickoff(inputs={"goal": goal, "context": str(context)})
            
            return {
                "analysis": str(result),
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "agent_used": "strategic_analyst"
            }
            
        except Exception as e:
            logger.error("Generic analysis failed", error=str(e), session_id=session_id)
            raise CrewAIError(f"Generic analysis failed: {str(e)}")
    
    async def get_status(self) -> Dict[str, Any]:
        """Get CrewAI service status"""
        
        if not settings.CREWAI_API_KEY:
            return {
                "status": "critical",
                "mode": "mock",
                "api_key_configured": False,
                "message": "API key not configured - service not operational",
                "error": "Missing CREWAI_API_KEY"
            }
        
        if not self.initialized:
            return {
                "status": "error",
                "mode": "failed",
                "api_key_configured": True,
                "message": "Service initialization failed",
                "error": "Failed to initialize CrewAI service"
            }
        
        return {
            "status": "healthy",
            "mode": "real_ai",
            "agents_count": len(self.agents),
            "crew_initialized": self.crew is not None,
            "api_key_configured": True
        }
    
    async def cleanup(self):
        """Cleanup CrewAI resources"""
        try:
            self.crew = None
            self.agents = {}
            self.initialized = False
            logger.info("CrewAI service cleaned up")
        except Exception as e:
            logger.error("Error cleaning up CrewAI service", error=str(e))
