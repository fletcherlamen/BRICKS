"""
Trinity BRICKS I ASSESS - Automated Code Quality Auditing Service

Provides:
- Repository cloning and analysis
- UBIC v1.5 compliance checking
- Test coverage measurement
- AI-powered code review
- Payment recommendations
"""

import os
import subprocess
import tempfile
import shutil
import json
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid
import structlog
from pathlib import Path
import anthropic

from app.core.config import settings

logger = structlog.get_logger(__name__)


class AssessService:
    """I ASSESS - Code auditing and quality assessment service"""
    
    def __init__(self):
        self.claude_client = None
        if settings.ANTHROPIC_API_KEY and settings.ANTHROPIC_API_KEY != "your-anthropic-api-key":
            try:
                self.claude_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
                logger.info("Claude API initialized for I ASSESS")
            except Exception as e:
                logger.warning("Failed to initialize Claude for I ASSESS", error=str(e))
    
    async def start_audit(
        self,
        repository_url: str,
        user_id: str,
        criteria: List[str] = None
    ) -> Dict[str, Any]:
        """
        Start a new code audit
        
        Args:
            repository_url: GitHub repository URL
            user_id: User identifier
            criteria: List of audit criteria (UBIC_compliance, test_coverage, etc.)
        
        Returns:
            Audit ID and initial status
        """
        audit_id = f"audit_{uuid.uuid4().hex[:16]}"
        
        logger.info("Starting audit",
                   audit_id=audit_id,
                   repository=repository_url,
                   user_id=user_id)
        
        # For now, return audit ID (actual processing will be async)
        return {
            "audit_id": audit_id,
            "status": "running",
            "repository": repository_url,
            "user_id": user_id,
            "started_at": datetime.now().isoformat()
        }
    
    async def check_ubic_compliance(self, repo_path: str) -> Dict[str, Any]:
        """
        Check if repository has all required UBIC v1.5 endpoints
        
        Scans code for the 9 required endpoints:
        /health, /capabilities, /state, /dependencies,
        /message, /send, /reload-config, /shutdown, /emergency-stop
        """
        required_endpoints = [
            "/health", "/capabilities", "/state", "/dependencies",
            "/message", "/send", "/reload-config",
            "/shutdown", "/emergency-stop"
        ]
        
        found_endpoints = []
        
        try:
            # Scan Python files for FastAPI route definitions
            for root, dirs, files in os.walk(repo_path):
                # Skip common non-code directories
                dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', '__pycache__', '.pytest_cache']]
                
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                
                                # Look for FastAPI route definitions
                                for endpoint in required_endpoints:
                                    patterns = [
                                        rf'@\w+\.(?:get|post|put|delete)\s*\(\s*["\']{ re.escape(endpoint)}["\']',
                                        rf'router\.(?:get|post|put|delete)\s*\(\s*["\']{ re.escape(endpoint)}["\']',
                                        rf'app\.(?:get|post|put|delete)\s*\(\s*["\']{ re.escape(endpoint)}["\']'
                                    ]
                                    
                                    for pattern in patterns:
                                        if re.search(pattern, content):
                                            if endpoint not in found_endpoints:
                                                found_endpoints.append(endpoint)
                                            break
                        except Exception as e:
                            logger.warning(f"Could not read file {file_path}", error=str(e))
        
        except Exception as e:
            logger.error("UBIC compliance check failed", error=str(e))
        
        missing = list(set(required_endpoints) - set(found_endpoints))
        compliance_percent = (len(found_endpoints) / len(required_endpoints)) * 100
        
        return {
            "total_required": len(required_endpoints),
            "found": len(found_endpoints),
            "missing": missing,
            "compliant": len(found_endpoints) == len(required_endpoints),
            "compliance_percent": compliance_percent,
            "found_endpoints": found_endpoints
        }
    
    async def run_tests(self, repo_path: str) -> Dict[str, Any]:
        """
        Execute pytest and measure test coverage
        """
        try:
            # Check if pytest exists in repo
            test_dirs = ['tests', 'test', 'testing']
            has_tests = any(os.path.exists(os.path.join(repo_path, d)) for d in test_dirs)
            
            if not has_tests:
                return {
                    "tests_passed": False,
                    "coverage_percent": 0,
                    "tests_run": 0,
                    "meets_80_threshold": False,
                    "error": "No test directory found"
                }
            
            # Run pytest with coverage
            result = subprocess.run(
                ["pytest", "--cov=.", "--cov-report=json", "--cov-report=term", "-v"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            # Try to load coverage report
            coverage_file = os.path.join(repo_path, "coverage.json")
            if os.path.exists(coverage_file):
                with open(coverage_file) as f:
                    coverage_data = json.load(f)
                
                coverage_percent = coverage_data.get("totals", {}).get("percent_covered", 0)
                tests_run = coverage_data.get("totals", {}).get("num_statements", 0)
            else:
                coverage_percent = 0
                tests_run = 0
            
            return {
                "tests_passed": result.returncode == 0,
                "coverage_percent": coverage_percent,
                "tests_run": tests_run,
                "meets_80_threshold": coverage_percent >= 80,
                "test_output": result.stdout[:1000] if result.stdout else "",
                "test_errors": result.stderr[:500] if result.stderr else ""
            }
            
        except subprocess.TimeoutExpired:
            return {
                "tests_passed": False,
                "coverage_percent": 0,
                "tests_run": 0,
                "meets_80_threshold": False,
                "error": "Tests timed out after 5 minutes"
            }
        except Exception as e:
            logger.error("Test execution failed", error=str(e))
            return {
                "tests_passed": False,
                "coverage_percent": 0,
                "tests_run": 0,
                "meets_80_threshold": False,
                "error": str(e)
            }
    
    async def ai_code_review(
        self,
        repo_path: str,
        ubic_results: Dict[str, Any],
        test_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Use Claude AI to perform code quality review
        """
        if not self.claude_client:
            return {
                "quality_score": 5,
                "production_ready": False,
                "findings": ["Claude API not configured - using basic analysis"],
                "recommendations": ["Configure ANTHROPIC_API_KEY for AI code review"],
                "mock": True
            }
        
        try:
            # Get sample code files
            code_samples = await self._get_code_samples(repo_path, max_files=5)
            
            # Build analysis prompt
            prompt = f"""Analyze this code repository:

**UBIC Compliance:**
- Required endpoints: {ubic_results['total_required']}
- Found: {ubic_results['found']}
- Missing: {ubic_results['missing']}
- Compliant: {ubic_results['compliant']}

**Test Results:**
- Tests passed: {test_results['tests_passed']}
- Coverage: {test_results['coverage_percent']:.1f}%
- Meets 80% threshold: {test_results['meets_80_threshold']}

**Code Samples:**
{code_samples}

Provide a brief assessment with:
1. Code quality score (1-10)
2. Is it production ready? (yes/no with brief reason)
3. Top 3 security/quality concerns
4. Top 3 recommended improvements

Be concise and data-driven."""

            response = self.claude_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            ai_response = response.content[0].text
            
            # Parse response for structured data
            return {
                "quality_score": self._extract_score(ai_response),
                "production_ready": "yes" in ai_response.lower() and "production ready" in ai_response.lower(),
                "ai_analysis": ai_response,
                "findings": self._extract_list(ai_response, "concerns"),
                "recommendations": self._extract_list(ai_response, "improvements")
            }
            
        except Exception as e:
            logger.error("AI code review failed", error=str(e))
            return {
                "quality_score": 5,
                "production_ready": False,
                "findings": [f"AI review failed: {str(e)}"],
                "recommendations": ["Fix AI review integration"],
                "error": str(e)
            }
    
    async def _get_code_samples(self, repo_path: str, max_files: int = 5) -> str:
        """Get sample code files for AI review"""
        samples = []
        count = 0
        
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', '__pycache__']]
            
            for file in files:
                if file.endswith('.py') and not file.startswith('test_'):
                    if count >= max_files:
                        break
                    
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()[:500]  # First 500 chars
                            samples.append(f"File: {file}\n{content}\n...")
                            count += 1
                    except:
                        continue
            
            if count >= max_files:
                break
        
        return "\n\n".join(samples) if samples else "No code files found"
    
    def _extract_score(self, text: str) -> int:
        """Extract numerical score from AI response"""
        match = re.search(r'(?:score|quality).*?(\d+)\s*(?:/|out of)\s*10', text, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 5  # Default
    
    def _extract_list(self, text: str, keyword: str) -> List[str]:
        """Extract bullet points from AI response"""
        lines = text.split('\n')
        items = []
        in_section = False
        
        for line in lines:
            if keyword.lower() in line.lower():
                in_section = True
                continue
            
            if in_section:
                # Look for bullet points or numbered lists
                if re.match(r'^\s*[\d\-\*•]\s*\.?\s*', line):
                    item = re.sub(r'^\s*[\d\-\*•]\s*\.?\s*', '', line).strip()
                    if item:
                        items.append(item)
                elif line.strip() and not line.strip().startswith('#'):
                    # Check if we're in a new section
                    if line.strip().endswith(':') or line.isupper():
                        break
        
        return items[:3] if items else ["No specific items found"]
    
    def calculate_payment_recommendation(self, audit_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate data-driven payment recommendation
        
        Scoring:
        - UBIC compliance: 30 points
        - Test coverage: 30 points
        - Tests passing: 20 points  
        - AI quality score: 20 points
        """
        score = 0
        max_score = 100
        breakdown = {}
        
        # UBIC compliance (30 points)
        if audit_results["ubic"]["compliant"]:
            score += 30
            breakdown["ubic"] = 30
        else:
            partial = (audit_results["ubic"]["found"] / audit_results["ubic"]["total_required"]) * 30
            score += partial
            breakdown["ubic"] = round(partial, 1)
        
        # Test coverage (30 points)
        coverage = audit_results["tests"]["coverage_percent"]
        if coverage >= 80:
            score += 30
            breakdown["coverage"] = 30
        elif coverage >= 60:
            score += 15
            breakdown["coverage"] = 15
        elif coverage > 0:
            score += (coverage / 80) * 30
            breakdown["coverage"] = round((coverage / 80) * 30, 1)
        else:
            breakdown["coverage"] = 0
        
        # Tests passing (20 points)
        if audit_results["tests"]["tests_passed"]:
            score += 20
            breakdown["tests_pass"] = 20
        else:
            breakdown["tests_pass"] = 0
        
        # AI code quality (20 points)
        ai_score = audit_results["ai_review"]["quality_score"]
        quality_points = (ai_score / 10) * 20
        score += quality_points
        breakdown["ai_quality"] = round(quality_points, 1)
        
        # Determine recommendation
        if score >= 90:
            recommendation = "APPROVE_FULL_PAYMENT"
            action = "Approve full payment"
            confidence = "high"
        elif score >= 70:
            recommendation = "APPROVE_PARTIAL_PAYMENT"
            action = "Approve 50-75% payment, request improvements"
            confidence = "medium"
        elif score >= 50:
            recommendation = "REQUEST_FIXES_FIRST"
            action = "Request fixes before payment"
            confidence = "medium"
        else:
            recommendation = "REJECT_DO_NOT_PAY"
            action = "Do not pay - significant issues found"
            confidence = "high"
        
        return {
            "total_score": round(score, 1),
            "max_score": max_score,
            "percentage": round((score / max_score) * 100, 1),
            "recommendation": recommendation,
            "action": action,
            "confidence": confidence,
            "score_breakdown": breakdown,
            "reasoning": self._generate_reasoning(audit_results, score, breakdown)
        }
    
    def _generate_reasoning(
        self,
        audit_results: Dict[str, Any],
        total_score: float,
        breakdown: Dict[str, float]
    ) -> str:
        """Generate human-readable reasoning for payment recommendation"""
        reasons = []
        
        # UBIC
        if audit_results["ubic"]["compliant"]:
            reasons.append(f"✅ Full UBIC compliance ({audit_results['ubic']['found']}/9 endpoints)")
        else:
            reasons.append(f"⚠️  UBIC: {audit_results['ubic']['found']}/9 endpoints (missing: {', '.join(audit_results['ubic']['missing'][:2])})")
        
        # Coverage
        cov = audit_results["tests"]["coverage_percent"]
        if cov >= 80:
            reasons.append(f"✅ Excellent test coverage ({cov:.1f}%)")
        elif cov >= 60:
            reasons.append(f"⚠️  Moderate coverage ({cov:.1f}%, target: 80%)")
        else:
            reasons.append(f"❌ Low test coverage ({cov:.1f}%, needs improvement)")
        
        # Tests
        if audit_results["tests"]["tests_passed"]:
            reasons.append("✅ All tests passing")
        else:
            reasons.append("❌ Tests failing")
        
        # AI quality
        quality = audit_results["ai_review"]["quality_score"]
        if quality >= 8:
            reasons.append(f"✅ High code quality ({quality}/10)")
        elif quality >= 6:
            reasons.append(f"⚠️  Good code quality ({quality}/10)")
        else:
            reasons.append(f"❌ Code quality needs improvement ({quality}/10)")
        
        return " | ".join(reasons)
    
    async def clone_repository(self, repository_url: str) -> str:
        """
        Clone repository to temporary directory
        
        Returns path to cloned repository
        """
        try:
            import git
            
            # Create temp directory
            temp_dir = tempfile.mkdtemp(prefix="i_assess_")
            
            logger.info("Cloning repository",
                       url=repository_url,
                       target=temp_dir)
            
            # Clone repository
            git.Repo.clone_from(repository_url, temp_dir, depth=1)
            
            logger.info("Repository cloned successfully",
                       path=temp_dir)
            
            return temp_dir
            
        except Exception as e:
            logger.error("Failed to clone repository", error=str(e))
            raise Exception(f"Failed to clone repository: {str(e)}")
    
    def cleanup_repository(self, repo_path: str):
        """Clean up cloned repository"""
        try:
            if repo_path and os.path.exists(repo_path):
                shutil.rmtree(repo_path)
                logger.info("Cleaned up repository", path=repo_path)
        except Exception as e:
            logger.warning("Failed to cleanup repository", error=str(e), path=repo_path)

