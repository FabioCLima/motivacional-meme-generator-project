#!/bin/bash
# Build script for the Motivacional Meme Generator package

set -e

echo "🔨 Building Motivacional Meme Generator Package"
echo "================================================"

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/
rm -rf src/*.egg-info/

# Install build dependencies
echo "📦 Installing build dependencies..."
pip install --upgrade build twine

# Build the package
echo "🏗️ Building package..."
python -m build

# Check the package
echo "🔍 Checking package..."
python -m twine check dist/*

echo "✅ Package built successfully!"
echo ""
echo "📁 Built files:"
ls -la dist/
echo ""
echo "📋 Next steps:"
echo "1. Test install: pip install dist/*.whl"
echo "2. Upload to PyPI: python -m twine upload dist/*"
echo "3. Or install locally: pip install -e ."
