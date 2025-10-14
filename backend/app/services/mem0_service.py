"""
Mem0.ai Service Integration - Trinity BRICKS I MEMORY
Handles persistent memory and context management with multi-user isolation
"""

from typing import Dict, List, Optional, Any
import structlog
from datetime import datetime
import hashlib
import json

from app.core.config import settings
from app.core.exceptions import Mem0Error

logger = structlog.get_logger(__name__)


class Mem0Service:
    """
    Mem0.ai service for persistent memory management
    
    Trinity BRICKS I MEMORY Features:
    - Multi-user isolation (each user has private memory namespace)
    - Semantic search across memories
    - Persistent storage with Redis caching
    """
    
    def __init__(self):
        self.initialized = False
        self.client = None
        self.redis_client = None
        
    async def initialize(self):
        """Initialize Mem0 service with Redis caching"""
        try:
            # Initialize Redis client for caching (Trinity BRICKS requirement)
            try:
                import redis.asyncio as redis
                redis_url = getattr(settings, 'REDIS_URL', "redis://redis:6379")
                self.redis_client = redis.from_url(redis_url, decode_responses=True)
                await self.redis_client.ping()
                logger.info("Redis client initialized successfully for I MEMORY")
            except Exception as e:
                logger.warning("Redis not available, caching disabled", error=str(e))
                self.redis_client = None
            
            # Import Mem0 client
            try:
                import mem0
            except ImportError as e:
                logger.warning("Mem0 not available, running in mock mode", error=str(e))
                self.initialized = False
                return
            
            # Check if API key is configured (optional for mock mode)
            if not settings.MEM0_API_KEY:
                logger.warning("Mem0 API key not configured, running in mock mode")
                self.initialized = False
                return
            
            # Initialize Mem0 client with error handling for aiohttp compatibility
            try:
                self.client = mem0.Mem0(
                    api_key=settings.MEM0_API_KEY,
                    base_url=settings.MEM0_BASE_URL
                )
                
                # Test the client with a simple operation
                test_result = self.client.search("test", limit=1)
                
                self.initialized = True
                logger.info("Mem0 service initialized successfully with multi-user support")
                
            except AttributeError as e:
                if "ConnectionTimeoutError" in str(e) or "aiohttp" in str(e):
                    logger.warning("Mem0 aiohttp compatibility issue, running in enhanced mock mode", error=str(e))
                    self.initialized = False
                    return
                else:
                    raise e
            
        except Exception as e:
            logger.warning("Failed to initialize Mem0 service, running in mock mode", error=str(e))
            self.initialized = False
    
    async def store_context(
        self,
        session_id: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Store session context in memory"""
        
        if not self.initialized:
            # Return mock response when Mem0 is not available
            return {
                "success": True,
                "session_id": session_id,
                "context_id": f"mock_context_{datetime.now().timestamp()}",
                "timestamp": datetime.now().isoformat(),
                "mock": True,
                "message": "Context stored in mock mode"
            }
        
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
            # Return mock response when Mem0 is not available
            return {
                "success": True,
                "session_id": session_id,
                "result_id": f"mock_result_{datetime.now().timestamp()}",
                "timestamp": datetime.now().isoformat(),
                "mock": True,
                "message": "Result stored in mock mode"
            }
        
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
            # Return mock response when Mem0 is not available
            return {
                "memories": [
                    {
                        "id": f"mock_memory_{i}",
                        "text": f"Mock memory {i} related to: {query}",
                        "metadata": {"mock": True, "relevance": 0.8 - (i * 0.1)}
                    }
                    for i in range(min(limit, 3))
                ],
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "mock": True,
                "message": "Retrieved mock memories"
            }
        
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
        
        if not settings.MEM0_API_KEY:
            return {
                "status": "critical",
                "mode": "fallback",
                "api_key_configured": False,
                "message": "API key not configured - using VPS database only (limited functionality)",
                "error": "Missing MEM0_API_KEY"
            }
        
        if not self.initialized:
            # Check if this is due to aiohttp compatibility issue
            try:
                import mem0
                mem0.Mem0(api_key=settings.MEM0_API_KEY)
            except AttributeError as e:
                if "ConnectionTimeoutError" in str(e) or "aiohttp" in str(e):
                    return {
                        "status": "warning",
                        "mode": "enhanced_mock",
                        "api_key_configured": True,
                        "message": "API key configured but mem0ai library has compatibility issues - using enhanced mock mode",
                        "error": "aiohttp compatibility issue",
                        "note": "Mem0 functionality simulated with VPS database persistence"
                    }
            
            return {
                "status": "error",
                "mode": "fallback",
                "api_key_configured": True,
                "message": "Mem0 initialization failed - using VPS database fallback",
                "error": "Service initialization failed"
            }
        
        try:
            # Test memory operations
            test_result = self.client.search("test", limit=1)
            
            return {
                "status": "healthy",
                "mode": "real_ai",
                "api_key_configured": True,
                "client_initialized": True,
                "test_query_successful": True
            }
            
        except Exception as e:
            logger.error("Mem0 health check failed", error=str(e))
            return {
                "status": "error",
                "mode": "failed",
                "api_key_configured": True,
                "error": str(e)
            }
    
    async def cleanup(self):
        """Cleanup Mem0 resources"""
        try:
            if self.redis_client:
                await self.redis_client.close()
            self.client = None
            self.redis_client = None
            self.initialized = False
            logger.info("Mem0 service cleaned up")
        except Exception as e:
            logger.error("Error cleaning up Mem0 service", error=str(e))
    
    # ============================================
    # Trinity BRICKS I MEMORY - Multi-User Methods
    # ============================================
    
    def _get_user_namespace(self, user_id: str) -> str:
        """Generate unique namespace for each user (Trinity BRICKS requirement)"""
        hash_obj = hashlib.sha256(user_id.encode())
        return f"user_{hash_obj.hexdigest()[:16]}"
    
    async def _get_cache_key(self, user_id: str, key_suffix: str) -> str:
        """Generate Redis cache key"""
        return f"i_memory:{self._get_user_namespace(user_id)}:{key_suffix}"
    
    async def _get_from_cache(self, cache_key: str) -> Optional[Any]:
        """Get data from Redis cache"""
        if not self.redis_client:
            return None
        try:
            data = await self.redis_client.get(cache_key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.warning("Cache get failed", error=str(e))
            return None
    
    async def _set_cache(self, cache_key: str, data: Any, ttl: int = 300):
        """Set data in Redis cache with TTL"""
        if not self.redis_client:
            return
        try:
            await self.redis_client.setex(cache_key, ttl, json.dumps(data))
        except Exception as e:
            logger.warning("Cache set failed", error=str(e))
    
    async def add(
        self,
        content: Dict[str, Any],
        user_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add memory with user isolation (Trinity BRICKS I MEMORY)
        
        Example:
            await memory.add(
                content={"developer": "Fletcher", "status": "verified"},
                user_id="james@fullpotential.com",
                metadata={"category": "developer_assessment"}
            )
        """
        user_namespace = self._get_user_namespace(user_id)
        
        if not self.initialized:
            # Mock mode
            memory_id = f"mock_{user_namespace}_{datetime.now().timestamp()}"
            return {
                "memory_id": memory_id,
                "user_id": user_id,
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "mock": True
            }
        
        try:
            memory_text = json.dumps(content)
            full_metadata = metadata or {}
            full_metadata.update({
                "original_user_id": user_id,
                "timestamp": datetime.now().isoformat()
            })
            
            result = self.client.add(
                memory_text,
                user_id=user_namespace,
                metadata=full_metadata
            )
            
            # Invalidate cache
            cache_key = await self._get_cache_key(user_id, "all_memories")
            if self.redis_client:
                await self.redis_client.delete(cache_key)
            
            logger.info("Memory added with user isolation", 
                       user_id=user_id, memory_id=result.get("id"))
            
            return {
                "memory_id": result.get("id"),
                "user_id": user_id,
                "content": content,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error("Failed to add memory", error=str(e), user_id=user_id)
            raise Mem0Error(f"Failed to add memory: {str(e)}")
    
    async def search(
        self,
        query: str,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Semantic search with user isolation (Trinity BRICKS I MEMORY)
        
        Example:
            results = await memory.search(
                query="What's Fletcher's status?",
                user_id="james@fullpotential.com",
                limit=5
            )
        """
        user_namespace = self._get_user_namespace(user_id)
        
        # Try cache first
        cache_key = await self._get_cache_key(user_id, f"search:{query}:{limit}")
        cached = await self._get_from_cache(cache_key)
        if cached:
            logger.info("Returning cached search results", user_id=user_id)
            return cached
        
        if not self.initialized:
            # Mock mode
            return [{
                "memory_id": f"mock_{user_namespace}_{i}",
                "content": {"text": f"Mock memory {i} for: {query}"},
                "relevance_score": 0.9 - (i * 0.1),
                "user_id": user_id,
                "mock": True
            } for i in range(min(limit, 3))]
        
        try:
            memories = self.client.search(query, user_id=user_namespace, limit=limit)
            
            results = []
            for memory in memories:
                try:
                    content = json.loads(memory.get("memory", "{}"))
                except:
                    content = {"text": memory.get("memory", "")}
                
                results.append({
                    "memory_id": memory.get("id"),
                    "content": content,
                    "relevance_score": memory.get("score", 0),
                    "user_id": user_id,
                    "metadata": memory.get("metadata", {})
                })
            
            # Cache results
            await self._set_cache(cache_key, results, ttl=180)
            
            logger.info("Searched memories", user_id=user_id, results_count=len(results))
            return results
        except Exception as e:
            logger.error("Failed to search memories", error=str(e), user_id=user_id)
            raise Mem0Error(f"Failed to search memories: {str(e)}")
    
    async def get_all(
        self,
        user_id: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get all memories for user (Trinity BRICKS I MEMORY)
        
        Example:
            all_memories = await memory.get_all(
                user_id="james@fullpotential.com"
            )
        """
        user_namespace = self._get_user_namespace(user_id)
        
        # Try cache
        cache_key = await self._get_cache_key(user_id, "all_memories")
        cached = await self._get_from_cache(cache_key)
        if cached:
            return cached[:limit]
        
        if not self.initialized:
            # Mock mode
            return [{
                "memory_id": f"mock_{user_namespace}_{i}",
                "content": {"text": f"Mock memory {i} for user {user_id}"},
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "mock": True
            } for i in range(min(limit, 5))]
        
        try:
            memories = self.client.get_all(user_id=user_namespace)
            
            results = []
            for memory in memories[:limit]:
                try:
                    content = json.loads(memory.get("memory", "{}"))
                except:
                    content = {"text": memory.get("memory", "")}
                
                results.append({
                    "memory_id": memory.get("id"),
                    "content": content,
                    "user_id": user_id,
                    "timestamp": memory.get("metadata", {}).get("timestamp", ""),
                    "metadata": memory.get("metadata", {})
                })
            
            # Cache results
            await self._set_cache(cache_key, results, ttl=300)
            
            logger.info("Retrieved all memories", user_id=user_id, count=len(results))
            return results
        except Exception as e:
            logger.error("Failed to get all memories", error=str(e), user_id=user_id)
            raise Mem0Error(f"Failed to get all memories: {str(e)}")
    
    async def delete(
        self,
        memory_id: str,
        user_id: str
    ) -> bool:
        """
        Delete memory with user ownership verification (Trinity BRICKS I MEMORY)
        """
        user_namespace = self._get_user_namespace(user_id)
        
        if not self.initialized:
            logger.info("Mock delete memory", memory_id=memory_id, user_id=user_id)
            return True
        
        try:
            self.client.delete(memory_id, user_id=user_namespace)
            
            # Invalidate cache
            cache_key = await self._get_cache_key(user_id, "all_memories")
            if self.redis_client:
                await self.redis_client.delete(cache_key)
            
            logger.info("Memory deleted", memory_id=memory_id, user_id=user_id)
            return True
        except Exception as e:
            logger.error("Failed to delete memory", error=str(e), memory_id=memory_id)
            return False
