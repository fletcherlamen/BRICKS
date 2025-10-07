"""
Proactive Constraint Prediction Engine
Part of STRATEGIC Framework - Predicts and prevents constraints before they occur
"""

import structlog
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

logger = structlog.get_logger(__name__)


class ConstraintPredictionService:
    """
    Proactive Constraint Prediction Engine
    
    S.T.R.A.T.E.G.I.C. Framework Component:
    - Strategic constraint identification
    - Tactical resource planning
    - Risk assessment and mitigation
    - Adaptive constraint resolution
    - Temporal constraint prediction
    - Environmental factor analysis
    - Goal-oriented constraint prevention
    - Intelligent constraint management
    - Continuous constraint monitoring
    """
    
    def __init__(self):
        self.constraint_types = self._initialize_constraint_types()
        self.prediction_models = self._initialize_prediction_models()
        self.active_constraints = []
        logger.info("Constraint Prediction Service initialized")
    
    def _initialize_constraint_types(self) -> Dict[str, Any]:
        """Initialize constraint type definitions"""
        return {
            "resource_constraints": {
                "types": ["time", "budget", "team_capacity", "infrastructure"],
                "severity_levels": ["low", "medium", "high", "critical"],
                "prediction_horizon": "30_days"
            },
            "technical_constraints": {
                "types": ["technology_debt", "scalability", "performance", "security"],
                "severity_levels": ["minor", "moderate", "major", "blocking"],
                "prediction_horizon": "60_days"
            },
            "business_constraints": {
                "types": ["market_conditions", "competition", "regulatory", "customer_demand"],
                "severity_levels": ["low_impact", "medium_impact", "high_impact", "critical_impact"],
                "prediction_horizon": "90_days"
            },
            "operational_constraints": {
                "types": ["dependencies", "integration_complexity", "deployment_risk", "maintenance_burden"],
                "severity_levels": ["manageable", "concerning", "problematic", "blocking"],
                "prediction_horizon": "45_days"
            }
        }
    
    def _initialize_prediction_models(self) -> Dict[str, Any]:
        """Initialize constraint prediction models"""
        return {
            "time_constraint_model": {
                "factors": ["team_size", "complexity", "dependencies", "unknowns"],
                "buffer_multiplier": 1.5  # Add 50% buffer
            },
            "budget_constraint_model": {
                "factors": ["development_cost", "infrastructure_cost", "operational_cost"],
                "buffer_multiplier": 1.3  # Add 30% buffer
            },
            "capacity_constraint_model": {
                "factors": ["team_velocity", "parallel_projects", "technical_debt"],
                "threshold": 0.8  # 80% capacity utilization
            }
        }
    
    async def predict_constraints(
        self,
        brick_name: str,
        brick_data: Dict[str, Any],
        project_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Predict potential constraints for a BRICK development"""
        try:
            predicted_constraints = {
                "resource_constraints": [],
                "technical_constraints": [],
                "business_constraints": [],
                "operational_constraints": []
            }
            
            # Predict resource constraints
            resource_constraints = self._predict_resource_constraints(brick_data, project_context)
            predicted_constraints["resource_constraints"] = resource_constraints
            
            # Predict technical constraints
            technical_constraints = self._predict_technical_constraints(brick_data)
            predicted_constraints["technical_constraints"] = technical_constraints
            
            # Predict business constraints
            business_constraints = self._predict_business_constraints(brick_data)
            predicted_constraints["business_constraints"] = business_constraints
            
            # Predict operational constraints
            operational_constraints = self._predict_operational_constraints(brick_data)
            predicted_constraints["operational_constraints"] = operational_constraints
            
            # Calculate constraint risk score
            risk_score = self._calculate_constraint_risk(predicted_constraints)
            
            # Generate mitigation strategies
            mitigation_strategies = self._generate_mitigation_strategies(predicted_constraints)
            
            # Determine if project is viable
            viability = self._assess_project_viability(risk_score, predicted_constraints)
            
            return {
                "status": "success",
                "brick_name": brick_name,
                "predicted_constraints": predicted_constraints,
                "total_constraints": sum(len(c) for c in predicted_constraints.values()),
                "constraint_risk_score": risk_score,
                "risk_level": self._categorize_risk(risk_score),
                "mitigation_strategies": mitigation_strategies,
                "project_viability": viability,
                "recommendation": self._generate_constraint_recommendation(risk_score, viability),
                "prediction_timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error("Failed to predict constraints", error=str(e))
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _predict_resource_constraints(
        self,
        brick_data: Dict[str, Any],
        project_context: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Predict resource-related constraints"""
        constraints = []
        
        # Time constraint
        estimated_time = brick_data.get("estimated_dev_time", "3_months")
        if "_month" in estimated_time or "months" in estimated_time:
            months = int(estimated_time.split("_")[0]) if "_month" in estimated_time else 3
            
            if months >= 6:
                constraints.append({
                    "type": "time",
                    "description": f"Long development timeline ({months} months)",
                    "severity": "high",
                    "impact": "Delayed time-to-market",
                    "probability": 0.7,
                    "predicted_date": (datetime.now() + timedelta(days=months*30)).isoformat()
                })
        
        # Budget constraint (estimated)
        if months >= 3:
            estimated_cost = months * 15000  # $15k per month estimate
            constraints.append({
                "type": "budget",
                "description": f"High development cost (${estimated_cost:,})",
                "severity": "medium" if estimated_cost < 50000 else "high",
                "impact": "Capital requirements",
                "probability": 0.8,
                "estimated_amount": estimated_cost
            })
        
        # Team capacity constraint
        if project_context:
            parallel_projects = project_context.get("parallel_projects", 1)
            if parallel_projects >= 2:
                constraints.append({
                    "type": "team_capacity",
                    "description": f"Team spread across {parallel_projects} projects",
                    "severity": "medium",
                    "impact": "Reduced development velocity",
                    "probability": 0.6
                })
        
        return constraints
    
    def _predict_technical_constraints(self, brick_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Predict technical constraints"""
        constraints = []
        
        # Technology stack constraints
        tech_stack = brick_data.get("technology_stack", [])
        if len(tech_stack) >= 5:
            constraints.append({
                "type": "technology_debt",
                "description": "Complex technology stack increases maintenance burden",
                "severity": "medium",
                "impact": "Higher operational costs",
                "probability": 0.5
            })
        
        # Scalability constraints
        user_base = brick_data.get("user_base", 0)
        if user_base >= 500 or brick_data.get("target_market") == "enterprise":
            constraints.append({
                "type": "scalability",
                "description": "High user base requires scalability planning",
                "severity": "high",
                "impact": "Performance degradation at scale",
                "probability": 0.6
            })
        
        # Integration complexity
        integration_points = brick_data.get("integration_points", [])
        if len(integration_points) >= 3:
            constraints.append({
                "type": "integration_complexity",
                "description": f"Multiple integration points ({len(integration_points)}) increase complexity",
                "severity": "medium",
                "impact": "Integration testing overhead",
                "probability": 0.7
            })
        
        return constraints
    
    def _predict_business_constraints(self, brick_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Predict business constraints"""
        constraints = []
        
        # Market competition
        target_market = brick_data.get("target_market", "unknown")
        if "enterprise" in target_market.lower():
            constraints.append({
                "type": "competition",
                "description": "High competition in enterprise market",
                "severity": "high",
                "impact": "Difficult customer acquisition",
                "probability": 0.8
            })
        
        # Customer demand validation
        if brick_data.get("status") == "concept":
            constraints.append({
                "type": "customer_demand",
                "description": "Unvalidated customer demand",
                "severity": "medium",
                "impact": "Product-market fit risk",
                "probability": 0.5
            })
        
        return constraints
    
    def _predict_operational_constraints(self, brick_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Predict operational constraints"""
        constraints = []
        
        # Dependency constraints
        dependencies = brick_data.get("dependencies", [])
        if dependencies:
            constraints.append({
                "type": "dependencies",
                "description": f"Depends on {len(dependencies)} other BRICKs",
                "severity": "medium",
                "impact": "Development blocked until dependencies ready",
                "probability": 0.6,
                "dependencies": dependencies
            })
        
        # Deployment risk
        if brick_data.get("status") in ["concept", "mvp"]:
            constraints.append({
                "type": "deployment_risk",
                "description": "Unproven deployment process",
                "severity": "medium",
                "impact": "Deployment delays",
                "probability": 0.4
            })
        
        return constraints
    
    def _calculate_constraint_risk(self, constraints: Dict[str, List[Dict[str, Any]]]) -> float:
        """Calculate overall constraint risk score (0-100)"""
        severity_scores = {
            "low": 1, "minor": 1, "low_impact": 1, "manageable": 1,
            "medium": 3, "moderate": 3, "medium_impact": 3, "concerning": 3,
            "high": 7, "major": 7, "high_impact": 7, "problematic": 7,
            "critical": 10, "blocking": 10, "critical_impact": 10
        }
        
        total_risk = 0
        total_constraints = 0
        
        for constraint_category, constraint_list in constraints.items():
            for constraint in constraint_list:
                severity = constraint.get("severity", "medium")
                probability = constraint.get("probability", 0.5)
                
                severity_score = severity_scores.get(severity, 3)
                weighted_score = severity_score * probability
                
                total_risk += weighted_score
                total_constraints += 1
        
        if total_constraints == 0:
            return 0.0
        
        # Normalize to 0-100
        avg_risk = total_risk / total_constraints
        return min(avg_risk * 10, 100)
    
    def _categorize_risk(self, risk_score: float) -> str:
        """Categorize risk level"""
        if risk_score >= 70:
            return "critical"
        elif risk_score >= 50:
            return "high"
        elif risk_score >= 30:
            return "medium"
        else:
            return "low"
    
    def _generate_mitigation_strategies(
        self,
        constraints: Dict[str, List[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """Generate mitigation strategies for predicted constraints"""
        strategies = []
        
        for constraint_category, constraint_list in constraints.items():
            for constraint in constraint_list:
                strategy = self._create_mitigation_strategy(constraint)
                if strategy:
                    strategies.append(strategy)
        
        # Sort by priority (severity * probability)
        strategies.sort(
            key=lambda x: x.get("priority_score", 0),
            reverse=True
        )
        
        return strategies[:10]  # Top 10 strategies
    
    def _create_mitigation_strategy(self, constraint: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a mitigation strategy for a specific constraint"""
        constraint_type = constraint.get("type")
        
        mitigation_map = {
            "time": {
                "strategy": "Add timeline buffer and parallel workstreams",
                "actions": ["Break down into smaller milestones", "Identify parallelizable tasks", "Add 50% time buffer"],
                "cost": "low"
            },
            "budget": {
                "strategy": "Secure funding and implement cost controls",
                "actions": ["Create detailed budget", "Identify cost-saving opportunities", "Secure funding commitment"],
                "cost": "medium"
            },
            "team_capacity": {
                "strategy": "Optimize resource allocation and prioritize ruthlessly",
                "actions": ["Reduce scope", "Hire contractors for specific tasks", "Defer lower-priority features"],
                "cost": "medium"
            },
            "scalability": {
                "strategy": "Design for scale from day one",
                "actions": ["Use scalable architecture patterns", "Implement caching", "Plan for horizontal scaling"],
                "cost": "medium"
            },
            "integration_complexity": {
                "strategy": "Simplify integrations and use standard protocols",
                "actions": ["Use API gateways", "Implement standard interfaces", "Create integration tests"],
                "cost": "low"
            },
            "competition": {
                "strategy": "Differentiate through unique value proposition",
                "actions": ["Identify competitive advantages", "Focus on niche features", "Build strong brand"],
                "cost": "medium"
            },
            "customer_demand": {
                "strategy": "Validate demand through MVP and customer interviews",
                "actions": ["Build minimal viable product", "Conduct customer interviews", "Run pilot program"],
                "cost": "low"
            },
            "dependencies": {
                "strategy": "Accelerate dependency completion or find alternatives",
                "actions": ["Prioritize dependency BRICKs", "Find interim solutions", "Reduce coupling"],
                "cost": "high"
            }
        }
        
        mitigation = mitigation_map.get(constraint_type)
        
        if not mitigation:
            return None
        
        # Calculate priority score
        severity_scores = {"low": 1, "minor": 1, "medium": 3, "moderate": 3, "high": 7, "major": 7, "critical": 10, "blocking": 10}
        severity = constraint.get("severity", "medium")
        probability = constraint.get("probability", 0.5)
        
        priority_score = severity_scores.get(severity, 3) * probability
        
        return {
            "constraint_type": constraint_type,
            "constraint_description": constraint.get("description"),
            "mitigation_strategy": mitigation["strategy"],
            "action_items": mitigation["actions"],
            "implementation_cost": mitigation["cost"],
            "priority_score": round(priority_score, 2),
            "expected_impact": "Reduces constraint risk by 60-80%"
        }
    
    def _assess_project_viability(
        self,
        risk_score: float,
        constraints: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Assess overall project viability considering constraints"""
        blocking_constraints = []
        
        for constraint_category, constraint_list in constraints.items():
            for constraint in constraint_list:
                if constraint.get("severity") in ["critical", "blocking", "critical_impact"]:
                    blocking_constraints.append(constraint)
        
        if blocking_constraints:
            return {
                "viable": False,
                "reason": f"{len(blocking_constraints)} blocking constraints identified",
                "blocking_constraints": blocking_constraints,
                "recommendation": "Resolve blocking constraints before proceeding"
            }
        
        if risk_score >= 70:
            return {
                "viable": "conditional",
                "reason": "High risk score requires mitigation",
                "risk_score": risk_score,
                "recommendation": "Implement mitigation strategies before proceeding"
            }
        
        return {
            "viable": True,
            "reason": "No blocking constraints, manageable risk",
            "risk_score": risk_score,
            "recommendation": "Proceed with development"
        }
    
    def _generate_constraint_recommendation(
        self,
        risk_score: float,
        viability: Dict[str, Any]
    ) -> str:
        """Generate recommendation based on constraint analysis"""
        if not viability.get("viable"):
            return f"⚠️ NOT RECOMMENDED: {viability.get('reason')} - Address blocking issues first"
        
        if viability.get("viable") == "conditional":
            return f"⚠️ PROCEED WITH CAUTION: {viability.get('reason')} - Implement risk mitigation"
        
        if risk_score < 30:
            return "✅ RECOMMENDED: Low constraint risk, proceed confidently"
        elif risk_score < 50:
            return "✅ APPROVED: Moderate constraints, manageable with planning"
        else:
            return "⚠️ HIGH RISK: Significant constraints, thorough planning required"
    
    async def monitor_active_constraints(self) -> Dict[str, Any]:
        """Monitor currently active constraints"""
        try:
            # Get active constraints
            active = self.active_constraints
            
            # Categorize by severity
            critical_constraints = [c for c in active if c.get("severity") in ["critical", "blocking"]]
            high_constraints = [c for c in active if c.get("severity") in ["high", "major"]]
            
            return {
                "status": "success",
                "active_constraints": active,
                "total_active": len(active),
                "critical_count": len(critical_constraints),
                "high_count": len(high_constraints),
                "requires_immediate_attention": len(critical_constraints) > 0,
                "monitoring_timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error("Failed to monitor constraints", error=str(e))
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def get_status(self) -> Dict[str, Any]:
        """Get service status"""
        return {
            "service": "constraint_prediction",
            "status": "operational",
            "prediction_models": len(self.prediction_models),
            "constraint_types": sum(len(ct["types"]) for ct in self.constraint_types.values()),
            "active_constraints": len(self.active_constraints)
        }
