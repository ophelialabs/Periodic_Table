#!/bin/bash
# Start script for the Interactive Periodic Table application

cd "$(dirname "$0")"

echo "=========================================="
echo "⚛️  Interactive Periodic Table of Elements"
echo "=========================================="
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate venv
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
echo "✓ Checking dependencies..."
pip list | grep -q Flask
if [ $? -ne 0 ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "=========================================="
echo "🚀 Starting Flask Application"
echo "=========================================="
echo ""
echo "🌐 Open your browser to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the app
python run.py
