#!/bin/bash
# VIZPILOT MCP Server - Testing Setup Script

echo "=========================================="
echo "VIZPILOT MCP Server - Testing Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
echo ""

# Install MCP SDK
echo "Installing MCP SDK..."
pip3 install mcp==0.9.0
echo ""

# Check Redis
echo "Checking Redis..."
if redis-cli ping > /dev/null 2>&1; then
    echo "✓ Redis is running"
else
    echo "✗ Redis is not running"
    echo "  Start Redis with: redis-server"
    echo "  Or with Docker: docker run -d -p 6379:6379 redis:latest"
fi
echo ""

# Check PostgreSQL
echo "Checking PostgreSQL..."
if pg_isready > /dev/null 2>&1; then
    echo "✓ PostgreSQL is running"
else
    echo "✗ PostgreSQL is not running"
    echo "  Check your Docker containers: docker ps"
fi
echo ""

# Check Django
echo "Checking Django setup..."
python3 manage.py check
echo ""

echo "=========================================="
echo "Setup complete! Ready to test."
echo "=========================================="
echo ""
echo "Run tests with:"
echo "  python3 test_mcp_server.py"
echo ""
