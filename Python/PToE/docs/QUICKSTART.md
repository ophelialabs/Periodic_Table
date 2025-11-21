# Quick Start Guide

## Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Installation**
   ```bash
   python -c "from src.element_database import ElementDatabase; db = ElementDatabase(); print(f'Loaded {db.get_element_count()} elements')"
   ```

## Running the Application

### Option 1: Launch the GUI Application
```bash
python run_app.py
```

This opens an interactive periodic table desktop application with:
- Color-coded periodic table grid
- Element search functionality
- Detailed element information panels
- 3D visualizations for selected elements
- Element comparison tools
- Analysis and report generation options

### Option 2: Generate Analysis Reports
```bash
python generate_analysis.py
```

This generates:
- **periodic_table_analysis.pdf** - Comprehensive statistical analysis with visualizations
- **PNG files** - Individual visualization files:
  - atomic_mass_distribution.png
  - elements_by_category.png
  - phase_distribution.png
  - atomic_mass_vs_electronegativity.png
  - melting_vs_boiling_points.png
  - densest_elements.png
  - elements_per_period.png
  - electronegativity_heatmap.png
  - property_correlation_matrix.png
- **elements_data.csv** - Complete element data table

## Using the GUI Application

### Main Window Layout
```
┌─────────────────────────────────────────────┐
│ Search Bar: [___________] [Clear]          │
├─────────────────────────┬───────────────────┤
│                         │                   │
│  Periodic Table Grid    │  Element Details  │
│  (Color-coded)          │  (4 Tabs)        │
│                         │                   │
│                         ├───────────────────┤
│                         │ Selected Elements │
│                         ├───────────────────┤
│                         │ Buttons:          │
│                         │ - Clear Selection │
│                         │ - Compare Selected│
│                         │ - Generate Report │
└─────────────────────────┴───────────────────┘
```

### Workflow

1. **Search for Elements**
   - Type in search box to filter by name, symbol, or category
   - Click "Clear" to reset

2. **View Element Details**
   - Click on element button to select it
   - View 4 detail tabs:
     - **Basic Info**: Name, number, appearance, summary
     - **Properties**: Configuration, ionization energies, thermal data
     - **Visualization**: 3D plots of atomic structure and properties
     - **Analysis**: Report generation and analysis options

3. **Compare Elements**
   - Click multiple elements to add them to selection
   - Click "Compare Selected" to view property comparison
   - Displays values for: atomic mass, electronegativity, melt, boil, density

4. **Generate Visualizations**
   - Click visualization buttons to view 3D plots
   - Click "Periodic Table Heatmap" for electronegativity visualization
   - Click "Property Distributions" for statistical analysis

5. **Generate Reports**
   - Click "Generate Report" to create comprehensive analysis
   - PDF will include statistics, charts, and visualizations
   - PNG files saved individually for reference

## Python API Usage

### Basic Example
```python
from src.element_database import ElementDatabase
from src.element_visual import ElementVisualizer

# Load the database
db = ElementDatabase()

# Get an element
hydrogen = db.get_element_by_symbol('H')
print(f"Atomic mass of {hydrogen.name}: {hydrogen.atomic_mass}")

# Search for elements
noble_gases = db.get_elements_by_category('noble gas')
print(f"Found {len(noble_gases)} noble gases")

# Create visualizer
viz = ElementVisualizer(db)

# Generate a visualization
fig = viz.plot_atomic_structure_3d(hydrogen)
viz.show_figure(fig)
```

### Analysis Example
```python
from src.element_database import ElementDatabase
from src.analysis_report import AnalysisReportGenerator

# Load and analyze
db = ElementDatabase()
generator = AnalysisReportGenerator(db, output_dir='analysis_output')

# Generate reports
generator.generate_full_report(include_pdf=True, include_png=True)
print(generator.generate_summary_statistics())
```

### Quantum Integration Example
```python
from src.research_agent import QuantumIntegration

# Create quantum integration
quantum = QuantumIntegration(use_azure=False)

# Submit analysis job
job_id = quantum.analyze_element_quantum_properties('Fe')
print(f"Submitted job: {job_id}")

# Check task status
status = quantum.research_manager.get_task_status(job_id)
print(f"Job status: {status}")
```

## Keyboard Shortcuts (in GUI)

- `Ctrl+F`: Focus search box (when implemented)
- `Escape`: Clear selection
- `?`: Help (when implemented)

## Troubleshooting

### Application won't start
```bash
# Check Python version
python --version  # Should be 3.7+

# Verify dependencies
pip install -r requirements.txt

# Try running with verbose output
python -u run_app.py
```

### Data file not found
Make sure the periodic table JSON file exists:
```bash
ls src/lib/Periodic-Table-JSON/PeriodicTableJSON.json
```

### Missing visualization displays
Requires matplotlib backend support. On headless systems, use:
```python
import matplotlib
matplotlib.use('Agg')  # For PNG output only
```

### Report generation takes too long
Large visualizations can take time to generate. Progress messages will display in console.

## Next Steps

1. **Run the Application**
   ```bash
   python run_app.py
   ```

2. **Explore Elements**
   - Click on different elements
   - Read their properties and summaries

3. **Generate Reports**
   ```bash
   python generate_analysis.py
   ```

4. **Integrate Quantum Features**
   - See ARCHITECTURE.md for quantum integration details
   - Placeholder code is ready for Azure Quantum integration

## Support

For detailed technical information, see:
- **ARCHITECTURE.md** - Module structure and design
- **src/element_database.py** - Database API documentation
- **src/element_visual.py** - Visualization methods
- **src/app/main_app.py** - GUI implementation

## License

See LICENSE.md for license information.
