# VIZPILOT MCP Server

<div align="center">

![VIZPILOT Logo](https://vizpilot.vizulabs.com/static/images/logo.png)

**Access 1000+ development protocols and steering rules directly in your IDE**

[![PyPI version](https://badge.fury.io/py/vizpilot-mcp.svg)](https://badge.fury.io/py/vizpilot-mcp)
[![Python Support](https://img.shields.io/pypi/pyversions/vizpilot-mcp.svg)](https://pypi.org/project/vizpilot-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/vizpilot-mcp)](https://pepy.tech/project/vizpilot-mcp)

[Website](https://vizpilot.vizulabs.com) • [Documentation](https://docs.vizpilot.vizulabs.com/mcp) • [Discord](https://discord.gg/vizpilot) • [Support](mailto:support@vizulabs.com)

</div>

## 🚀 What is VIZPILOT MCP?

VIZPILOT MCP Server brings the power of curated development protocols directly into your IDE through the Model Context Protocol (MCP). Get instant access to:

- **1000+ Development Protocols** - Best practices for Django, React, Vue, Angular, Node.js, and more
- **Technology-Specific Steering Rules** - Auto-injected guidance for your tech stack
- **Real-time Protocol Search** - Find the right protocol instantly
- **Usage Tracking** - Monitor your API usage and limits
- **Secure Authentication** - API key-based access control

## 📦 Installation

### Quick Install

```bash
pip install vizpilot-mcp
```

### Alternative Methods

**Using pipx (isolated environment):**
```bash
pipx install vizpilot-mcp
```

**Using uvx (on-demand execution):**
```bash
uvx vizpilot-mcp
```

## 🎯 Quick Start

### 1. Get Your API Key

1. Sign up at [vizpilot.com](https://vizpilot.vizulabs.com)
2. Navigate to [Dashboard → API Keys](https://vizpilot.vizulabs.com/dashboard/api-keys)
3. Generate a new API key

### 2. Configure Your IDE

#### Kiro IDE

Add to `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "vizpilot": {
      "command": "vizpilot-mcp",
      "env": {
        "VIZPILOT_API_KEY": "your_api_key_here",
        "VIZPILOT_BASE_URL": "https://vizpilot.vizulabs.com"
      }
    }
  }
}
```

#### Cursor IDE

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "vizpilot": {
      "command": "vizpilot-mcp",
      "env": {
        "VIZPILOT_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

#### VS Code (with MCP Extension)

Add to `.vscode/mcp.json`:

```json
{
  "mcpServers": {
    "vizpilot": {
      "command": "vizpilot-mcp",
      "env": {
        "VIZPILOT_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### 3. Start Using

Restart your IDE and start using VIZPILOT protocols!

## 🛠️ Available Tools

The MCP server provides 6 powerful tools:

### 1. `list_technologies`
List all available technologies/frameworks with access information.

```json
{
  "api_key": "your_api_key"
}
```

### 2. `list_protocols`
List all protocols for a specific technology.

```json
{
  "api_key": "your_api_key",
  "technology_slug": "django"
}
```

### 3. `get_protocol`
Get full content of a specific protocol.

```json
{
  "api_key": "your_api_key",
  "technology_slug": "django",
  "protocol_slug": "authentication"
}
```

### 4. `get_steering_rules`
Get steering rules for auto-injection in your IDE.

```json
{
  "api_key": "your_api_key",
  "technology_slug": "django"
}
```

### 5. `search_protocols`
Search protocols across all technologies.

```json
{
  "api_key": "your_api_key",
  "query": "authentication",
  "technology_slug": "django"
}
```

### 6. `get_user_info`
Get your subscription info, usage stats, and rate limits.

```json
{
  "api_key": "your_api_key"
}
```

## 🎨 Supported Technologies

- **Backend:** Django, Laravel, .NET, Node.js, Express, FastAPI
- **Frontend:** React, Vue, Angular, Svelte, Next.js, Nuxt.js
- **Mobile:** React Native, Flutter, iOS (Swift), Android (Kotlin)
- **Database:** PostgreSQL, MySQL, MongoDB, Redis
- **DevOps:** Docker, Kubernetes, AWS, Azure, GCP
- **And many more...**

## 💎 Subscription Tiers

### Free Tier
- Access to basic protocols
- 100 API calls per day
- Community support

### Starter ($9/month)
- Access to all basic + intermediate protocols
- 1,000 API calls per day
- Email support

### Pro ($29/month)
- Access to all protocols including advanced
- 10,000 API calls per day
- Priority support
- Early access to new protocols

### Enterprise (Custom)
- Unlimited API calls
- Custom protocols
- Dedicated support
- SLA guarantees

[View Pricing](https://vizpilot.vizulabs.com/pricing)

## 📚 Documentation

### Full Documentation
Visit [docs.vizpilot.com/mcp](https://docs.vizpilot.vizulabs.com/mcp) for:
- Detailed setup guides
- IDE-specific configurations
- API reference
- Best practices
- Troubleshooting

### Example Usage

```python
# Example: Using VIZPILOT MCP in your IDE
# The IDE will automatically call these tools based on your context

# When you're working on Django authentication:
# → MCP automatically fetches Django authentication protocol
# → Steering rules are injected for best practices
# → You get real-time guidance as you code
```

## 🔒 Security

- **API Key Authentication** - Secure token-based access
- **Rate Limiting** - Prevent abuse and ensure fair usage
- **Watermarking** - Content tracking for security
- **HTTPS Only** - All communications encrypted
- **No Code Execution** - Read-only access to protocols

## 🤝 Support

### Community Support
- [Discord Community](https://discord.gg/vizpilot)
- [GitHub Issues](https://github.com/vizulabs/vizpilot-mcp/issues)
- [Documentation](https://docs.vizpilot.vizulabs.com)

### Professional Support
- Email: [support@vizulabs.com](mailto:support@vizulabs.com)
- Priority support for Pro/Enterprise users

## 🐛 Troubleshooting

### MCP Server Not Connecting

1. **Check API Key:**
   ```bash
   echo $VIZPILOT_API_KEY
   ```

2. **Test Connection:**
   ```bash
   vizpilot-mcp --test
   ```

3. **Check Logs:**
   - Kiro: Check IDE console
   - Cursor: Check `~/.cursor/logs/mcp.log`

### Rate Limit Errors

Check your usage:
```bash
vizpilot-mcp --usage
```

Upgrade your plan at [vizpilot.com/pricing](https://vizpilot.vizulabs.com/pricing)

### Common Issues

**Issue:** "Invalid API key"
- **Solution:** Regenerate API key in dashboard

**Issue:** "Technology not found"
- **Solution:** Check available technologies with `list_technologies` tool

**Issue:** "Rate limit exceeded"
- **Solution:** Wait for rate limit reset or upgrade plan

## 🔄 Updates

Stay updated with the latest protocols and features:

```bash
pip install --upgrade vizpilot-mcp
```

## 📝 Changelog

See [CHANGELOG.md](https://github.com/vizulabs/vizpilot-mcp/blob/main/CHANGELOG.md) for version history.

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](https://github.com/vizulabs/vizpilot-mcp/blob/main/CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Show Your Support

If you find VIZPILOT MCP helpful, please:
- ⭐ Star the [GitHub repository](https://github.com/vizulabs/vizpilot-mcp)
- 🐦 Share on [Twitter](https://twitter.com/intent/tweet?text=Check%20out%20VIZPILOT%20MCP%20-%20Development%20protocols%20in%20your%20IDE!&url=https://vizpilot.vizulabs.com)
- 📝 Write a review or blog post

## 🔗 Links

- **Website:** [vizpilot.com](https://vizpilot.vizulabs.com)
- **Documentation:** [docs.vizpilot.com](https://docs.vizpilot.vizulabs.com)
- **GitHub:** [github.com/vizulabs/vizpilot-mcp](https://github.com/vizulabs/vizpilot-mcp)
- **PyPI:** [pypi.org/project/vizpilot-mcp](https://pypi.org/project/vizpilot-mcp)
- **Discord:** [discord.gg/vizpilot](https://discord.gg/vizpilot)

---

<div align="center">

Made with ❤️ by [VizuLabs](https://vizulabs.com)

**Happy Coding! 🚀**

</div>
