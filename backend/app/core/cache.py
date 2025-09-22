"""
Redis cache configuration and management
"""

import redis.asyncio as redis
import structlog
from typing import Optional

from app.core.config import settings

logger = structlog.get_logger(__name__)

# Global Redis client
redis_client: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    """Get Redis client instance"""
    global redis_client
    
    if redis_client is None:
        try:
            redis_client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            
            # Test connection
            await redis_client.ping()
            logger.info("Redis connection established")
            
        except Exception as e:
            logger.error("Failed to connect to Redis", error=str(e))
            raise
    
    return redis_client


async def close_redis():
    """Close Redis connection"""
    global redis_client
    
    if redis_client:
        try:
            await redis_client.close()
            redis_client = None
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error("Error closing Redis connection", error=str(e))


class CacheManager:
    """Cache management utilities"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    async def set(self, key: str, value: str, expire: Optional[int] = None):
        """Set cache value"""
        try:
            await self.redis.set(key, value, ex=expire)
        except Exception as e:
            logger.error("Failed to set cache", key=key, error=str(e))
            raise
    
    async def get(self, key: str) -> Optional[str]:
        """Get cache value"""
        try:
            return await self.redis.get(key)
        except Exception as e:
            logger.error("Failed to get cache", key=key, error=str(e))
            return None
    
    async def delete(self, key: str):
        """Delete cache value"""
        try:
            await self.redis.delete(key)
        except Exception as e:
            logger.error("Failed to delete cache", key=key, error=str(e))
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        try:
            return await self.redis.exists(key)
        except Exception as e:
            logger.error("Failed to check cache existence", key=key, error=str(e))
            return False
    
    async def set_json(self, key: str, data: dict, expire: Optional[int] = None):
        """Set JSON data in cache"""
        import json
        try:
            json_data = json.dumps(data)
            await self.set(key, json_data, expire)
        except Exception as e:
            logger.error("Failed to set JSON cache", key=key, error=str(e))
            raise
    
    async def get_json(self, key: str) -> Optional[dict]:
        """Get JSON data from cache"""
        import json
        try:
            data = await self.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error("Failed to get JSON cache", key=key, error=str(e))
            return None
