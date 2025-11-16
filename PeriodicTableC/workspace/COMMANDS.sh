#!/bin/bash
# ESSENTIAL COMMANDS - Save this for quick reference

# ========================================
# 🚀 START APPLICATION
# ========================================

# Quick start (recommended)
cd /Users/jesse/periodictable/workspace && ./quickstart.sh

# Manual start with watch mode (auto-reload)
cd /Users/jesse/periodictable/workspace && dotnet watch run --project PeriodicTableWeb/PeriodicTableWeb.csproj

# Run once
cd /Users/jesse/periodictable/workspace && dotnet run --project PeriodicTableWeb/PeriodicTableWeb.csproj

# ========================================
# 🔨 BUILD COMMANDS
# ========================================

# Build entire solution
dotnet build

# Build specific project
dotnet build PeriodicTableQuantum/PeriodicTableQuantum.csproj

# Clean build
dotnet clean && dotnet build

# Release build
dotnet build -c Release

# ========================================
# 📦 PACKAGE MANAGEMENT
# ========================================

# Restore NuGet packages
dotnet restore

# List installed packages
dotnet list package

# Add new package
dotnet add PeriodicTableWeb.csproj package PackageName

# ========================================
# 🧪 TESTING & DEBUGGING
# ========================================

# Run with Debug configuration
dotnet run --configuration Debug

# Check Q# compilation
dotnet build PeriodicTableQuantum/

# Publish for deployment
dotnet publish -c Release -o ./publish

# ========================================
# 🔧 DEVELOPMENT TASKS
# ========================================

# Format code
dotnet format

# Check code quality
dotnet tool list

# Run unit tests (when added)
dotnet test

# ========================================
# 📋 PROJECT INFO
# ========================================

# List solution structure
dotnet sln list

# Show .NET version
dotnet --version

# Check Q# version
dotnet qsharp --version

# ========================================
# 🌐 BROWSER ACCESS
# ========================================

# Development URL
https://localhost:5001/periodic-table

# ========================================
# 📚 DOCUMENTATION FILES
# ========================================

# Main documentation
open README.md

# Quick reference
open QUICK_REFERENCE.md

# Architecture overview
open SOLUTION_OVERVIEW.md

# Complete file index
open PROJECT_INDEX.md

# Welcome guide
open WELCOME.md

# ========================================
# 🎯 VS CODE SHORTCUTS
# ========================================

# Open Command Palette
Cmd+Shift+P

# Run Task
Cmd+Shift+P -> Run Task

# Start Debugging
F5

# Add Breakpoint
Cmd+K Cmd+B

# View Terminal
Ctrl+`

# ========================================
# 🔍 TROUBLESHOOTING
# ========================================

# Port already in use (find process)
lsof -i :5001

# Kill process using port
kill -9 <PID>

# Use different port
dotnet run --project PeriodicTableWeb/PeriodicTableWeb.csproj -- --urls "https://localhost:5002"

# View logs
tail -f logs.txt

# Clear build cache
rm -rf bin obj

# ========================================
# 📊 PERFORMANCE & DIAGNOSTICS
# ========================================

# Profile application
dotnet trace collect -p <PID>

# Memory dump
dotnet dump collect -p <PID>

# Event trace
dotnet trace collect --providers=Microsoft-DotNETRuntime

# ========================================
# 🚀 DEPLOYMENT
# ========================================

# Build for production
dotnet build -c Release

# Publish to folder
dotnet publish -c Release -o ./publish

# Deploy to Azure App Service
dotnet publish -c Release && az webapp up --name periodic-table-app

# ========================================
# 📝 TIPS & TRICKS
# ========================================

# Create new Razor component
# File: Components/Pages/NewComponent.razor
# Add: @page "/new-route"

# Create new C# service
# File: Services/NewService.cs
# Class: public class NewService { }

# Add to DI in Program.cs
# Line: builder.Services.AddTransient<NewService>();

# Create new Q# operation
# File: src/NewOperation.qs
# Operation: operation NewOp(input : Int) : Double[] { ... }

# ========================================
# 🔗 USEFUL LINKS
# ========================================

# Q# Documentation
https://learn.microsoft.com/quantum/

# Blazor Documentation
https://learn.microsoft.com/aspnet/core/blazor/

# Azure Quantum
https://azure.microsoft.com/services/quantum/

# .NET Documentation
https://learn.microsoft.com/dotnet/

# ========================================
# 📞 HELP & SUPPORT
# ========================================

# Get help with dotnet command
dotnet help <command>

# Check project structure
ls -la

# View file contents
cat filename.ext

# Edit file with nano
nano filename.ext

# ========================================

# To run any command:
# 1. Copy the command line (don't include #)
# 2. Paste into Terminal
# 3. Press Enter
# 4. Wait for completion

# Example:
# $ cd /Users/jesse/periodictable/workspace
# $ dotnet build
# (build process runs)
# $ ✓ Successfully built

# ========================================
