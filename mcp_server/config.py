"""
MCP Server Configuration
Handles environment variables and settings for the MCP server.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# MCP Server Settings
MCP_SERVER_NAME = os.getenv('MCP_SERVER_NAME', 'vizpilot-mcp')
MCP_SERVER_VERSION = os.getenv('MCP_SERVER_VERSION', '1.0.0')
MCP_LOG_LEVEL = os.getenv('MCP_LOG_LEVEL', 'INFO')

# Database Settings (from Django)
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://vizpilot:vizpilot123@localhost:5432/vizpilot_db')

# Redis Settings (for caching and rate limiting)
# Build from individual env vars if REDIS_URL not set
if 'REDIS_URL' in os.environ:
    REDIS_URL = os.getenv('REDIS_URL')
else:
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    # Inside Docker, use internal port 6379, not the external mapped port
    redis_port = '6379' if redis_host != 'localhost' else os.getenv('REDIS_PORT', '6379')
    redis_db = os.getenv('REDIS_DB', '0')
    REDIS_URL = f'redis://{redis_host}:{redis_port}/{redis_db}'

# API Settings
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8004')

# Rate Limiting (requests per minute, requests per day)
RATE_LIMITS = {
    'free': {'per_minute': 5, 'per_day': 100},
    'starter': {'per_minute': 20, 'per_day': 1000},
    'pro': {'per_minute': 100, 'per_day': None},  # None = unlimited
    'enterprise': {'per_minute': None, 'per_day': None},  # None = unlimited
}

# Cache TTL (in seconds)
CACHE_TTL = {
    'protocol': 3600,  # 1 hour
    'steering_rules': 86400,  # 24 hours
    'user_info': 300,  # 5 minutes
    'technology_list': 3600,  # 1 hour
}

# Watermark Settings
WATERMARK_ENABLED = os.getenv('WATERMARK_ENABLED', 'true').lower() == 'true'
WATERMARK_FORMAT = "<!-- VIZPILOT - Licensed to: {email} | Key: {key_prefix} | ID: {watermark_id} -->"

# Logging
LOG_FILE = os.getenv('MCP_LOG_FILE', str(BASE_DIR / 'logs' / 'mcp_server.log'))
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Django Settings Module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vizpilot_config.settings')
