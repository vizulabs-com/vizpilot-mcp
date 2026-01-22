#!/bin/bash
# Setup GitHub Distribution for VIZPILOT MCP
# This script prepares and pushes the MCP server to GitHub

set -e

echo "🚀 VIZPILOT MCP - GitHub Distribution Setup"
echo "==========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if we're in NEXA directory
if [ ! -f "setup.py" ]; then
    echo -e "${RED}❌ Error: setup.py not found. Please run from NEXA directory.${NC}"
    exit 1
fi

echo "📁 Current directory: $(pwd)"
echo ""

# Step 1: Prepare README for GitHub
echo "📝 Preparing README for GitHub..."
if [ -f "MCP_README.md" ]; then
    cp MCP_README.md README_MCP_PACKAGE.md
    echo -e "${GREEN}✅ README prepared${NC}"
else
    echo -e "${YELLOW}⚠️  MCP_README.md not found, skipping${NC}"
fi

# Step 2: Create/Update .gitignore
echo ""
echo "📝 Creating .gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Environment variables
.env
.env.local
.env.*.local

# Django specific (exclude from MCP package)
db.sqlite3
db.sqlite3-journal
media/
staticfiles/
celerybeat-schedule
celerybeat.pid

# Django apps (not part of MCP package)
accounts/
api/
dashboard/
protocols/
subscriptions/
templates/
static/
vizpilot_config/
manage.py
docker-compose.yml
Dockerfile
docker-entrypoint.sh

# Documentation (keep only MCP docs)
.Vizwiki/
SYSDOCS/

# Test files
test_*.py
test_*.sh
*.pyc

# OS
.DS_Store
Thumbs.db
*.log
EOF

echo -e "${GREEN}✅ .gitignore created${NC}"

# Step 3: Create examples directory
echo ""
echo "📁 Creating examples directory..."
mkdir -p examples

# Kiro example
cat > examples/kiro-config.json << 'EOF'
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
EOF

# Cursor example
cat > examples/cursor-config.json << 'EOF'
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
EOF

# VS Code example
cat > examples/vscode-config.json << 'EOF'
{
  "mcp.servers": {
    "vizpilot": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "env": {
        "VIZPILOT_API_KEY": "your_api_key_here"
      }
    }
  }
}
EOF

echo -e "${GREEN}✅ Example configurations created${NC}"

# Step 4: Create GitHub-specific README
echo ""
echo "📝 Creating GitHub README..."
cat > README.md << 'EOF'
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
EOF

echo -e "${GREEN}✅ GitHub README created${NC}"

# Step 5: Initialize git if needed
echo ""
if [ ! -d .git ]; then
    echo "🔧 Initializing git repository..."
    git init
    echo -e "${GREEN}✅ Git initialized${NC}"
else
    echo -e "${GREEN}✅ Git already initialized${NC}"
fi

# Step 6: Check for GitHub remote
echo ""
echo "🔗 Checking GitHub remote..."
if git remote | grep -q origin; then
    echo -e "${YELLOW}⚠️  Remote 'origin' already exists${NC}"
    echo "Current remote:"
    git remote -v
    echo ""
    read -p "Do you want to update it to vizulabs-com/vizpilot-mcp? [y/N]: " update_remote
    if [[ $update_remote =~ ^[Yy]$ ]]; then
        git remote set-url origin https://github.com/vizulabs-com/vizpilot-mcp.git
        echo -e "${GREEN}✅ Remote updated${NC}"
    fi
else
    git remote add origin https://github.com/vizulabs-com/vizpilot-mcp.git
    echo -e "${GREEN}✅ Remote added: https://github.com/vizulabs-com/vizpilot-mcp.git${NC}"
fi

# Step 7: Stage files
echo ""
echo "📦 Staging files for commit..."
git add mcp_server/
git add setup.py pyproject.toml MANIFEST.in
git add LICENSE CHANGELOG.md README.md
git add examples/
git add .gitignore

echo -e "${GREEN}✅ Files staged${NC}"

# Step 8: Show status
echo ""
echo "📊 Git status:"
git status --short

# Step 9: Commit
echo ""
read -p "Do you want to commit these changes? [y/N]: " do_commit
if [[ $do_commit =~ ^[Yy]$ ]]; then
    git commit -m "Initial commit: VIZPILOT MCP Server v1.0.0

- MCP server implementation with 6 tools
- API key authentication
- Rate limiting and caching
- Content watermarking
- Support for multiple IDEs (Kiro, Cursor, VS Code)
- Comprehensive documentation"
    
    echo -e "${GREEN}✅ Changes committed${NC}"
else
    echo "Skipping commit. You can commit manually later."
    exit 0
fi

# Step 10: Push to GitHub
echo ""
read -p "Do you want to push to GitHub now? [y/N]: " do_push
if [[ $do_push =~ ^[Yy]$ ]]; then
    echo "📤 Pushing to GitHub..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Successfully pushed to GitHub!${NC}"
    else
        echo -e "${RED}❌ Push failed. You may need to:${NC}"
        echo "   1. Create the repository on GitHub first"
        echo "   2. Authenticate with GitHub"
        echo "   3. Check your internet connection"
        exit 1
    fi
else
    echo "Skipping push. You can push manually later with:"
    echo "  git push -u origin main"
    exit 0
fi

# Step 11: Create tag
echo ""
read -p "Do you want to create v1.0.0 tag? [y/N]: " do_tag
if [[ $do_tag =~ ^[Yy]$ ]]; then
    git tag -a v1.0.0 -m "Release version 1.0.0"
    git push origin v1.0.0
    echo -e "${GREEN}✅ Tag v1.0.0 created and pushed${NC}"
fi

# Success message
echo ""
echo -e "${GREEN}🎉 GitHub distribution setup complete!${NC}"
echo ""
echo "Repository: https://github.com/vizulabs-com/vizpilot-mcp"
echo ""
echo "Users can install with:"
echo "  pip install git+https://github.com/vizulabs-com/vizpilot-mcp.git"
echo ""
echo "Next steps:"
echo "1. Go to GitHub and verify the repository"
echo "2. Create a release at: https://github.com/vizulabs-com/vizpilot-mcp/releases"
echo "3. Test installation: pip install git+https://github.com/vizulabs-com/vizpilot-mcp.git"
echo "4. Share with users!"
