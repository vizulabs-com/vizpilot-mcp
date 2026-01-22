# VIZPILOT MCP Server

<div align="center">

**Access 1000+ development protocols and steering rules directly in your IDE**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

[Website](https://vizpilot.vizulabs.com) • [Documentation](https://docs.vizpilot.vizulabs.com/mcp) • [Support](mailto:support@vizulabs.com)

</div>

## 🚀 Quick Start

### Installation

```bash
# Install the package
pip install git+https://github.com/vizulabs-com/vizpilot-mcp.git

# View setup instructions
vizpilot-welcome
```

The `vizpilot-welcome` command displays:
- ✅ Installation confirmation
- 🔑 API key instructions
- ⚙️ IDE configuration examples
- 📚 Available MCP tools
- 🔗 Documentation links

### Get Your API Key

1. Sign up at [vizpilot.vizulabs.com](https://vizpilot.vizulabs.com)
2. Navigate to [Dashboard → API Keys](https://vizpilot.vizulabs.com/dashboard/api-keys)
3. Generate a new API key

### Configure Your IDE

**Kiro IDE** (`~/.kiro/settings/mcp.json`):

```json
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
```

**Cursor IDE** (`~/.cursor/mcp.json`):

```json
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
```

See [examples/](examples/) for more IDE configurations.

### Restart Your IDE

After configuration, restart your IDE to activate the VIZPILOT MCP server.

## 📚 Features

- **1000+ Development Protocols** - Django, React, Vue, Angular, Node.js, and more
- **Technology-Specific Steering Rules** - Auto-injected guidance for your IDE
- **Real-time Protocol Search** - Find protocols instantly across all technologies
- **Usage Tracking** - Monitor API usage and subscription limits
- **Secure Authentication** - API key-based access with rate limiting
- **Caching** - Fast responses with intelligent caching

## 🛠️ Available MCP Tools

| Tool | Description |
|------|-------------|
| `list_technologies` | Browse all available technologies/frameworks |
| `list_protocols` | View protocols for a specific technology |
| `get_protocol` | Get full protocol content with markdown formatting |
| `get_steering_rules` | Get IDE steering rules for auto-injection |
| `search_protocols` | Search across all protocols by keyword |
| `get_user_info` | Check subscription status, usage stats, and rate limits |

## 💡 Usage Examples

### List Available Technologies
```python
# Returns: Django, React, Vue, Angular, Node.js, Python, etc.
list_technologies(api_key="your_api_key")
```

### Get Django Protocols
```python
# Returns: All Django-related protocols
list_protocols(api_key="your_api_key", technology_slug="django")
```

### Search for Authentication Protocols
```python
# Returns: All protocols related to authentication
search_protocols(api_key="your_api_key", query="authentication")
```

## 🔄 Updates

```bash
pip install --upgrade git+https://github.com/vizulabs-com/vizpilot-mcp.git
```

## 🐛 Troubleshooting

### Welcome Message Not Showing During Installation?

This is normal! Pip suppresses output from setup.py. Run this command to view setup instructions:

```bash
vizpilot-welcome
```

### Can't Find vizpilot-welcome Command?

Make sure Python's bin directory is in your PATH:

```bash
# Check if it's installed
pip show vizpilot-mcp

# Try running directly
python -m mcp_server.__main__
```

### MCP Server Not Connecting?

1. Verify your API key is correct
2. Check IDE configuration file location
3. Restart your IDE after configuration changes
4. Check IDE logs for error messages

## 📖 Documentation

- [Full Documentation](https://docs.vizpilot.vizulabs.com/mcp)
- [API Reference](https://docs.vizpilot.vizulabs.com/mcp/api)
- [IDE Setup Guides](https://docs.vizpilot.vizulabs.com/mcp/setup)
- [Troubleshooting Guide](https://docs.vizpilot.vizulabs.com/mcp/troubleshooting)

## 🤝 Support

- **Issues:** [GitHub Issues](https://github.com/vizulabs-com/vizpilot-mcp/issues)
- **Email:** support@vizulabs.com
- **Documentation:** [docs.vizpilot.vizulabs.com](https://docs.vizpilot.vizulabs.com)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🌟 Show Your Support

If you find VIZPILOT MCP helpful:
- ⭐ Star this repository
- 🐦 Share on social media
- 📝 Write a review
- 🤝 Contribute to the project

---

<div align="center">

Made with ❤️ by [VizuLabs](https://vizulabs.com)

**[Get Started](https://vizpilot.vizulabs.com)** • **[Documentation](https://docs.vizpilot.vizulabs.com)** • **[Support](mailto:support@vizulabs.com)**

</div>
