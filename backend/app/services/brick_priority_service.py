"""
Next BRICK Priority Queue System
Prioritizes BRICK development based on strategic value, revenue potential, and dependencies
"""

import structlog
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

logger = structlog.get_logger(__name__)


class BRICKPriorityService:
    """Service for prioritizing next BRICK development"""
    
    def __init__(self):
        self.priority_criteria = self._initialize_priority_criteria()
        self.priority_queue = []
        logger.info("BRICK Priority Service initialized")
    
    def _initialize_priority_criteria(self) -> Dict[str, Any]:
        """Initialize priority scoring criteria"""
        return {
            "scoring_weights": {
                "revenue_potential": 0.30,
                "strategic_value": 0.25,
                "development_effort": 0.15,  # Inverse - lower effort = higher score
                "dependency_readiness": 0.15,
                "market_demand": 0.10,
                "competitive_advantage": 0.05
            },
            "effort_levels": {
                "low": {"score": 10, "weeks": "1-2"},
                "medium": {"score": 6, "weeks": "3-4"},
                "high": {"score": 3, "weeks": "5-8"},
                "very_high": {"score": 1, "weeks": "9+"}
            },
            "strategic_value_levels": {
                "core_revenue": 10,
                "ai_capability": 9,
                "operational_efficiency": 7,
                "market_expansion": 6,
                "innovation": 5
            }
        }
    
    async def calculate_brick_priority(
        self,
        brick_name: str,
        brick_data: Dict[str, Any],
        ecosystem_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Calculate priority score for a BRICK"""
        try:
            scores = {}
            
            # 1. Revenue Potential Score (0-10)
            revenue_score = self._score_revenue_potential(brick_data)
            scores["revenue_potential"] = revenue_score
            
            # 2. Strategic Value Score (0-10)
            strategic_score = self._score_strategic_value(brick_data)
            scores["strategic_value"] = strategic_score
            
            # 3. Development Effort Score (0-10, inverse)
            effort_score = self._score_development_effort(brick_data)
            scores["development_effort"] = effort_score
            
            # 4. Dependency Readiness Score (0-10)
            dependency_score = self._score_dependency_readiness(brick_data, ecosystem_context)
            scores["dependency_readiness"] = dependency_score
            
            # 5. Market Demand Score (0-10)
            market_score = self._score_market_demand(brick_data)
            scores["market_demand"] = market_score
            
            # 6. Competitive Advantage Score (0-10)
            competitive_score = self._score_competitive_advantage(brick_data)
            scores["competitive_advantage"] = competitive_score
            
            # Calculate weighted total score
            total_score = sum(
                scores[criterion] * self.priority_criteria["scoring_weights"][criterion]
                for criterion in scores.keys()
            )
            
            # Normalize to 0-100
            final_score = total_score * 10
            
            # Determine priority level
            priority_level = self._determine_priority_level(final_score)
            
            return {
                "status": "success",
                "brick_name": brick_name,
                "priority_score": round(final_score, 2),
                "priority_level": priority_level,
                "component_scores": scores,
                "recommendation": self._generate_priority_recommendation(
                    brick_name, final_score, scores
                ),
                "estimated_timeline": self._estimate_timeline(brick_data),
                "dependencies_met": dependency_score >= 8.0
            }
        
        except Exception as e:
            logger.error("Failed to calculate BRICK priority", error=str(e))
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _score_revenue_potential(self, brick_data: Dict[str, Any]) -> float:
        """Score revenue potential (0-10)"""
        revenue = brick_data.get("monthly_revenue", 0)
        revenue_potential = brick_data.get("revenue_potential", "unknown")
        
        # Existing revenue
        if revenue > 0:
            if revenue >= 5000:
                return 10.0
            elif revenue >= 2000:
                return 8.0
            elif revenue >= 1000:
                return 6.0
            else:
                return 4.0
        
        # Potential revenue (for new BRICKs)
        potential_mapping = {
            "very_high": 10.0,
            "high": 8.0,
            "medium": 5.0,
            "low": 3.0,
            "unknown": 1.0
        }
        
        return potential_mapping.get(revenue_potential, 1.0)
    
    def _score_strategic_value(self, brick_data: Dict[str, Any]) -> float:
        """Score strategic value (0-10)"""
        strategic_value = brick_data.get("strategic_value", "unknown")
        
        if strategic_value in self.priority_criteria["strategic_value_levels"]:
            return float(self.priority_criteria["strategic_value_levels"][strategic_value])
        
        # Default based on value proposition
        value_prop = brick_data.get("value_proposition", "").lower()
        if "autonomous" in value_prop or "ai" in value_prop:
            return 9.0
        elif "automation" in value_prop:
            return 7.0
        else:
            return 5.0
    
    def _score_development_effort(self, brick_data: Dict[str, Any]) -> float:
        """Score development effort (0-10, inverse - lower effort = higher score)"""
        effort_level = brick_data.get("estimated_dev_time", "medium")
        
        effort_mapping = {
            "1_month": 10.0,
            "2_months": 8.0,
            "3_months": 6.0,
            "6_months": 3.0,
            "1_year": 1.0
        }
        
        return effort_mapping.get(effort_level, 5.0)
    
    def _score_dependency_readiness(
        self,
        brick_data: Dict[str, Any],
        ecosystem_context: Optional[Dict[str, Any]]
    ) -> float:
        """Score dependency readiness (0-10)"""
        dependencies = brick_data.get("dependencies", [])
        
        if not dependencies:
            return 10.0  # No dependencies = ready to go
        
        if not ecosystem_context:
            return 5.0  # Can't check, assume medium
        
        # Check how many dependencies are met
        met_count = 0
        for dep in dependencies:
            dep_brick = ecosystem_context.get("existing_bricks", {}).get(dep)
            if dep_brick and dep_brick.get("status") == "production":
                met_count += 1
        
        readiness_percentage = met_count / len(dependencies) if dependencies else 1.0
        return readiness_percentage * 10.0
    
    def _score_market_demand(self, brick_data: Dict[str, Any]) -> float:
        """Score market demand (0-10)"""
        user_base = brick_data.get("user_base", 0)
        target_market = brick_data.get("target_market", "unknown")
        
        # Existing user base
        if user_base > 0:
            if user_base >= 500:
                return 10.0
            elif user_base >= 200:
                return 8.0
            elif user_base >= 100:
                return 6.0
            else:
                return 4.0
        
        # Potential market demand
        market_mapping = {
            "enterprise": 9.0,
            "small_business": 7.0,
            "consumer": 5.0,
            "niche": 4.0,
            "unknown": 3.0
        }
        
        for market_type, score in market_mapping.items():
            if market_type.lower() in target_market.lower():
                return score
        
        return 5.0
    
    def _score_competitive_advantage(self, brick_data: Dict[str, Any]) -> float:
        """Score competitive advantage (0-10)"""
        expansion_potential = brick_data.get("expansion_potential", "unknown")
        
        potential_mapping = {
            "very_high": 10.0,
            "high": 8.0,
            "medium": 5.0,
            "low": 3.0,
            "unknown": 5.0
        }
        
        return potential_mapping.get(expansion_potential, 5.0)
    
    def _determine_priority_level(self, score: float) -> str:
        """Determine priority level from score"""
        if score >= 80:
            return "critical"
        elif score >= 65:
            return "high"
        elif score >= 50:
            return "medium"
        else:
            return "low"
    
    def _generate_priority_recommendation(
        self,
        brick_name: str,
        score: float,
        component_scores: Dict[str, float]
    ) -> str:
        """Generate recommendation based on priority score"""
        if score >= 80:
            return f"IMMEDIATE PRIORITY: {brick_name} - Start development ASAP"
        elif score >= 65:
            return f"HIGH PRIORITY: {brick_name} - Schedule for next sprint"
        elif score >= 50:
            return f"MEDIUM PRIORITY: {brick_name} - Add to backlog"
        else:
            return f"LOW PRIORITY: {brick_name} - Monitor and reassess"
    
    def _estimate_timeline(self, brick_data: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate development timeline"""
        estimated_dev_time = brick_data.get("estimated_dev_time", "unknown")
        
        timeline_mapping = {
            "1_month": {"weeks": 4, "sprints": 2, "complexity": "low"},
            "2_months": {"weeks": 8, "sprints": 4, "complexity": "medium"},
            "3_months": {"weeks": 12, "sprints": 6, "complexity": "high"},
            "6_months": {"weeks": 24, "sprints": 12, "complexity": "very_high"},
            "1_year": {"weeks": 52, "sprints": 26, "complexity": "extreme"}
        }
        
        return timeline_mapping.get(estimated_dev_time, {
            "weeks": "unknown",
            "sprints": "unknown",
            "complexity": "unknown"
        })
    
    async def generate_priority_queue(
        self,
        ecosystem_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate priority queue for all potential BRICKs"""
        try:
            if not ecosystem_context:
                return {
                    "status": "error",
                    "message": "Ecosystem context required"
                }
            
            priority_queue = []
            
            # Analyze all potential BRICKs
            for brick_name, brick_data in ecosystem_context.get("potential_bricks", {}).items():
                priority_result = await self.calculate_brick_priority(
                    brick_name,
                    brick_data,
                    ecosystem_context
                )
                
                if priority_result["status"] == "success":
                    priority_queue.append({
                        "brick_name": brick_name,
                        "brick_data": brick_data,
                        "priority_score": priority_result["priority_score"],
                        "priority_level": priority_result["priority_level"],
                        "recommendation": priority_result["recommendation"],
                        "estimated_timeline": priority_result["estimated_timeline"],
                        "dependencies_met": priority_result["dependencies_met"]
                    })
            
            # Sort by priority score (highest first)
            priority_queue.sort(key=lambda x: x["priority_score"], reverse=True)
            
            # Categorize by priority level
            categorized = {
                "critical": [b for b in priority_queue if b["priority_level"] == "critical"],
                "high": [b for b in priority_queue if b["priority_level"] == "high"],
                "medium": [b for b in priority_queue if b["priority_level"] == "medium"],
                "low": [b for b in priority_queue if b["priority_level"] == "low"]
            }
            
            return {
                "status": "success",
                "priority_queue": priority_queue,
                "categorized_queue": categorized,
                "next_brick_recommendation": priority_queue[0] if priority_queue else None,
                "total_bricks_analyzed": len(priority_queue),
                "analysis_timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error("Failed to generate priority queue", error=str(e))
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def get_status(self) -> Dict[str, Any]:
        """Get service status"""
        return {
            "service": "brick_priority",
            "status": "operational",
            "priority_queue_size": len(self.priority_queue),
            "scoring_criteria": len(self.priority_criteria["scoring_weights"])
        }
