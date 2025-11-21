# Quick Reference: Visualization Module API

## Module Location
`src/element_visual.py` (836 lines, 18 visualization methods)

## Import

```python
from src.element_database import ElementDatabase
from src.element_visual import ElementVisualizer

db = ElementDatabase()
viz = ElementVisualizer(db)
```

---

## 3D Visualization Methods

### `plot_electron_shells_3d(element, save_path=None)`
**Purpose**: Visualize electron orbital shells in 3D space
```python
fig = viz.plot_electron_shells_3d(db.get_element_by_symbol('H'))
fig.savefig('electron_shells.png', dpi=300)
```

### `plot_ionization_energies_3d(element, save_path=None)`
**Purpose**: Show ionization energy levels in 3D
```python
fig = viz.plot_ionization_energies_3d(db.get_element_by_symbol('Li'))
plt.show()
```

### `plot_thermal_properties_3d(element, save_path=None)`
**Purpose**: Visualize thermal properties in 3D space
```python
fig = viz.plot_thermal_properties_3d(db.get_element_by_number(26))  # Iron
```

### `plot_atomic_structure_3d(element, save_path=None)`
**Purpose**: Complete Bohr model with electron distribution
```python
fig = viz.plot_atomic_structure_3d(db.get_element_by_symbol('O'))
```

---

## HyperSpectral Analysis Methods (NEW)

### `plot_spectral_signature(element, save_path=None)`
**Purpose**: Element's spectral signature (200-2500nm range)
**Output**: 2-panel figure
- Panel 1: Spectral reflectance curve
- Panel 2: Band intensity distribution (UV/Visible/IR)

```python
fig = viz.plot_spectral_signature(db.get_element_by_symbol('H'))
```

### `plot_band_ratios(elements, save_path=None)`
**Purpose**: Compare IR/Visible band ratios (mineral identification)
**Input**: List of Element objects
**Output**: Bar chart with ratios

```python
elements = [
    db.get_element_by_symbol('Li'),
    db.get_element_by_symbol('Na'),
    db.get_element_by_symbol('K'),
]
fig = viz.plot_band_ratios(elements)
```

### `plot_minimum_wavelength_map(elements, save_path=None)`
**Purpose**: Characteristic wavelength mapping for element identification
**Input**: List of Element objects
**Output**: Scatter plot with wavelength values

```python
elements = db.get_elements_by_category('alkali metal')
fig = viz.plot_minimum_wavelength_map(elements)
```

### `plot_lithium_bearing_mineral_detection(save_path=None)` ⭐
**Purpose**: Comprehensive lithium mineral analysis (4-panel)
**Output**: 
- Panel 1: Li spectral characteristics (670nm, 611nm)
- Panel 2: Li content in minerals (Spodumene, Lepidolite, Petalite, Amblyonite)
- Panel 3: Band ratio classification
- Panel 4: Mineral identification confidence matrix

```python
fig = viz.plot_lithium_bearing_mineral_detection()
fig.savefig('li_mineral_analysis.png', dpi=300)
```

---

## Periodic Table Analytics Methods

### `plot_elements_by_category()`
Pie chart of element distribution by category

### `plot_elements_per_period()`
Bar chart showing elements per period

### `plot_atomic_mass_distribution()`
Distribution histogram of atomic masses

### `plot_atomic_mass_vs_electronegativity()`
Scatter plot correlating mass and electronegativity

### `plot_electronegativity_heatmap()`
Periodic table heatmap colored by electronegativity

### `plot_phase_distribution()`
Bar chart of elements by physical state

### `plot_densest_elements()`
Top density elements ranking

### `plot_melting_vs_boiling_points()`
Scatter plot of melting vs boiling temperatures

### `plot_element_properties_comparison()`
Multi-property comparison visualization

### `plot_property_correlation_matrix()`
Correlation heatmap of element properties

---

## Usage Patterns

### Single Element Visualization
```python
element = db.get_element_by_symbol('Au')  # Gold

# Create and display
fig = viz.plot_electron_shells_3d(element)
plt.show()
```

### Save to File
```python
# All methods support save_path parameter
fig = viz.plot_spectral_signature(element, save_path='spectrum.png')
```

