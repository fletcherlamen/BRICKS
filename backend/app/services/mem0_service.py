"""
Mem0.ai Service Integration
Handles persistent memory and context management
"""

from typing import Dict, List, Optional, Any
import structlog
from datetime import datetime

from app.core.config import settings
from app.core.exceptions import Mem0Error

logger = structlog.get_logger(__name__)


class Mem0Service:
    """Mem0.ai service for persistent memory management"""
    
    def __init__(self):
        self.initialized = False
        self.client = None
        
    async def initialize(self):
        """Initialize Mem0 service"""
        try:
            if not settings.MEM0_API_KEY:
                raise Mem0Error("Mem0 API key not configured")
            
            # Import Mem0 client
            try:
                import mem0
            except ImportError:
                raise Mem0Error("Mem0 not installed. Run: pip install mem0ai")
            
            # Initialize Mem0 client
            self.client = mem0.Mem0(
                api_key=settings.MEM0_API_KEY,
                base_url=settings.MEM0_BASE_URL
            )
            
            self.initialized = True
            logger.info("Mem0 service initialized successfully")
            
        except Exception as e:
            logger.error("Failed to initialize Mem0 service", error=str(e))
            raise Mem0Error(f"Mem0 initialization failed: {str(e)}")
    
    async def store_context(
        self,
        session_id: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Store session context in memory"""
        
        if not self.initialized:
            raise Mem0Error("Mem0 service not initialized")
        
        try:
            # Convert context to memory entries
            memories = []
            
            for key, value in context.items():
                memory_entry = {
                    "text": f"{key}: {str(value)}",
                    "metadata": {
                        "session_id": session_id,
                        "context_key": key,
                        "timestamp": datetime.now().isoformat(),
                        "type": "context"
                    }
                }
                memories.append(memory_entry)
            
            # Store memories
            results = []
            for memory in memories:
                result = self.client.add(
                    memory["text"],
                    metadata=memory["metadata"]
                )
                results.append(result)
            
            logger.info("Context stored in memory", session_id=session_id, memories_count=len(memories))
            
            return {
                "stored_memories": results,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error("Failed to store context", error=str(e), session_id=session_id)
            raise Mem0Error(f"Failed to store context: {str(e)}")
    
    async def store_result(
        self,
        session_id: str,
        result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Store orchestration results in memory"""
        
        if not self.initialized:
            raise Mem0Error("Mem0 service not initialized")
        
        try:
            # Create memory entries for results
            memories = []
            
            for key, value in result.items():
                memory_entry = {
                    "text": f"Result for {key}: {str(value)}",
                    "metadata": {
                        "session_id": session_id,
                        "result_key": key,
                        "timestamp": datetime.now().isoformat(),
                        "type": "result"
                    }
                }
                memories.append(memory_entry)
            
            # Store memories
            results = []
            for memory in memories:
                result = self.client.add(
                    memory["text"],
                    metadata=memory["metadata"]
                )
                results.append(result)
            
            logger.info("Results stored in memory", session_id=session_id, results_count=len(results))
            
            return {
                "stored_results": results,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error("Failed to store results", error=str(e), session_id=session_id)
            raise Mem0Error(f"Failed to store results: {str(e)}")
    
    async def retrieve_relevant_memories(
        self,
        query: str,
        context: Dict[str, Any],
        limit: int = 10
    ) -> Dict[str, Any]:
        """Retrieve memories relevant to a query"""
        
        if not self.initialized:
            raise Mem0Error("Mem0 service not initialized")
        
        try:
            # Search for relevant memories
            memories = self.client.search(query, limit=limit)
            
            logger.info("Retrieved relevant memories", query=query, count=len(memories))
            
            return {
                "memories": memories,
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "count": len(memories)
            }
            
        except Exception as e:
            logger.error("Failed to retrieve memories", error=str(e), query=query)
            raise Mem0Error(f"Failed to retrieve memories: {str(e)}")
    
    async def find_similar_strategies(
        self,
        goal: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Find similar successful strategies from memory"""
        
        if not self.initialized:
            raise Mem0Error("Mem0 service not initialized")
        
        try:
            # Search for similar strategies
            strategy_query = f"successful strategy for {goal}"
            memories = self.client.search(strategy_query, limit=5)
            
            # Filter for strategy-related memories
            strategies = []
            for memory in memories:
                if memory.get("metadata", {}).get("type") == "strategy":
                    strategies.append(memory)
            
            logger.info("Found similar strategies", goal=goal, strategies_count=len(strategies))
            
            return {
                "similar_strategies": strategies,
                "goal": goal,
                "timestamp": datetime.now().isoformat(),
                "count": len(strategies)
            }
            
        except Exception as e:
            logger.error("Failed to find similar strategies", error=str(e), goal=goal)
            raise Mem0Error(f"Failed to find similar strategies: {str(e)}")
    
    async def store_strategy(
        self,
        strategy: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Store a successful strategy in memory"""
        
        if not self.initialized:
            raise Mem0Error("Mem0 service not initialized")
        
        try:
            # Create strategy memory entry
            strategy_text = f"Successful strategy: {strategy.get('description', '')}"
            
            result = self.client.add(
                strategy_text,
                metadata={
                    "session_id": session_id,
                    "type": "strategy",
                    "success_rate": strategy.get("success_rate", 0),
                    "revenue_impact": strategy.get("revenue_impact", 0),
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            logger.info("Strategy stored in memory", session_id=session_id, strategy_id=result.get("id"))
            
            return {
                "stored_strategy": result,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error("Failed to store strategy", error=str(e), session_id=session_id)
            raise Mem0Error(f"Failed to store strategy: {str(e)}")
    
    async def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        
        if not self.initialized:
            raise Mem0Error("Mem0 service not initialized")
        
        try:
            # Get all memories
            all_memories = self.client.get_all()
            
            # Calculate statistics
            stats = {
                "total_memories": len(all_memories),
                "memory_types": {},
                "recent_memories": 0,
                "session_count": 0
            }
            
            # Analyze memory types and sessions
            sessions = set()
            recent_count = 0
            cutoff_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            for memory in all_memories:
                metadata = memory.get("metadata", {})
                
                # Count memory types
                memory_type = metadata.get("type", "unknown")
                stats["memory_types"][memory_type] = stats["memory_types"].get(memory_type, 0) + 1
                
                # Count sessions
                session_id = metadata.get("session_id")
                if session_id:
                    sessions.add(session_id)
                
                # Count recent memories
                timestamp_str = metadata.get("timestamp")
                if timestamp_str:
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        if timestamp >= cutoff_date:
                            recent_count += 1
                    except:
                        pass
            
            stats["recent_memories"] = recent_count
            stats["session_count"] = len(sessions)
            
            return stats
            
        except Exception as e:
            logger.error("Failed to get memory stats", error=str(e))
            raise Mem0Error(f"Failed to get memory stats: {str(e)}")
    
    async def get_status(self) -> Dict[str, Any]:
        """Get Mem0 service status"""
        
        if not self.initialized:
            return {"status": "not_initialized"}
        
        try:
            # Test memory operations
            test_result = self.client.search("test", limit=1)
            
            return {
                "status": "healthy",
                "api_key_configured": bool(settings.MEM0_API_KEY),
                "client_initialized": self.client is not None,
                "test_query_successful": True
            }
            
        except Exception as e:
            logger.error("Mem0 health check failed", error=str(e))
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def cleanup(self):
        """Cleanup Mem0 resources"""
        try:
            self.client = None
            self.initialized = False
            logger.info("Mem0 service cleaned up")
        except Exception as e:
            logger.error("Error cleaning up Mem0 service", error=str(e))
