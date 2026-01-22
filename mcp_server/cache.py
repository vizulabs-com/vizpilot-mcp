"""
Redis Cache Module
Handles caching for MCP server to improve performance.
"""
import json
import redis
from typing import Any, Optional
from .config import REDIS_URL, CACHE_TTL


class CacheManager:
    """
    Manages Redis caching for MCP server.
    """
    
    def __init__(self):
        """Initialize Redis connection."""
        self.redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        Returns None if key doesn't exist.
        """
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            # Log error but don't fail
            print(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = None):
        """
        Set value in cache with optional TTL.
        """
        try:
            serialized = json.dumps(value)
            if ttl:
                self.redis_client.setex(key, ttl, serialized)
            else:
                self.redis_client.set(key, serialized)
        except Exception as e:
            # Log error but don't fail
            print(f"Cache set error: {e}")
    
    def delete(self, key: str):
        """Delete key from cache."""
        try:
            self.redis_client.delete(key)
        except Exception as e:
            print(f"Cache delete error: {e}")
    
    def clear_pattern(self, pattern: str):
        """Delete all keys matching pattern."""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
        except Exception as e:
            print(f"Cache clear pattern error: {e}")
    
    # Convenience methods for specific cache types
    
    def get_protocol(self, protocol_id: str) -> Optional[dict]:
        """Get cached protocol."""
        return self.get(f"protocol:{protocol_id}")
    
    def set_protocol(self, protocol_id: str, protocol_data: dict):
        """Cache protocol."""
        self.set(f"protocol:{protocol_id}", protocol_data, CACHE_TTL['protocol'])
    
    def get_steering_rules(self, technology_slug: str) -> Optional[list]:
        """Get cached steering rules."""
        return self.get(f"steering:{technology_slug}")
    
    def set_steering_rules(self, technology_slug: str, rules: list):
        """Cache steering rules."""
        self.set(f"steering:{technology_slug}", rules, CACHE_TTL['steering_rules'])
    
    def get_user_info(self, user_id: str) -> Optional[dict]:
        """Get cached user info."""
        return self.get(f"user:{user_id}")
    
    def set_user_info(self, user_id: str, user_data: dict):
        """Cache user info."""
        self.set(f"user:{user_id}", user_data, CACHE_TTL['user_info'])
    
    def get_technologies(self) -> Optional[list]:
        """Get cached technology list."""
        return self.get("technologies:all")
    
    def set_technologies(self, technologies: list):
        """Cache technology list."""
        self.set("technologies:all", technologies, CACHE_TTL['technology_list'])
    
    def invalidate_protocol(self, protocol_id: str):
        """Invalidate protocol cache."""
        self.delete(f"protocol:{protocol_id}")
    
    def invalidate_technology(self, technology_slug: str):
        """Invalidate all caches for a technology."""
        self.delete(f"steering:{technology_slug}")
        self.clear_pattern(f"protocol:*:{technology_slug}:*")


# Global cache instance
cache = CacheManager()
