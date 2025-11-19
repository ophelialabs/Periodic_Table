# Quick Start Guide - Interactive Periodic Table

## 🚀 Getting Started

### Step 1: Verify Setup
```bash
cd /Users/jesse/Desktop/Company/Tools/PeriodicTable/Python/PToE_flask
python test_setup.py
```

### Step 2: Run the Application
```bash
python run.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5001
```

### Step 3: Open in Browser
Visit: **http://localhost:5001**

---

## 📋 What You'll See

1. **Periodic Table Grid** - All 118 elements color-coded by category
2. **Search Bar** - Find elements by name, symbol, or atomic number
3. **Interactive Elements** - Click any element to view details

---

## 🧬 Element Details Modal Includes

✅ **Basic Properties**
- Atomic number and mass
- Category and phase
- Electron configuration
- Electronegativity
- Discovery information

✅ **3D Visualizations**
- Bohr Model (2D)
- Bohr Model (3D) - Interactive
- de Broglie Wave visualization
- Schrödinger probability density

✅ **Additional Content**
- Element image
- Spectral bands
- Wikipedia summary
- Source link

---

## 🎨 Element Categories (Color Coded)

🔴 **Red** - Alkali Metals
🟡 **Yellow** - Alkaline Earth Metals
🔵 **Blue** - Transition Metals
🟣 **Purple** - Lanthanides & Actinides
🟢 **Green** - Nonmetals & Halogens
🟦 **Cyan** - Noble Gases
🟪 **Magenta** - Metalloids & Post-Transition Metals

---

## 🔧 Troubleshooting

### Port Already in Use
If you get "Address already in use", edit `run.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```
to:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Dependencies Missing
Install them manually:
```bash
pip install Flask flask-bootstrap flask-moment flask-caching flask-wtf python-dotenv
```

### Import Errors
Make sure you're in the correct directory:
```bash
cd /Users/jesse/Desktop/Company/Tools/PeriodicTable/Python/PToE_flask
```

---

## 📚 API Endpoints

You can access the data programmatically:

- **All Elements**: `http://localhost:5000/api/elements`
- **By Atomic Number**: `http://localhost:5000/api/element/1` (Hydrogen)
- **By Symbol**: `http://localhost:5000/api/element/H`

---

## 🎓 Learning Features

- **Interactive Exploration** - Click elements to learn
- **Accurate Data** - From Wikipedia and scientific sources
- **Visual Learning** - See electron orbitals and probability clouds
- **3D Models** - Interact with realistic atomic structures

---

## 💡 Tips

1. **Search** works in real-time as you type
2. **Hover** over elements to see them highlight
3. **Click** to view comprehensive details
4. **3D Models** can be rotated with your mouse/touch
5. **Spectral Bands** show unique light signatures

---

## 📞 Support

If something isn't working:

1. Check the browser console (F12 → Console tab)
2. Look at the terminal output where you ran `python run.py`
3. Try a different browser
4. Make sure WebGL is enabled for 3D models

---

Enjoy exploring the elements! ⚛️
