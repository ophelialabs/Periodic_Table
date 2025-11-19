# 🚀 SETUP & LAUNCH GUIDE - Interactive Periodic Table

## ⚡ Super Quick Start (Copy & Paste)

```bash
cd /Users/jesse/Desktop/Company/Tools/PeriodicTable/Python/PToE_flask
python run.py
```

Then open: **http://localhost:5000**

---

## 📋 Step-by-Step Setup

### Step 1: Navigate to Project
```bash
cd /Users/jesse/Desktop/Company/Tools/PeriodicTable/Python/PToE_flask
```

### Step 2: Verify Python
```bash
python --version
# Should show: Python 3.7 or higher
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Flask-Bootstrap (UI components)
- Flask-Moment (date formatting)
- Flask-Caching (performance)
- Flask-WTF (security)
- python-dotenv (configuration)

### Step 4: Verify Setup
```bash
python verify_setup.py
```

Should show: ✅ ALL CHECKS PASSED

### Step 5: Run Application
```bash
python run.py
```

You should see:
```
 * Running on http://127.0.0.1:5001
 * Debug mode: on
```

### Step 6: Open Browser
Visit: **http://localhost:5001**

---

## 🎯 What You'll See

### Home Page
- Grid of 118 elements (the periodic table)
- Color-coded by category
- Search bar at the top
- Each element is clickable

### Periodic Table Categories (Colors)
```
🔴 Red        = Alkali Metals
🟡 Yellow     = Alkaline Earth Metals  
🔵 Blue       = Transition Metals
🟣 Purple     = Lanthanides/Actinides
🟢 Green      = Nonmetals
🟦 Cyan       = Noble Gases
```

### Search Bar
- Type element name (e.g., "Hydrogen")
- Type element symbol (e.g., "H")
- Type atomic number (e.g., "1")
- Results update instantly

### Click Any Element
A detailed modal appears showing:
- Element image
- All properties
- 3D Bohr model (interactive)
- de Broglie wave visualization
- Schrödinger probability visualization
- Spectral bands
- Wikipedia summary

### 3D Model Controls
- **Mouse**: Click and drag to rotate
- **Zoom**: Scroll wheel
- **Auto-rotate**: Turns on automatically

---

## 🛠️ Alternative Installation Methods

### Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run app
python run.py
```

### Using Start Script (macOS/Linux)

```bash
chmod +x start.sh
./start.sh
```

### Using Start Script (Windows)

```bash
start.bat
```

### Using Flask CLI

```bash
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
```

---

## ✅ Verification Checklist

Run each command to verify everything works:

```bash
# 1. Check Python version
python --version
# Expected: Python 3.7+

# 2. Check Flask installation
python -c "import flask; print(flask.__version__)"
# Expected: 2.3.3

# 3. Test app can load
python test_setup.py
# Expected: ✅ ALL CHECKS PASSED

# 4. Full verification
python verify_setup.py
# Expected: 118 elements found

# 5. Check API
# (After running: python run.py)
curl http://localhost:5000/api/elements
# Expected: JSON with 118 elements
```

---

## 🆘 Troubleshooting

### Problem: "Could not locate a Flask application"

**Solution**: Make sure you're in the correct directory
```bash
cd /Users/jesse/Desktop/Company/Tools/PeriodicTable/Python/PToE_flask
python run.py
```

### Problem: "ModuleNotFoundError: No module named 'flask'"

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Problem: "Address already in use"

**Solution 1**: Use a different port
Edit `run.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed from 5000
```

