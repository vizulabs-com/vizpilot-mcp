"""
VIZPILOT MCP Server Package
Provides MCP server for IDE integration.
"""
from .config import MCP_SERVER_NAME, MCP_SERVER_VERSION

__version__ = MCP_SERVER_VERSION
__all__ = ['MCP_SERVER_NAME', 'MCP_SERVER_VERSION']

# Lazy imports to avoid Django setup on package import
def get_app():
    from .server import app
    return app

def get_main():
    from .server import main
    return main

def get_mcp_tools():
    from .tools import mcp_tools
    return mcp_tools
