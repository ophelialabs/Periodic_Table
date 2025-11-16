<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Interactive Periodic Table with Quantum Research - Development Guidelines

## Project Overview
This workspace contains a .NET Blazor web application integrated with Q# quantum simulations for visualizing atomic structures and quantum probability distributions.

## Architecture
- **PeriodicTableWeb**: Blazor Server-side web application (C#, Razor)
- **PeriodicTableQuantum**: Q# quantum operations library
- **Services**: Research Agent Manager, Dynamic Model Generator, Element Data Service
- **Models**: Element, 3D Model Data, Quantum Simulation Results

## Key Integration Points
1. **Element Selection**: Triggers 3D atomic model generation
2. **Quantum Simulation**: Runs Q# operations to simulate electron distributions
3. **3D Visualization**: Renders electron clouds and orbital shells
4. **Material Properties**: Generates visual properties based on quantum results

## Q# Standards
- Use QIR target profile for Azure Quantum compatibility
- All operations must be classically callable
- Results returned as measurement probabilities and spatial data
- Support IonQ target for production quantum hardware

## Coding Standards
- Follow C# naming conventions (PascalCase for classes, camelCase for variables)
- Use dependency injection in Blazor components
- Implement proper error handling and logging
- Structure Razor components with clear separation of markup and code

## Testing & Deployment
- Build: `dotnet build`
- Run: `dotnet watch run`
- Deploy to Azure Quantum when validated on local simulator
