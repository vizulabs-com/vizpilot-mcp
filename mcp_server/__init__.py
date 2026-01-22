"""
VIZPILOT MCP Server Package
Provides MCP server for IDE integration.
"""
from .server import app, main
from .tools import mcp_tools
from .config import MCP_SERVER_NAME, MCP_SERVER_VERSION

__version__ = MCP_SERVER_VERSION
__all__ = ['app', 'main', 'mcp_tools', 'MCP_SERVER_NAME', 'MCP_SERVER_VERSION']