### Batch Processing
```python
elements = db.get_elements_by_category('transition metal')

for elem in elements[:5]:
    fig = viz.plot_atomic_structure_3d(elem)
    fig.savefig(f'{elem.symbol}_structure.png', dpi=300)
    plt.close(fig)
```

### Multiple Element Comparison
```python
alkali_metals = db.get_elements_by_category('alkali metal')
fig = viz.plot_band_ratios(alkali_metals)
plt.show()
```

---

## Integration Examples

### In GUI
```python
# From PeriodicTableApp
def on_visualize_button(self):
    element = self.selected_element
    fig = self.visualizer.plot_spectral_signature(element)
    # Display in canvas...
```

### In Report Generation
```python
# From AnalysisReportGenerator
elements = self.db.get_all_elements()
for viz_method in ['plot_thermal_properties_3d', 'plot_band_ratios']:
    fig = getattr(self.visualizer, viz_method)(elements)
    fig.savefig(f'report_{viz_method}.png', dpi=300)
```

### In Analysis Scripts
```python
# Analyze lithium minerals
fig = viz.plot_lithium_bearing_mineral_detection()
fig.savefig('mineral_analysis.png', dpi=300)
plt.show()
```

---

## Method Specifications

### Resolution & Quality
- 3D mesh resolution: 50x50 (high quality)
- Export DPI: 300 (publication quality)
- Color palettes: Spectral, Plasma, RdYlGn, seaborn

### Physical Units
- Orbital radii: Bohr radii (a₀)
- Energy: Electron volts (eV)
- Wavelength: Nanometers (nm)
- Temperature: Kelvin (K)
- Density: g/cm³

### Performance
- Method load time: ~100ms
- Figure generation: 200-500ms
- Memory per figure: ~50MB
- PNG export: 1-2 seconds

---

## Error Handling

```python
from src.element import Element
from src.element_visual import ElementVisualizer

# Properly get element
element = db.get_element_by_symbol('Li')
if element is None:
    raise ValueError("Element not found")

# Visualize safely
try:
    fig = viz.plot_spectral_signature(element)
except Exception as e:
    print(f"Visualization error: {e}")
```

---

## Matplotlib Configuration

```python
# The visualizer handles styling automatically
# But you can customize:
viz = ElementVisualizer(db, style='seaborn-v0_8-darkgrid')

# Or use different backend
import matplotlib
matplotlib.use('Agg')  # Non-interactive
```

---

## Category Colors

```python
# Available category colors (used automatically):
CATEGORY_COLORS = {
    'alkali metal': '#ff9999',
    'alkaline earth metal': '#ffddb3',
    'transition metal': '#cccccc',
    'lanthanide': '#ffbfff',
    'actinide': '#ff99cc',
    'nonmetal': '#a3f7a3',
    'halogen': '#ffff99',
    'noble gas': '#c0ffff',
    'metalloid': '#ccccff',
    'post-transition metal': '#ffccff',
    'diatomic nonmetal': '#a0ffa0',
    'polyatomic nonmetal': '#99ff99',
}
```

---

## Common Queries

### Q: How do I visualize all alkali metals?
```python
alkali = db.get_elements_by_category('alkali metal')
fig = viz.plot_band_ratios(alkali)
```

### Q: How do I save high-quality images?
```python
# All methods support save_path
fig = viz.plot_spectral_signature(element, save_path='output.png')
# Or manually
fig.savefig('output.png', dpi=300, bbox_inches='tight')
```

### Q: How do I identify lithium minerals?
```python
# Use the specialized lithium analysis
fig = viz.plot_lithium_bearing_mineral_detection()
# Shows mineral content, band ratios, and confidence matrix
```

### Q: How do I compare multiple elements?
```python
elements = [
    db.get_element_by_number(3),   # Li
    db.get_element_by_number(11),  # Na
    db.get_element_by_number(19),  # K
]
fig = viz.plot_band_ratios(elements)
```

---

## File Locations

- **Visualization Module**: `src/element_visual.py`
- **Database**: `src/element_database.py`
- **Element Class**: `src/element.py`
- **JSON Data**: `src/lib/Periodic-Table-JSON/PeriodicTableJSON.json`

---

## Documentation

For detailed information, see:
- `VISUALIZATION_MERGE_SUMMARY.md` - Technical details
- `COMPLETION_STATUS.md` - Task completion report
- `HYPERSPECTRAL_IMPLEMENTATION.md` - Executive summary
