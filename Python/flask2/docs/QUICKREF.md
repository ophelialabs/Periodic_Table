# Quick Reference - Periodic Table Explorer

## 🚀 Getting Started

### Start the Server
```bash
cd /Users/jesse/Desktop/Company/Tools/PeriodicTable/Python/flask2
python run_server.py
```

Access: http://127.0.0.1:5000

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
flask2/
├── README.md                    # Project overview (UPDATE)
├── PHASE1_SUMMARY.md           # Completion status
├── PHASE3_GUIDE.md             # Implementation guide
├── requirements.txt             # Dependencies
├── run_server.py               # Server launcher
├── generate_analysis.py        # Report generator
│
├── src/
│   ├── element_database.py     # 119 elements, search/filter
│   ├── analysis_report.py      # Stats, CSV export, visualization data
│   ├── app/
│   │   ├── __init__.py         # Flask app, routes
│   │   ├── templates/
│   │   │   ├── base.html       # Base layout
│   │   │   └── main/index.html # Main page
│   │   └── static/
│   │       ├── css/            # Responsive styles
│   │       └── js/             # 7 modules
│   ├── components/             # [Future]
│   └── lib/Periodic-Table-JSON/# Element data
│
└── agent/agent.py              # Quantum agent [Phase 2]
```

## 🎨 Key Features

| Feature | Status | File |
|---------|--------|------|
| Periodic Table UI | ✅ Complete | `periodic-table.js` |
| Search/Filter | ✅ Complete | `search.js` |
| Element Details | ✅ Complete | `element-details.js` |
| Responsive Design | ✅ Complete | `responsive.css` |
| Panel Resizing | ✅ Complete | `resizable.js` |
| Visualization Framework | ✅ Ready | `visualizations.js` |
| 3D Visualization | 🔄 Phase 3 | `3d-renderer.js` [TODO] |
| Chart Visualization | 🔄 Phase 3 | `chart-renderer.js` [TODO] |
| Element Comparison | 🔄 Phase 3 | `element-details.js` |
| PDF Reports | 🔄 Phase 4 | `analysis_report.py` |

## 🔧 Development Tasks

### To Add a New Visualization:
1. Update `visualizations.js` - replace placeholder function
2. Add data generation in `analysis_report.py` if needed
3. Add API endpoint in `src/app/__init__.py` if needed
4. Test the visualization modal

Example:
```javascript
// In visualizations.js
function generatePropertyHeatmapViz(element) {
  // Return chart HTML or create container for Three.js
  return `<canvas id="heatmap"></canvas>`;
}
```

### To Add a New Route:
1. Edit `src/app/__init__.py` - add @app.route
2. Use `app.db` for database queries
3. Use `app.analysis` for data generation
4. Return jsonify(data) for JSON responses

Example:
```python
@app.route('/api/element/<symbol>')
def get_element(symbol):
    element = app.db.get_element_by_symbol(symbol)
    if element:
        return jsonify(element)
    return jsonify({'error': 'Not found'}), 404
```

### To Update Styles:
- Global styles: `static/css/style.css`
- Periodic table: `static/css/periodic-table.css`
- Responsive: `static/css/responsive.css`

Use these color variables:
- Primary: `#667eea` (purple)
- Secondary: `#764ba2` (dark purple)
- Background: `#0f0f0f` (dark)
- Panel bg: `#1a1a1a`
- Border: `#333`

## 📊 Data Access

### Get All Elements
```javascript
// Already loaded in frontend
const element = elementsData.find(e => e.symbol === 'H');
```

### Backend Database
```python
from src.element_database import ElementDatabase
db = ElementDatabase()

# Search
elements = db.search('hydrogen')  # By name
elements = db.get_elements_by_category('nonmetal')
element = db.get_element_by_symbol('H')

# Statistics
count = db.get_element_count()  # 119
categories = db.get_categories()
min_val, max_val = db.get_property_range('atomic_mass')
```

## 🐛 Debugging

### Check Server Logs
Server logs show all HTTP requests and errors
```
127.0.0.1 - - [time] "GET / HTTP/1.1" 200
```

### Browser Console
- `console.log()` for debugging JavaScript
- Check Network tab for API calls
- Check Elements tab for DOM inspection

### Common Issues

| Issue | Solution |
|-------|----------|
| Elements not showing | Check `elementsData` in console |
| Search not working | Check `search.js` event listeners |
| Styles broken | Clear browser cache (Cmd+Shift+R) |
| API 404 error | Check route spelling in `__init__.py` |
| Slow performance | Check file sizes in Network tab |

## 📈 Performance Tips

- Elements cached in memory (~50KB)
- Search runs client-side for speed
- CSS animations use GPU acceleration
- Lazy load visualizations when clicked
- Use pagination for large datasets (if added)

## 🧪 Testing

### Test Element Search
```javascript
// In browser console
performSearch();  // Should filter elements
```

### Test Visualization
```javascript
// In browser console
showVisualization('3d-atomic');  // Should open modal
```

### Test Database
```bash
python -c "from src.element_database import ElementDatabase; db = ElementDatabase(); print(db.get_element_count())"
# Output: 119
```

## 📚 Dependencies

**Backend**:
- Flask 2.3.3 - Web framework
- Matplotlib 3.7.2 - Plotting library
- NumPy 1.24.3 - Scientific computing
- Pandas 2.0.3 - Data analysis

**Frontend**:
- Vanilla JavaScript (no frameworks)
- CSS3 with Flexbox/Grid
- Jinja2 templates

**Optional Upcoming**:
- Three.js - 3D graphics (Phase 3)
- Plotly - Interactive charts (Phase 3)
- reportlab - PDF generation (Phase 4)

## 🚀 Quick Commands

```bash
# Start development server
python run_server.py

# Generate analysis report
python generate_analysis.py

# Test database
python -c "from src.element_database import ElementDatabase; print(ElementDatabase().get_element_count())"

# Install new dependencies
pip install [package-name]
pip freeze > requirements.txt

# Check code syntax
python -m py_compile src/*.py src/app/*.py
```

## 🎯 Phase 3 Priority

When implementing visualizations, start with:
1. **Heatmap** (easiest) - Property distribution
2. **Distribution Chart** (medium) - Histograms
3. **Spectral Plot** (medium) - Line chart
4. **3D Atomic** (hardest) - Three.js Bohr model

## 📞 Resources

- **Three.js Docs**: https://threejs.org/docs/
- **Chart.js Docs**: https://www.chartjs.org/docs/latest/
- **Flask Docs**: https://flask.palletsprojects.com/
- **Periodic Table JSON**: `src/lib/Periodic-Table-JSON/`

## ✅ Checklist Before Deployment

- [ ] All visualizations implemented
- [ ] Tests pass without errors
- [ ] Mobile responsive verified
- [ ] Performance optimized
- [ ] Security headers configured
- [ ] Error handling complete
- [ ] Documentation updated
- [ ] Dependencies pinned

---

**Last Updated**: November 21, 2025
**Framework Status**: Phase 1 Complete, Phase 3 Ready
**Maintenance**: Active Development
