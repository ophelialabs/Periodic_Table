# Architecture and Module Documentation

## Project Structure

```
PToE/
├── src/
│   ├── __init__.py                  # Package initialization
│   ├── element.py                   # Element data structure
│   ├── element_database.py          # Database for periodic table
│   ├── element_visual.py            # Visualization module (ElementVisualizer)
│   ├── research_agent.py            # Quantum research agent
│   ├── analysis_report.py           # Report and analysis generator
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main_app.py              # Main tkinter GUI application
│   │   ├── api.py                   # Flask API endpoints (legacy)
│   │   ├── data_loader.py           # Data loading utilities
│   │   ├── analysis.py              # Analysis utilities
│   │   └── visualizations.py        # Visualization helpers
│   └── lib/
│       └── Periodic-Table-JSON/     # Periodic table data
│           ├── PeriodicTableJSON.json
│           ├── periodic-table-lookup.json
│           └── PeriodicTableCSV.csv
├── agent/
│   └── agent.py
├── docs/
├── run_app.py                       # Entry point for GUI
├── generate_analysis.py             # Report generation script
└── requirements.txt
```

## Core Modules

### 1. Element (`src/element.py`)
Represents a single chemical element with all properties.

**Key Classes:**
- `Element`: Wraps element data with property accessors

**Key Properties:**
- Basic: `number`, `symbol`, `name`, `atomic_mass`
- Electronic: `electron_configuration`, `shells`, `electronegativity`
- Thermal: `melt`, `boil`, `density`, `molar_heat`
- Visual: `color` (CPK hex), `bohr_model_image`, `bohr_model_3d`

### 2. ElementDatabase (`src/element_database.py`)
Manages loading and accessing periodic table data.

**Key Classes:**
- `ElementDatabase`: Load and query element data

**Key Methods:**
- `get_element_by_number()`, `get_element_by_symbol()`, `get_element_by_name()`
- `get_elements_by_category()`, `get_elements_by_period()`, `get_elements_by_group()`
- `search_elements()` - Search by name, symbol, or category
- `get_dataframe()` - Get pandas DataFrame for analysis

### 3. ElementVisualizer (`src/element_visual.py`)
Provides comprehensive visualization methods for elements and analysis.

**Key Methods:**

#### Element-Specific Visualizations (3D)
- `plot_electron_shells_3d()` - Concentric shell visualization
- `plot_ionization_energies_3d()` - Ionization energy bars
- `plot_thermal_properties_3d()` - Temperature properties
- `plot_atomic_structure_3d()` - Complete atomic overview

#### Periodic Table Visualizations
- `plot_element_properties_comparison()` - Compare properties across elements
- `plot_electronegativity_heatmap()` - Periodic table color-coded by electronegativity
- `plot_atomic_mass_distribution()` - Histogram of atomic masses
- `plot_elements_by_category()` - Bar chart of elements per category
- `plot_phase_distribution()` - Pie chart of phases
- `plot_elements_per_period()` - Distribution by period
- `plot_atomic_mass_vs_electronegativity()` - Scatter plot
- `plot_melting_vs_boiling_points()` - Temperature scatter plot
- `plot_densest_elements()` - Top N densest elements
- `plot_property_correlation_matrix()` - Correlation heatmap

### 4. Main Application (`src/app/main_app.py`)
Tkinter-based desktop GUI for the periodic table.

**Key Classes:**
- `PeriodicTableApp`: Main application window

**Features:**
- Interactive periodic table grid with color-coded elements
- Real-time search and filtering
- Element detail viewer (4 tabs: Basic Info, Properties, Visualization, Analysis)
- Multi-element selection and comparison
- Visualization generation buttons
- Report generation options

### 5. Research Agent (`src/research_agent.py`)
Framework for quantum research tasks and Azure Quantum integration.

**Key Classes:**
- `ResearchTaskType`: Enum for task types
- `QuantumJob`: Data class for quantum jobs
- `QuantumProcessor`: Submits and tracks quantum jobs
- `ResearchAgentManager`: Manages research operations
- `AzureQuantumConnector`: Placeholder for Azure Quantum integration
- `QuantumIntegration`: High-level quantum interface

**Task Types:**
- ELECTRON_ORBITAL_SIMULATION
- MOLECULAR_STRUCTURE_ANALYSIS
- BINDING_ENERGY_CALCULATION
- MATERIAL_PROPERTY_CHARACTERIZATION
- QUANTUM_STATE_VISUALIZATION

### 6. Analysis Report Generator (`src/analysis_report.py`)
Generates comprehensive analysis reports with visualizations.

**Key Classes:**
- `AnalysisReportGenerator`: Generate PDF and PNG reports

**Key Methods:**
- `generate_full_report()` - Generate complete analysis
- `_generate_pdf_report()` - PDF with statistics and visualizations
- `_generate_png_visualizations()` - Individual PNG files
- `generate_element_details_csv()` - Export data to CSV
- `generate_summary_statistics()` - Text summary

## Usage Examples

### Running the Application
```bash
# Launch the interactive GUI
python run_app.py
```

### Generating Analysis Reports
```bash
# Create PDF report and PNG visualizations
python generate_analysis.py
```

### Programmatic Usage
```python
from src.element_database import ElementDatabase
from src.element_visual import ElementVisualizer

# Load database
db = ElementDatabase()

# Create visualizer
viz = ElementVisualizer(db)

# Get an element
hydrogen = db.get_element_by_symbol('H')

# Generate visualization
fig = viz.plot_atomic_structure_3d(hydrogen)
viz.show_figure(fig)

# Compare elements
elements = [db.get_element_by_symbol(s) for s in ['H', 'O', 'N']]
fig = viz.plot_element_properties_comparison(elements, 'atomic_mass')
viz.show_figure(fig)

# Generate report
from src.analysis_report import AnalysisReportGenerator
generator = AnalysisReportGenerator(db)
generator.generate_full_report()
```

## Data Source

The periodic table data comes from `src/lib/Periodic-Table-JSON/`:

- **PeriodicTableJSON.json**: Full periodic table with all properties
- **periodic-table-lookup.json**: Quick lookup table
- **PeriodicTableCSV.csv**: Comma-separated values format

Each element includes:
- Atomic number, symbol, name, atomic mass
- Electron configuration and shells
- Electronegativity and ionization energies
- Melting/boiling points and density
- Category, phase, period, group, block
- Images and references

## Dependencies

See `requirements.txt` for complete list:
- tkinter (built-in) - GUI framework
- matplotlib - 2D/3D plotting
- seaborn - Statistical visualization
- plotly - Interactive visualizations
- pandas - Data analysis
- numpy - Numerical computations
- scipy - Scientific computing
- Pillow - Image handling

## Future Enhancements

- [ ] 3D model viewer for Bohr models (GLB files)
- [ ] Spectral data visualization
- [ ] Azure Quantum integration for real quantum simulations
- [ ] Drag-and-drop element combination
- [ ] Advanced molecular geometry predictions
- [ ] HyperSpectral analysis visualization
- [ ] Element similarity recommendations
- [ ] Wikipedia integration for detailed information

## Author and License

Created as part of the Periodic Table Desktop Application project.
See LICENSE.md for license information.
