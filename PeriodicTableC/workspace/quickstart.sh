#!/bin/bash
# Quick Start Script for Periodic Table Quantum Project

echo "🔬 Interactive Periodic Table - Quick Start"
echo "==========================================="
echo ""

# Check if dotnet is installed
if ! command -v dotnet &> /dev/null; then
    echo "❌ .NET SDK not found. Please install .NET 8.0 from https://dotnet.microsoft.com/download"
    exit 1
fi

echo "✅ .NET SDK found: $(dotnet --version)"
echo ""

# Navigate to workspace
cd "$(dirname "$0")"

echo "📦 Restoring NuGet packages..."
dotnet restore

if [ $? -ne 0 ]; then
    echo "❌ Package restore failed"
    exit 1
fi

echo "✅ Packages restored"
echo ""

echo "🔨 Building project..."
dotnet build

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo "✅ Build successful"
echo ""

echo "🚀 Starting development server..."
echo "📱 Open browser to: https://localhost:5001/periodic-table"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

dotnet watch run --project PeriodicTableWeb/PeriodicTableWeb.csproj
