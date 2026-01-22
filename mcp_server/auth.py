"""
Authentication Module
Handles API key validation and user authorization.
"""
import hashlib
from typing import Optional, Tuple
from .database import DatabaseManager
from .rate_limiter import rate_limiter


class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass


class AuthorizationError(Exception):
    """Raised when user doesn't have access to resource."""
    pass


class RateLimitError(Exception):
    """Raised when rate limit is exceeded."""
    pass


class AuthManager:
    """
    Manages authentication and authorization for MCP server.
    """
    
    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """Hash API key using SHA-256."""
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    @staticmethod
    def authenticate(api_key: str) -> Tuple[object, object]:
        """
        Authenticate user by API key.
        
        Returns:
            (user, api_key_obj)
        
        Raises:
            AuthenticationError: If authentication fails
        """
        if not api_key:
            raise AuthenticationError("API key is required")
        
        # Hash the API key
        key_hash = AuthManager.hash_api_key(api_key)
        
        # Get user and API key from database
        result = DatabaseManager.get_user_by_api_key(key_hash)
        
        if not result:
            raise AuthenticationError("Invalid or expired API key")
        
        user, api_key_obj = result
        
        # Check if user is active
        if not user.is_active:
            raise AuthenticationError("User account is inactive")
        
        return user, api_key_obj
    
    @staticmethod
    def check_rate_limit(user, tier: str):
        """
        Check rate limit for user.
        
        Raises:
            RateLimitError: If rate limit exceeded
        """
        allowed, info = rate_limiter.check_rate_limit(str(user.id), tier)
        
        if not allowed:
            error_msg = "Rate limit exceeded. "
            if info['remaining_minute'] is not None and info['remaining_minute'] <= 0:
                error_msg += f"Per-minute limit reached. Reset in {info['reset_minute']} seconds. "
            if info['remaining_day'] is not None and info['remaining_day'] <= 0:
                error_msg += f"Daily limit reached. Reset in {info['reset_day']} seconds."
            
            raise RateLimitError(error_msg)
        
        return info
    
    @staticmethod
    def authorize_technology_access(user, technology) -> bool:
        """
        Check if user has access to a technology.
        
        Returns:
            bool: True if user has access
        
        Raises:
            AuthorizationError: If user doesn't have access
        """
        has_access = DatabaseManager.check_user_has_access(user, technology)
        
        if not has_access:
            subscription = DatabaseManager.get_user_subscription(user)
            if subscription:
                tier = subscription.plan.tier
                raise AuthorizationError(
                    f"Your {tier} plan doesn't include access to {technology.name}. "
                    f"Upgrade to {technology.tier_required} or higher."
                )
            else:
                raise AuthorizationError(
                    f"No active subscription. Please subscribe to access {technology.name}."
                )
        
        return True
    
    @staticmethod
    def authorize_protocol_access(user, protocol) -> bool:
        """
        Check if user has access to a protocol.
        
        Returns:
            bool: True if user has access
        
        Raises:
            AuthorizationError: If user doesn't have access
        """
        # First check technology access
        AuthManager.authorize_technology_access(user, protocol.technology)
        
        # Then check protocol tier
        subscription = DatabaseManager.get_user_subscription(user)
        if not subscription:
            raise AuthorizationError("No active subscription")
        
        tier_hierarchy = {'free': 0, 'starter': 1, 'pro': 2, 'enterprise': 3}
        user_tier_level = tier_hierarchy.get(subscription.plan.tier, 0)
        protocol_tier_level = tier_hierarchy.get(protocol.tier_required, 0)
        
        if user_tier_level < protocol_tier_level:
            raise AuthorizationError(
                f"This protocol requires {protocol.tier_required} tier or higher. "
                f"Your current tier: {subscription.plan.tier}"
            )
        
        return True
    
    @staticmethod
    def get_user_context(user) -> dict:
        """
        Get user context including subscription and limits.
        """
        subscription = DatabaseManager.get_user_subscription(user)
        
        if not subscription:
            return {
                'user_id': str(user.id),
                'email': user.email,
                'tier': 'none',
                'subscription_status': 'none',
                'has_subscription': False
            }
        
        return {
            'user_id': str(user.id),
            'email': user.email,
            'tier': subscription.plan.tier,
            'subscription_status': subscription.status,
            'plan_name': subscription.plan.name,
            'billing_cycle': subscription.billing_cycle,
            'current_period_end': subscription.current_period_end.isoformat(),
            'has_subscription': True,
            'limits': subscription.plan.limits
        }


# Global auth manager instance
auth_manager = AuthManager()
