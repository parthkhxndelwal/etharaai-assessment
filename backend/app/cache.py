"""Redis cache manager"""

import redis.asyncio as redis
from typing import Optional, Any
import json
from datetime import datetime, date
from .config import settings


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime objects"""
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


class CacheManager:
    """Singleton Redis client manager"""
    
    client: Optional[redis.Redis] = None
    
    @classmethod
    async def connect(cls):
        """Initialize Redis connection"""
        cls.client = await redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True
        )
        # Test connection
        await cls.client.ping()
        print("✅ Connected to Redis")
    
    @classmethod
    async def close(cls):
        """Close Redis connection"""
        if cls.client:
            await cls.client.close()
            print("✅ Closed Redis connection")
    
    @classmethod
    async def get(cls, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not cls.client:
            return None
        
        value = await cls.client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    @classmethod
    async def set(cls, key: str, value: Any, ttl: int = 300):
        """
        Set value in cache with TTL
        
        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            ttl: Time to live in seconds (default: 300s)
        """
        if not cls.client:
            return
        
        if isinstance(value, (dict, list)):
            value = json.dumps(value, cls=DateTimeEncoder)
        
        await cls.client.setex(key, ttl, value)
    
    @classmethod
    async def delete(cls, key: str):
        """Delete key from cache"""
        if not cls.client:
            return
        
        await cls.client.delete(key)
    
    @classmethod
    async def delete_pattern(cls, pattern: str):
        """
        Delete all keys matching a pattern
        
        Args:
            pattern: Redis key pattern (e.g., "employees:*")
        """
        if not cls.client:
            return
        
        cursor = 0
        while True:
            cursor, keys = await cls.client.scan(cursor, match=pattern, count=100)
            if keys:
                await cls.client.delete(*keys)
            if cursor == 0:
                break
    
    @classmethod
    async def clear_all(cls):
        """Clear all cache (use with caution)"""
        if not cls.client:
            return
        
        await cls.client.flushdb()


# Convenience functions
async def cache_get(key: str) -> Optional[Any]:
    """Get value from cache"""
    return await CacheManager.get(key)


async def cache_set(key: str, value: Any, ttl: int = 300):
    """Set value in cache"""
    await CacheManager.set(key, value, ttl)


async def cache_delete(key: str):
    """Delete key from cache"""
    await CacheManager.delete(key)


async def cache_delete_pattern(pattern: str):
    """Delete all keys matching pattern"""
    await CacheManager.delete_pattern(pattern)
