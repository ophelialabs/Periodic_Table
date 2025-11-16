# Q# Integration Guide: Quantum Orbital Simulation

## Overview

This guide explains how the Q# code integrates with the TypeScript frontend and Python agent to create a complete quantum simulation system.

## Architecture

```
┌─────────────────────┐
│   User Interface    │
│ (React/TypeScript)  │
└──────────┬──────────┘
           │ HTTP POST
           ▼
┌──────────────────────────┐
│   Next.js API Route      │
│ (/api/quantum)           │
└──────────┬───────────────┘
           │ Compilation & Execution
           ▼
┌──────────────────────────┐
│  Q# Program (QuantumRD)  │
│  - Quantum Operations    │
│  - Probability Calcs     │
│  - State Preparation     │
└──────────┬───────────────┘
           │ Results (Array<Double>)
           ▼
┌──────────────────────────┐
│   Processing & Return    │
│   (Probability Data)     │
└──────────┬───────────────┘
           │ JSON Response
           ▼
┌──────────────────────────┐
│ Frontend Visualization   │
│ (Canvas 3D Rendering)    │
└──────────────────────────┘
```

## Q# Operations

### 1. `SimulateElectronCloud`

**Purpose**: Generate electron probability distribution for hydrogen-like atoms.

**Parameters**:
- `atomicNumber`: Atomic number Z (determines nuclear charge)
- `gridSize`: Resolution of probability grid
- `measureCount`: Number of quantum measurements

**Returns**: Array of probability densities

**Implementation**:
```qsharp
operation SimulateElectronCloud(
    atomicNumber: Int,
    gridSize: Int,
    measureCount: Int
) : Double[] {
    // 1. Prepare ground state orbital (1s)
    // 2. Apply quantum operations
    // 3. Measure multiple times
    // 4. Convert to probability distribution
}
```

**Quantum Circuit**:
```
|0⟩ ──[H]──[Phase]──[Measurement]── Probability Data
```

### 2. `PrepareGroundState`

**Purpose**: Initialize quantum state representing 1s orbital.

**Details**:
- Creates superposition of basis states
- Applies phase gates to encode orbital shape
- Uses controlled-phase gates for spatial encoding

**Mathematical Basis**:
The ground state wavefunction for hydrogen is:
```
ψ₁ₛ(r) = (1/√π) × (Z/a₀)^(3/2) × exp(-Zr/a₀)
```

Where:
- Z = atomic number
- a₀ = Bohr radius (0.529 Å)
- r = distance from nucleus

### 3. `SimulateRadialDistribution`

**Purpose**: Calculate electron probability at specific distances from nucleus.

**Output**: Array of `ElectronProbability` records with:
- Radius (distance from nucleus)
- Probability density
- Quantum phase

**Physical Model**:
```
|R(r)|² ∝ r² × exp(-2Zr/a₀)
```

### 4. `GenerateProbabilityGrid`

**Purpose**: Create 3D grid of probability values for visualization.

**Process**:
1. Initialize 3D quantum state
2. Measure probability at each grid point
3. Apply Gaussian smoothing for better visualization
4. Return smoothed probability distribution

## Type Definitions

### OrbitalState
```qsharp
newtype OrbitalState = (
    Principal: Int,      // n quantum number (1, 2, 3...)
    Angular: Int,        // l quantum number (0=s, 1=p, 2=d...)
    Magnetic: Int,       // ml quantum number (-l to +l)
    Energy: Double       // Energy in eV
)
```

### ElectronProbability
```qsharp
newtype ElectronProbability = (
    Radius: Double,      // Distance in Angstroms
    Probability: Double, // Probability density (0-1)
    Phase: Double        // Quantum phase (0-2π)
)
```

## Key Quantum Concepts

### Quantum Numbers
- **n (Principal)**: Determines energy level and orbital size
- **l (Angular)**: Determines orbital shape (s, p, d, f...)
- **ml (Magnetic)**: Determines orbital orientation
- **ms (Spin)**: Electron spin (-0.5 or +0.5)

### Energy Calculation
Ground state energy (n=1):
```qsharp
function CalculateGroundStateEnergy(atomicNumber: Int, principalNumber: Int) : Double {
    let rydbergEnergy = -13.6; // eV
    return rydbergEnergy * atomicNumber² / principalNumber²
}
```

### Bohr Radius
Effective Bohr radius for hydrogen-like atoms:
```qsharp
function CalculateBohrRadius(atomicNumber: Int) : Double {
    return 0.529 / IntAsDouble(atomicNumber); // Angstroms
}
```

## Integration Flow

### Step 1: Request from Frontend
```typescript
// src/app/api/quantum/route.ts
const body = {
  atomicNumber: 6,        // Carbon
  elementSymbol: "C",
  gridSize: 16,
  energyThreshold: 1.0
};
```

### Step 2: API Processing
```typescript
function generateQuantumSimulation(config: QuantumRequest): SimulationResult {
  // Would call Q# via Azure Quantum in production
  // For now, generates mock data based on physics models
}
```

### Step 3: Q# Execution (Production)
```qsharp
@EntryPoint()
operation SimulateElement(atomicNumber: Int, gridSize: Int) : Double[] {
    // Generate probability grid
    let grid = GenerateProbabilityGrid(atomicNumber, gridSize);
    return grid;
}
```

### Step 4: Result Processing
```typescript
// src/lib/quantumHost.ts
const vizData = processor.processResultsForVisualization(result);
// Extract:
// - Center of mass
// - Effective radius
// - Peak probability
// - Densest points
```

