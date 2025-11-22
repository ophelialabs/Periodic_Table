# Phase 3 Development Guide - Advanced Visualization Enhancements

## Overview
Phase 3 focuses on implementing actual 3D visualizations and chart-based analysis using matplotlib and Three.js. The framework is ready, and placeholder implementations are in place.

## Architecture

### Current Visualization System
- **Frontend**: `js/visualizations.js` contains modal creation and framework
- **Backend**: `src/analysis_report.py` has methods for data generation
- **Routes**: `src/app/__init__.py` has API endpoints ready

### Data Flow for Visualizations
```
User clicks visualization button
  ↓
showVisualization('type') in visualizations.js
  ↓
Creates modal window with element data
  ↓
Calls generateXxxViz(element) for placeholder
  ↓
Replace with actual implementation:
  - For 3D: Use Three.js to render 3D model
  - For charts: Call API endpoint for data, render with matplotlib/Plotly
  - For analysis: Generate heatmap/histogram data
```

## Implementation Plan

### Step 1: Set Up Three.js for 3D Visualizations

#### 1.1 Update `base.html` to include Three.js
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@r128/examples/js/controls/OrbitControls.js"></script>
```

#### 1.2 Create `src/app/static/js/3d-renderer.js`
```javascript
class Renderer3D {
  constructor(containerId) {
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(75, width/height, 0.1, 1000);
    this.renderer = new THREE.WebGLRenderer({antialias: true});
    // ... initialization code
  }
  
  renderBohrModel(element) {
    // Create nucleus
    // Create electron orbitals
    // Animate if needed
  }
  
  renderElectronShells(element) {
    // Visualize electron configuration
  }
}
```

#### 1.3 Update `visualizations.js` to use 3D renderer
Replace placeholder content in `generate3DAtomicViz()` with:
```javascript
function generate3DAtomicViz(element) {
  const container = document.createElement('div');
  container.style.cssText = 'width: 100%; height: 100%;';
  const renderer = new Renderer3D(container);
  renderer.renderBohrModel(element);
  return container.innerHTML;
}
```

### Step 2: Implement Matplotlib Chart Visualizations

#### 2.1 Update `src/app/__init__.py` to add chart endpoints
```python
@app.route('/api/analysis/spectral/<symbol>')
def get_spectral_data(symbol):
    """Get spectral data for element."""
    element = app.db.get_element_by_symbol(symbol)
    if element:
        data = app.analysis.generate_spectral_data(symbol)
        return jsonify(data)
    return jsonify({'error': 'Element not found'}), 404

@app.route('/api/analysis/heatmap/<property>')
def get_heatmap_data(property):
    """Get heatmap data for property."""
    data = app.analysis.generate_heatmap_data(property)
    return jsonify(data)
```

#### 2.2 Update `src/analysis_report.py` with chart generation
```python
def generate_spectral_data(self, symbol):
    """Generate spectral signature data for wavelength range 200-2500nm."""
    # Return spectrum data as JSON
    return {
        'wavelengths': [...],
        'intensity': [...],
        'peaks': [...]
    }

def generate_band_ratio_data(self, symbol):
    """Generate IR and visible wavelength band ratios."""
    # Return band ratio analysis
    return {
        'ir_bands': {...},
        'visible_bands': {...},
        'ratios': {...}
    }
