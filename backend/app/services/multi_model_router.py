"""
Multi-Model Router Service
Routes requests to appropriate AI models based on task requirements
"""

from typing import Dict, List, Optional, Any
import structlog
import asyncio
from datetime import datetime

from app.core.config import settings
from app.core.exceptions import AIOrchestrationError

logger = structlog.get_logger(__name__)


class MultiModelRouter:
    """Multi-model router for AI service orchestration"""
    
    def __init__(self):
        self.initialized = False
        self.models = {}
        self.routing_rules = {}
        
    async def initialize(self):
        """Initialize multi-model router"""
        try:
            # Initialize available models
            await self._initialize_models()
            
            # Setup routing rules
            self._setup_routing_rules()
            
            self.initialized = True
            logger.info("Multi-model router initialized successfully")
            
        except Exception as e:
            logger.error("Failed to initialize multi-model router", error=str(e))
            raise AIOrchestrationError(f"Multi-model router initialization failed: {str(e)}")
    
    async def _initialize_models(self):
        """Initialize available AI models"""
        
        # OpenAI GPT models
        if settings.OPENAI_API_KEY:
            try:
                import openai
                self.models["gpt-4"] = {
                    "client": openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY),
                    "model": "gpt-4",
                    "capabilities": ["reasoning", "analysis", "creative_writing"],
                    "cost": "high",
                    "speed": "medium"
                }
                self.models["gpt-3.5-turbo"] = {
                    "client": openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY),
                    "model": "gpt-3.5-turbo",
                    "capabilities": ["general", "fast_response"],
                    "cost": "medium",
                    "speed": "fast"
                }
                logger.info("OpenAI models initialized")
            except Exception as e:
                logger.error("Failed to initialize OpenAI models", error=str(e))
        
        # Anthropic Claude models (v0.7.8 uses different API)
        if settings.ANTHROPIC_API_KEY:
            try:
                import anthropic
                # For Anthropic v0.7.8, use AsyncAnthropic with completions API
                client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
                
                self.models["claude-2.1"] = {
                    "client": client,
                    "model": "claude-2.1",
                    "capabilities": ["reasoning", "analysis", "code_generation"],
                    "cost": "medium",
                    "speed": "medium"
                }
                self.models["claude-instant"] = {
                    "client": client,
                    "model": "claude-instant-1.2",
                    "capabilities": ["fast_response", "general"],
                    "cost": "low",
                    "speed": "fast"
                }
                logger.info("Anthropic models initialized (Claude 2.1, Claude Instant)")
            except Exception as e:
                logger.error("Failed to initialize Anthropic models", error=str(e))
        
        # Google Gemini models
        if settings.GOOGLE_GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)
                self.models["gemini-pro"] = {
                    "client": genai.GenerativeModel('gemini-pro'),
                    "model": "gemini-pro",
                    "capabilities": ["multimodal", "creative", "fast"],
                    "cost": "low",
                    "speed": "fast"
                }
                logger.info("Google Gemini models initialized")
            except Exception as e:
                logger.error("Failed to initialize Google Gemini models", error=str(e))
    
    def _setup_routing_rules(self):
        """Setup advanced routing rules for different task types with cost optimization"""
        
        self.routing_rules = {
            "strategic_analysis": {
                "preferred_models": ["claude-3-opus", "gpt-4"],
                "fallback_models": ["claude-3-sonnet", "gpt-3.5-turbo"],
                "requirements": ["reasoning", "analysis"],
                "cost_weight": 0.3,
                "quality_weight": 0.7,
                "max_tokens": 4000,
                "temperature": 0.3
            },
            "creative_writing": {
                "preferred_models": ["gpt-4", "claude-3-opus"],
                "fallback_models": ["gpt-3.5-turbo", "gemini-pro"],
                "requirements": ["creative_writing"],
                "cost_weight": 0.4,
                "quality_weight": 0.6,
                "max_tokens": 3000,
                "temperature": 0.8
            },
            "code_generation": {
                "preferred_models": ["claude-3-opus", "gpt-4"],
                "fallback_models": ["claude-3-sonnet", "gpt-3.5-turbo"],
                "requirements": ["code_generation"],
                "cost_weight": 0.2,
                "quality_weight": 0.8,
                "max_tokens": 6000,
                "temperature": 0.1
            },
            "fast_response": {
                "preferred_models": ["gemini-pro", "gpt-3.5-turbo"],
                "fallback_models": ["claude-3-sonnet"],
                "requirements": ["fast_response"],
                "cost_weight": 0.8,
                "quality_weight": 0.2,
                "max_tokens": 1000,
                "temperature": 0.5
            },
            "multimodal": {
                "preferred_models": ["gemini-pro"],
                "fallback_models": ["gpt-4"],
                "requirements": ["multimodal"],
                "cost_weight": 0.5,
                "quality_weight": 0.5,
                "max_tokens": 2000,
                "temperature": 0.4
            },
            "brick_development": {
                "preferred_models": ["gpt-4"],
                "fallback_models": ["gpt-3.5-turbo", "gemini-pro"],
                "requirements": ["code_generation", "reasoning", "analysis"],
                "cost_weight": 0.1,
                "quality_weight": 0.9,
                "max_tokens": 8000,
                "temperature": 0.2
            },
            "revenue_optimization": {
                "preferred_models": ["claude-3-opus", "gpt-4"],
                "fallback_models": ["claude-3-sonnet", "gpt-3.5-turbo"],
                "requirements": ["reasoning", "analysis"],
                "cost_weight": 0.2,
                "quality_weight": 0.8,
                "max_tokens": 5000,
                "temperature": 0.3
            },
            "enterprise_automation": {
                "preferred_models": ["claude-3-sonnet", "gpt-4"],
                "fallback_models": ["gpt-3.5-turbo", "gemini-pro"],
                "requirements": ["reasoning", "analysis"],
                "cost_weight": 0.6,
                "quality_weight": 0.4,
                "max_tokens": 3000,
                "temperature": 0.4
            }
        }
        
        # Cost optimization settings
        self.cost_optimization = {
            "budget_limit": 100.0,  # Daily budget in USD
            "cost_tracking": {},
            "usage_thresholds": {
                "warning": 0.8,  # 80% of budget
                "critical": 0.95  # 95% of budget
            }
        }
        
        # Performance tracking
        self.performance_metrics = {
            "response_times": {},
            "success_rates": {},
            "cost_per_request": {},
            "quality_scores": {}
        }
    
    async def route_request(
        self,
        prompt: str,
        task_type: str = "general",
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Route request to appropriate AI model"""
        
        if not self.initialized:
            raise AIOrchestrationError("Multi-model router not initialized")
        
        try:
            # Select appropriate model
            model_name = self._select_model(task_type)
            
            if not model_name:
                raise AIOrchestrationError("No suitable model found for task")
            
            logger.info("Routing request to AI model", model=model_name, task_type=task_type)
            
            # Execute request with timeout
            result = await asyncio.wait_for(
                self._execute_request(model_name, prompt, context),
                timeout=60.0  # Increased timeout for AI processing
            )
            
            logger.info("Request routed successfully", model=model_name, task_type=task_type)
            
            return {
                "status": "success",
                "response": result,
                "model_used": model_name,
                "task_type": task_type,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error("Request routing failed", error=str(e), task_type=task_type)
            raise AIOrchestrationError(f"Request routing failed: {str(e)}")
    
    def _select_model(self, task_type: str) -> Optional[str]:
        """Select the best model for the task with cost optimization"""
        
        if task_type not in self.routing_rules:
            task_type = "general"
        
        rule = self.routing_rules.get(task_type, {})
        preferred_models = rule.get("preferred_models", [])
        fallback_models = rule.get("fallback_models", [])
        
        # Check budget constraints
        if self._is_budget_exceeded():
            logger.warning("Budget exceeded, using cost-optimized model selection")
            return self._select_cost_optimized_model(preferred_models + fallback_models)
        
        # Try preferred models with cost consideration
        for model_name in preferred_models:
            if model_name in self.models:
                if self._is_model_affordable(model_name, rule):
                    return model_name
        
        # Try fallback models with cost consideration
        for model_name in fallback_models:
            if model_name in self.models:
                if self._is_model_affordable(model_name, rule):
                    return model_name
        
        # If budget is tight, select most cost-effective available model
        if self._is_budget_tight():
            return self._select_cost_optimized_model(list(self.models.keys()))
        
        # Return any available model
        for model_name in self.models.keys():
            return model_name
        
        return None
    
    def _is_budget_exceeded(self) -> bool:
        """Check if daily budget is exceeded"""
        today = datetime.now().strftime("%Y-%m-%d")
        daily_cost = self.cost_optimization["cost_tracking"].get(today, 0)
        return daily_cost >= self.cost_optimization["budget_limit"]
    
    def _is_budget_tight(self) -> bool:
        """Check if budget is getting tight"""
        today = datetime.now().strftime("%Y-%m-%d")
        daily_cost = self.cost_optimization["cost_tracking"].get(today, 0)
        threshold = self.cost_optimization["budget_limit"] * self.cost_optimization["usage_thresholds"]["warning"]
        return daily_cost >= threshold
    
    def _is_model_affordable(self, model_name: str, rule: Dict[str, Any]) -> bool:
        """Check if model is affordable given current budget"""
        if model_name not in self.models:
            return False
        
        # Get estimated cost for this request
        estimated_cost = self._estimate_request_cost(model_name, rule)
        today = datetime.now().strftime("%Y-%m-%d")
        daily_cost = self.cost_optimization["cost_tracking"].get(today, 0)
        
        return (daily_cost + estimated_cost) <= self.cost_optimization["budget_limit"]
    
    def _select_cost_optimized_model(self, available_models: List[str]) -> Optional[str]:
        """Select most cost-effective model from available options"""
        if not available_models:
            return None
        
        # Model cost rankings (lower is better)
        cost_rankings = {
            "gemini-pro": 1,
            "gpt-3.5-turbo": 2,
            "claude-3-sonnet": 3,
            "gpt-4": 4,
            "claude-3-opus": 5
        }
        
        # Sort by cost (ascending)
        sorted_models = sorted(
            available_models,
            key=lambda x: cost_rankings.get(x, 999)
        )
        
        return sorted_models[0] if sorted_models else None
    
    def _estimate_request_cost(self, model_name: str, rule: Dict[str, Any]) -> float:
        """Estimate cost for a request"""
        # Simplified cost estimation (in USD)
        cost_per_1k_tokens = {
            "gpt-4": 0.03,
            "gpt-3.5-turbo": 0.002,
            "claude-3-opus": 0.015,
            "claude-3-sonnet": 0.003,
            "gemini-pro": 0.001
        }
        
        max_tokens = rule.get("max_tokens", 2000)
        base_cost = cost_per_1k_tokens.get(model_name, 0.01)
        
        return (max_tokens / 1000) * base_cost
    
    def _track_request_cost(self, model_name: str, rule: Dict[str, Any], actual_tokens: int = None):
        """Track actual cost of a request"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in self.cost_optimization["cost_tracking"]:
            self.cost_optimization["cost_tracking"][today] = 0
        
        if actual_tokens:
            cost = self._estimate_request_cost(model_name, rule) * (actual_tokens / rule.get("max_tokens", 2000))
        else:
            cost = self._estimate_request_cost(model_name, rule)
        
        self.cost_optimization["cost_tracking"][today] += cost
        
        # Log budget status
        daily_cost = self.cost_optimization["cost_tracking"][today]
        budget_limit = self.cost_optimization["budget_limit"]
        
        if daily_cost >= budget_limit * self.cost_optimization["usage_thresholds"]["critical"]:
            logger.critical(f"Budget critical: {daily_cost:.2f}/{budget_limit:.2f} USD used")
        elif daily_cost >= budget_limit * self.cost_optimization["usage_thresholds"]["warning"]:
            logger.warning(f"Budget warning: {daily_cost:.2f}/{budget_limit:.2f} USD used")
    
    async def _execute_request(
        self,
        model_name: str,
        prompt: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Execute request with selected model and performance tracking"""
        
        model_info = self.models[model_name]
        model = model_info["model"]
        client = model_info["client"]
        
        # Get task type for routing rules
        task_type = context.get("task_type", "general") if context else "general"
        rule = self.routing_rules.get(task_type, {})
        
        start_time = datetime.now()
        
        try:
            if model.startswith("gpt"):
                # OpenAI models
                response = await client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are an AI assistant helping with business intelligence and strategic analysis for the I PROACTIVE BRICK Orchestration Intelligence system."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=rule.get("max_tokens", 2000),
                    temperature=rule.get("temperature", 0.7)
                )
                
                # Track usage and cost
                usage = response.usage
                self._track_request_cost(model_name, rule, usage.total_tokens if usage else None)
                self._track_performance(model_name, start_time, True)
                
                return response.choices[0].message.content
            
            elif model.startswith("claude"):
                # Anthropic models (version 0.7.8 uses completions API)
                import anthropic
                response = await client.completions.create(
                    model=model,
                    max_tokens_to_sample=rule.get("max_tokens", 2000),
                    temperature=rule.get("temperature", 0.7),
                    prompt=f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}"
                )
                
                # Track usage and cost (Anthropic doesn't provide detailed usage in response)
                self._track_request_cost(model_name, rule)
                self._track_performance(model_name, start_time, True)
                
                return response.completion
            
            elif model.startswith("gemini"):
                # Google Gemini models
                response = await client.generate_content(prompt)
                
                # Track usage and cost
                self._track_request_cost(model_name, rule)
                self._track_performance(model_name, start_time, True)
                
                return response.text
            
            else:
                raise AIOrchestrationError(f"Unsupported model: {model}")
                
        except Exception as e:
            self._track_performance(model_name, start_time, False)
            logger.error("Model execution failed", model=model, error=str(e))
            raise AIOrchestrationError(f"Model execution failed: {str(e)}")
    
    def _track_performance(self, model_name: str, start_time: datetime, success: bool):
        """Track performance metrics for a model"""
        response_time = (datetime.now() - start_time).total_seconds()
        
        # Initialize metrics if not exists
        if model_name not in self.performance_metrics["response_times"]:
            self.performance_metrics["response_times"][model_name] = []
            self.performance_metrics["success_rates"][model_name] = {"success": 0, "total": 0}
        
        # Track response time
        self.performance_metrics["response_times"][model_name].append(response_time)
        
        # Keep only last 100 response times
        if len(self.performance_metrics["response_times"][model_name]) > 100:
            self.performance_metrics["response_times"][model_name] = self.performance_metrics["response_times"][model_name][-100:]
        
        # Track success rate
        self.performance_metrics["success_rates"][model_name]["total"] += 1
        if success:
            self.performance_metrics["success_rates"][model_name]["success"] += 1
    
    async def get_multiple_perspectives(
        self,
        prompt: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get multiple perspectives from different models"""
        
        perspectives = {}
        available_models = list(self.models.keys())[:3]  # Limit to 3 models
        
        for model_name in available_models:
            try:
                result = await self._execute_request(model_name, prompt, context)
                perspectives[model_name] = result
            except Exception as e:
                logger.error(f"Failed to get perspective from {model_name}", error=str(e))
                perspectives[model_name] = f"Error: {str(e)}"
        
        return {
            "perspectives": perspectives,
            "timestamp": datetime.now().isoformat(),
            "models_used": list(perspectives.keys())
        }
    
    async def analyze_gaps(
        self,
        goal: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze gaps using multiple models"""
        
        prompt = f"""
        Analyze potential gaps and opportunities for: {goal}
        
        Context: {context}
        
        Please provide:
        1. Current capability assessment
        2. Identified gaps
        3. Priority recommendations
        4. Implementation suggestions
        """
        
        return await self.route_request(prompt, "strategic_analysis", context)
    
    async def review_code(
        self,
        code: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Review code using AI models"""
        
        prompt = f"""
        Please review the following code for quality, efficiency, and best practices:
        
        Code:
        {code}
        
        Context: {context}
        
        Provide:
        1. Code quality assessment
        2. Potential improvements
        3. Security considerations
        4. Performance optimizations
        """
        
        return await self.route_request(prompt, "code_generation", context)
    
    async def analyze_and_execute(
        self,
        goal: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze and execute a general task"""
        
        prompt = f"""
        Analyze and provide recommendations for: {goal}
        
        Context: {context}
        
        Please provide comprehensive analysis and actionable recommendations.
        """
        
        return await self.route_request(prompt, "strategic_analysis", context)
    
    async def get_status(self) -> Dict[str, Any]:
        """Get comprehensive multi-model router status with metrics"""
        
        today = datetime.now().strftime("%Y-%m-%d")
        daily_cost = self.cost_optimization["cost_tracking"].get(today, 0)
        budget_limit = self.cost_optimization["budget_limit"]
        
        # Calculate performance metrics
        performance_summary = {}
        for model_name in self.models.keys():
            if model_name in self.performance_metrics["response_times"]:
                response_times = self.performance_metrics["response_times"][model_name]
                success_data = self.performance_metrics["success_rates"].get(model_name, {"success": 0, "total": 0})
                
                performance_summary[model_name] = {
                    "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
                    "success_rate": (success_data["success"] / success_data["total"]) * 100 if success_data["total"] > 0 else 0,
                    "total_requests": success_data["total"]
                }
        
        return {
            "status": "healthy" if self.initialized else "not_initialized",
            "available_models": list(self.models.keys()),
            "routing_rules": list(self.routing_rules.keys()),
            "models_count": len(self.models),
            "cost_optimization": {
                "daily_budget": budget_limit,
                "daily_usage": daily_cost,
                "budget_utilization": (daily_cost / budget_limit) * 100,
                "budget_status": self._get_budget_status(daily_cost, budget_limit),
                "cost_tracking": self.cost_optimization["cost_tracking"]
            },
            "performance_metrics": performance_summary,
            "routing_configuration": {
                "task_types": list(self.routing_rules.keys()),
                "cost_weights": {k: v.get("cost_weight", 0) for k, v in self.routing_rules.items()},
                "quality_weights": {k: v.get("quality_weight", 0) for k, v in self.routing_rules.items()}
            },
            "last_updated": datetime.now().isoformat()
        }
    
    def _get_budget_status(self, daily_cost: float, budget_limit: float) -> str:
        """Get budget status string"""
        utilization = daily_cost / budget_limit
        
        if utilization >= self.cost_optimization["usage_thresholds"]["critical"]:
            return "critical"
        elif utilization >= self.cost_optimization["usage_thresholds"]["warning"]:
            return "warning"
        else:
            return "healthy"
    
    async def cleanup(self):
        """Cleanup multi-model router resources"""
        try:
            self.models = {}
            self.routing_rules = {}
            self.initialized = False
            logger.info("Multi-model router cleaned up")
        except Exception as e:
            logger.error("Error cleaning up multi-model router", error=str(e))

