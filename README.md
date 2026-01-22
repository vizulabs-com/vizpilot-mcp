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
pip install git+https://github.com/vizulabs-com/vizpilot-mcp.git
```

### Get Your API Key

1. Sign up at [vizpilot.com](https://vizpilot.vizulabs.com)
2. Navigate to [Dashboard → API Keys](https://vizpilot.vizulabs.com/dashboard/api-keys)
3. Generate a new API key

### Configure Your IDE

**Kiro IDE:**

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

See [examples/](examples/) for more IDE configurations.

## 📚 Features

- **1000+ Development Protocols** - Django, React, Vue, Angular, Node.js, and more
- **Technology-Specific Steering Rules** - Auto-injected guidance
- **Real-time Protocol Search** - Find protocols instantly
- **Usage Tracking** - Monitor API usage and limits
- **Secure Authentication** - API key-based access

## 🛠️ Available Tools

1. `list_technologies` - List all available technologies
2. `list_protocols` - List protocols for a technology
3. `get_protocol` - Get full protocol content
4. `get_steering_rules` - Get steering rules for IDE injection
5. `search_protocols` - Search across all protocols
6. `get_user_info` - Get subscription and usage info

## 📖 Documentation

- [Installation Guide](docs/installation.md)
- [Configuration Guide](docs/configuration.md)
- [Troubleshooting](docs/troubleshooting.md)
- [API Reference](docs/api-reference.md)

## 🔄 Updates

```bash
pip install --upgrade git+https://github.com/vizulabs-com/vizpilot-mcp.git
```

## 🐛 Issues & Support

- **Issues:** [GitHub Issues](https://github.com/vizulabs-com/vizpilot-mcp/issues)
- **Email:** support@vizulabs.com
- **Discord:** [Join our community](https://discord.gg/vizpilot)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🌟 Show Your Support

If you find VIZPILOT MCP helpful:
- ⭐ Star this repository
- 🐦 Share on social media
- 📝 Write a review

---

Made with ❤️ by [VizuLabs](https://vizulabs.com)
