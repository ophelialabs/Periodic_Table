# 🔧 PORT CONFIGURATION GUIDE

## Port Issue on macOS

### Why Port 5000 is Problematic

On macOS Monterey (12.0) and later, **port 5000 is reserved by the AirPlay Receiver service**. This prevents Flask from using port 5000 by default.

**Solution:** The app now uses **port 5001** by default, which avoids this conflict.

---

## 🚀 Quick Fix - Use Port 5001 (Recommended)

The application now automatically uses **port 5001** by default.

```bash
python run.py
# Opens on: http://localhost:5001
```

No configuration needed!

---

## ⚙️ Alternative: Disable AirPlay Receiver (Optional)

If you want to use port 5000 specifically, you can disable the AirPlay Receiver service:

### macOS Steps:
1. **Open System Preferences**
2. Go to **System Preferences** → **Sharing**
3. Find **AirPlay Receiver** in the left sidebar
4. **Uncheck** the checkbox next to "AirPlay Receiver"
5. Restart your computer (or just close System Preferences)

Now port 5000 will be available.

### To Use Port 5000:
```bash
# Set PORT environment variable
export PORT=5000
python run.py
# Opens on: http://localhost:5000
```

---

## 🎯 Custom Port Configuration

### Temporarily Use Different Port
```bash
export PORT=8000
python run.py
# Opens on: http://localhost:8000
```

### Change Default Port in Code
Edit `run.py` and change:
```python
port = int(os.environ.get('PORT', 5001))  # Change 5001 to desired port
```

---

## 🔍 Troubleshooting Port Issues

### Check What's Using a Port
```bash
# macOS/Linux
lsof -i :5001

# Windows
netstat -ano | findstr :5001
```

### Kill Process Using Port (macOS/Linux)
```bash
# Find the PID
lsof -i :5001

# Kill it
kill -9 <PID>
```

### Kill Process Using Port (Windows)
```bash
# Find the PID
netstat -ano | findstr :5001

# Kill it
taskkill /PID <PID> /F
```

---

## 📋 Quick Reference

| Scenario | Command |
|----------|---------|
| Default (port 5001) | `python run.py` |
| Use port 5000 | `export PORT=5000 && python run.py` |
| Use port 8000 | `export PORT=8000 && python run.py` |
| Check port usage | `lsof -i :5001` |
| Kill port process | `kill -9 <PID>` |

---

## ✅ Verification

After starting the app:
```bash
# Check the terminal output
# Should see: "Running on http://127.0.0.1:PORT"

# Test API endpoint
curl http://localhost:5001/api/elements
# Should return JSON with 118 elements
```

---

## 📌 Summary

✅ **Default:** Port 5001 (no conflicts)  
✅ **Alternative:** Port 5000 (disable AirPlay first)  
✅ **Custom:** Any port via PORT environment variable  

**Recommended:** Use port 5001 (already configured)

---

For more help, see: `SETUP_LAUNCH.md` Troubleshooting section
