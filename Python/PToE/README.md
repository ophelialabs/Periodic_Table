Desktop application for interactive periodic table with quantum research integration.

## Getting Started

### Installation

```bash
source venv/bin/activate
```

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run_app.py
```

3. Generate analysis reports and visualizations:
```bash
python generate_analysis.py
```

## Application Features

### Main GUI Features
- **Interactive Periodic Table**: Color-coded elements by category
- **Search Functionality**: Search elements by name, symbol, or category
- **Element Details**: View comprehensive information for each element
- **Element Selection**: Select multiple elements for comparison
- **Visualization Tools**: Generate 3D visualizations of atomic structure, ionization energies, electron shells, and thermal properties

### Implemented Features

✓ Interactive Web-Based Table (tkinter GUI)
- Elements grid with CPK color coding
- Real-time search functionality
- Click to view details
- Multi-element selection

✓ 3D Visualizations
- Interactive 3D atomic structure visualization
- Ionization energy visualization
- Electron shell structure visualization
- Thermal properties visualization

✓ Generate Visualizations
- Electron shell structure charts
- Ionization energies graphs
- Atomic mass distribution histogram
- Elements by category bar chart
- Phase distribution pie chart
- Atomic mass vs electronegativity scatter plot
- Melting vs boiling points analysis
- Densest elements ranking
- Elements per period distribution
- Electronegativity heatmap

✓ Element Comparison
- Compare up to multiple elements side-by-side
- Compare properties across selected elements
- Visual property distribution analysis

✓ Analysis Report Generator
- Generate comprehensive PDF analysis report
- Create individual PNG visualizations
- Export element data to CSV
- Statistical summary generation

✓ Quantum Integration Framework
- Quantum research agent structure
- Job submission and tracking
- Framework for Azure Quantum integration
- Support for quantum state analysis

### Upcoming Features

Features Roadmap
1. [ ] Web-based Interactive Table
    - Elements grid
    - Color-coded categories
    - Search functionality
    - Click to view details
    - Implement drag and drop functionality to combine two or more elements together and display results
    

2. [ ] 3D Visualizations
    - Interactive visualizations with hover data
    - Bohr Model 3D (interactive GLB viewer)
    - de Broglie Wave (canvas animation)
    - Schrödinger Wave (probability visualization)
    - Orbital shape rendering (s, p, d, f orbitals)
    - Molecular geometry predictions
    - Energy distribution visualizations

3. Generate Visualizations:
    - Electron Shell Structure
    - Ionization Energies
    - Thermal Properties
    - Atomic Structure
    - Atomic mass distribution histogram
    - Elements by category bar chart
    - Phase distribution pie chart
    - Atomic mass vs electronegativity scatter plot
    - Melting vs boiling points analysis
    - Densest elements ranking
    - Elements per period distribution
    - Periodic table heatmap by atomic mass
    - Correlation matrix of element properties

    ElementVisualizer
    1. `plot_electron_shells_3d(element)`: Visualize electron shell structure
    2. `plot_ionization_energies_3d(element)`: Visualize ionization energies
    3. `plot_thermal_properties_3d(element)`: Visualize thermal properties
    4. `plot_atomic_structure_3d(element)`: Visualize complete atomic structure
    5. `plot_element_properties_comparison(elements, property)`: Compare properties across elements
    6. `plot_electronegativity_heatmap(df)`: Create periodic table heatmap


3. [ ] HyperSpectral analysis visualization
    - band ratios
    - minimum wavelength mapping
    - classified lithium-bearing minerals

4. [ ] Element similarity recommendations

5. [ ] Wikipedia integration

6. [ ] Database integration for extended properties

7. [ ] 🧮 Quantum Integration
    - Bridge frontend actions to quantum operations
    - Quantum State Analysis
    - Job Submission that generates QIR code preperation.
    - Azure Quantum: Integration with quantum hardware providers (IonQ, Quantinuum). User should only have to login to choose QPU provider and submit jobs

8. [ ] 🔬 Quantum Research Agent
    - [ ] Electron orbital simulations
    - [ ] Molecular structure analysis
    - [ ] Binding energy calculations
    - [ ] Material property characterization
    - [ ] Real-time quantum state visualization

9. [ ] Generate comprehensive analysis reports and visualizations. This will:
    - Print a detailed statistical report (pdf)
    - Generate 9 high-quality PNG visualizations in the `periodic_table_analysis/` directory
