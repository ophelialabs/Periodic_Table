# Developer Guide - Periodic Table with Quantum Research Agent

## Overview

This document provides technical guidance for developers working on the Interactive Periodic Table application.

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────┐
│         Desktop Application (Tkinter GUI)           │
│                   main_app.py                       │
└──────────────────────┬──────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   ┌─────────┐  ┌───────────┐  ┌──────────┐
   │ Element │  │ Research  │  │  Model   │
   │ Visual  │  │  Agent    │  │Generator │
   └─────────┘  └─────┬─────┘  └──────────┘
                      │
        ┌─────────────▼──────────────┐
        │  QuantumProcessor          │
        │  (Local + Azure)           │
        └─────────────┬──────────────┘
                      │
        ┌─────────────┴──────────────┐
        │                            │
        ▼                            ▼
   ┌──────────┐            ┌──────────────────┐
   │ Q# Code  │            │ Azure Quantum    │
   │ Simulator│            │ (IonQ, etc.)     │
   └──────────┘            └──────────────────┘
```

## Module Reference

### Core Modules

#### 1. `element.py` - Element Data Structure

Defines the fundamental Element class and properties.

**Key Classes:**
- `Element`: Dataclass representing a chemical element
- `ElementState`: Enum for physical states

**Key Methods:**
- `get_electron_count()`: Returns atomic number (for neutral atoms)
- `get_valence_electrons()`: Extract valence electron count
- `is_metal()` / `is_nonmetal()`: Category checks
- `get_bohr_radius_estimation()`: Calculate approximate Bohr radius
- `to_dict()`: Serialize to dictionary

**Example Usage:**
```python
from src.element import Element, ElementState

hydrogen = Element(
    atomic_number=1,
    symbol='H',
    name='Hydrogen',
    atomic_mass=1.008,
    # ... other properties
)

print(f"Bohr radius: {hydrogen.get_bohr_radius_estimation():.2f} Å")
```

#### 2. `element_database.py` - Element Data Management

Manages the complete periodic table database.

**Key Classes:**
- `ElementDatabase`: Stores and retrieves element information

**Key Methods:**
- `get_element(atomic_number)`: Get element by Z value
- `get_element_by_symbol(symbol)`: Get element by symbol
- `get_elements_by_category(category)`: Filter by type
- `get_elements_by_period(period)` / `get_elements_by_group(group)`: Get row/column
- `search_elements(query)`: Full-text search
- `get_all_elements()`: Get all elements sorted by atomic number

**Example Usage:**
```python
from src.element_database import ElementDatabase

db = ElementDatabase()
oxygen = db.get_element(8)
metals = db.get_elements_by_category("Metal")
results = db.search_elements("iron")
```

#### 3. `element_visual.py` - GUI Components

Tkinter-based visual components for displaying elements.

**Key Classes:**
- `ElementVisual`: Individual element tile widget
- `ElementDetailView`: Tabbed detail panel for element properties

**Key Methods:**
- `ElementVisual.select()` / `deselect()`: Selection state management
- `ElementVisual.update_quantum_data(data)`: Update with quantum results
- `ElementVisual._draw_bohr_model()`: Render atomic model
- `ElementDetailView.set_element(element)`: Update displayed element

**Example Usage:**
```python
from src.element_visual import ElementVisual

def on_select(element):
    print(f"Selected: {element.name}")

visual = ElementVisual(parent_frame, element, on_select=on_select)
visual.update_quantum_data({'probabilities': [0.1, 0.2, ...], 'orbital_data': {...}})
```

#### 4. `research_agent.py` - Quantum Research Management

Orchestrates quantum simulations and research tasks.

**Key Classes:**
- `ResearchTaskType`: Enum of available research types
- `ResearchTask`: Represents a single research job
- `QuantumProcessor`: Interface to quantum execution
- `ResearchAgentManager`: Main orchestrator

**Key Methods (ResearchAgentManager):**
- `create_research_task(task_type, element, parameters)`: Create a task
- `execute_task_async(task_id, on_complete)`: Run asynchronously
- `execute_task_sync(task_id)`: Run synchronously (blocking)
- `get_task_result(task_id)`: Get results after completion
- `create_and_run_orbital_analysis(element, n, on_complete)`: Convenience method

**Task Types:**
- `MOLECULAR_SIMULATION`: Model molecular structures
- `ELECTRON_ORBITAL`: Simulate orbital states
- `BINDING_ENERGY`: Calculate binding strengths
- `QUANTUM_STATE`: General quantum state analysis
- `MATERIAL_PROPERTY`: Predict material characteristics

**Example Usage:**
```python
from src.research_agent import ResearchAgentManager, ResearchTaskType

