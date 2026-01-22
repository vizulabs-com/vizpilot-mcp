"""
Watermark Module
Adds watermarks to protocol content for tracking and anti-piracy.
"""
import uuid
from datetime import datetime
from .config import WATERMARK_ENABLED, WATERMARK_FORMAT


class WatermarkManager:
    """
    Manages content watermarking for protocols and steering rules.
    """
    
    @staticmethod
    def generate_watermark_id() -> str:
        """Generate unique watermark ID."""
        return str(uuid.uuid4())
    
    @staticmethod
    def add_watermark(content: str, user_email: str, key_prefix: str, 
                     watermark_id: str = None) -> tuple[str, str]:
        """
        Add watermark to content.
        
        Args:
            content: The content to watermark
            user_email: User's email
            key_prefix: API key prefix
            watermark_id: Optional watermark ID (generated if not provided)
        
        Returns:
            (watermarked_content, watermark_id)
        """
        if not WATERMARK_ENABLED:
            return content, ""
        
        if not watermark_id:
            watermark_id = WatermarkManager.generate_watermark_id()
        
        # Create watermark text
        watermark = WATERMARK_FORMAT.format(
            email=user_email,
            key_prefix=key_prefix,
            watermark_id=watermark_id
        )
        
        # Add watermark at the end of content
        watermarked_content = f"{content}\n\n{watermark}"
        
        return watermarked_content, watermark_id
    
    @staticmethod
    def add_watermark_to_protocol(protocol_content: str, user_email: str, 
                                  key_prefix: str, protocol_id: str) -> tuple[str, str]:
        """
        Add watermark to protocol content with protocol-specific info.
        
        Returns:
            (watermarked_content, watermark_id)
        """
        watermark_id = WatermarkManager.generate_watermark_id()
        
        if not WATERMARK_ENABLED:
            return protocol_content, watermark_id
        
        # Create detailed watermark for protocols
        watermark = f"""

---

<!-- VIZPILOT PROTOCOL WATERMARK -->
<!-- Licensed to: {user_email} -->
<!-- API Key: {key_prefix}... -->
<!-- Protocol ID: {protocol_id} -->
<!-- Watermark ID: {watermark_id} -->
<!-- Accessed: {datetime.utcnow().isoformat()}Z -->
<!-- 
  This content is licensed for personal use only.
  Redistribution, sharing, or commercial use is prohibited.
  Violations will be tracked and may result in account termination.
-->
"""
        
        watermarked_content = f"{protocol_content}{watermark}"
        
        return watermarked_content, watermark_id
    
    @staticmethod
    def add_watermark_to_steering_rules(rules: list, user_email: str, 
                                       key_prefix: str) -> tuple[list, str]:
        """
        Add watermark to steering rules list.
        
        Returns:
            (watermarked_rules, watermark_id)
        """
        watermark_id = WatermarkManager.generate_watermark_id()
        
        if not WATERMARK_ENABLED:
            return rules, watermark_id
        
        # Add watermark as a comment rule at the end
        watermark_rule = {
            'content': f'# VIZPILOT - Licensed to: {user_email} | Key: {key_prefix} | ID: {watermark_id}',
            'category': 'watermark',
            'priority': 9999
        }
        
        watermarked_rules = rules + [watermark_rule]
        
        return watermarked_rules, watermark_id
    
    @staticmethod
    def extract_watermark_id(content: str) -> str | None:
        """
        Extract watermark ID from content.
        Used for tracking leaked content.
        """
        import re
        
        # Try to find watermark ID in content
        pattern = r'Watermark ID: ([a-f0-9-]+)'
        match = re.search(pattern, content)
        
        if match:
            return match.group(1)
        
        return None


# Global watermark manager instance
watermark_manager = WatermarkManager()
