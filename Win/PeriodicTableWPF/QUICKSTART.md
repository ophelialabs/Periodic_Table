# Quick Start Guide

## Installation

### Prerequisites
1. **Visual Studio 2022** or later (Community Edition works)
   - Install ".NET desktop development" workload
   - Install "Desktop development with C++" (for graphics)

2. **Microsoft Quantum Development Kit**
   ```bash
   dotnet workload restore
   ```

3. **.NET 8.0 SDK**
   ```bash
   dotnet --version  # Should be 8.0 or higher
   ```

### Setup Steps

1. **Clone/Extract Project**
   ```bash
   cd PeriodicTableWPF
   ```

2. **Restore Dependencies**
   ```bash
   dotnet restore
   ```

3. **Build Solution**
   ```bash
   dotnet build
   ```

4. **Run Application**
   ```bash
   dotnet run --project PeriodicTableApp
   ```

## First Time Usage

### 1. Launch Application
- The main window displays a periodic table on the left
- Center area shows 3D visualization (initially empty)
- Right panel shows element properties

### 2. Select an Element
- Click on any element from the periodic table list
- Element name and properties appear in the right panel
- Status bar shows: "Selected: [Element Name]"

### 3. Run Quantum Simulation
- Click "Simulate Element" button
- Progress bar shows simulation progress
- Status updates in real-time
- 3D electron cloud renders in center viewport

### 4. Explore Molecular Bonding
- Select first element (already selected)
- Choose second element from dropdown
- Click "Simulate Bond"
- Visualization shows both atoms connected by bond

## Key Features to Try

### Element Properties
- **Atomic Number**: Unique identifier (1-118)
- **Atomic Mass**: Weight in amu
- **Electron Configuration**: Shell notation
- **Quantum Properties** (after simulation):
  - Conductivity (blue to green)
  - Density (height bar)
  - Hardness (red intensity)
  - Reactivity (yellow intensity)

### 3D Interactions
- **Rotate**: Click and drag in 3D viewport
- **Zoom**: Mouse wheel
- **Pan**: Right-click and drag

### Quantum Simulations
- **Single Element**: Fast (~100ms local)
- **Molecular Bond**: Medium (~500ms local)
- **Material Composite**: Slower (depends on number of elements)

## Troubleshooting

### Build Errors
**Error**: "The type or namespace name 'Model3D' could not be found"
- **Solution**: Add reference to `System.Windows.Media.Media3D`
- In `.csproj`: Already included with `UseWPF=true`

**Error**: "Microsoft.Quantum.Sdk not found"
- **Solution**: Run `dotnet workload restore`
- Or install QDK extension in Visual Studio

### Runtime Issues
**Problem**: Viewport shows nothing
- **Solution**: Check viewport initialization in `MainWindow.xaml.cs`
- Verify `Camera` position: Position="0,0,4"

**Problem**: Simulation doesn't start
- **Solution**: Check selection in Status bar
- Ensure "IsLoading" is false
- Check error message in status bar

**Problem**: 3D model is too small/large
- **Solution**: Adjust mesh generation scale in `ElementVisualizer.cs`
- Modify radius parameters: `AddSphereMesh(..., radius, ...)`

## Project Customization

### Adding More Elements
Edit `PeriodicTableDataService.cs`:
```csharp
new Element { 
    AtomicNumber = 10, 
    Symbol = "Ne", 
    Name = "Neon",
    // ... other properties
}
```

### Changing 3D Colors
In `Element.cs`:
```csharp
public string Color { get; set; } = "#FFFFFF";  // Hex color
```

Or in `ElementVisualizer.cs`:
```csharp
System.Windows.Media.Color shellColor = 
    InterpolateColor(Colors.Blue, Colors.Green, probability);
```

### Adjusting Quantum Parameters
In `QuantumProcessor.cs`:
```csharp
// Increase/decrease qubit allocation
use qubits = Qubit[number];

// Modify simulation complexity
for i in 0..iterations - 1 { ... }
```

## Understanding the Output

### Electron Cloud Visualization
- **Red Center**: Nucleus (proton)
- **Blue-Green Spheres**: Electron probability shells
- **Yellow Dots**: Individual electron positions
- **Size**: Larger shells = higher probability of finding electron

### Molecular Bond Visualization
- **Left Sphere**: First element (colored)
- **Right Sphere**: Second element (colored)
- **Orange Cylinder**: Bond between atoms
- **Thickness**: Proportional to bond strength

### Material Structure
- **Cyan-Red Lattice**: Crystal structure
- **Size of Atoms**: Related to material hardness
- **Lighting Color**: Related to conductivity

## Performance Tips

### For Smooth Performance
1. **Use Local Simulator**: Faster than cloud
2. **Reduce Sample Points**: Lower in SimulateElectronOrbital
3. **Cache Results**: Reuse previous simulations
4. **Simplify Meshes**: Reduce longitude/latitude divisions

### Azure Quantum (Production)
1. **Set up credentials**: Configure Azure auth
2. **Enable cloud mode**: `new QuantumProcessor("ionq", useAzure: true)`
3. **Monitor costs**: Quantum jobs are billed by minute
4. **Use error mitigation**: Enable noise handling

## Next Steps

1. **Explore Code**:
   - Read `Element.cs` for data model
   - Study `QuantumProcessor.cs` for Q# integration
   - Review `ElementVisualizer.cs` for 3D generation

2. **Run Specific Simulations**:
   - Try different elements (H, He, C, Fe, Au)
   - Compare bond simulations
   - Analyze material composites

3. **Extend Functionality**:
   - Add more elements to database
   - Implement new visualization modes
   - Create analysis tools

4. **Deploy to Cloud**:
   - Register Azure Quantum workspace
   - Submit simulations to real hardware
   - Collect and analyze results

## Support & Resources

- **Q# Documentation**: https://learn.microsoft.com/quantum/
- **WPF Learning**: https://learn.microsoft.com/dotnet/desktop/wpf/
- **Quantum Computing Basics**: https://learn.microsoft.com/quantum/concepts/
- **GitHub Issues**: Report bugs or suggest features

## Example Workflows

### Workflow 1: Element Analysis
1. Select Hydrogen (H)
2. Click "Simulate Element"
3. Observe: Simple electron cloud (1 electron)
4. Compare properties to other elements

### Workflow 2: Bond Formation Study
1. Select Carbon (C)
2. Choose Oxygen (O) from dropdown
3. Click "Simulate Bond"
4. Note: Strong bond (O-C bond strength shown)
5. Try Carbon-Hydrogen next

### Workflow 3: Material Property Exploration
1. Select Iron (Fe)
2. Simulate element (observe: metallic properties)
3. Then simulate Fe-O bond (iron-oxygen)
4. Analyze predicted material properties

## Keyboard Shortcuts

- **F5**: Run simulation (if available)
- **Ctrl+Z**: Clear visualization
- **Escape**: Deselect element

(These can be extended in `MainWindow.xaml`)

## Contact & Feedback

For issues, questions, or contributions:
- Check README.md for architecture details
- Review QSH_INTEGRATION.md for Q# specifics
- Examine code comments for implementation notes
