# Interactive Periodic Table with Quantum Research

A modern, interactive web application showcasing the periodic table of elements integrated with Q# quantum simulations for atomic modeling and electron distribution visualization.

## Features

- **Interactive Periodic Table**: Click elements to view detailed properties
- **3D Atomic Models**: Visualize electron shells and orbital configurations
- **Quantum Simulations**: Run Q# quantum algorithms to simulate electron distributions
- **Real-time Visualization**: Dynamic 3D electron cloud rendering
- **Material Properties**: Generate and display material properties based on quantum results
- **Data Plots**: Visualize quantum state probability distributions

## Project Structure

```
PeriodicTableWeb/              # Blazor Server web application
├── Components/               # Razor components
│   ├── Pages/              # Page components
│   │   └── PeriodicTable.razor
│   └── Layout/             # Layout components
├── Models/                 # Data models
├── Services/               # Business logic
├── Program.cs              # Application startup
└── PeriodicTableWeb.csproj

PeriodicTableQuantum/          # Q# quantum operations
├── src/
│   └── QuantumRD.qs       # Quantum algorithms
└── PeriodicTableQuantum.csproj
```

## Architecture

### C# Services
- **ElementDataService**: Manages periodic table element data
- **ResearchAgentManager**: Orchestrates 3D model generation and quantum simulations
- **DynamicModelGenerator**: Converts quantum results to 3D visualizations
- **LocalQuantumProcessor**: Simulates quantum operations locally
- **QuantumProcessor**: Interface for quantum operations

### Q# Operations
- `SimulateElectronDistribution`: Simulates electron probability distributions
- `SimulateOrbitalPhase`: Models orbital phase relationships
- `CalculateElectronDensity`: Computes electron density amplitudes

### Data Flow
1. User selects element → `ElementDataService` loads properties
2. `ResearchAgentManager` generates 3D atomic model
3. 3D model displayed in UI
4. User runs simulation → `LocalQuantumProcessor` executes Q# operations
5. `DynamicModelGenerator` converts results to 3D electron spheres
6. Results visualized with probability distribution charts

## Getting Started

### Prerequisites
- .NET 8.0 SDK
- Q# Development Kit (included with QDK)
- VS Code with C# and Q# extensions

### Build

```bash
dotnet build
```

### Run

```bash
dotnet watch run
```

Navigate to `https://localhost:5001/periodic-table`

## Integration with Q#

The application uses a **local quantum processor** that:
1. Allocates qubits
2. Applies quantum gates (H, Ry, Rz, X, Z)
3. Measures qubits
4. Returns classical probability distributions
5. Resets qubits for resource management

To deploy to Azure Quantum (IonQ):
1. Set up Azure Quantum workspace
2. Configure `AzureQuantumProcessor` service
3. Update `Program.cs` dependency injection
4. Submit jobs to IonQ target

## Technical Details

### Quantum Algorithms
- **Superposition**: Creates equal superposition of electron states
- **Controlled Rotations**: Simulates orbital interactions
- **Phase Oracles**: Marks low-energy states
- **Measurement**: Collapses quantum state to classical results

### 3D Visualization
- Nucleus rendered as core sphere
- Electron clouds positioned at orbital radii
- Electron spheres colored by shell number
- Opacity represents probability amplitude
- Interactive canvas with zoom/pan capabilities

### Probability Distributions
- Generated from quantum measurement outcomes
- Smoothed across adjacent states
- Normalized for valid probability interpretation
- Visualized as bar charts showing state amplitudes

## Development Guidelines

See `.github/copilot-instructions.md` for detailed development standards and integration guidelines.

## Future Enhancements

- [ ] 3D interactive visualization with Three.js
- [ ] Full periodic table (all 118 elements)
- [ ] Azure Quantum integration for real quantum hardware
- [ ] Advanced orbital visualization (p, d, f orbitals)
- [ ] Molecular bonding simulations
- [ ] Performance optimization for large simulations
- [ ] Export results as charts/data

## License

This project is provided as-is for educational and research purposes.

## Support

For issues and questions, refer to the Q# documentation at https://learn.microsoft.com/quantum/


