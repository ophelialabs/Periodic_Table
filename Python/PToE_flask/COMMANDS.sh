#!/bin/bash
# Command Reference for Interactive Periodic Table Project

echo "
╔════════════════════════════════════════════════════════════════╗
║  Interactive Periodic Table - Command Reference               ║
║  Location: /Users/jesse/Desktop/Company/Tools/PeriodicTable   ║
║           /Python/PToE_flask                                   ║
╚════════════════════════════════════════════════════════════════╝

📋 TABLE OF CONTENTS:
  1. Quick Start Commands
  2. Development Commands
  3. Verification Commands
  4. Installation Commands
  5. Deployment Commands

═══════════════════════════════════════════════════════════════════

1️⃣  QUICK START COMMANDS
──────────────────────────────────────────────────────────────────

Navigate to project:
  cd /Users/jesse/Desktop/Company/Tools/PeriodicTable/Python/PToE_flask

Run the application:
  python run.py

Using start script (macOS/Linux):
  chmod +x start.sh
  ./start.sh

Using start script (Windows):
  start.bat

Using Flask CLI:
  export FLASK_APP=run.py
  flask run

Access application:
  http://localhost:5001

═══════════════════════════════════════════════════════════════════

2️⃣  DEVELOPMENT COMMANDS
──────────────────────────────────────────────────────────────────

Activate virtual environment:
  source venv/bin/activate  # macOS/Linux
  venv\\Scripts\\activate    # Windows

Run in debug mode:
  python run.py

Run on specific port:
  python run.py  # Edit port in run.py

Run with Flask development server:
  flask run
  flask run --port 5001

Clear Flask cache:
  python -c \"from app import create_app; app = create_app(); app.config['CACHE_TYPE'] = 'simple'\"

═══════════════════════════════════════════════════════════════════

3️⃣  VERIFICATION COMMANDS
──────────────────────────────────────────────────────────────────

Quick setup test:
  python test_setup.py

Comprehensive verification:
  python verify_setup.py

Check Python version:
  python --version

Check installed packages:
  pip list

Check specific package:
  pip show flask

View app structure:
  ls -la src/app/

Check if periodic table data exists:
  ls -lh src/lib/Periodic-Table-JSON/PeriodicTableJSON.json

═══════════════════════════════════════════════════════════════════

4️⃣  INSTALLATION COMMANDS
──────────────────────────────────────────────────────────────────

Install all dependencies:
  pip install -r requirements.txt

Install specific packages:
  pip install Flask==2.3.3
  pip install flask-bootstrap==3.3.7.1
  pip install flask-moment==1.0.5
  pip install flask-caching==2.0.2
  pip install flask-wtf==1.1.1
  pip install python-dotenv==1.0.0

Upgrade pip:
  pip install --upgrade pip

Reinstall all dependencies (clean):
  pip uninstall -r requirements.txt -y
  pip install -r requirements.txt

═══════════════════════════════════════════════════════════════════

5️⃣  DEPLOYMENT COMMANDS
──────────────────────────────────────────────────────────────────

Install production server (Gunicorn):
  pip install gunicorn

Run with Gunicorn:
  gunicorn -w 4 -b 0.0.0.0:8000 run:app

Run with specified workers:
  gunicorn -w 4 -b 127.0.0.1:5000 run:app

Generate requirements file:
  pip freeze > requirements.txt

═══════════════════════════════════════════════════════════════════

🌐 API ENDPOINTS
──────────────────────────────────────────────────────────────────

Get all elements:
  curl http://localhost:5001/api/elements

Get element by atomic number (example: Hydrogen):
  curl http://localhost:5001/api/element/1

Get element by symbol (example: H):
  curl http://localhost:5001/api/element/H

═══════════════════════════════════════════════════════════════════

📂 FILE LOCATIONS
──────────────────────────────────────────────────────────────────

Main application:
  /Users/jesse/Desktop/Company/Tools/PeriodicTable/Python/PToE_flask/run.py

Configuration:
  /Users/jesse/Desktop/Company/Tools/PeriodicTable/Python/PToE_flask/config.py

Templates:
  /Users/jesse/Desktop/Company/Tools/PeriodicTable/Python/PToE_flask/src/app/templates/

Periodic table data:
  /Users/jesse/Desktop/Company/Tools/PeriodicTable/Python/PToE_flask/src/lib/Periodic-Table-JSON/PeriodicTableJSON.json

═══════════════════════════════════════════════════════════════════

🆘 TROUBLESHOOTING COMMANDS
──────────────────────────────────────────────────────────────────

Check if port 5000 is in use:
  lsof -i :5000           # macOS/Linux
  netstat -ano | findstr :5000  # Windows

Kill process on port 5000:
  kill -9 <PID>          # macOS/Linux
  taskkill /PID <PID> /F # Windows

Check Flask app can load:
  python -c \"from app import create_app; print('OK')\"

Verify requirements:
  python -m pip check

Check for syntax errors:
  python -m py_compile src/app/*.py

View error logs:
  # Check terminal output where you ran 'python run.py'

View Python path:
  python -c \"import sys; print(sys.path)\"

═══════════════════════════════════════════════════════════════════

📚 DOCUMENTATION COMMANDS
──────────────────────────────────────────────────────────────────

View quick start:
  cat QUICK_START.md

View implementation details:
  cat IMPLEMENTATION.md

View app documentation:
  cat README_APP.md

View project delivery summary:
  cat PROJECT_DELIVERY.md

═══════════════════════════════════════════════════════════════════

💡 USEFUL SHORTCUTS
──────────────────────────────────────────────────────────────────

Create Python 3 virtual environment:
  python3 -m venv venv

Activate venv and install requirements:
  source venv/bin/activate && pip install -r requirements.txt

One-liner to run app:
  cd /Users/jesse/Desktop/Company/Tools/PeriodicTable/Python/PToE_flask && python run.py

═══════════════════════════════════════════════════════════════════

🔗 IMPORTANT LINKS
──────────────────────────────────────────────────────────────────

Local Application:
  http://localhost:5000

All Elements API:
  http://localhost:5000/api/elements

Element Details API:
  http://localhost:5000/api/element/1

Browser Developer Tools:
  F12 or Right-click → Inspect → Console tab

═══════════════════════════════════════════════════════════════════

✅ VERIFICATION CHECKLIST
──────────────────────────────────────────────────────────────────

Run these commands to verify everything is working:

1. python test_setup.py              # Should show ✅ all checks
2. python verify_setup.py            # Should show all 118 elements
3. curl http://localhost:5000/       # After running: python run.py
4. Open http://localhost:5000 in browser

═══════════════════════════════════════════════════════════════════

🎯 QUICK REFERENCE
──────────────────────────────────────────────────────────────────

Start app:        python run.py
Stop app:         Ctrl+C
Open browser:     http://localhost:5000
View data API:    http://localhost:5000/api/elements
Check setup:      python verify_setup.py

═══════════════════════════════════════════════════════════════════

Need help? Check:
  • QUICK_START.md for fast setup
  • README_APP.md for features
  • IMPLEMENTATION.md for technical details
  • PROJECT_DELIVERY.md for full summary

═══════════════════════════════════════════════════════════════════
"
