#!/bin/bash
# RedBot Setup Script - Quick setup for teammates

set -e

echo "🤖 RedBot Setup Script"
echo "======================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+ first."
    exit 1
fi
echo "✅ Python 3 found"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✅ Dependencies installed"

# Setup .env
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created (edit if needed)"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the app:"
echo "  1. source venv/bin/activate"
echo "  2. streamlit run streamlit.py"
echo ""
echo "Optional: Start ClickHouse (requires Docker):"
echo "  docker-compose up -d"
echo ""