manager = ResearchAgentManager()

def on_complete(task):
    if task.status == "completed":
        print(f"Results: {task.result}")
    else:
        print(f"Error: {task.error}")

task_id = manager.create_research_task(
    ResearchTaskType.ELECTRON_ORBITAL,
    element,
    {'n': 2, 'l': 0}
)
manager.execute_task_async(task_id, on_complete)
```

#### 5. `model_generator.py` - 3D Model Generation

Creates 3D molecular and orbital models.

**Key Classes:**
- `Vector3D`: 3D vector with operations
- `Atom`: Represents an atom in 3D space
- `Bond`: Represents a chemical bond
- `OrbitalType`: Enum for orbital types (s, p, d, f)
- `MolecularGeometry`: VSEPR geometry predictions
- `OrbitalVisualizer`: Generates orbital mesh data
- `MolecularModel`: Complete molecular representation

**Key Methods:**
- `MolecularGeometry.predict_geometry()`: VSEPR predictions
- `MolecularGeometry.generate_positions()`: 3D atom positioning
- `OrbitalVisualizer.generate_orbital_surface()`: Mesh generation
- `MolecularModel.add_atom()` / `add_bond()`: Build models
- `MolecularModel.get_mesh_data()`: Get rendering data
- `MolecularModel.calculate_properties()`: Compute properties

**Example Usage:**
```python
from src.model_generator import MolecularModel, OrbitalType, OrbitalVisualizer, Vector3D

# Create molecular model
model = MolecularModel("H2O")
model.add_atom("O", Vector3D(0, 0, 0), 8)
model.add_atom("H", Vector3D(0.96, 0, 0), 1)
model.add_atom("H", Vector3D(-0.96, 0, 0), 1)
model.add_bond(0, 1)
model.add_bond(0, 2)

mesh = model.get_mesh_data()
props = model.calculate_properties()

# Generate orbital visualization
orbital_mesh = OrbitalVisualizer.generate_orbital_surface(OrbitalType.P_ORBITAL, n=2, l=1)
```

#### 6. `main_app.py` - Main GUI Application

The primary Tkinter application.

**Key Classes:**
- `PeriodicTableApp`: Main application window (tk.Tk subclass)

**Key Methods:**
- `_create_main_layout()`: Build UI
- `_populate_periodic_table()`: Display elements
- `_on_element_selected(element)`: Handle selection
- `_analyze_orbital()`: Run orbital analysis
- `_run_quantum_sim()`: Execute simulation
- `_show_3d_model()`: Display 3D representation

**Features:**
- Periodic table grid with search/filter
- Element detail panels
- Quantum data visualization
- Task status tracking

## Q# Integration

### Q# File Structure

`quantum/QuantumRD.qs` contains quantum operations:

```qsharp
namespace QuantumRD {
    operation CalculateElectronOrbital(...) : (Double[], Double) { ... }
    operation SimulateMolecularStructure(...) : (Double[], Double, Double) { ... }
    operation AnalyzeMaterialProperties(...) : (Double, Double[], Double) { ... }
    // Additional operations...
}
```

### Calling Q# from Python

**Method 1: Direct Invocation (requires Q# SDK)**
```python
# This would use Microsoft.Quantum.IQSharp
# Not directly callable from Python without QDK integration
```

**Method 2: Via Azure Quantum (Recommended)**
```python
from utils.azure_quantum_integration import QuantumSimulationRunner

runner = QuantumSimulationRunner(config)
results = runner.run_orbital_analysis(atomic_number=8, n=2, l=1)
```

**Method 3: Local Simulation**
```python
from src.research_agent import QuantumProcessor