```

#### 2.3 Create `src/app/static/js/chart-renderer.js`
```javascript
class ChartRenderer {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
  }
  
  async renderSpectralChart(element) {
    const data = await fetchData(`/api/analysis/spectral/${element.symbol}`);
    // Use Chart.js or Plotly to render
  }
  
  async renderHeatmap(property) {
    const data = await fetchData(`/api/analysis/heatmap/${property}`);
    // Render heatmap visualization
  }
}
```

### Step 3: Update Placeholder Visualizations

#### For 3D Visualizations:
- `generate3DAtomicViz()` - Bohr model with electrons orbiting nucleus
- `generate3DIonizationViz()` - Energy level diagram
- `generate3DElectronViz()` - Electron shell structure
- `generate3DThermalViz()` - Temperature property visualization

#### For HyperSpectral:
- `generateSpectralViz()` - 200-2500nm wavelength plot
- `generateBandRatioViz()` - IR/visible ratio visualization
- `generateWavelengthViz()` - Wavelength mapping chart

#### For Property Analysis:
- `generateMineralViz()` - 4-panel mineral detection
- `generateHeatmapViz()` - Property distribution across table
- `generateDistributionViz()` - Histogram and statistics

### Step 4: Element Comparison Feature

#### 4.1 Update `element-details.js`
```javascript
function initiateComparison(symbols) {
  // Create comparison layout
  // Fetch data for multiple elements
  // Render side-by-side comparison
}
```

#### 4.2 Update CSS for comparison layout
```css
.comparison-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.comparison-element {
  padding: 1rem;
  border: 1px solid #667eea;
  border-radius: 8px;
}
```

#### 4.3 Add API endpoint
```python
@app.route('/api/compare')
def compare_elements():
    symbols = request.args.getlist('symbols')
    elements = [app.db.get_element_by_symbol(s) for s in symbols]
    return jsonify(elements)
```

## Required Dependencies

Add to `requirements.txt`:
```
plotly>=5.16.1          # For interactive charts
pandas>=2.0.3           # For data manipulation
seaborn>=0.12.2         # For heatmaps
scipy>=1.11.2           # Already included
numpy>=1.24.3           # Already included
```

For frontend (CDN-based, no pip needed):
- Three.js: `https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`
- Chart.js: `https://cdn.jsdelivr.net/npm/chart.js`
- Plotly.js: `https://cdn.plot.ly/plotly-latest.min.js`

## Testing Checklist

- [ ] Three.js loads without errors
- [ ] 3D visualizations render correctly
- [ ] Spectral charts generate properly
- [ ] Heatmaps display correct color gradients
- [ ] Element comparison view works
- [ ] Visualization modal closes and opens smoothly
- [ ] Responsive design maintained in visualization windows
- [ ] API endpoints return correct JSON data
- [ ] Error handling for missing elements
- [ ] Performance optimized for complex visualizations

## File Locations Reference

```
src/
├── app/
│   ├── __init__.py              # Add API endpoints here
│   └── static/
│       ├── js/
│       │   ├── visualizations.js     # Update placeholder functions
│       │   ├── 3d-renderer.js        # NEW: Three.js wrapper
│       │   └── chart-renderer.js     # NEW: Chart.js wrapper
│       └── css/
│           └── style.css             # Update for modals
│
├── analysis_report.py           # Add data generation methods
└── lib/
    └── Periodic-Table-JSON/
        └── [element data for reference]
```

## Common Issues & Solutions

### Issue: Three.js not rendering
- Check WebGL support in browser
- Verify container has height/width set
- Check console for shader errors

### Issue: Charts not updating
- Verify API endpoint returns JSON
- Check data format matches chart library
- Debug fetch requests in browser console

### Issue: Performance slow with many visualizations
- Implement lazy loading
- Cache generated visualizations
- Use WebWorkers for heavy computation

## Success Criteria for Phase 3

✅ All 10 visualization buttons functional
✅ 3D Bohr model renders correctly
✅ Spectral charts display accurately
✅ Heatmaps show property distributions
✅ Element comparison working
✅ Responsive in all screen sizes
✅ <500ms load time for visualizations
✅ No console errors

## Next: Phase 4-8

Once Phase 3 complete:
- Phase 4: PDF report generation
- Phase 5: Database enhancements
- Phase 6: Azure Quantum integration
- Phase 7: AI agent integration
- Phase 8: Advanced analytics

---

**Framework Ready**: Yes ✅
**Estimated Time to Complete**: 4-6 hours for full implementation
**Difficulty Level**: Medium (mostly API integration and chart rendering)
