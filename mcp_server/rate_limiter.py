"""
Rate Limiter Module
Implements tier-based rate limiting using Redis.
"""
import redis
from datetime import datetime, timedelta
from typing import Tuple
from .config import REDIS_URL, RATE_LIMITS


class RateLimiter:
    """
    Implements rate limiting per subscription tier.
    Uses Redis for distributed rate limiting.
    """
    
    def __init__(self):
        """Initialize Redis connection."""
        self.redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    
    def check_rate_limit(self, user_id: str, tier: str) -> Tuple[bool, dict]:
        """
        Check if user has exceeded rate limit.
        
        Returns:
            (allowed: bool, info: dict)
            info contains: remaining_minute, remaining_day, reset_minute, reset_day
        """
        limits = RATE_LIMITS.get(tier, RATE_LIMITS['free'])
        
        # Check per-minute limit
        minute_allowed = True
        remaining_minute = None
        reset_minute = None
        
        if limits['per_minute'] is not None:
            minute_key = f"ratelimit:minute:{user_id}:{datetime.now().strftime('%Y%m%d%H%M')}"
            minute_count = self.redis_client.get(minute_key)
            
            if minute_count is None:
                minute_count = 0
                self.redis_client.setex(minute_key, 60, 0)
            else:
                minute_count = int(minute_count)
            
            remaining_minute = limits['per_minute'] - minute_count
            minute_allowed = minute_count < limits['per_minute']
            reset_minute = 60 - datetime.now().second
        
        # Check per-day limit
        day_allowed = True
        remaining_day = None
        reset_day = None
        
        if limits['per_day'] is not None:
            day_key = f"ratelimit:day:{user_id}:{datetime.now().strftime('%Y%m%d')}"
            day_count = self.redis_client.get(day_key)
            
            if day_count is None:
                day_count = 0
                # Set expiry to end of day
                seconds_until_midnight = (
                    datetime.combine(datetime.now().date() + timedelta(days=1), datetime.min.time()) 
                    - datetime.now()
                ).seconds
                self.redis_client.setex(day_key, seconds_until_midnight, 0)
            else:
                day_count = int(day_count)
            
            remaining_day = limits['per_day'] - day_count
            day_allowed = day_count < limits['per_day']
            
            # Calculate seconds until midnight
            reset_day = (
                datetime.combine(datetime.now().date() + timedelta(days=1), datetime.min.time()) 
                - datetime.now()
            ).seconds
        
        allowed = minute_allowed and day_allowed
        
        info = {
            'remaining_minute': remaining_minute,
            'remaining_day': remaining_day,
            'reset_minute': reset_minute,
            'reset_day': reset_day,
            'tier': tier
        }
        
        return allowed, info
    
    def increment_usage(self, user_id: str):
        """
        Increment usage counters for user.
        Call this after successful request.
        """
        # Increment minute counter
        minute_key = f"ratelimit:minute:{user_id}:{datetime.now().strftime('%Y%m%d%H%M')}"
        self.redis_client.incr(minute_key)
        self.redis_client.expire(minute_key, 60)
        
        # Increment day counter
        day_key = f"ratelimit:day:{user_id}:{datetime.now().strftime('%Y%m%d')}"
        self.redis_client.incr(day_key)
        
        # Set expiry to end of day if not set
        if self.redis_client.ttl(day_key) == -1:
            seconds_until_midnight = (
                datetime.combine(datetime.now().date() + timedelta(days=1), datetime.min.time()) 
                - datetime.now()
            ).seconds
            self.redis_client.expire(day_key, seconds_until_midnight)
    
    def get_usage(self, user_id: str) -> dict:
        """
        Get current usage for user.
        """
        minute_key = f"ratelimit:minute:{user_id}:{datetime.now().strftime('%Y%m%d%H%M')}"
        day_key = f"ratelimit:day:{user_id}:{datetime.now().strftime('%Y%m%d')}"
        
        minute_count = self.redis_client.get(minute_key)
        day_count = self.redis_client.get(day_key)
        
        return {
            'minute_count': int(minute_count) if minute_count else 0,
            'day_count': int(day_count) if day_count else 0
        }
    
    def reset_user_limits(self, user_id: str):
        """
        Reset all rate limits for a user.
        Use for admin override or testing.
        """
        # Clear all rate limit keys for user
        pattern = f"ratelimit:*:{user_id}:*"
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)


# Global rate limiter instance
rate_limiter = RateLimiter()
