"""
AI Orchestrator - Core orchestration intelligence
Coordinates multiple AI systems for strategic BRICKS development
"""

from typing import Dict, List, Optional, Any
import asyncio
import structlog
from datetime import datetime

from app.core.config import settings
from app.core.exceptions import AIOrchestrationError, CrewAIError, Mem0Error, DevinAIError
from app.services.crewai_service import CrewAIService
from app.services.mem0_service import Mem0Service
from app.services.devin_service import DevinService
from app.services.copilot_service import CopilotService
from app.services.github_copilot_service import GitHubCopilotService
from app.services.multi_model_router import MultiModelRouter
# Phase 3 - Strategic Intelligence Services
from app.services.bricks_context_service import BRICKSContextService
from app.services.revenue_analysis_service import RevenueAnalysisService
from app.services.strategic_gap_service import StrategicGapService
from app.services.brick_priority_service import BRICKPriorityService
from app.services.constraint_prediction_service import ConstraintPredictionService
from app.services.strategic_intelligence_service import StrategicIntelligenceService
from app.services.human_ai_collaboration_service import HumanAICollaborationService
# Phase 4 - Revenue Integration Loop Services
from app.services.church_kit_connector import ChurchKitConnector
from app.services.global_sky_connector import GlobalSkyConnector
from app.services.treasury_optimizer import TreasuryOptimizer
from app.services.autonomous_brick_proposer import AutonomousBRICKProposer

logger = structlog.get_logger(__name__)


