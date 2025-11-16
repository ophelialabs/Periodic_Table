# Quick Start Guide

## Installation

### 1. Clone/Download Project
```bash
cd PeriodicTableCP
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Install Q# SDK
For quantum operation compilation:
```bash
dotnet tool install -g Microsoft.Quantum.IQSharp
qsharp --version
```

## Running the Application

### Start the GUI
```bash
python main.py
```

Or alternatively:
```bash
python -m src.main_app
```

## First Time Usage

1. **Launch Application**: Run the command above
2. **Explore Periodic Table**: Browse elements with scroll/search
3. **Select an Element**: Click any element tile
4. **View Details**: Check properties in right panel
5. **Run Simulation**: Click "Analyze" button
6. **View Results**: See orbital data in "Quantum Data" tab
7. **3D Model**: Click "3D Model" for molecular geometry

## Key Features Tour

### Search Elements
- Type in search box: "iron", "Fe", "hydrogen"
- Results update in real-time

### Filter by Category
- Select categories: Metal, Nonmetal, etc.
- Displays only matching elements

### Quantum Analysis
- Select element → Click "Analyze"
- Wait for simulation completion
- View results in "Quantum Data" tab

### Task Monitoring
- Click "Tasks" tab to see simulation status
- Monitor multiple concurrent simulations

## Configuration

### Local Mode (Default)
Works without any setup, uses local simulator.

### Azure Quantum Mode
To use real quantum hardware:

1. Create `config.json` from `config.json.example`
2. Add your Azure credentials
3. Set `"enabled": true`

## Troubleshooting

### Application Won't Start
```bash
# Check Python version
python --version  # Should be 3.9+

# Verify tkinter
python -m tkinter  # Should show test window
```

### Simulations Not Running
- Check that Tkinter is installed
- Verify Python version compatibility
- Try local mode without Azure

### Q# Compilation Issues
```bash
# Verify Q# installation
qsharp --version

# Update if needed
dotnet tool update -g Microsoft.Quantum.IQSharp
```

## File Structure

```
PeriodicTableCP/
├── main.py                 # Entry point
├── requirements.txt        # Python packages
├── README.md              # Full documentation
├── DEVELOPER.md           # Technical guide
├── QUICKSTART.md          # This file
├── qsharp.json            # Q# project config
├── config.json.example    # Configuration template
├── src/
│   ├── __init__.py
│   ├── element.py         # Element data class
│   ├── element_database.py # Element management
│   ├── element_visual.py   # GUI components
│   ├── research_agent.py   # Quantum tasks
│   ├── model_generator.py  # 3D models
│   └── main_app.py        # Main GUI
├── quantum/
│   └── QuantumRD.qs       # Q# operations
└── utils/
    ├── __init__.py
    └── azure_quantum_integration.py
```

## Common Commands

### Search for Element
1. Type element name in search box
2. Elements filter automatically

### Run Orbital Analysis
1. Select element
2. Click "Analyze" button
3. Results appear in "Quantum Data" tab

### View Molecular Structure
1. Select element
2. Click "3D Model" button
3. See geometry information

### Check Task Status
1. Click "Tasks" tab
2. See status of all simulations

## Tips & Tricks

- **Fast Search**: Type element symbol (e.g., "Au" for gold)
- **Multiple Simulations**: Click "Analyze" for different elements
- **Batch Analysis**: Run many simulations sequentially
- **Export Results**: Copy-paste from results pane to file
- **Customize**: Edit `config.json` for UI/simulation settings

## Next Steps

- Read `README.md` for complete documentation
- Check `DEVELOPER.md` for technical details
- Explore Q# code in `quantum/QuantumRD.qs`
- Configure Azure Quantum for real hardware access

## Support

Having issues? Check:
1. README.md "Troubleshooting" section
2. DEVELOPER.md for technical details
3. Python version compatibility
4. Tkinter installation

Enjoy exploring quantum chemistry!

---

Need help? Check the full documentation files included in the project.
