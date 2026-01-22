"""
VIZPILOT MCP Server - Post-install welcome message
"""

def show_welcome():
    """Display welcome message with VIZPILOT logo after installation"""
    
    logo = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ██╗   ██╗██╗███████╗██████╗ ██╗██╗      ██████╗ ████████╗   ║
║   ██║   ██║██║╚══███╔╝██╔══██╗██║██║     ██╔═══██╗╚══██╔══╝   ║
║   ██║   ██║██║  ███╔╝ ██████╔╝██║██║     ██║   ██║   ██║      ║
║   ╚██╗ ██╔╝██║ ███╔╝  ██╔═══╝ ██║██║     ██║   ██║   ██║      ║
║    ╚████╔╝ ██║███████╗██║     ██║███████╗╚██████╔╝   ██║      ║
║     ╚═══╝  ╚═╝╚══════╝╚═╝     ╚═╝╚══════╝ ╚═════╝    ╚═╝      ║
║                                                                  ║
║                    MCP SERVER v1.0.0                            ║
║              Access 1000+ Development Protocols                 ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

✅ Installation successful!

📚 Next Steps:

1. Get your API key:
   → Visit: https://vizpilot.vizulabs.com/dashboard/api-keys
   → Generate a new API key

2. Configure your IDE:

   Kiro IDE (~/.kiro/settings/mcp.json):
   {
     "mcpServers": {
       "vizpilot": {
         "command": "python",
         "args": ["-m", "mcp_server.server"],
         "env": {
           "VIZPILOT_API_KEY": "your_api_key_here",
           "VIZPILOT_BASE_URL": "https://vizpilot.vizulabs.com"
         }
       }
     }
   }

   Cursor IDE (~/.cursor/mcp.json):
   {
     "mcpServers": {
       "vizpilot": {
         "command": "python",
         "args": ["-m", "mcp_server.server"],
         "env": {
           "VIZPILOT_API_KEY": "your_api_key_here"
         }
       }
     }
   }

3. Restart your IDE

4. Start using VIZPILOT MCP tools:
   • list_technologies - Browse available technologies
   • list_protocols - View protocols for a technology
   • get_protocol - Get full protocol content
   • get_steering_rules - Get IDE steering rules
   • search_protocols - Search across all protocols
   • get_user_info - Check your subscription & usage

📖 Documentation: https://docs.vizpilot.vizulabs.com/mcp
🐛 Issues: https://github.com/vizulabs-com/vizpilot-mcp/issues
💬 Support: support@vizulabs.com

Happy coding! 🚀
"""
    
    print(logo)


if __name__ == "__main__":
    show_welcome()