class AIOrchestrator:
    """Main orchestrator for coordinating AI systems"""
    
    def __init__(self):
        # Phase 2 Services
        self.crewai_service: Optional[CrewAIService] = None
        self.mem0_service: Optional[Mem0Service] = None
        self.devin_service: Optional[DevinService] = None
        self.copilot_service: Optional[CopilotService] = None
        self.github_copilot_service: Optional[GitHubCopilotService] = None
        self.multi_model_router: Optional[MultiModelRouter] = None
        
        # Phase 3 Services - Strategic Intelligence Layer
        self.bricks_context_service: Optional[BRICKSContextService] = None
        self.revenue_analysis_service: Optional[RevenueAnalysisService] = None
        self.strategic_gap_service: Optional[StrategicGapService] = None
        self.brick_priority_service: Optional[BRICKPriorityService] = None
        self.constraint_prediction_service: Optional[ConstraintPredictionService] = None
        self.strategic_intelligence_service: Optional[StrategicIntelligenceService] = None
        self.human_ai_collaboration_service: Optional[HumanAICollaborationService] = None
        
        # Phase 4 Services - Revenue Integration Loop
        self.church_kit_connector: Optional[ChurchKitConnector] = None
        self.global_sky_connector: Optional[GlobalSkyConnector] = None
        self.treasury_optimizer: Optional[TreasuryOptimizer] = None
        self.autonomous_brick_proposer: Optional[AutonomousBRICKProposer] = None
        
        self.initialized = False
        
    async def initialize(self):
        """Initialize all AI services"""
        try:
            logger.info("Initializing AI Orchestrator")
            
            # PHASE 1: Initialize core AI services first (these are dependencies)
            core_tasks = []
            
            if settings.CREWAI_API_KEY:
                core_tasks.append(self._init_crewai())
            if settings.MEM0_API_KEY:
                core_tasks.append(self._init_mem0())
            if settings.DEVIN_API_KEY:
                core_tasks.append(self._init_devin())
            if settings.COPILOT_STUDIO_API_KEY:
                core_tasks.append(self._init_copilot())
            if settings.GITHUB_COPILOT_TOKEN:
                core_tasks.append(self._init_github_copilot())
            
            # Initialize multi-model router FIRST (critical dependency)
            await self._init_multi_model_router()
            logger.info("✅ Multi-Model Router initialized (with Real AI support)")
            
            # Wait for core services
            if core_tasks:
                await asyncio.gather(*core_tasks, return_exceptions=True)
            
            # PHASE 2: Initialize services that depend on Multi-Model Router
            dependent_tasks = []
            
            # Phase 3 - Strategic Intelligence Services (need multi-model router)
            dependent_tasks.append(self._init_bricks_context())
            dependent_tasks.append(self._init_revenue_analysis())
            dependent_tasks.append(self._init_strategic_gap())
            dependent_tasks.append(self._init_brick_priority())
            dependent_tasks.append(self._init_constraint_prediction())
            dependent_tasks.append(self._init_human_ai_collaboration())
            dependent_tasks.append(self._init_strategic_intelligence())
            
            # Phase 4 - Revenue Integration Loop (need multi-model router)
            dependent_tasks.append(self._init_church_kit_connector())
            dependent_tasks.append(self._init_global_sky_connector())
            dependent_tasks.append(self._init_treasury_optimizer())
            dependent_tasks.append(self._init_autonomous_brick_proposer())
            
            # Wait for all dependent services to initialize
            results = await asyncio.gather(*dependent_tasks, return_exceptions=True)
            
            # Check for initialization errors
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Service initialization failed", error=str(result))
                    raise result
            
            self.initialized = True
            logger.info("AI Orchestrator initialized successfully")
            
        except Exception as e:
            logger.error("Failed to initialize AI Orchestrator", error=str(e))
            raise AIOrchestrationError(f"Failed to initialize orchestrator: {str(e)}")
    
    async def _init_crewai(self):
        """Initialize CrewAI service"""
        try:
            self.crewai_service = CrewAIService()
            await self.crewai_service.initialize()
            logger.info("CrewAI service initialized")
        except Exception as e:
            raise CrewAIError(f"Failed to initialize CrewAI: {str(e)}")
    
    async def _init_mem0(self):
        """Initialize Mem0 service"""
        try:
            self.mem0_service = Mem0Service()
            await self.mem0_service.initialize()
            logger.info("Mem0 service initialized")
        except Exception as e:
            raise Mem0Error(f"Failed to initialize Mem0: {str(e)}")
    
    async def _init_devin(self):
        """Initialize Devin AI service"""
        try:
            self.devin_service = DevinService()
            await self.devin_service.initialize()
            logger.info("Devin AI service initialized")
        except Exception as e:
            raise DevinAIError(f"Failed to initialize Devin AI: {str(e)}")
    
    async def _init_copilot(self):
        """Initialize Copilot service"""
        try:
            self.copilot_service = CopilotService()
            await self.copilot_service.initialize()
            logger.info("Copilot service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Copilot: {str(e)}")
    
    async def _init_github_copilot(self):
        """Initialize GitHub Copilot service"""
        try:
            self.github_copilot_service = GitHubCopilotService()
            await self.github_copilot_service.initialize()
            logger.info("GitHub Copilot service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize GitHub Copilot: {str(e)}")
    
    async def _init_multi_model_router(self):
        """Initialize multi-model router"""
        try:
            self.multi_model_router = MultiModelRouter()
            await self.multi_model_router.initialize()
            logger.info("Multi-model router initialized")
        except Exception as e:
            logger.error(f"Failed to initialize multi-model router: {str(e)}")
    
    async def _init_bricks_context(self):
        """Initialize BRICKS context service"""
        try:
            self.bricks_context_service = BRICKSContextService()
            logger.info("BRICKS context service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize BRICKS context service: {str(e)}")
    
    async def _init_revenue_analysis(self):
        """Initialize revenue analysis service"""
        try:
            self.revenue_analysis_service = RevenueAnalysisService()
            logger.info("Revenue analysis service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize revenue analysis service: {str(e)}")
    
    async def _init_strategic_gap(self):
        """Initialize strategic gap service"""
        try:
            self.strategic_gap_service = StrategicGapService()
            logger.info("Strategic gap service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize strategic gap service: {str(e)}")
    
    async def _init_brick_priority(self):
        """Initialize BRICK priority service"""
        try:
            self.brick_priority_service = BRICKPriorityService()
            logger.info("BRICK priority service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize BRICK priority service: {str(e)}")
    
    async def _init_constraint_prediction(self):
        """Initialize constraint prediction service"""
        try:
            self.constraint_prediction_service = ConstraintPredictionService()
            logger.info("Constraint prediction service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize constraint prediction service: {str(e)}")
    
    async def _init_human_ai_collaboration(self):
        """Initialize human-AI collaboration service"""
        try:
            self.human_ai_collaboration_service = HumanAICollaborationService()
            logger.info("Human-AI collaboration service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize human-AI collaboration service: {str(e)}")
    
    async def _init_strategic_intelligence(self):
        """Initialize strategic intelligence service with Real AI"""
        try:
            self.strategic_intelligence_service = StrategicIntelligenceService(
                bricks_context_service=self.bricks_context_service,
                revenue_analysis_service=self.revenue_analysis_service,
                strategic_gap_service=self.strategic_gap_service,
                brick_priority_service=self.brick_priority_service,
                constraint_prediction_service=self.constraint_prediction_service,
                multi_model_router=self.multi_model_router
            )
            logger.info("Strategic intelligence service initialized with Real AI support")
        except Exception as e:
            logger.error(f"Failed to initialize strategic intelligence service: {str(e)}")
    
    async def _init_church_kit_connector(self):
        """Initialize Church Kit Generator connector"""
        try:
            self.church_kit_connector = ChurchKitConnector()
            await self.church_kit_connector.initialize()
            logger.info("Church Kit Generator connector initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Church Kit connector: {str(e)}")
    
    async def _init_global_sky_connector(self):
        """Initialize Global Sky AI connector"""
        try:
            self.global_sky_connector = GlobalSkyConnector()
            await self.global_sky_connector.initialize()
            logger.info("Global Sky AI connector initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Global Sky connector: {str(e)}")
    
    async def _init_treasury_optimizer(self):
        """Initialize Treasury Optimizer"""
        try:
            self.treasury_optimizer = TreasuryOptimizer()
            await self.treasury_optimizer.initialize()
            logger.info("Treasury Optimizer initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Treasury Optimizer: {str(e)}")
    
    async def _init_autonomous_brick_proposer(self):
        """Initialize Autonomous BRICK Proposer with Real AI"""
        try:
            self.autonomous_brick_proposer = AutonomousBRICKProposer(
                church_kit_connector=self.church_kit_connector,
                global_sky_connector=self.global_sky_connector,
                treasury_optimizer=self.treasury_optimizer,
                strategic_intelligence=self.strategic_intelligence_service,
                human_ai_collaboration=self.human_ai_collaboration_service,
                multi_model_router=self.multi_model_router
            )
            logger.info("Autonomous BRICK Proposer initialized with Real AI support")
        except Exception as e:
            logger.error(f"Failed to initialize Autonomous BRICK Proposer: {str(e)}")
    
    async def orchestrate_task(
        self,
        task_type: str,
        goal: str,
        context: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Orchestrate a complex task across multiple AI systems"""
        
        if not self.initialized:
            raise AIOrchestrationError("Orchestrator not initialized")
        
        logger.info(
            "Starting orchestrated task",
            task_type=task_type,
            goal=goal,
            session_id=session_id
        )
        
        try:
            # Store context in memory
            if self.mem0_service:
                await self.mem0_service.store_context(session_id, context)
            
            # Route task to appropriate AI systems
            results = {}
            
            if task_type == "strategic_analysis":
                results = await self._orchestrate_strategic_analysis(goal, context, session_id)
            elif task_type == "brick_development":
                results = await self._orchestrate_brick_development(goal, context, session_id)
            elif task_type == "revenue_optimization":
                results = await self._orchestrate_revenue_optimization(goal, context, session_id)
            elif task_type == "gap_analysis":
                results = await self._orchestrate_gap_analysis(goal, context, session_id)
            else:
                # Generic orchestration
                results = await self._orchestrate_generic_task(goal, context, session_id)
            
            # Store results in memory
            if self.mem0_service:
                await self.mem0_service.store_result(session_id, results)
            
            logger.info("Orchestrated task completed successfully", session_id=session_id)
            return results
            
        except Exception as e:
            logger.error("Orchestrated task failed", error=str(e), session_id=session_id)
            raise AIOrchestrationError(f"Task orchestration failed: {str(e)}")
    
    async def _orchestrate_strategic_analysis(
        self,
        goal: str,
        context: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Orchestrate strategic analysis using multiple AI systems"""
        
        results = {"analysis": {}, "recommendations": {}, "insights": {}}
        
        # Use CrewAI for complex multi-agent analysis
        if self.crewai_service:
            crew_result = await self.crewai_service.analyze_strategic_opportunity(
                goal, context, session_id
            )
            results["analysis"]["crewai"] = crew_result
        
        # Use multi-model router for diverse perspectives
        if self.multi_model_router:
            perspectives = await self.multi_model_router.get_multiple_perspectives(
                f"Strategic analysis: {goal}", context
            )
            results["analysis"]["multi_model"] = perspectives
        
        # Use Mem0 to retrieve relevant historical context
        if self.mem0_service:
            historical_context = await self.mem0_service.retrieve_relevant_memories(
                goal, context
            )
            results["analysis"]["historical"] = historical_context
        
        return results
    
    async def _orchestrate_brick_development(
        self,
        goal: str,
        context: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Orchestrate BRICK development using AI systems"""
        
        results = {"planning": {}, "development": {}, "testing": {}}
        
        # Use CrewAI for development planning
        if self.crewai_service:
            plan = await self.crewai_service.plan_brick_development(goal, context, session_id)
            results["planning"]["crewai"] = plan
        
        # Use Devin AI for autonomous coding
        if self.devin_service:
            development = await self.devin_service.develop_brick(
                goal, context, session_id
            )
            results["development"]["devin"] = development
        
        # Use multi-model router for code review
        if self.multi_model_router:
            review = await self.multi_model_router.review_code(
                results.get("development", {}).get("devin", {}).get("code", ""),
                context
            )
            results["testing"]["code_review"] = review
        
        return results
    
    async def _orchestrate_revenue_optimization(
        self,
        goal: str,
        context: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Orchestrate revenue optimization analysis"""
        
        results = {"opportunities": {}, "analysis": {}, "recommendations": {}}
        
        # Use CrewAI for business analysis
        if self.crewai_service:
            business_analysis = await self.crewai_service.analyze_revenue_opportunities(
                goal, context, session_id
            )
            results["analysis"]["business"] = business_analysis
        
        # Use Mem0 to find similar successful strategies
        if self.mem0_service:
            similar_strategies = await self.mem0_service.find_similar_strategies(
                goal, context
            )
            results["analysis"]["similar_strategies"] = similar_strategies
        
        return results
    
    async def _orchestrate_gap_analysis(
        self,
        goal: str,
        context: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Orchestrate strategic gap analysis"""
        
        results = {"gaps": {}, "priorities": {}, "recommendations": {}}
        
        # Use multiple AI systems for comprehensive gap analysis
        if self.crewai_service and self.multi_model_router:
            # Parallel analysis
            crew_task = self.crewai_service.identify_strategic_gaps(goal, context, session_id)
            router_task = self.multi_model_router.analyze_gaps(goal, context)
            
            crew_gaps, router_gaps = await asyncio.gather(crew_task, router_task)
            
            results["gaps"]["crewai"] = crew_gaps
            results["gaps"]["multi_model"] = router_gaps
        
        return results
    
    async def _orchestrate_generic_task(
        self,
        goal: str,
        context: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Generic orchestration for unknown task types"""
        
        results = {"analysis": {}, "execution": {}}
        
        # Use multi-model router as primary system
        if self.multi_model_router:
            analysis = await self.multi_model_router.analyze_and_execute(goal, context)
            results["analysis"] = analysis
        
        # Supplement with CrewAI if available
        if self.crewai_service:
            crew_analysis = await self.crewai_service.generic_analysis(goal, context, session_id)
            results["execution"]["crewai"] = crew_analysis
        
        return results
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get status of all AI systems"""
        
        status = {
            "orchestrator": "healthy" if self.initialized else "not_initialized",
            "services": {}
        }
        
        # Phase 2 Services
        if self.crewai_service:
            status["services"]["crewai"] = await self.crewai_service.get_status()
        if self.mem0_service:
            status["services"]["mem0"] = await self.mem0_service.get_status()
        if self.devin_service:
            status["services"]["devin"] = await self.devin_service.get_status()
        if self.copilot_service:
            status["services"]["copilot"] = await self.copilot_service.get_status()
        if self.github_copilot_service:
            status["services"]["github_copilot"] = await self.github_copilot_service.get_status()
        if self.multi_model_router:
            status["services"]["multi_model_router"] = await self.multi_model_router.get_status()
        
        # Phase 3 Services - Strategic Intelligence
        if self.bricks_context_service:
            status["services"]["bricks_context"] = await self.bricks_context_service.get_status()
        if self.revenue_analysis_service:
            status["services"]["revenue_analysis"] = await self.revenue_analysis_service.get_status()
        if self.strategic_gap_service:
            status["services"]["strategic_gap"] = await self.strategic_gap_service.get_status()
        if self.brick_priority_service:
            status["services"]["brick_priority"] = await self.brick_priority_service.get_status()
        if self.constraint_prediction_service:
            status["services"]["constraint_prediction"] = await self.constraint_prediction_service.get_status()
        if self.human_ai_collaboration_service:
            status["services"]["human_ai_collaboration"] = await self.human_ai_collaboration_service.get_status()
        if self.strategic_intelligence_service:
            status["services"]["strategic_intelligence"] = await self.strategic_intelligence_service.get_status()
        
        # Phase 4 Services - Revenue Integration Loop
        if self.church_kit_connector:
            status["services"]["church_kit_generator"] = await self.church_kit_connector.get_status()
        if self.global_sky_connector:
            status["services"]["global_sky_ai"] = await self.global_sky_connector.get_status()
        if self.treasury_optimizer:
            status["services"]["treasury_optimization"] = await self.treasury_optimizer.get_status()
        if self.autonomous_brick_proposer:
            status["services"]["autonomous_brick_proposer"] = await self.autonomous_brick_proposer.get_status()
        
        return status
    
    async def health_check(self) -> str:
        """Perform health check on all systems"""
        
        try:
            if not self.initialized:
                return "not_initialized"
            
            # Check each service
            healthy_services = 0
            total_services = 0
            
            services = [
                self.crewai_service,
                self.mem0_service,
                self.devin_service,
                self.copilot_service,
                self.github_copilot_service,
                self.multi_model_router
            ]
            
            for service in services:
                if service:
                    total_services += 1
                    try:
                        status = await service.get_status()
                        if status.get("status") == "healthy":
                            healthy_services += 1
                    except Exception:
                        pass
            
            if total_services == 0:
                return "no_services"
            
            health_ratio = healthy_services / total_services
            if health_ratio >= 0.8:
                return "healthy"
            elif health_ratio >= 0.5:
                return "degraded"
            else:
                return "unhealthy"
                
        except Exception as e:
            logger.error("Health check failed", error=str(e))
            return "error"
    
    async def cleanup(self):
        """Cleanup resources"""
        try:
            logger.info("Cleaning up AI Orchestrator")
            
            cleanup_tasks = []
            
            if self.crewai_service:
                cleanup_tasks.append(self.crewai_service.cleanup())
            if self.mem0_service:
                cleanup_tasks.append(self.mem0_service.cleanup())
            if self.devin_service:
                cleanup_tasks.append(self.devin_service.cleanup())
            if self.copilot_service:
                cleanup_tasks.append(self.copilot_service.cleanup())
            if self.github_copilot_service:
                cleanup_tasks.append(self.github_copilot_service.cleanup())
            if self.multi_model_router:
                cleanup_tasks.append(self.multi_model_router.cleanup())
            
            if cleanup_tasks:
                await asyncio.gather(*cleanup_tasks, return_exceptions=True)
            
            self.initialized = False
            logger.info("AI Orchestrator cleanup completed")
            
        except Exception as e:
            logger.error("Error during cleanup", error=str(e))