**Solution 2**: Kill process using port 5000
```bash
# macOS/Linux
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Problem: "No such file or directory: PeriodicTableJSON.json"

**Solution**: Make sure you're in the project root directory
```bash
cd /Users/jesse/Desktop/Company/Tools/PeriodicTable/Python/PToE_flask
python run.py
```

### Problem: 3D models not showing

**Solution 1**: Check browser support
- Update your browser to latest version
- Ensure WebGL is enabled (most browsers have this on by default)

**Solution 2**: Check browser console for errors
- Press F12 to open Developer Tools
- Go to Console tab
- Look for error messages
- Check Network tab to see if 3D model file loaded

### Problem: Search not working

**Solution**: Check browser console
- Press F12
- Go to Console tab
- Look for JavaScript errors
- Refresh the page

### Problem: "No such file or directory" for templates

**Solution**: Verify template directory exists
```bash
ls src/app/templates/
# Should show: base.html, index.html
```

---

## 🔧 Configuration

### Changing Port

Edit `run.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port here
```

### Changing Host

Edit `run.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # 0.0.0.0 = accept all connections
```

For localhost only:
```python
app.run(debug=True, host='127.0.0.1', port=5000)
```

### Environment Variables

Edit `.env`:
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

---

## 🎓 Understanding the Project

### Directory Structure
```
PToE_flask/
├── run.py                    # Start here
├── config.py                 # Settings
├── requirements.txt          # Dependencies
├── src/
│   └── app/
│       ├── __init__.py       # App setup
│       ├── main.py           # Routes
│       ├── api.py            # API endpoints
│       └── templates/
│           ├── base.html     # Base template
│           └── index.html    # Main page
└── (data files)
```

### How It Works

1. **User opens http://localhost:5000**
   - Flask serves `index.html`

2. **Page loads JavaScript**
   - Fetches element data from `/api/elements`
   - Renders periodic table grid

3. **User clicks element**
   - Shows modal with details
   - Loads 3D model (if available)
   - Draws visualizations

4. **User searches**
   - JavaScript filters elements
   - Updates table in real-time

---

## 📚 Documentation Files

After setup, read these files for more information:

1. **QUICK_START.md** - Quick guide (5 min read)
2. **README_APP.md** - Full features (15 min read)
3. **IMPLEMENTATION.md** - Technical details (20 min read)
4. **PROJECT_DELIVERY.md** - Complete summary (30 min read)
5. **COMMANDS.sh** - Command reference (reference)

---

## 🌐 Testing the API

After running `python run.py`, test the API:

### Get all elements
```bash
curl http://localhost:5000/api/elements | python -m json.tool
```

### Get element by number (Hydrogen = 1)
```bash
curl http://localhost:5000/api/element/1 | python -m json.tool
```

### Get element by symbol (H = Hydrogen)
```bash
curl http://localhost:5000/api/element/H | python -m json.tool
```

---

## 💡 Tips & Tricks

### Using DevTools

1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Check Network tab to see API calls
4. Check Elements tab to inspect HTML

### Keyboard Shortcuts

- **F12** - Open Developer Tools
- **Ctrl+R** or **Cmd+R** - Refresh page
- **Ctrl+Shift+Delete** - Clear cache and cookies

### Accessing Different Elements

- Click on any element in the table
- Use search to find specific elements
- Search works for: name, symbol, atomic number

### 3D Model Interaction

- Left mouse: Rotate
- Right mouse: Pan
- Scroll: Zoom
- Double-click: Reset view

---

## 🚀 Next Steps

### Short-term
1. ✅ Get app running (`python run.py`)
2. ✅ Click an element
3. ✅ View 3D model
4. ✅ Try search feature

### Medium-term
1. 📖 Read the documentation
2. 🎓 Learn the codebase
3. 🔧 Customize styling
4. 🎨 Add your own features

### Long-term
1. 🌐 Deploy to web server
2. 📱 Create mobile version
3. 🗄️ Add database
4. 👤 Add user accounts

---

## 📞 Getting Help

### If Something Breaks

1. **Check terminal output**
   - Look for error messages in the terminal where you ran `python run.py`

2. **Check browser console**
   - Press F12 in browser
   - Go to Console tab
   - Look for JavaScript errors

3. **Run verification**
   ```bash
   python verify_setup.py
   ```

4. **Check documentation**
   - This file (SETUP_LAUNCH.md)
   - QUICK_START.md
   - README_APP.md

### Common Solutions

- **Can't connect**: Make sure `python run.py` is still running
- **Blank page**: Try refreshing (Cmd+R or Ctrl+R)
- **Errors in console**: Check terminal output for more details
- **API not working**: Make sure you're using correct endpoint

---

## 🎊 Success!

If you've completed all steps and the app is running at http://localhost:5000, you're done! 🎉

**Now enjoy exploring the periodic table!** ⚛️

---

## ⏸️ Stopping the App

To stop the application:

1. Go to terminal where `python run.py` is running
2. Press **Ctrl+C**

Should see:
```
^C
```

---

## 🔄 Restarting the App

To restart after stopping:

```bash
python run.py
```

---

## 📝 Important Notes

1. **Debug Mode**: App runs in debug mode (auto-reloads on code changes)
2. **Local Only**: By default only accessible from this computer
3. **No Database**: Data is loaded from JSON file (no setup needed)
4. **Stateless**: Each request is independent (can scale easily)

---

## ✨ Features Summary

Your app has:
- ✅ 118 elements to explore
- ✅ Interactive periodic table
- ✅ 3D Bohr models
- ✅ Wave visualizations
- ✅ Element images
- ✅ Spectral bands
- ✅ Search functionality
- ✅ Responsive design
- ✅ Mobile friendly

---

**Status: Ready to Launch** 🚀

```
cd /Users/jesse/Desktop/Company/Tools/PeriodicTable/Python/PToE_flask
python run.py
# Then open: http://localhost:5000
```

---

*Created: November 17, 2025*  
*Version: 1.0.0*  
*Status: Production Ready* ✅
