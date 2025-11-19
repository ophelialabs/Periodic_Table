#!/usr/bin/env python3
"""
Test script to verify the Flask app can be loaded correctly.
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("✓ Loading Flask...")
    from flask import Flask
    print("✓ Flask imported successfully")
    
    print("✓ Loading app factory...")
    from app import create_app
    print("✓ App factory imported successfully")
    
    print("✓ Creating app instance...")
    app = create_app()
    print("✓ App instance created successfully")
    
    print("\n" + "="*50)
    print("🎉 Flask App Setup Successful!")
    print("="*50)
    print("\nTo run the app, use:")
    print("  python run.py")
    print("\nThen open your browser to:")
    print("  http://localhost:5000")
    print("\n" + "="*50)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
