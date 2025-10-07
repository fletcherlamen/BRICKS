"""
BRICKS Ecosystem Context Integration Service
Integrates BRICKS specifications and context for strategic intelligence
"""

import structlog
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.strategic import BRICKEcosystem

logger = structlog.get_logger(__name__)


class BRICKSContextService:
    """Service for managing BRICKS ecosystem context and specifications"""
    
    def __init__(self):
        self.bricks_ecosystem = None  # Will be loaded from database
        self.context_cache = {}
        logger.info("BRICKS Context Service initialized - will load from VPS database")
    
    async def _load_bricks_from_database(self) -> Dict[str, Any]:
        """Load BRICKS ecosystem from VPS database"""
        try:
            async with AsyncSessionLocal() as db:
                # Fetch all BRICKs from database
                result = await db.execute(select(BRICKEcosystem))
                bricks = result.scalars().all()
                
                ecosystem = {
                    "existing_bricks": {},
                    "potential_bricks": {},
                    "ecosystem_relationships": self._get_default_relationships()
                }
                
                for brick in bricks:
                    brick_data = {
                        "name": brick.brick_name,
                        "status": brick.status,
                        "revenue_stream": brick.revenue_stream,
                        "monthly_revenue": brick.monthly_revenue or 0,
                        "user_base": brick.user_base or 0,
                        "technology_stack": brick.technology_stack or [],
                        "integration_points": brick.integration_points or [],
                        "expansion_potential": brick.expansion_potential,
                        "strategic_value": brick.strategic_value,
                        "revenue_potential": brick.revenue_potential,
                        "dependencies": brick.dependencies or [],
                        "value_proposition": brick.value_proposition,
                        "target_market": brick.target_market,
                        "estimated_dev_time": brick.estimated_dev_time
                    }
                    
                    if brick.brick_type == "existing":
                        ecosystem["existing_bricks"][brick.brick_id] = brick_data
                    else:
                        ecosystem["potential_bricks"][brick.brick_id] = brick_data
                
                logger.info("BRICKs loaded from VPS database",
                           existing=len(ecosystem["existing_bricks"]),
                           potential=len(ecosystem["potential_bricks"]))
                
                return ecosystem
                
        except Exception as e:
            logger.error("Failed to load BRICKs from database, using fallback", error=str(e))
            return self._get_fallback_ecosystem()
    
    def _get_default_relationships(self) -> Dict[str, Any]:
        """Get default ecosystem relationships (business intelligence rules)"""
        return {
            "revenue_multipliers": [
                {
                    "brick_a": "church_kit_generator",
                    "brick_b": "automated_marketing_suite",
                    "multiplier": 1.5,
                    "reason": "Cross-selling opportunity"
                },
                {
                    "brick_a": "global_sky_ai",
                    "brick_b": "ai_orchestration_intelligence",
                    "multiplier": 2.0,
                    "reason": "Technology synergy"
                }
            ],
            "integration_opportunities": [
                {
                    "bricks": ["church_kit_generator", "global_sky_ai", "treasury_optimization"],
                    "opportunity": "Unified church management platform",
                    "revenue_potential": 10000,
                    "complexity": "high"
                }
            ]
        }
    
    def _get_fallback_ecosystem(self) -> Dict[str, Any]:
        """Fallback ecosystem data if database is unavailable"""
        return {
            "existing_bricks": {
                "church_kit_generator": {
                    "name": "Church Kit Generator",
                    "status": "production",
                    "revenue_stream": "subscription",
                    "monthly_revenue": 2500,
                    "user_base": 150,
                    "technology_stack": ["React", "FastAPI", "PostgreSQL"],
                    "integration_points": ["payment_processing", "email_automation", "content_management"],
                    "expansion_potential": "high",
                    "strategic_value": "core_revenue"
                },
                "global_sky_ai": {
                    "name": "Global Sky AI",
                    "status": "production",
                    "revenue_stream": "service_fee",
                    "monthly_revenue": 1800,
                    "user_base": 75,
                    "technology_stack": ["AI/ML", "Python", "Cloud Services"],
                    "integration_points": ["ai_orchestration", "data_processing", "api_gateway"],
                    "expansion_potential": "very_high",
                    "strategic_value": "ai_capability"
                },
                "treasury_optimization": {
                    "name": "Treasury Optimization",
                    "status": "development",
                    "revenue_stream": "management_fee",
                    "monthly_revenue": 0,
                    "user_base": 0,
                    "technology_stack": ["Analytics", "Dashboard", "Automation"],
                    "integration_points": ["financial_data", "reporting", "automation"],
                    "expansion_potential": "high",
                    "strategic_value": "operational_efficiency"
                }
            },
            "potential_bricks": {
                "ai_orchestration_intelligence": {
                    "name": "I PROACTIVE BRICK Orchestration Intelligence",
                    "status": "mvp_phase_3",
                    "revenue_potential": "high",
                    "dependencies": ["church_kit_generator", "global_sky_ai"],
                    "value_proposition": "Autonomous AI orchestration and strategic intelligence",
                    "target_market": "Enterprise automation",
                    "estimated_dev_time": "3_months"
                },
                "automated_marketing_suite": {
                    "name": "Automated Marketing Suite",
                    "status": "concept",
                    "revenue_potential": "medium",
                    "dependencies": ["church_kit_generator"],
                    "value_proposition": "AI-powered marketing automation for churches",
                    "target_market": "Religious organizations",
                    "estimated_dev_time": "2_months"
                }
            },
            "ecosystem_relationships": self._get_default_relationships()
        }
    
    async def get_ecosystem_context(self, brick_name: Optional[str] = None) -> Dict[str, Any]:
        """Get BRICKS ecosystem context from VPS database"""
        try:
            # Load ecosystem from database
            if not self.bricks_ecosystem:
                self.bricks_ecosystem = await self._load_bricks_from_database()
            
            if brick_name:
                # Get specific BRICK context
                brick_data = (
                    self.bricks_ecosystem["existing_bricks"].get(brick_name) or
                    self.bricks_ecosystem["potential_bricks"].get(brick_name)
                )
                
                if not brick_data:
                    return {
                        "status": "not_found",
                        "message": f"BRICK '{brick_name}' not found in ecosystem"
                    }
                
                # Get related BRICKs
                related_bricks = self._find_related_bricks(brick_name)
                
                return {
                    "status": "success",
                    "brick": brick_data,
                    "related_bricks": related_bricks,
                    "integration_opportunities": self._find_integration_opportunities(brick_name),
                    "revenue_impact": self._calculate_revenue_impact(brick_name)
                }
            else:
                # Get full ecosystem context
                return {
                    "status": "success",
                    "ecosystem": self.bricks_ecosystem,
                    "total_existing_bricks": len(self.bricks_ecosystem["existing_bricks"]),
                    "total_potential_bricks": len(self.bricks_ecosystem["potential_bricks"]),
                    "total_monthly_revenue": self._calculate_total_revenue(),
                    "ecosystem_health": self._assess_ecosystem_health()
                }
        
        except Exception as e:
            logger.error("Failed to get ecosystem context", error=str(e))
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _find_related_bricks(self, brick_name: str) -> List[Dict[str, Any]]:
        """Find BRICKs related to the given BRICK"""
        related = []
        
        # Check revenue multipliers
        for multiplier in self.bricks_ecosystem["ecosystem_relationships"]["revenue_multipliers"]:
            if brick_name in [multiplier["brick_a"], multiplier["brick_b"]]:
                related_brick_name = (
                    multiplier["brick_b"] if multiplier["brick_a"] == brick_name 
                    else multiplier["brick_a"]
                )
                related.append({
                    "brick_name": related_brick_name,
                    "relationship": "revenue_multiplier",
                    "multiplier": multiplier["multiplier"],
                    "reason": multiplier["reason"]
                })
        
        # Check integration opportunities
        for opportunity in self.bricks_ecosystem["ecosystem_relationships"]["integration_opportunities"]:
            if brick_name in opportunity["bricks"]:
                related.append({
                    "opportunity": opportunity["opportunity"],
                    "bricks_involved": opportunity["bricks"],
                    "revenue_potential": opportunity["revenue_potential"],
                    "complexity": opportunity["complexity"]
                })
        
        return related
    
    def _find_integration_opportunities(self, brick_name: str) -> List[Dict[str, Any]]:
        """Find integration opportunities for the given BRICK"""
        opportunities = []
        
        for opportunity in self.bricks_ecosystem["ecosystem_relationships"]["integration_opportunities"]:
            if brick_name in opportunity["bricks"]:
                opportunities.append(opportunity)
        
        return opportunities
    
    def _calculate_revenue_impact(self, brick_name: str) -> Dict[str, Any]:
        """Calculate revenue impact of the given BRICK"""
        brick_data = (
            self.bricks_ecosystem["existing_bricks"].get(brick_name) or
            self.bricks_ecosystem["potential_bricks"].get(brick_name)
        )
        
        if not brick_data:
            return {"impact": "unknown"}
        
        # Calculate direct revenue
        direct_revenue = brick_data.get("monthly_revenue", 0)
        
        # Calculate multiplier effects
        multiplier_revenue = 0
        for multiplier in self.bricks_ecosystem["ecosystem_relationships"]["revenue_multipliers"]:
            if brick_name in [multiplier["brick_a"], multiplier["brick_b"]]:
                other_brick = (
                    multiplier["brick_b"] if multiplier["brick_a"] == brick_name 
                    else multiplier["brick_a"]
                )
                other_brick_data = self.bricks_ecosystem["existing_bricks"].get(other_brick, {})
                other_revenue = other_brick_data.get("monthly_revenue", 0)
                multiplier_revenue += other_revenue * (multiplier["multiplier"] - 1)
        
        total_impact = direct_revenue + multiplier_revenue
        
        return {
            "direct_revenue": direct_revenue,
            "multiplier_revenue": multiplier_revenue,
            "total_monthly_impact": total_impact,
            "impact_level": self._categorize_impact(total_impact)
        }
    
    def _categorize_impact(self, revenue: float) -> str:
        """Categorize revenue impact level"""
        if revenue >= 5000:
            return "very_high"
        elif revenue >= 2000:
            return "high"
        elif revenue >= 1000:
            return "medium"
        elif revenue > 0:
            return "low"
        else:
            return "potential"
    
    def _calculate_total_revenue(self) -> float:
        """Calculate total monthly revenue from existing BRICKs"""
        total = 0
        for brick in self.bricks_ecosystem["existing_bricks"].values():
            total += brick.get("monthly_revenue", 0)
        return total
    
    def _assess_ecosystem_health(self) -> Dict[str, Any]:
        """Assess overall ecosystem health"""
        total_bricks = (
            len(self.bricks_ecosystem["existing_bricks"]) +
            len(self.bricks_ecosystem["potential_bricks"])
        )
        
        production_bricks = sum(
            1 for brick in self.bricks_ecosystem["existing_bricks"].values()
            if brick["status"] == "production"
        )
        
        total_revenue = self._calculate_total_revenue()
        
        return {
            "health_score": min(100, (production_bricks * 30 + total_revenue / 100)),
            "total_bricks": total_bricks,
            "production_bricks": production_bricks,
            "development_bricks": total_bricks - production_bricks,
            "monthly_revenue": total_revenue,
            "status": "healthy" if production_bricks >= 2 and total_revenue > 2000 else "growing"
        }
    
    async def add_brick_to_ecosystem(
        self,
        brick_name: str,
        brick_data: Dict[str, Any],
        brick_type: str = "potential"
    ) -> Dict[str, Any]:
        """Add a new BRICK to the ecosystem"""
        try:
            target_dict = (
                self.bricks_ecosystem["potential_bricks"] if brick_type == "potential"
                else self.bricks_ecosystem["existing_bricks"]
            )
            
            target_dict[brick_name] = brick_data
            
            logger.info("BRICK added to ecosystem", brick_name=brick_name, brick_type=brick_type)
            
            return {
                "status": "success",
                "message": f"BRICK '{brick_name}' added to {brick_type} BRICKs",
                "brick_data": brick_data
            }
        
        except Exception as e:
            logger.error("Failed to add BRICK to ecosystem", error=str(e))
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def analyze_brick_dependencies(self, brick_name: str) -> Dict[str, Any]:
        """Analyze dependencies and requirements for a BRICK"""
        try:
            brick_data = (
                self.bricks_ecosystem["existing_bricks"].get(brick_name) or
                self.bricks_ecosystem["potential_bricks"].get(brick_name)
            )
            
            if not brick_data:
                return {
                    "status": "not_found",
                    "message": f"BRICK '{brick_name}' not found"
                }
            
            # Get dependencies
            dependencies = brick_data.get("dependencies", [])
            
            # Check if dependencies are met
            dependencies_status = []
            for dep in dependencies:
                dep_brick = self.bricks_ecosystem["existing_bricks"].get(dep)
                if dep_brick:
                    dependencies_status.append({
                        "dependency": dep,
                        "status": dep_brick["status"],
                        "met": dep_brick["status"] == "production"
                    })
                else:
                    dependencies_status.append({
                        "dependency": dep,
                        "status": "missing",
                        "met": False
                    })
            
            all_met = all(dep["met"] for dep in dependencies_status)
            
            return {
                "status": "success",
                "brick_name": brick_name,
                "dependencies": dependencies_status,
                "all_dependencies_met": all_met,
                "ready_for_development": all_met,
                "recommendation": (
                    "Ready to proceed with development" if all_met
                    else "Complete dependencies first"
                )
            }
        
        except Exception as e:
            logger.error("Failed to analyze BRICK dependencies", error=str(e))
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def get_technology_stack_analysis(self) -> Dict[str, Any]:
        """Analyze technology stack across BRICKS ecosystem"""
        try:
            tech_usage = {}
            
            for brick_name, brick_data in self.bricks_ecosystem["existing_bricks"].items():
                for tech in brick_data.get("technology_stack", []):
                    if tech not in tech_usage:
                        tech_usage[tech] = {
                            "count": 0,
                            "bricks": [],
                            "total_revenue": 0
                        }
                    tech_usage[tech]["count"] += 1
                    tech_usage[tech]["bricks"].append(brick_name)
                    tech_usage[tech]["total_revenue"] += brick_data.get("monthly_revenue", 0)
            
            # Rank technologies by usage and revenue
            ranked_technologies = sorted(
                [
                    {
                        "technology": tech,
                        "usage_count": data["count"],
                        "bricks": data["bricks"],
                        "total_revenue": data["total_revenue"],
                        "strategic_importance": "high" if data["count"] >= 2 else "medium"
                    }
                    for tech, data in tech_usage.items()
                ],
                key=lambda x: (x["usage_count"], x["total_revenue"]),
                reverse=True
            )
            
            return {
                "status": "success",
                "technologies": ranked_technologies,
                "total_unique_technologies": len(tech_usage),
                "most_used_technology": ranked_technologies[0]["technology"] if ranked_technologies else None,
                "recommendation": "Leverage shared technologies for faster development"
            }
        
        except Exception as e:
            logger.error("Failed to analyze technology stack", error=str(e))
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def get_integration_map(self) -> Dict[str, Any]:
        """Get integration map showing how BRICKs connect"""
        try:
            integration_map = {
                "nodes": [],
                "edges": [],
                "clusters": []
            }
            
            # Add existing BRICKs as nodes
            for brick_name, brick_data in self.bricks_ecosystem["existing_bricks"].items():
                integration_map["nodes"].append({
                    "id": brick_name,
                    "label": brick_data["name"],
                    "type": "existing",
                    "status": brick_data["status"],
                    "revenue": brick_data.get("monthly_revenue", 0)
                })
            
            # Add potential BRICKs as nodes
            for brick_name, brick_data in self.bricks_ecosystem["potential_bricks"].items():
                integration_map["nodes"].append({
                    "id": brick_name,
                    "label": brick_data["name"],
                    "type": "potential",
                    "status": brick_data["status"]
                })
            
            # Add edges from revenue multipliers
            for multiplier in self.bricks_ecosystem["ecosystem_relationships"]["revenue_multipliers"]:
                integration_map["edges"].append({
                    "from": multiplier["brick_a"],
                    "to": multiplier["brick_b"],
                    "type": "revenue_multiplier",
                    "strength": multiplier["multiplier"],
                    "reason": multiplier["reason"]
                })
            
            # Add edges from dependencies
            for brick_name, brick_data in self.bricks_ecosystem["potential_bricks"].items():
                for dep in brick_data.get("dependencies", []):
                    integration_map["edges"].append({
                        "from": dep,
                        "to": brick_name,
                        "type": "dependency",
                        "reason": "Required for development"
                    })
            
            return {
                "status": "success",
                "integration_map": integration_map,
                "total_nodes": len(integration_map["nodes"]),
                "total_edges": len(integration_map["edges"])
            }
        
        except Exception as e:
            logger.error("Failed to get integration map", error=str(e))
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def get_status(self) -> Dict[str, Any]:
        """Get service status"""
        return {
            "service": "bricks_context",
            "status": "operational",
            "total_bricks": (
                len(self.bricks_ecosystem["existing_bricks"]) +
                len(self.bricks_ecosystem["potential_bricks"])
            ),
            "existing_bricks": len(self.bricks_ecosystem["existing_bricks"]),
            "potential_bricks": len(self.bricks_ecosystem["potential_bricks"]),
            "total_revenue": self._calculate_total_revenue(),
            "cached_contexts": len(self.context_cache)
        }