processor = QuantumProcessor()
result = processor.run_quantum_simulation(task)
```

### Q# Operation Details

#### CalculateElectronOrbital
Simulates electron probability distribution in orbital.

**Input Parameters:**
- `atomicNumber` (Int): Element Z value
- `principalQuantumNumber` (Int): Orbital level n
- `angularMomentumQuantumNumber` (Int): Orbital type l

**Output:**
- Array of Double: Probability amplitudes for states
- Double: Energy level in eV

**Algorithm:**
1. Initialize 4 qubits in superposition
2. Apply controlled phase rotations based on quantum numbers
3. Measure and collect state probabilities
4. Calculate Bohr model energy: E_n = -13.6 × Z / n² eV

#### SimulateMolecularStructure
Models bonding in diatomic molecules.

**Input Parameters:**
- `atom1AtomicNumber` (Int): First atom Z
- `atom2AtomicNumber` (Int): Second atom Z
- `bondOrder` (Double): Bond multiplicity (1, 2, 3)

**Output:**
- Array of Double: Orbital occupancy measurements
- Double: Total molecular energy
- Double: Bond length (Ångströms)

**Algorithm:**
1. Prepare molecular orbital state
2. Apply CNOT ladder for entanglement
3. Apply phase gates weighted by bond order
4. Measure resulting state
5. Calculate bond properties

## Extension Points

### Adding New Research Tasks

1. **Add task type to ResearchTaskType enum:**
```python
class ResearchTaskType(Enum):
    CUSTOM_TASK = "custom_task"
```

2. **Implement simulation method in QuantumProcessor:**
```python
def _simulate_custom(self, task: ResearchTask) -> Dict[str, Any]:
    # Implementation
    return results
```

3. **Add Q# operation:**
```qsharp
operation CustomOperation(...) : ReturnType { ... }
```

### Adding New Elements

Modify `element_database.py`:
```python
def _load_elements(self):
    elements_data = [
        # ... existing elements ...
        Element(
            atomic_number=119,
            symbol='Uue',
            name='Ununennium',
            # ... other properties ...
        ),
    ]
```

### Extending Visualizations

**Custom Orbital Shapes:**
```python
class OrbitalVisualizer:
    @staticmethod
    def _generate_custom_orbital(...) -> Tuple[List, List]:
        # Generate custom vertices and faces
        vertices = [...]
        faces = [...]
        return vertices, faces
```

## Testing

### Unit Tests

Create `tests/test_element.py`:
```python
import unittest
from src.element import Element, ElementState

class TestElement(unittest.TestCase):
    def test_element_creation(self):
        h = Element(...)
        self.assertEqual(h.atomic_number, 1)
    
    def test_valence_electrons(self):
        c = Element(...)
        self.assertEqual(c.get_valence_electrons(), 4)
```

### Integration Tests

Test quantum simulations:
```python
def test_orbital_simulation(self):
    manager = ResearchAgentManager()
    task_id = manager.create_research_task(...)
    result = manager.execute_task_sync(task_id)
    self.assertIn('probabilities', result)
```

## Performance Optimization

### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_element(atomic_number: int) -> Element:
    # Cached element retrieval
    pass
```

### Lazy Loading
```python
class ElementDatabase:
    def __init__(self):
        self._elements = {}
        self._loaded = False
    
    def _ensure_loaded(self):
        if not self._loaded:
            self._load_elements()
```

### Threading
```python
import threading

def execute_task_async(self, task_id: str):
    thread = threading.Thread(target=self._execute_worker, args=(task_id,))
    thread.daemon = True
    thread.start()
```

## Debugging

### Enable Logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Processing element: {element.symbol}")
```

### Profiling
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Code to profile

profiler.disable()
stats = pstats.Stats(profiler)
stats.print_stats()
```

## Azure Quantum Configuration

### Setup Workspace

1. Create Azure account
2. Create quantum workspace
3. Configure credentials

### Configuration File
```json
{
  "workspace_id": "...",
  "subscription_id": "...",
  "resource_group": "...",
  "location": "westus",
  "provider": "ionq"
}
```

## Deployment

### Package Application
```bash
pyinstaller --onefile --windowed src/main_app.py
```

### Create Distribution
```bash
pip install build
python -m build
```

## Contributing Guidelines

1. Follow PEP 8 style guide
2. Add docstrings to all functions
3. Include type hints
4. Write tests for new features
5. Update documentation

## References

- Python Tkinter: https://docs.python.org/3/library/tkinter.html
- Q# Language: https://docs.microsoft.com/quantum
- Azure Quantum: https://azure.microsoft.com/services/quantum/
- Quantum Chemistry: https://en.wikipedia.org/wiki/Quantum_chemistry

---

Last Updated: 2025
