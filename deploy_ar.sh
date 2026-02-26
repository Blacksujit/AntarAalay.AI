#!/bin/bash

echo "🚀 AntarAalay AR - Quick Deployment Script"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required but not installed."
    exit 1
fi

echo "✅ Python3 found"

# Create deployment directory
DEPLOY_DIR="antaralay-ar-deploy"
echo "📁 Creating deployment directory: $DEPLOY_DIR"

mkdir -p $DEPLOY_DIR

# Copy files
echo "📋 Copying AR viewer files..."
cp AR_DEPLOY/index.html $DEPLOY_DIR/
cp AR_DEPLOY/package.json $DEPLOY_DIR/

# Create production version
echo "🔧 Creating production AR viewer..."
cp AR_VIEWER_PRODUCTION.html $DEPLOY_DIR/production.html

cd $DEPLOY_DIR

echo "🌐 Starting local server on http://localhost:8080"
echo "📱 Test AR at: http://localhost:8080/production.html"
echo "🔄 Press Ctrl+C to stop server"

# Start local server
python3 -m http.server 8080
