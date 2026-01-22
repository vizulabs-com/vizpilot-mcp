#!/usr/bin/env python3
"""
VIZPILOT MCP Server
Provides protocol access via Model Context Protocol
Connects to VIZPILOT API (configurable via environment variables)
"""
import json
import sys
import os
import requests
from typing import Any, Dict

# Ensure unbuffered output for MCP communication
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Configuration from environment
API_KEY = os.environ.get('VIZPILOT_API_KEY', '')
BASE_URL = os.environ.get('VIZPILOT_BASE_URL', 'http://localhost:8004')
IDE_TYPE = os.environ.get('IDE_TYPE', 'kiro')


def send_response(response: Dict[str, Any]) -> None:
    """Send JSON response to stdout"""
    print(json.dumps(response), flush=True)


def handle_initialize(request_id: Any, params: Dict[str, Any]) -> None:
    """Handle initialize request"""
    send_response({
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "resources": {}
            },
            "serverInfo": {
                "name": "vizpilot-mcp",
                "version": "1.0.0"
            }
        }
    })


def handle_tools_list(request_id: Any, params: Dict[str, Any]) -> None:
    """Handle tools/list request"""
    send_response({
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "tools": [
                {
                    "name": "list_technologies",
                    "description": "List all available technologies from NEXA",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                },
                {
                    "name": "list_protocols",
                    "description": "List all protocols for a technology",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "technology": {
                                "type": "string",
                                "description": "Technology slug (e.g., 'django')"
                            }
                        }
                    }
                },
                {
                    "name": "get_protocol",
                    "description": "Get a specific protocol by slug",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "slug": {
                                "type": "string",
                                "description": "Protocol slug"
                            },
                            "technology": {
                                "type": "string",
                                "description": "Technology slug (optional)"
                            }
                        },
                        "required": ["slug"]
                    }
                }
            ]
        }
    })


def handle_tools_call(request_id: Any, params: Dict[str, Any]) -> None:
    """Handle tools/call request"""
    tool_name = params.get("name")
    arguments = params.get("arguments", {})
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        if tool_name == "list_technologies":
            # Call NEXA API
            response = requests.get(
                f"{BASE_URL}/api/technologies/",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            # Format response
            technologies = data.get("technologies", [])
            text = f"Found {data.get('count', 0)} technologies:\n\n"
            
            for tech in technologies:
                text += f"• **{tech['name']}** (`{tech['slug']}`)\n"
                text += f"  Tier: {tech['tier_required']}\n"
                text += f"  Protocols: {tech['protocol_count']}\n"
                if tech.get('description'):
                    text += f"  {tech['description']}\n"
                text += "\n"
            
            send_response({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                }
            })
            
        elif tool_name == "list_protocols":
            technology = arguments.get("technology", "")
            
            # Build query parameters
            params_dict = {}
            if technology:
                params_dict["technology"] = technology
            
            # Call NEXA API (using the function from views.py)
            response = requests.get(
                f"{BASE_URL}/api/v1/protocols/",
                headers=headers,
                params=params_dict,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            # Format response
            protocols = data.get("results", [])
            text = f"Found {data.get('count', 0)} protocols"
            if technology:
                text += f" for {technology}"
            text += ":\n\n"
            
            for p in protocols[:20]:  # Limit to first 20
                text += f"• {p.get('icon', '📄')} **{p['name']}** (`{p['slug']}`)\n"
                text += f"  Version: {p['current_version']}\n"
                if p.get('description'):
                    text += f"  {p['description'][:100]}...\n"
                text += "\n"
            
            send_response({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                }
            })
            
        elif tool_name == "get_protocol":
            slug = arguments.get("slug")
            technology = arguments.get("technology", "")
            
            if not slug:
                send_response({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32602,
                        "message": "'slug' parameter is required"
                    }
                })
                return
            
            # Build query parameters
            params_dict = {}
            if technology:
                params_dict["technology"] = technology
            
            # Call NEXA API
            response = requests.get(
                f"{BASE_URL}/api/v1/protocols/{slug}/",
                headers=headers,
                params=params_dict,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            # Format response with protocol files
            text = f"# {data.get('icon', '📄')} {data['name']}\n\n"
            text += f"**Slug:** `{data['slug']}`\n"
            text += f"**Version:** {data['current_version']}\n"
            text += f"**Description:** {data.get('description', 'N/A')}\n\n"
            
            files = data.get('files', [])
            if files:
                text += f"## Protocol Content\n\n"
                for file in files:
                    text += "```markdown\n"
                    text += file['content']
                    text += "\n```\n\n"
            else:
                text += "No protocol content available.\n"
            
            send_response({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                }
            })
            
        else:
            send_response({
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Unknown tool '{tool_name}'"
                }
            })
            
    except requests.exceptions.RequestException as e:
        send_response({
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32603,
                "message": f"API request failed: {str(e)}"
            }
        })
    except Exception as e:
        send_response({
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        })


def main():
    """Main MCP server loop"""
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            request_id = request.get("id")
            method = request.get("method")
            params = request.get("params", {})
            
            if method == "initialize":
                handle_initialize(request_id, params)
            elif method == "tools/list":
                handle_tools_list(request_id, params)
            elif method == "tools/call":
                handle_tools_call(request_id, params)
            else:
                send_response({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                })
        except json.JSONDecodeError:
            send_response({
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            })
        except Exception as e:
            send_response({
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            })


if __name__ == "__main__":
    main()
