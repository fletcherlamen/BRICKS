"""
Multi-Model Router Service
Routes requests to appropriate AI models based on task requirements
"""

from typing import Dict, List, Optional, Any
import structlog
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
        
        # Anthropic Claude models
        if settings.ANTHROPIC_API_KEY:
            try:
                import anthropic
                self.models["claude-3-opus"] = {
                    "client": anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY),
                    "model": "claude-3-opus-20240229",
                    "capabilities": ["reasoning", "analysis", "code_generation"],
                    "cost": "high",
                    "speed": "medium"
                }
                self.models["claude-3-sonnet"] = {
                    "client": anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY),
                    "model": "claude-3-sonnet-20240229",
                    "capabilities": ["balanced", "reasoning"],
                    "cost": "medium",
                    "speed": "medium"
                }
                logger.info("Anthropic models initialized")
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
        """Setup routing rules for different task types"""
        
        self.routing_rules = {
            "strategic_analysis": {
                "preferred_models": ["claude-3-opus", "gpt-4"],
                "fallback_models": ["claude-3-sonnet", "gpt-3.5-turbo"],
                "requirements": ["reasoning", "analysis"]
            },
            "creative_writing": {
                "preferred_models": ["gpt-4", "claude-3-opus"],
                "fallback_models": ["gpt-3.5-turbo", "gemini-pro"],
                "requirements": ["creative_writing"]
            },
            "code_generation": {
                "preferred_models": ["claude-3-opus", "gpt-4"],
                "fallback_models": ["claude-3-sonnet", "gpt-3.5-turbo"],
                "requirements": ["code_generation"]
            },
            "fast_response": {
                "preferred_models": ["gemini-pro", "gpt-3.5-turbo"],
                "fallback_models": ["claude-3-sonnet"],
                "requirements": ["fast_response"]
            },
            "multimodal": {
                "preferred_models": ["gemini-pro"],
                "fallback_models": ["gpt-4"],
                "requirements": ["multimodal"]
            }
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
            
            # Execute request
            result = await self._execute_request(model_name, prompt, context)
            
            logger.info("Request routed successfully", model=model_name, task_type=task_type)
            
            return {
                "result": result,
                "model_used": model_name,
                "task_type": task_type,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error("Request routing failed", error=str(e), task_type=task_type)
            raise AIOrchestrationError(f"Request routing failed: {str(e)}")
    
    def _select_model(self, task_type: str) -> Optional[str]:
        """Select the best model for the task"""
        
        if task_type not in self.routing_rules:
            task_type = "general"
        
        # Try preferred models first
        preferred_models = self.routing_rules.get(task_type, {}).get("preferred_models", [])
        for model_name in preferred_models:
            if model_name in self.models:
                return model_name
        
        # Try fallback models
        fallback_models = self.routing_rules.get(task_type, {}).get("fallback_models", [])
        for model_name in fallback_models:
            if model_name in self.models:
                return model_name
        
        # Return any available model
        for model_name in self.models.keys():
            return model_name
        
        return None
    
    async def _execute_request(
        self,
        model_name: str,
        prompt: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Execute request with selected model"""
        
        model_info = self.models[model_name]
        model = model_info["model"]
        client = model_info["client"]
        
        try:
            if model.startswith("gpt"):
                # OpenAI models
                response = await client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are an AI assistant helping with business intelligence and strategic analysis."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2000,
                    temperature=0.7
                )
                return response.choices[0].message.content
            
            elif model.startswith("claude"):
                # Anthropic models
                response = await client.messages.create(
                    model=model,
                    max_tokens=2000,
                    temperature=0.7,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.content[0].text
            
            elif model.startswith("gemini"):
                # Google Gemini models
                response = await client.generate_content(prompt)
                return response.text
            
            else:
                raise AIOrchestrationError(f"Unsupported model: {model}")
                
        except Exception as e:
            logger.error("Model execution failed", model=model, error=str(e))
            raise AIOrchestrationError(f"Model execution failed: {str(e)}")
    
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
        """Get multi-model router status"""
        
        return {
            "status": "healthy" if self.initialized else "not_initialized",
            "available_models": list(self.models.keys()),
            "routing_rules": list(self.routing_rules.keys()),
            "models_count": len(self.models)
        }
    
    async def cleanup(self):
        """Cleanup multi-model router resources"""
        try:
            self.models = {}
            self.routing_rules = {}
            self.initialized = False
            logger.info("Multi-model router cleaned up")
        except Exception as e:
            logger.error("Error cleaning up multi-model router", error=str(e))
