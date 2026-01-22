#!/bin/bash

# Script to update all vizpilot.com URLs to vizpilot.vizulabs.com
# This ensures consistency across the entire codebase

echo "🔄 Updating all vizpilot.com URLs to vizpilot.vizulabs.com..."

# Update Python files
find . -type f -name "*.py" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|https://vizpilot\.com|https://vizpilot.vizulabs.com|g' {} +
find . -type f -name "*.py" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|https://api\.vizpilot\.com|https://vizpilot.vizulabs.com|g' {} +
find . -type f -name "*.py" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|https://docs\.vizpilot\.com|https://docs.vizpilot.vizulabs.com|g' {} +

# Update HTML templates
find . -type f -name "*.html" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|https://vizpilot\.com|https://vizpilot.vizulabs.com|g' {} +
find . -type f -name "*.html" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|https://api\.vizpilot\.com|https://vizpilot.vizulabs.com|g' {} +
find . -type f -name "*.html" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|https://docs\.vizpilot\.com|https://docs.vizpilot.vizulabs.com|g' {} +

# Update Markdown files
find . -type f -name "*.md" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|https://vizpilot\.com|https://vizpilot.vizulabs.com|g' {} +
find . -type f -name "*.md" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|https://api\.vizpilot\.com|https://vizpilot.vizulabs.com|g' {} +
find . -type f -name "*.md" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|https://docs\.vizpilot\.com|https://docs.vizpilot.vizulabs.com|g' {} +
find . -type f -name "*.md" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|(https://vizpilot\.com)|(https://vizpilot.vizulabs.com)|g' {} +

# Update JSON files
find . -type f -name "*.json" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|https://vizpilot\.com|https://vizpilot.vizulabs.com|g' {} +
find . -type f -name "*.json" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|https://api\.vizpilot\.com|https://vizpilot.vizulabs.com|g' {} +
find . -type f -name "*.json" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|https://docs\.vizpilot\.com|https://docs.vizpilot.vizulabs.com|g' {} +

# Update shell scripts
find . -type f -name "*.sh" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|https://vizpilot\.com|https://vizpilot.vizulabs.com|g' {} +
find . -type f -name "*.sh" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|https://api\.vizpilot\.com|https://vizpilot.vizulabs.com|g' {} +
find . -type f -name "*.sh" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|https://docs\.vizpilot\.com|https://docs.vizpilot.vizulabs.com|g' {} +

# Update TOML files
find . -type f -name "*.toml" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|https://vizpilot\.com|https://vizpilot.vizulabs.com|g' {} +
find . -type f -name "*.toml" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|https://api\.vizpilot\.com|https://vizpilot.vizulabs.com|g' {} +
find . -type f -name "*.toml" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|https://docs\.vizpilot\.com|https://docs.vizpilot.vizulabs.com|g' {} +

# Update .env files
find . -type f -name ".env*" -not -path "*/venv/*" -not -path "*/.git/*" -exec sed -i '' 's|@vizpilot\.com|@vizpilot.vizulabs.com|g' {} +

echo "✅ URL update complete!"
echo ""
echo "Updated URLs:"
echo "  vizpilot.com → vizpilot.vizulabs.com"
echo "  api.vizpilot.com → vizpilot.vizulabs.com"
echo "  docs.vizpilot.com → docs.vizpilot.vizulabs.com"
echo ""
echo "Please review the changes and commit them."
