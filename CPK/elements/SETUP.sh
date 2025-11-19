#!/bin/bash

# Interactive 3D Periodic Table - Quick Setup Guide

echo "🧪 Setting up Interactive 3D Periodic Table..."
echo ""

# Check Node.js
echo "✓ Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+."
    exit 1
fi
echo "✓ Node.js $(node -v) found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"
echo ""

# Check for .env.local
echo "🔑 Setting up environment variables..."
if [ ! -f ".env.local" ]; then
    echo "⚠️  .env.local not found. Creating template..."
    cat > .env.local << 'EOF'
# OpenAI API Key (Required)
OPENAI_API_KEY=sk_test_your_key_here

# CopilotKit Configuration
NEXT_PUBLIC_COPILOT_KIT_PUBLIC_API_KEY=ck_pub_336d5ab8498da237aaccefc683ed17e7

# Google Maps API Key (Optional)
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=AIzaSyDK7BXtZz4ypjq0yr-7FrrAcl3oCoPpxK8
EOF
    echo "✓ Template created. Please update .env.local with your API keys"
else
    echo "✓ .env.local found"
fi
echo ""

# Install Python dependencies for agent
echo "🐍 Setting up Python agent environment..."
if command -v python3 &> /dev/null; then
    cd agent
    python3 -m venv venv 2>/dev/null || true
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    fi
    pip install -r requirements.txt > /dev/null 2>&1
    cd ..
    echo "✓ Python agent dependencies installed"
else
    echo "⚠️  Python 3 not found. Agent functionality may be limited."
fi
echo ""

# Summary
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Update .env.local with your API keys:"
echo "   - Get OpenAI API key from: https://platform.openai.com/api-keys"
echo "   - CopilotKit key provided (already filled)"
echo "   - Google Maps key provided (optional)"
echo ""
echo "2. Start development server:"
echo "   npm run dev"
echo ""
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "4. Try these commands with the AI assistant:"
echo "   - 'Show me all transition metals'"
echo "   - 'Create a scatter plot of atomic mass'"
echo "   - 'Tell me about Carbon'"
echo ""
echo "📚 For more info, see PERIODIC_TABLE_README.md"
echo ""
