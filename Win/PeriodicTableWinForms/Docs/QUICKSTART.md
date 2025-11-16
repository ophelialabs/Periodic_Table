# Quick Start Guide

## Installation & Setup

### 1. Prerequisites

Ensure you have the following installed:
- .NET 8.0 SDK or later
- Visual Studio 2022 (recommended) or VS Code
- Q# Development Kit (automatic via NuGet)

### 2. Clone Repository

```bash
cd /Users/jesse/periodictable
ls
```

### 3. Build Project

```bash
cd PeriodicTableWinForms
dotnet restore
dotnet build
```

### 4. Run Application

```bash
dotnet run
```

## First Steps

### Select an Element

1. **Launch the application**
   - A window will appear with a grid of element buttons
   - Elements are color-coded by category

2. **Click an Element Button**
   - Example: Click "C" for Carbon (Z=6)
   - Information panel shows element details
   - Atomic number, mass, electronegativity displayed

### Analyze the Element

1. **Click "Analyze Element" Button**
   - Status changes to "Analyzing..."
   - Quantum simulation runs (typically 100-500ms)
   - Progress indicator shows completion

2. **Observe Results**
   - 3D electron cloud appears in the visualization panel
   - Electron particles shown based on quantum probability
   - Quantum state timeline graph displayed

### Explore the Visualization

1. **Rotate the Model**
   - Click **"Rotate Left"** / **"Rotate Right"** for Y-axis rotation
   - Click **"Rotate Up"** / **"Rotate Down"** for X-axis rotation
   - Click **"Reset View"** to return to default angle

2. **Understand the Display**
   - White sphere in center = nucleus
   - Colored particles = electrons
   - Particle size/opacity = probability amplitude
   - Larger/brighter = higher probability

### Generate a Report

1. **Click "Generate Report" Button**
2. **New window opens** with detailed analysis:
   - Element properties
   - Quantum state statistics
   - 3D model generation parameters
   - Center of mass calculations

## Example Elements to Try

| Element | Why Interesting |
|---------|-----------------|
| **H** (Hydrogen) | Simplest element, 1 electron |
| **He** (Helium) | Noble gas, 2 electrons |
| **C** (Carbon) | Organic chemistry basis, 6 electrons |
| **O** (Oxygen) | Highly electronegative, 8 electrons |
| **Fe** (Iron) | Transition metal, 26 electrons |
| **Cu** (Copper) | Conductive metal, 29 electrons |

## Understanding the Visualization

### 3D Electron Cloud

The visualization shows a quantum simulation of electron behavior:

- **Center Point**: Nucleus (protons + neutrons)
- **Electron Particles**: Probability distribution of electrons
- **Color**: Based on element classification
- **Size**: Represents quantum amplitude at that position
- **Opacity**: Confidence level of that electron position

### Quantum State Graph

The bottom-right shows a timeline of quantum amplitudes:

- **X-axis**: Different quantum states (0-1023)
- **Y-axis**: Probability amplitude
- **Curve**: Shows peak probability at ground state

## Keyboard Shortcuts (Future Enhancement)

- `Ctrl+A`: Analyze current element
- `Ctrl+R`: Generate report
- `Space`: Toggle animation
- `Escape`: Close report window

## Troubleshooting

### Application Won't Start

**Error**: "Failed to create CoreCLR"
**Solution**: Ensure .NET 8.0 SDK is installed
```bash
dotnet --version  # Check version
```

### Quantum Simulation Timeout

**Error**: "Simulation exceeded timeout"
**Solution**: Reduce element complexity or check system resources

### 3D Visualization Not Rendering

**Error**: Black screen in visualization panel
**Solution**: 
1. Click "Reset View" to refresh
2. Ensure graphics drivers are updated
3. Try analyzing a different element

## Performance Tips

- **Faster Analysis**: Select light elements (H, He, C)
- **Better Performance**: Run on machines with 4+ GB RAM
- **Smooth Rotation**: Close other applications during use

## Next Steps

### Learn More

- Read [README.md](README.md) for detailed documentation
- Check [QUANTUM_INTEGRATION.md](QUANTUM_INTEGRATION.md) for technical details
- Review [DEVELOPMENT.md](DEVELOPMENT.md) for development setup

### Extend the Application

- Add more elements to the database
- Create new Q# quantum operations
- Implement molecular simulations
- Export 3D models

### Deploy to Cloud

1. Set up Azure Quantum account
2. Update connection strings in `QuantumProcessor.cs`
3. Deploy to Azure (see DEVELOPMENT.md)

## Support & Feedback

For issues or suggestions:
1. Check the documentation files
2. Review the code comments
3. Consult Q# language documentation

---

**Happy exploring!** 🚀
