"""
Strategic Gap Detection Service
Identifies gaps in BRICKS ecosystem and strategic opportunities
"""

import structlog
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = structlog.get_logger(__name__)


class StrategicGapService:
    """Service for detecting strategic gaps and opportunities in BRICKS ecosystem"""
    
    def __init__(self):
        self.gap_detection_rules = self._initialize_gap_detection_rules()
        self.detected_gaps = []
        logger.info("Strategic Gap Detection Service initialized")
    
    def _initialize_gap_detection_rules(self) -> Dict[str, Any]:
        """Initialize gap detection rules and criteria"""
        return {
            "capability_gaps": [
                {
                    "category": "technology",
                    "name": "AI/ML Capabilities",
                    "importance": "high",
                    "current_coverage": ["global_sky_ai"],
                    "desired_coverage": ["orchestration", "automation", "prediction"]
                },
                {
                    "category": "market",
                    "name": "Enterprise Market",
                    "importance": "high",
                    "current_coverage": [],
                    "desired_coverage": ["enterprise_automation", "workflow_management"]
                },
                {
                    "category": "integration",
                    "name": "Cross-System Integration",
                    "importance": "medium",
                    "current_coverage": ["basic_apis"],
                    "desired_coverage": ["unified_platform", "data_sync", "single_sign_on"]
                }
            ],
            "market_gaps": [
                {
                    "segment": "Small Business",
                    "current_penetration": 0.05,
                    "market_size": 50000,
                    "revenue_potential": 75000,
                    "competition": "medium"
                },
                {
                    "segment": "Enterprise",
                    "current_penetration": 0.01,
                    "market_size": 10000,
                    "revenue_potential": 150000,
                    "competition": "high"
                }
            ],
            "revenue_gaps": [
                {
                    "gap_type": "pricing_tier",
                    "description": "Missing premium tier pricing",
                    "impact": "medium",
                    "potential_revenue": 800
                },
                {
                    "gap_type": "value_added_services",
                    "description": "No consulting or professional services",
                    "impact": "high",
                    "potential_revenue": 3000
                }
            ]
        }
    
    async def detect_strategic_gaps(
        self,
        bricks_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Detect strategic gaps in BRICKS ecosystem"""
        try:
            detected_gaps = {
                "capability_gaps": [],
                "market_gaps": [],
                "revenue_gaps": [],
                "technology_gaps": [],
                "competitive_gaps": []
            }
            
            # Analyze capability gaps
            for gap_rule in self.gap_detection_rules["capability_gaps"]:
                coverage_level = len(gap_rule["current_coverage"]) / len(gap_rule["desired_coverage"])
                
                if coverage_level < 0.5:
                    detected_gaps["capability_gaps"].append({
                        "category": gap_rule["category"],
                        "gap_name": gap_rule["name"],
                        "importance": gap_rule["importance"],
                        "coverage_level": f"{coverage_level*100:.1f}%",
                        "missing_capabilities": [
                            cap for cap in gap_rule["desired_coverage"]
                            if cap not in gap_rule["current_coverage"]
                        ],
                        "priority": "high" if gap_rule["importance"] == "high" else "medium"
                    })
            
            # Analyze market gaps
            for market_gap in self.gap_detection_rules["market_gaps"]:
                if market_gap["current_penetration"] < 0.10:  # Less than 10% penetration
                    detected_gaps["market_gaps"].append({
                        "market_segment": market_gap["segment"],
                        "current_penetration": f"{market_gap['current_penetration']*100:.1f}%",
                        "market_size": market_gap["market_size"],
                        "revenue_potential": market_gap["revenue_potential"],
                        "competition_level": market_gap["competition"],
                        "priority": "high" if market_gap["revenue_potential"] > 100000 else "medium"
                    })
            
            # Analyze revenue gaps
            for revenue_gap in self.gap_detection_rules["revenue_gaps"]:
                detected_gaps["revenue_gaps"].append({
                    "gap_type": revenue_gap["gap_type"],
                    "description": revenue_gap["description"],
                    "impact": revenue_gap["impact"],
                    "potential_revenue": revenue_gap["potential_revenue"],
                    "priority": "high" if revenue_gap["impact"] == "high" else "medium"
                })
            
            # Analyze technology gaps
            detected_gaps["technology_gaps"] = self._detect_technology_gaps(bricks_context)
            
            # Analyze competitive gaps
            detected_gaps["competitive_gaps"] = self._detect_competitive_gaps()
            
            # Calculate total gap impact
            total_gap_count = sum(len(gaps) for gaps in detected_gaps.values())
            high_priority_gaps = sum(
                sum(1 for gap in gaps if gap.get("priority") == "high")
                for gaps in detected_gaps.values()
            )
            
            return {
                "status": "success",
                "detected_gaps": detected_gaps,
                "total_gaps": total_gap_count,
                "high_priority_gaps": high_priority_gaps,
                "gap_severity": self._calculate_gap_severity(detected_gaps),
                "top_priority_gaps": self._get_top_priority_gaps(detected_gaps),
                "strategic_recommendations": self._generate_gap_recommendations(detected_gaps),
                "analysis_timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error("Failed to detect strategic gaps", error=str(e))
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _detect_technology_gaps(self, bricks_context: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect technology stack gaps"""
        technology_gaps = []
        
        # Common technology gaps
        common_gaps = [
            {
                "technology": "Real-time Analytics",
                "current_status": "missing",
                "importance": "high",
                "impact": "Data-driven decision making",
                "priority": "high"
            },
            {
                "technology": "Mobile Applications",
                "current_status": "missing",
                "importance": "medium",
                "impact": "Mobile user engagement",
                "priority": "medium"
            },
            {
                "technology": "Advanced Security",
                "current_status": "basic",
                "importance": "high",
                "impact": "Enterprise customer trust",
                "priority": "high"
            }
        ]
        
        return common_gaps
    
    def _detect_competitive_gaps(self) -> List[Dict[str, Any]]:
        """Detect competitive positioning gaps"""
        return [
            {
                "gap": "Enterprise Features",
                "competitor_has": True,
                "we_have": False,
                "impact": "high",
                "examples": ["SSO", "Advanced reporting", "API access"],
                "priority": "high"
            },
            {
                "gap": "White Label Options",
                "competitor_has": True,
                "we_have": False,
                "impact": "medium",
                "examples": ["Custom branding", "Reseller programs"],
                "priority": "medium"
            }
        ]
    
    def _calculate_gap_severity(self, gaps: Dict[str, List[Dict[str, Any]]]) -> str:
        """Calculate overall gap severity"""
        total_gaps = sum(len(gap_list) for gap_list in gaps.values())
        high_priority = sum(
            sum(1 for gap in gap_list if gap.get("priority") == "high")
            for gap_list in gaps.values()
        )
        
        if high_priority >= 5:
            return "critical"
        elif high_priority >= 3:
            return "high"
        elif total_gaps >= 5:
            return "medium"
        else:
            return "low"
    
    def _get_top_priority_gaps(self, gaps: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Get top 5 priority gaps"""
        all_gaps = []
        
        for gap_type, gap_list in gaps.items():
            for gap in gap_list:
                all_gaps.append({
                    "gap_type": gap_type,
                    "gap_data": gap,
                    "priority_score": self._calculate_priority_score(gap)
                })
        
        # Sort by priority score
        all_gaps.sort(key=lambda x: x["priority_score"], reverse=True)
        
        return all_gaps[:5]
    
    def _calculate_priority_score(self, gap: Dict[str, Any]) -> float:
        """Calculate priority score for a gap"""
        score = 0.0
        
        # Base score from priority
        if gap.get("priority") == "high":
            score += 10.0
        elif gap.get("priority") == "medium":
            score += 5.0
        
        # Add score from importance
        if gap.get("importance") == "high":
            score += 5.0
        
        # Add score from impact
        if gap.get("impact") == "high":
            score += 5.0
        
        # Add score from revenue potential
        if gap.get("potential_revenue"):
            score += min(gap["potential_revenue"] / 1000, 10.0)
        
        return score
    
    def _generate_gap_recommendations(self, gaps: Dict[str, List[Dict[str, Any]]]) -> List[str]:
        """Generate strategic recommendations to address gaps"""
        recommendations = []
        
        # High priority capability gaps
        capability_gaps = [g for g in gaps.get("capability_gaps", []) if g.get("priority") == "high"]
        if capability_gaps:
            recommendations.append(
                f"Address {len(capability_gaps)} high-priority capability gaps to strengthen competitive position"
            )
        
        # High revenue potential market gaps
        market_gaps = [g for g in gaps.get("market_gaps", []) if g.get("priority") == "high"]
        if market_gaps:
            total_potential = sum(g.get("revenue_potential", 0) for g in market_gaps)
            recommendations.append(
                f"Target {len(market_gaps)} high-potential market segments (${total_potential:,.0f} opportunity)"
            )
        
        # Revenue optimization
        revenue_gaps = gaps.get("revenue_gaps", [])
        if revenue_gaps:
            total_potential = sum(g.get("potential_revenue", 0) for g in revenue_gaps)
            recommendations.append(
                f"Implement revenue optimization strategies (${total_potential:,.0f}/month potential)"
            )
        
        # Technology gaps
        tech_gaps = [g for g in gaps.get("technology_gaps", []) if g.get("priority") == "high"]
        if tech_gaps:
            recommendations.append(
                f"Invest in {len(tech_gaps)} critical technology capabilities"
            )
        
        # Default recommendation
        if not recommendations:
            recommendations.append("Continue monitoring ecosystem for emerging gaps")
        
        return recommendations
    
    async def get_status(self) -> Dict[str, Any]:
        """Get service status"""
        return {
            "service": "strategic_gap_detection",
            "status": "operational",
            "gap_detection_rules": len(self.gap_detection_rules.get("capability_gaps", [])),
            "detected_gaps": len(self.detected_gaps)
        }
