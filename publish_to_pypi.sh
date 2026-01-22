#!/bin/bash
# VIZPILOT MCP Server - PyPI Publishing Script
# This script automates the process of building and publishing to PyPI

set -e

echo "🚀 VIZPILOT MCP Server - PyPI Publishing"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo -e "${RED}❌ Error: setup.py not found. Please run this script from NEXA directory.${NC}"
    exit 1
fi

# Check if required tools are installed
echo "🔍 Checking required tools..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

if ! python3 -m pip show build &> /dev/null; then
    echo -e "${YELLOW}⚠️  'build' package not found. Installing...${NC}"
    python3 -m pip install build
fi

if ! python3 -m pip show twine &> /dev/null; then
    echo -e "${YELLOW}⚠️  'twine' package not found. Installing...${NC}"
    python3 -m pip install twine
fi

echo -e "${GREEN}✅ All required tools are installed${NC}"
echo ""

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info
echo -e "${GREEN}✅ Cleaned${NC}"
echo ""

# Build the package
echo "📦 Building package..."
python3 -m build
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Package built successfully${NC}"
echo ""

# Check the package
echo "🔍 Checking package..."
python3 -m twine check dist/*
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Package check failed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Package check passed${NC}"
echo ""

# Ask for confirmation
echo "📊 Package contents:"
ls -lh dist/
echo ""

read -p "Do you want to upload to TestPyPI first? (recommended) [y/N]: " test_upload
if [[ $test_upload =~ ^[Yy]$ ]]; then
    echo ""
    echo "📤 Uploading to TestPyPI..."
    python3 -m twine upload --repository testpypi dist/*
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Successfully uploaded to TestPyPI${NC}"
        echo ""
        echo "🧪 Test installation with:"
        echo "   pip install --index-url https://test.pypi.org/simple/ vizpilot-mcp"
        echo ""
        read -p "Press Enter to continue to production PyPI or Ctrl+C to exit..."
    else
        echo -e "${RED}❌ TestPyPI upload failed${NC}"
        exit 1
    fi
fi

echo ""
read -p "⚠️  Upload to production PyPI? This cannot be undone! [y/N]: " prod_upload
if [[ ! $prod_upload =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Upload to PyPI
echo ""
echo "📤 Uploading to PyPI..."
python3 -m twine upload dist/*

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Successfully published to PyPI!${NC}"
    echo ""
    echo "🎉 Package is now available at:"
    echo "   https://pypi.org/project/vizpilot-mcp/"
    echo ""
    echo "📥 Users can install with:"
    echo "   pip install vizpilot-mcp"
    echo ""
    echo "📊 Track downloads at:"
    echo "   https://pypistats.org/packages/vizpilot-mcp"
    echo ""
else
    echo -e "${RED}❌ PyPI upload failed${NC}"
    exit 1
fi