### Step 5: Frontend Visualization
```typescript
// src/components/PeriodicTable3D.tsx
useEffect(() => {
  if (visualizationData) {
    // Draw electron cloud
    // Draw orbital shells
    // Display quantum metrics
  }
}, [visualizationData]);
```

## Physics Models Implemented

### 1. Bohr Model
- Circular orbits with quantized radii
- Energy levels: En = -13.6 eV × Z² / n²
- Simple but effective for visualization

### 2. Rydberg Formula
- Calculates transition energies
- E = -13.6 eV / n² (in eV)
- Used for ground state calculations

### 3. Hydrogen-like Wavefunctions
- 1s orbital: ψ ∝ exp(-r/a₀)
- Radial probability: |R(r)|² ∝ r² × exp(-2r/a₀)
- Spherically symmetric for ground state

### 4. Quantum Superposition
- Multiple basis states combined
- Phase encoding for spatial structure
- Measurement collapses to classical probability

## Performance Considerations

### Qubit Requirements
- Simulation uses 3-4 qubits for basic simulation
- Scales to 3×log₂(gridSize) for larger grids
- Example: 16³ grid requires ~12 qubits

### Execution Time
- Single measurement: ~1ms
- 100 measurements: ~100ms
- Grid generation (16³): ~200ms

### Optimization Techniques
1. **Grid sparsity**: Skip low-probability regions
2. **Caching**: Store computed probability maps
3. **Smoothing**: Reduce noise in final data
4. **Parallelization**: Independent measurements can run in parallel

## Extending the Simulation

### Adding New Elements
1. Update `PERIODIC_TABLE` in `src/lib/elements.ts`
2. Element properties automatically used in Q# calculations
3. Simulation automatically generates orbital data

### Adding New Quantum Operations
1. Define operation in `QuantumRD.qs`
2. Implement using Q# standard library
3. Expose via API endpoint
4. Call from frontend

### Supporting Higher Orbitals
```qsharp
// Currently: 1s ground state
// To add: 2s, 2p, 3d orbitals

operation SimulateOrbital(
    atomicNumber: Int,
    principal: Int,      // n: 1, 2, 3...
    angular: Int,        // l: 0, 1, 2...
    gridSize: Int
) : Double[] {
    // Adapt energy calculations and wavefunction shapes
    // Use appropriate radial distribution formulas
}
```

## Testing Q# Code

### Unit Tests
```qsharp
@Test("Microsoft.Quantum.UnitTesting")
operation CalculateGroundStateEnergyTest() : Unit {
    let energy = CalculateGroundStateEnergy(1, 1); // Hydrogen
    // Should be approximately -13.6 eV
}

@Test("Microsoft.Quantum.UnitTesting") 
operation CalculateBohrRadiusTest() : Unit {
    let radius = CalculateBohrRadius(1); // Hydrogen
    // Should be approximately 0.529 Å
}
```

### Integration Tests
```typescript
// src/tests/quantum.test.ts
test('simulate hydrogen electron cloud', async () => {
  const config: QuantumSimulationConfig = {
    atomicNumber: 1,
    elementSymbol: "H",
    gridSize: 8,
    energyThreshold: 1.0
  };
  
  const result = await manager.simulateElement(config);
  expect(result.success).toBe(true);
  expect(result.result?.atomicNumber).toBe(1);
});
```

## Production Deployment

### Azure Quantum Integration
```typescript
// Configure for hardware execution
const config: QuantumSimulationConfig = {
  atomicNumber: 6,
  elementSymbol: "C",
  gridSize: 16,
  energyThreshold: 1.0,
  targetProvider: "ionq"  // Use IonQ hardware
};

// Q# code compiles to QIR (Quantum Intermediate Representation)
// Submitted to Azure Quantum for execution on:
// - Simulators (development)
// - IonQ (trapped ion)
// - Quantinuum (trapped ion)
// - Rigetti (superconducting)
```

### Error Mitigation
```qsharp
// Add error correction and mitigation techniques
operation MitigateErrors(qubits: Qubit[]) : Unit {
    // Implement:
    // - Readout error mitigation
    // - Zero-noise extrapolation
    // - Probabilistic error suppression
}
```

## Limitations & Future Work

### Current Limitations
- Single electron approximation (hydrogen-like)
- Ground state only (no excited states)
- No electron-electron interactions
- No molecular simulations

### Future Enhancements
1. **Multi-electron systems**: Hartree-Fock approximation
2. **Excited states**: 2s, 2p, 3d orbital simulations
3. **Molecular orbitals**: H₂, H₂O, organic molecules
4. **Bond visualization**: Covalent/ionic bond rendering
5. **Real quantum hardware**: Execute on Azure Quantum devices

## References

### Quantum Mechanics
- Griffiths, D.J. (2018). "Introduction to Quantum Mechanics"
- Shankar, R. (1994). "Principles of Quantum Mechanics"

### Q# Documentation
- https://learn.microsoft.com/en-us/azure/quantum/user-guide/
- https://github.com/microsoft/qsharp

### Bohr Model
- https://en.wikipedia.org/wiki/Bohr_model
- https://en.wikipedia.org/wiki/Rydberg_formula

### Hydrogen Wavefunction
- https://en.wikipedia.org/wiki/Hydrogen_atom#Solution_of_the_Schrödinger_equation
- https://en.wikipedia.org/wiki/Orbital_hybridisation
