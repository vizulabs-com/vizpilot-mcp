#!/usr/bin/env python3
"""
VIZPILOT MCP Welcome
Shows setup instructions and getting started guide
"""


def show_welcome():
    """Display welcome message and setup instructions"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              🚀 VIZPILOT MCP - Welcome! 🚀                  ║
║                                                              ║
║         Access Development Protocols in Your IDE            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

✅ Installation Complete!

📚 Quick Start Guide:

1️⃣  Get Your API Key
   • Go to your VIZPILOT instance (e.g., http://localhost:8004)
   • Navigate to Dashboard → API Keys
   • Generate a new API key for your IDE

2️⃣  Configure Your IDE

   For Kiro IDE:
   • Create: ~/.kiro/settings/mcp.json
   • Add configuration:
   
   {
     "mcpServers": {
       "vizpilot": {
         "command": "python3",
         "args": ["-m", "vizpilot_mcp.server"],
         "env": {
           "VIZPILOT_API_KEY": "your_api_key_here",
           "VIZPILOT_BASE_URL": "http://localhost:8004",
           "IDE_TYPE": "kiro"
         }
       }
     }
   }

   For Cursor IDE:
   • Create: ~/.cursor/mcp.json
   • Use same configuration, change IDE_TYPE to "cursor"

   For Qoder IDE:
   • Create: ~/.qoder/mcp.json
   • Use same configuration, change IDE_TYPE to "qoder"

3️⃣  Restart Your IDE
   • Close and reopen your IDE
   • MCP tools will be available

4️⃣  Test the Connection
   • Try: "List available technologies"
   • Try: "Get Django protocols"
   • Try: "Show authentication protocol"

📖 Available MCP Tools:

   • list_technologies    - List all available technologies
   • list_protocols       - List protocols for a technology
   • get_protocol         - Get full protocol content

🔗 Resources:

   • Support: support@vizulabs.com

💡 Tips:

   • Keep your API key secure (never commit to git)
   • Update VIZPILOT_BASE_URL if using a different server
   • Check IDE logs if MCP tools don't appear

🎉 Happy Coding with VIZPILOT!

""")


if __name__ == "__main__":
    show_welcome()
