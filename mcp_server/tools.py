"""
MCP Tools Implementation
Implements all MCP tools for protocol delivery.
"""
from typing import Any
from .database import DatabaseManager
from .cache import cache
from .auth import auth_manager, AuthenticationError, AuthorizationError, RateLimitError
from .watermark import watermark_manager
from .rate_limiter import rate_limiter


class MCPTools:
    """
    Implements all MCP tools for VIZPILOT.
    """
    
    @staticmethod
    def list_technologies(api_key: str) -> dict[str, Any]:
        """
        List all available technologies.
        
        Args:
            api_key: User's API key
        
        Returns:
            {
                "technologies": [
                    {
                        "slug": "django",
                        "name": "Django",
                        "description": "...",
                        "tier_required": "free",
                        "protocol_count": 25,
                        "has_access": true
                    }
                ]
            }
        """
        try:
            # Authenticate user
            user, api_key_obj = auth_manager.authenticate(api_key)
            
            # Get user subscription
            subscription = DatabaseManager.get_user_subscription(user)
            tier = subscription.plan.tier if subscription else 'free'
            
            # Check rate limit
            auth_manager.check_rate_limit(user, tier)
            
            # Check cache first
            cached = cache.get_technologies()
            if cached:
                technologies = cached
            else:
                # Get technologies from database
                tech_objects = DatabaseManager.get_technologies()
                technologies = [
                    {
                        'slug': tech.slug,
                        'name': tech.name,
                        'description': tech.description,
                        'tier_required': tech.tier_required,
                        'protocol_count': tech.protocol_count,
                        'icon_url': tech.icon_url,
                        'color': tech.color
                    }
                    for tech in tech_objects
                ]
                
                # Cache the result
                cache.set_technologies(technologies)
            
            # Add access info for each technology
            for tech in technologies:
                tech_obj = DatabaseManager.get_technology_by_slug(tech['slug'])
                tech['has_access'] = DatabaseManager.check_user_has_access(user, tech_obj)
            
            # Increment usage
            rate_limiter.increment_usage(str(user.id))
            
            return {
                'success': True,
                'technologies': technologies,
                'user_tier': tier
            }
            
        except (AuthenticationError, AuthorizationError, RateLimitError) as e:
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Internal error: {str(e)}'
            }
    
    @staticmethod
    def list_protocols(api_key: str, technology_slug: str) -> dict[str, Any]:
        """
        List protocols for a technology.
        
        Args:
            api_key: User's API key
            technology_slug: Technology slug (e.g., "django")
        
        Returns:
            {
                "protocols": [
                    {
                        "id": "uuid",
                        "slug": "authentication",
                        "title": "Authentication Protocol",
                        "description": "...",
                        "tier_required": "starter",
                        "difficulty": "intermediate",
                        "estimated_read_time": 10
                    }
                ]
            }
        """
        try:
            # Authenticate user
            user, api_key_obj = auth_manager.authenticate(api_key)
            
            # Get user subscription
            subscription = DatabaseManager.get_user_subscription(user)
            tier = subscription.plan.tier if subscription else 'free'
            
            # Check rate limit
            auth_manager.check_rate_limit(user, tier)
            
            # Get technology
            technology = DatabaseManager.get_technology_by_slug(technology_slug)
            if not technology:
                return {
                    'success': False,
                    'error': f'Technology "{technology_slug}" not found'
                }
            
            # Check technology access
            auth_manager.authorize_technology_access(user, technology)
            
            # Get protocols
            protocols = DatabaseManager.get_protocols(technology_slug, tier)
            
            protocol_list = [
                {
                    'id': str(protocol.id),
                    'slug': protocol.slug,
                    'title': protocol.title,
                    'description': protocol.description,
                    'tier_required': protocol.tier_required,
                    'difficulty': protocol.difficulty,
                    'estimated_read_time': protocol.estimated_read_time,
                    'tags': protocol.tags,
                    'is_featured': protocol.is_featured,
                    'view_count': protocol.view_count
                }
                for protocol in protocols
            ]
            
            # Increment usage
            rate_limiter.increment_usage(str(user.id))
            
            return {
                'success': True,
                'technology': {
                    'slug': technology.slug,
                    'name': technology.name
                },
                'protocols': protocol_list,
                'count': len(protocol_list)
            }
            
        except (AuthenticationError, AuthorizationError, RateLimitError) as e:
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Internal error: {str(e)}'
            }
    
    @staticmethod
    def get_protocol(api_key: str, protocol_id: str = None, 
                    technology_slug: str = None, protocol_slug: str = None) -> dict[str, Any]:
        """
        Get full protocol content.
        
        Args:
            api_key: User's API key
            protocol_id: Protocol UUID (optional if using slugs)
            technology_slug: Technology slug (required if using protocol_slug)
            protocol_slug: Protocol slug (optional if using protocol_id)
        
        Returns:
            {
                "protocol": {
                    "id": "uuid",
                    "title": "...",
                    "content": "Full markdown content with watermark",
                    "metadata": {...}
                }
            }
        """
        try:
            # Authenticate user
            user, api_key_obj = auth_manager.authenticate(api_key)
            
            # Get user subscription
            subscription = DatabaseManager.get_user_subscription(user)
            tier = subscription.plan.tier if subscription else 'free'
            
            # Check rate limit
            auth_manager.check_rate_limit(user, tier)
            
            # Get protocol
            if protocol_id:
                protocol = DatabaseManager.get_protocol_by_id(protocol_id)
            elif technology_slug and protocol_slug:
                protocol = DatabaseManager.get_protocol_by_slug(technology_slug, protocol_slug)
            else:
                return {
                    'success': False,
                    'error': 'Either protocol_id or (technology_slug + protocol_slug) required'
                }
            
            if not protocol:
                return {
                    'success': False,
                    'error': 'Protocol not found'
                }
            
            # Check protocol access
            auth_manager.authorize_protocol_access(user, protocol)
            
            # Check cache first
            cached = cache.get_protocol(str(protocol.id))
            if cached:
                content = cached['content']
            else:
                content = protocol.content_markdown
            
            # Add watermark
            watermarked_content, watermark_id = watermark_manager.add_watermark_to_protocol(
                content,
                user.email,
                api_key_obj.key_prefix,
                str(protocol.id)
            )
            
            # Track protocol view
            DatabaseManager.track_protocol_view(user, protocol, api_key_obj)
            
            # Track access log
            DatabaseManager.track_access_log(
                user=user,
                api_key=api_key_obj,
                content_type='protocol',
                content_id=str(protocol.id),
                technology_id=str(protocol.technology.id),
                watermark_id=watermark_id,
                ip_address='0.0.0.0',  # Will be set by server
                user_agent=''
            )
            
            # Increment usage
            rate_limiter.increment_usage(str(user.id))
            
            result = {
                'success': True,
                'protocol': {
                    'id': str(protocol.id),
                    'slug': protocol.slug,
                    'title': protocol.title,
                    'description': protocol.description,
                    'technology': {
                        'slug': protocol.technology.slug,
                        'name': protocol.technology.name
                    },
                    'content': watermarked_content,
                    'tier_required': protocol.tier_required,
                    'difficulty': protocol.difficulty,
                    'estimated_read_time': protocol.estimated_read_time,
                    'tags': protocol.tags,
                    'version': protocol.version,
                    'updated_at': protocol.updated_at.isoformat()
                }
            }
            
            # Cache the protocol (without watermark)
            cache.set_protocol(str(protocol.id), {
                'content': content,
                'metadata': result['protocol']
            })
            
            return result
            
        except (AuthenticationError, AuthorizationError, RateLimitError) as e:
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Internal error: {str(e)}'
            }
    
    @staticmethod
    def get_steering_rules(api_key: str, technology_slug: str) -> dict[str, Any]:
        """
        Get steering rules for a technology.
        
        Args:
            api_key: User's API key
            technology_slug: Technology slug
        
        Returns:
            {
                "steering_rules": [
                    {
                        "content": "Always use class-based views",
                        "category": "architecture",
                        "priority": 100
                    }
                ]
            }
        """
        try:
            # Authenticate user
            user, api_key_obj = auth_manager.authenticate(api_key)
            
            # Get user subscription
            subscription = DatabaseManager.get_user_subscription(user)
            tier = subscription.plan.tier if subscription else 'free'
            
            # Check rate limit
            auth_manager.check_rate_limit(user, tier)
            
            # Get technology
            technology = DatabaseManager.get_technology_by_slug(technology_slug)
            if not technology:
                return {
                    'success': False,
                    'error': f'Technology "{technology_slug}" not found'
                }
            
            # Check technology access
            auth_manager.authorize_technology_access(user, technology)
            
            # Check cache first
            cached = cache.get_steering_rules(technology_slug)
            if cached:
                rules = cached
            else:
                # Get steering rules from database
                rule_objects = DatabaseManager.get_steering_rules(technology_slug, tier)
                rules = [
                    {
                        'content': rule.content,
                        'category': rule.category,
                        'priority': rule.priority
                    }
                    for rule in rule_objects
                ]
                
                # Cache the result
                cache.set_steering_rules(technology_slug, rules)
            
            # Add watermark
            watermarked_rules, watermark_id = watermark_manager.add_watermark_to_steering_rules(
                rules,
                user.email,
                api_key_obj.key_prefix
            )
            
            # Increment usage
            rate_limiter.increment_usage(str(user.id))
            
            return {
                'success': True,
                'technology': {
                    'slug': technology.slug,
                    'name': technology.name
                },
                'steering_rules': watermarked_rules,
                'count': len(rules)
            }
            
        except (AuthenticationError, AuthorizationError, RateLimitError) as e:
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Internal error: {str(e)}'
            }
    
    @staticmethod
    def search_protocols(api_key: str, query: str, technology_slug: str = None) -> dict[str, Any]:
        """
        Search protocols across all technologies or within a specific technology.
        
        Args:
            api_key: User's API key
            query: Search query
            technology_slug: Optional technology filter
        
        Returns:
            {
                "results": [
                    {
                        "id": "uuid",
                        "title": "...",
                        "description": "...",
                        "technology": {...},
                        "relevance_score": 0.95
                    }
                ]
            }
        """
        try:
            # Authenticate user
            user, api_key_obj = auth_manager.authenticate(api_key)
            
            # Get user subscription
            subscription = DatabaseManager.get_user_subscription(user)
            tier = subscription.plan.tier if subscription else 'free'
            
            # Check rate limit
            auth_manager.check_rate_limit(user, tier)
            
            # Search protocols
            protocols = DatabaseManager.search_protocols(query, technology_slug, tier)
            
            results = [
                {
                    'id': str(protocol.id),
                    'slug': protocol.slug,
                    'title': protocol.title,
                    'description': protocol.description,
                    'technology': {
                        'slug': protocol.technology.slug,
                        'name': protocol.technology.name
                    },
                    'tier_required': protocol.tier_required,
                    'difficulty': protocol.difficulty,
                    'tags': protocol.tags
                }
                for protocol in protocols
            ]
            
            # Increment usage
            rate_limiter.increment_usage(str(user.id))
            
            return {
                'success': True,
                'query': query,
                'technology_filter': technology_slug,
                'results': results,
                'count': len(results)
            }
            
        except (AuthenticationError, AuthorizationError, RateLimitError) as e:
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Internal error: {str(e)}'
            }
    
    @staticmethod
    def get_user_info(api_key: str) -> dict[str, Any]:
        """
        Get user subscription and usage information.
        
        Args:
            api_key: User's API key
        
        Returns:
            {
                "user": {
                    "email": "...",
                    "tier": "pro",
                    "subscription_status": "active",
                    "usage": {...}
                }
            }
        """
        try:
            # Authenticate user
            user, api_key_obj = auth_manager.authenticate(api_key)
            
            # Get user context
            user_context = auth_manager.get_user_context(user)
            
            # Get usage info
            usage = DatabaseManager.get_user_daily_usage(user)
            
            # Get rate limit info
            subscription = DatabaseManager.get_user_subscription(user)
            tier = subscription.plan.tier if subscription else 'free'
            _, rate_info = rate_limiter.check_rate_limit(str(user.id), tier)
            
            return {
                'success': True,
                'user': {
                    **user_context,
                    'usage_today': usage,
                    'rate_limits': rate_info
                }
            }
            
        except (AuthenticationError, AuthorizationError, RateLimitError) as e:
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Internal error: {str(e)}'
            }


# Global tools instance
mcp_tools = MCPTools()
