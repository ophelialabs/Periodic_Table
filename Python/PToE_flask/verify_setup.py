#!/usr/bin/env python3
"""
Complete setup verification and installation script
"""
import sys
import os
import json

print("\n" + "="*60)
print("🧪 INTERACTIVE PERIODIC TABLE - SETUP VERIFICATION")
print("="*60 + "\n")

checks_passed = 0
checks_total = 0

def check(name, condition, error_msg=""):
    global checks_passed, checks_total
    checks_total += 1
    if condition:
        print(f"✅ {name}")
        checks_passed += 1
        return True
    else:
        print(f"❌ {name}")
        if error_msg:
            print(f"   └─ {error_msg}")
        return False

# Python version
check("Python Version", sys.version_info >= (3, 7), 
      f"Found Python {sys.version_info.major}.{sys.version_info.minor}, need 3.7+")

# Flask
try:
    import flask
    check("Flask", True)
except ImportError:
    check("Flask", False, "Run: pip install Flask==2.3.3")

# Flask extensions
try:
    import flask_bootstrap
    check("Flask-Bootstrap", True)
except ImportError:
    check("Flask-Bootstrap", False, "Run: pip install flask-bootstrap==3.3.7.1")

try:
    import flask_moment
    check("Flask-Moment", True)
except ImportError:
    check("Flask-Moment", False, "Run: pip install flask-moment==1.0.5")

try:
    import flask_caching
    check("Flask-Caching", True)
except ImportError:
    check("Flask-Caching", False, "Run: pip install flask-caching==2.0.2")

try:
    import flask_wtf
    check("Flask-WTF", True)
except ImportError:
    check("Flask-WTF", False, "Run: pip install flask-wtf==1.1.1")

try:
    import dotenv
    check("python-dotenv", True)
except ImportError:
    check("python-dotenv", False, "Run: pip install python-dotenv==1.0.0")

# File structure
check("config.py exists", os.path.exists("config.py"))
check("run.py exists", os.path.exists("run.py"))
check(".env exists", os.path.exists(".env"))

# App structure
check("app/__init__.py exists", os.path.exists("src/app/__init__.py"))
check("app/main.py exists", os.path.exists("src/app/main.py"))
check("app/api.py exists", os.path.exists("src/app/api.py"))
check("templates/base.html exists", os.path.exists("src/app/templates/base.html"))
check("templates/index.html exists", os.path.exists("src/app/templates/index.html"))

# Data files
data_file = "src/lib/Periodic-Table-JSON/PeriodicTableJSON.json"
data_exists = os.path.exists(data_file)
check("Periodic table data exists", data_exists)

if data_exists:
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
            num_elements = len(data.get('elements', []))
            check(f"Valid JSON with {num_elements} elements", num_elements == 118)
    except:
        check("Valid JSON data", False, "Data file is corrupted")

# Summary
print("\n" + "="*60)
print(f"RESULT: {checks_passed}/{checks_total} checks passed")
print("="*60 + "\n")

if checks_passed == checks_total:
    print("🎉 ALL CHECKS PASSED! Ready to run:\n")
    print("   python run.py")
    print("\n   Then open: http://localhost:5000\n")
    sys.exit(0)
elif checks_passed >= checks_total - 2:
    print("⚠️  MINOR ISSUES - Most checks passed")
    print("   Try running: pip install -r requirements.txt\n")
    sys.exit(1)
else:
    print("❌ SETUP INCOMPLETE")
    print("   Please install all dependencies:\n")
    print("   pip install -r requirements.txt\n")
    sys.exit(1)
