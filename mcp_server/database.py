"""
Database Connection Module
Handles Django ORM connection for MCP server.
"""
import os
import sys
import django
from pathlib import Path

# Add parent directory to path for Django imports
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vizpilot_config.settings')
django.setup()

# Import Django models
from protocols.models import Technology, Protocol, SteeringRule, ProtocolView
from api.models import APIKey, AccessLog, DailyUsage
from subscriptions.models import Subscription, Plan
from accounts.models import User
from django.db.models import Q, Count
from django.utils import timezone


class DatabaseManager:
    """
    Manages database queries for MCP server.
    """
    
    @staticmethod
    def get_user_by_api_key(key_hash: str) -> tuple[User, APIKey] | None:
        """
        Get user and API key by key hash.
        Returns (user, api_key) or None if not found/invalid.
        """
        try:
            api_key = APIKey.objects.select_related('user').get(
                key_hash=key_hash,
                is_active=True,
                revoked_at__isnull=True
            )
            
            # Check if key is expired
            if api_key.expires_at and api_key.expires_at < timezone.now():
                return None
            
            return api_key.user, api_key
        except APIKey.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_subscription(user: User) -> Subscription | None:
        """Get active subscription for user."""
        try:
            return Subscription.objects.select_related('plan').get(
                user=user,
                status__in=['active', 'trialing']
            )
        except Subscription.DoesNotExist:
            return None
    
    @staticmethod
    def get_technologies(tier: str = None) -> list[Technology]:
        """
        Get all active technologies.
        Filter by tier if provided.
        """
        query = Technology.objects.filter(is_active=True)
        
        if tier:
            # Get technologies accessible by this tier
            tier_hierarchy = {'free': 0, 'starter': 1, 'pro': 2, 'enterprise': 3}
            user_tier_level = tier_hierarchy.get(tier, 0)
            
            accessible_tiers = [t for t, level in tier_hierarchy.items() if level <= user_tier_level]
            query = query.filter(tier_required__in=accessible_tiers)
        
        return list(query.order_by('display_order', 'name'))
    
    @staticmethod
    def get_technology_by_slug(slug: str) -> Technology | None:
        """Get technology by slug."""
        try:
            return Technology.objects.get(slug=slug, is_active=True)
        except Technology.DoesNotExist:
            return None
    
    @staticmethod
    def get_protocols(technology_slug: str, tier: str = None) -> list[Protocol]:
        """
        Get protocols for a technology.
        Filter by tier if provided.
        """
        query = Protocol.objects.filter(
            technology__slug=technology_slug,
            is_active=True,
            published_at__isnull=False
        ).select_related('technology')
        
        if tier:
            # Get protocols accessible by this tier
            tier_hierarchy = {'free': 0, 'starter': 1, 'pro': 2, 'enterprise': 3}
            user_tier_level = tier_hierarchy.get(tier, 0)
            
            accessible_tiers = [t for t, level in tier_hierarchy.items() if level <= user_tier_level]
            query = query.filter(tier_required__in=accessible_tiers)
        
        return list(query.order_by('-is_featured', '-published_at'))
    
    @staticmethod
    def get_protocol_by_id(protocol_id: str) -> Protocol | None:
        """Get protocol by ID."""
        try:
            return Protocol.objects.select_related('technology').get(
                id=protocol_id,
                is_active=True,
                published_at__isnull=False
            )
        except Protocol.DoesNotExist:
            return None
    
    @staticmethod
    def get_protocol_by_slug(technology_slug: str, protocol_slug: str) -> Protocol | None:
        """Get protocol by technology and protocol slug."""
        try:
            return Protocol.objects.select_related('technology').get(
                technology__slug=technology_slug,
                slug=protocol_slug,
                is_active=True,
                published_at__isnull=False
            )
        except Protocol.DoesNotExist:
            return None
    
    @staticmethod
    def get_steering_rules(technology_slug: str, tier: str = None) -> list[SteeringRule]:
        """
        Get steering rules for a technology.
        Filter by tier if provided.
        """
        query = SteeringRule.objects.filter(
            technology__slug=technology_slug,
            is_active=True
        ).select_related('technology')
        
        if tier:
            # Get steering rules accessible by this tier
            tier_hierarchy = {'free': 0, 'starter': 1, 'pro': 2, 'enterprise': 3}
            user_tier_level = tier_hierarchy.get(tier, 0)
            
            accessible_tiers = [t for t, level in tier_hierarchy.items() if level <= user_tier_level]
            query = query.filter(tier_required__in=accessible_tiers)
        
        return list(query.order_by('priority', 'display_order'))
    
    @staticmethod
    def search_protocols(query: str, technology_slug: str = None, tier: str = None) -> list[Protocol]:
        """
        Search protocols by query string.
        Uses PostgreSQL full-text search.
        """
        from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
        
        # Build search query
        search_query = SearchQuery(query)
        search_vector = SearchVector('title', weight='A') + SearchVector('description', weight='B') + SearchVector('content_markdown', weight='C')
        
        protocols = Protocol.objects.annotate(
            rank=SearchRank(search_vector, search_query)
        ).filter(
            rank__gte=0.1,
            is_active=True,
            published_at__isnull=False
        ).select_related('technology')
        
        # Filter by technology if provided
        if technology_slug:
            protocols = protocols.filter(technology__slug=technology_slug)
        
        # Filter by tier if provided
        if tier:
            tier_hierarchy = {'free': 0, 'starter': 1, 'pro': 2, 'enterprise': 3}
            user_tier_level = tier_hierarchy.get(tier, 0)
            accessible_tiers = [t for t, level in tier_hierarchy.items() if level <= user_tier_level]
            protocols = protocols.filter(tier_required__in=accessible_tiers)
        
        return list(protocols.order_by('-rank', '-is_featured')[:50])
    
    @staticmethod
    def track_protocol_view(user: User, protocol: Protocol, api_key: APIKey = None):
        """Track protocol view for analytics."""
        # Create protocol view record
        ProtocolView.objects.create(
            user=user,
            protocol=protocol
        )
        
        # Update protocol view count
        protocol.view_count += 1
        protocol.save(update_fields=['view_count'])
        
        # Update daily usage
        today = timezone.now().date()
        daily_usage, created = DailyUsage.objects.get_or_create(
            user=user,
            date=today,
            defaults={
                'protocol_views': 0,
                'api_requests': 0,
                'usage_by_technology': {},
                'usage_by_ide': {}
            }
        )
        
        daily_usage.protocol_views += 1
        daily_usage.api_requests += 1
        
        # Update technology usage
        tech_slug = protocol.technology.slug
        if tech_slug not in daily_usage.usage_by_technology:
            daily_usage.usage_by_technology[tech_slug] = 0
        daily_usage.usage_by_technology[tech_slug] += 1
        
        # Update IDE usage if API key provided
        if api_key:
            ide_type = api_key.ide_type
            if ide_type not in daily_usage.usage_by_ide:
                daily_usage.usage_by_ide[ide_type] = 0
            daily_usage.usage_by_ide[ide_type] += 1
        
        daily_usage.save()
    
    @staticmethod
    def track_access_log(user: User, api_key: APIKey, content_type: str, content_id: str, 
                        technology_id: str, watermark_id: str, ip_address: str, 
                        user_agent: str = '', response_time_ms: int = None):
        """Track access log for audit and watermark tracking."""
        AccessLog.objects.create(
            user=user,
            api_key=api_key,
            content_type=content_type,
            content_id=content_id,
            technology_id=technology_id,
            watermark_id=watermark_id,
            ip_address=ip_address,
            user_agent=user_agent,
            ide_type=api_key.ide_type if api_key else '',
            response_time_ms=response_time_ms
        )
    
    @staticmethod
    def get_user_daily_usage(user: User) -> dict:
        """Get user's usage for today."""
        today = timezone.now().date()
        try:
            usage = DailyUsage.objects.get(user=user, date=today)
            return {
                'api_requests': usage.api_requests,
                'protocol_views': usage.protocol_views,
                'steering_rule_views': usage.steering_rule_views,
                'unique_protocols': usage.unique_protocols,
                'usage_by_technology': usage.usage_by_technology,
                'usage_by_ide': usage.usage_by_ide
            }
        except DailyUsage.DoesNotExist:
            return {
                'api_requests': 0,
                'protocol_views': 0,
                'steering_rule_views': 0,
                'unique_protocols': 0,
                'usage_by_technology': {},
                'usage_by_ide': {}
            }
    
    @staticmethod
    def check_user_has_access(user: User, technology: Technology) -> bool:
        """Check if user has access to a technology based on subscription."""
        subscription = DatabaseManager.get_user_subscription(user)
        if not subscription:
            return False
        
        # Check tier access
        tier_hierarchy = {'free': 0, 'starter': 1, 'pro': 2, 'enterprise': 3}
        user_tier_level = tier_hierarchy.get(subscription.plan.tier, 0)
        tech_tier_level = tier_hierarchy.get(technology.tier_required, 0)
        
        return user_tier_level >= tech_tier_level
