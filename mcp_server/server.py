"""
VIZPILOT MCP Server
Main MCP server implementation using the MCP SDK.
"""
import asyncio
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from .tools import mcp_tools
from .config import MCP_SERVER_NAME, MCP_SERVER_VERSION, MCP_LOG_LEVEL

# Configure logging
logging.basicConfig(
    level=getattr(logging, MCP_LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Create MCP server instance
app = Server(MCP_SERVER_NAME)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available MCP tools.
    """
    return [
        Tool(
            name="list_technologies",
            description="List all available technologies/frameworks with access information",
            inputSchema={
                "type": "object",
                "properties": {
                    "api_key": {
                        "type": "string",
                        "description": "Your VIZPILOT API key"
                    }
                },
                "required": ["api_key"]
            }
        ),
        Tool(
            name="list_protocols",
            description="List all protocols for a specific technology",
            inputSchema={
                "type": "object",
                "properties": {
                    "api_key": {
                        "type": "string",
                        "description": "Your VIZPILOT API key"
                    },
                    "technology_slug": {
                        "type": "string",
                        "description": "Technology slug (e.g., 'django', 'react')"
                    }
                },
                "required": ["api_key", "technology_slug"]
            }
        ),
        Tool(
            name="get_protocol",
            description="Get full content of a specific protocol",
            inputSchema={
                "type": "object",
                "properties": {
                    "api_key": {
                        "type": "string",
                        "description": "Your VIZPILOT API key"
                    },
                    "protocol_id": {
                        "type": "string",
                        "description": "Protocol UUID (optional if using slugs)"
                    },
                    "technology_slug": {
                        "type": "string",
                        "description": "Technology slug (required if using protocol_slug)"
                    },
                    "protocol_slug": {
                        "type": "string",
                        "description": "Protocol slug (optional if using protocol_id)"
                    }
                },
                "required": ["api_key"]
            }
        ),
        Tool(
            name="get_steering_rules",
            description="Get steering rules for a technology (for IDE auto-injection)",
            inputSchema={
                "type": "object",
                "properties": {
                    "api_key": {
                        "type": "string",
                        "description": "Your VIZPILOT API key"
                    },
                    "technology_slug": {
                        "type": "string",
                        "description": "Technology slug (e.g., 'django', 'react')"
                    }
                },
                "required": ["api_key", "technology_slug"]
            }
        ),
        Tool(
            name="search_protocols",
            description="Search protocols across all technologies or within a specific technology",
            inputSchema={
                "type": "object",
                "properties": {
                    "api_key": {
                        "type": "string",
                        "description": "Your VIZPILOT API key"
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "technology_slug": {
                        "type": "string",
                        "description": "Optional technology filter"
                    }
                },
                "required": ["api_key", "query"]
            }
        ),
        Tool(
            name="get_user_info",
            description="Get your subscription info, usage stats, and rate limits",
            inputSchema={
                "type": "object",
                "properties": {
                    "api_key": {
                        "type": "string",
                        "description": "Your VIZPILOT API key"
                    }
                },
                "required": ["api_key"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool calls from IDE.
    """
    logger.info(f"Tool called: {name} with arguments: {arguments}")
    
    try:
        # Route to appropriate tool
        if name == "list_technologies":
            result = mcp_tools.list_technologies(arguments.get("api_key"))
        
        elif name == "list_protocols":
            result = mcp_tools.list_protocols(
                arguments.get("api_key"),
                arguments.get("technology_slug")
            )
        
        elif name == "get_protocol":
            result = mcp_tools.get_protocol(
                arguments.get("api_key"),
                arguments.get("protocol_id"),
                arguments.get("technology_slug"),
                arguments.get("protocol_slug")
            )
        
        elif name == "get_steering_rules":
            result = mcp_tools.get_steering_rules(
                arguments.get("api_key"),
                arguments.get("technology_slug")
            )
        
        elif name == "search_protocols":
            result = mcp_tools.search_protocols(
                arguments.get("api_key"),
                arguments.get("query"),
                arguments.get("technology_slug")
            )
        
        elif name == "get_user_info":
            result = mcp_tools.get_user_info(arguments.get("api_key"))
        
        else:
            result = {
                "success": False,
                "error": f"Unknown tool: {name}"
            }
        
        # Format result as JSON string
        import json
        result_text = json.dumps(result, indent=2)
        
        logger.info(f"Tool {name} completed successfully")
        
        return [TextContent(type="text", text=result_text)]
    
    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}", exc_info=True)
        error_result = {
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }
        import json
        return [TextContent(type="text", text=json.dumps(error_result, indent=2))]


async def async_main():
    """
    Main async entry point for MCP server.
    Runs the server using stdio transport.
    """
    logger.info(f"Starting {MCP_SERVER_NAME} v{MCP_SERVER_VERSION}")
    
    async with stdio_server() as (read_stream, write_stream):
        logger.info("MCP server running on stdio")
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


def main():
    """
    Synchronous entry point for console script.
    """
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
