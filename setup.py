"""
VIZPILOT MCP Server - Setup Configuration
Package for distributing VIZPILOT MCP server to PyPI
"""
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
import os
import sys

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define requirements directly
requirements = [
    "mcp>=0.1.0",
    "httpx>=0.24.0",
    "redis>=4.5.0",
    "python-dotenv>=1.0.0",
]


def show_welcome_message():
    """Display welcome message with VIZPILOT logo"""
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

5. Example usage in your IDE:
   Simply ask your AI assistant:
   "List all Django protocols from VIZPILOT"
   "Get the Django authentication protocol"
   "Search VIZPILOT for React best practices"
   
   The MCP tools work automatically in the background!

💬 Support: support@vizulabs.com

Happy coding! 🚀
"""
    print(logo)


class PostInstallCommand(install):
    """Post-installation command to show welcome message"""
    def run(self):
        install.run(self)
        # Show welcome message immediately after installation
        show_welcome_message()


class PostDevelopCommand(develop):
    """Post-development installation command to show welcome message"""
    def run(self):
        develop.run(self)
        # Show welcome message immediately after installation
        show_welcome_message()

setup(
    name="vizpilot-mcp",
    version="1.0.0",
    author="VizuLabs",
    author_email="support@vizulabs.com",
    description="VIZPILOT MCP Server - Access development protocols and steering rules in your IDE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vizulabs/vizpilot-mcp",
    project_urls={
        "Bug Tracker": "https://github.com/vizulabs/vizpilot-mcp/issues",
        "Documentation": "https://docs.vizpilot.vizulabs.com/mcp",
        "Homepage": "https://vizpilot.vizulabs.com",
        "Source": "https://github.com/vizulabs/vizpilot-mcp",
    },
    packages=find_packages(exclude=["tests", "tests.*", "docs", "docs.*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    keywords="mcp ide protocols development django react vue angular nodejs python javascript",
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "vizpilot-mcp=mcp_server.server:main",
            "vizpilot-welcome=mcp_server.__main__:show_welcome",
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
        'develop': PostDevelopCommand,
    },
    include_package_data=True,
    zip_safe=False,
)
