# Quick Start Guide

## Installation

### macOS Prerequisites
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install CMake
brew install cmake

# Install Qt (optional, for UI)
brew install qt6

# Install Q# compiler
dotnet tool install --global Microsoft.Quantum.IQSharp

# Verify installations
cmake --version
clang++ --version
qsharp --version
```

### Windows Prerequisites
```powershell
# Install Visual Studio 2019 or later with C++ workload
# https://visualstudio.microsoft.com/

# Install CMake
choco install cmake

# Install Q# compiler
dotnet tool install --global Microsoft.Quantum.IQSharp

# Verify installations
cmake --version
cl.exe /?  # MSVC compiler
qsharp --version
```

### Linux Prerequisites (Ubuntu 20.04+)
```bash
# Install build essentials
sudo apt-get install build-essential cmake

# Install Q# compiler
dotnet tool install --global Microsoft.Quantum.IQSharp

# Verify
cmake --version
g++ --version
qsharp --version
```

## Project Setup

### 1. Clone and Navigate
```bash
cd /Users/jesse/periodictable/CP/PeriodicTableCP
```

### 2. Build the C++ Library

**Using VS Code Tasks (Recommended)**:
1. Open Command Palette (Cmd+Shift+P on macOS, Ctrl+Shift+P on Windows/Linux)
2. Type "Tasks: Run Task"
3. Select "CMake: Configure"
4. Select "CMake: Build"

**Or from Terminal**:
```bash
# Configure
cmake -B build -S .

# Build
cmake --build build --config Release
```

### 3. Build Q# Quantum Operations
```bash
cd QuantumRD

# Build quantum project
qsharp build

cd ..
```

### 4. Verify Installation
```bash
# Check if library built successfully
ls -la build/libPeriodicTableLib.a  # macOS/Linux
# or
dir build\PeriodicTableLib.lib      # Windows
```

## Creating a Simple Application

### Example 1: Simulate a Single Element

Create `test_carbon.cpp`:

```cpp
#include "ResearchAgentManager.h"
#include "QuantumTargetIntegration.h"
#include <iostream>
#include <memory>

int main() {
    // Create quantum target (local simulator)
    auto simulator = std::make_shared<LocalQuantumSimulator>();
    
    // Create quantum processor
    auto processor = std::make_shared<QuantumProcessor>(simulator);
    
    // Create model generator
    auto model_gen = std::make_shared<ModelGenerator>();
    
    // Create research manager
    auto manager = std::make_shared<ResearchAgentManager>(processor, model_gen);
    
    // Create carbon element
    auto carbon = std::make_shared<ElementData>(6, "C", "Carbon");
    carbon->valence_electrons = 4;
    carbon->electron_configuration = "1s² 2s² 2p²";
    carbon->mass = 12.01;
    
    std::cout << "Simulating " << carbon->name << " (Z=" << carbon->atomic_number << ")\n";
    std::cout << "Valence electrons: " << carbon->valence_electrons << "\n";
    std::cout << "Configuration: " << carbon->electron_configuration << "\n";
    
    try {
        // Run simulation
        auto result = manager->simulate_element(carbon);
        
        if (result) {
            std::cout << "\n=== Simulation Results ===\n";
            std::cout << "Band Gap Energy: " << result->quantum_data.material_properties.band_gap_energy << " eV\n";
            std::cout << "Magnetic Moment: " << result->quantum_data.material_properties.magnetic_moment << " μB\n";
            std::cout << "Number of Orbitals: " << result->quantum_data.electron_orbitals.size() << "\n";
            std::cout << "Success!\n";
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
```

Compile and run:
```bash
g++ -std=c++17 test_carbon.cpp -L build -lPeriodicTableLib -I include -o test_carbon
./test_carbon
```

### Example 2: Molecular Bonding Simulation

Create `test_bonding.cpp`:

```cpp
#include "ResearchAgentManager.h"
#include "QuantumTargetIntegration.h"
#include <iostream>
#include <memory>

int main() {
    auto simulator = std::make_shared<LocalQuantumSimulator>();
    auto processor = std::make_shared<QuantumProcessor>(simulator);
    auto model_gen = std::make_shared<ModelGenerator>();
    auto manager = std::make_shared<ResearchAgentManager>(processor, model_gen);
    
    // Create oxygen and hydrogen elements
    auto oxygen = std::make_shared<ElementData>(8, "O", "Oxygen");
    oxygen->valence_electrons = 6;
    oxygen->electron_configuration = "1s² 2s² 2p⁴";
    
    auto hydrogen = std::make_shared<ElementData>(1, "H", "Hydrogen");
    hydrogen->valence_electrons = 1;
    hydrogen->electron_configuration = "1s¹";
    
    std::cout << "Simulating O-H molecular bonding\n";
    
    try {
        auto result = manager->simulate_molecular_bond(oxygen, hydrogen);
        
        if (result) {
            std::cout << "Bonding simulation complete!\n";
            std::cout << "Molecular properties calculated.\n";
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
```

### Example 3: Element Visualization

Create `test_visualization.cpp`:

```cpp
#include "ElementVisualizationController.h"
#include "ElementData.h"
#include <iostream>
#include <memory>

int main() {
    ElementVisualizationController visualizer;
    
    // Register callbacks
    visualizer.on_element_selected([](const auto& element) {
        std::cout << "Selected element: " << element->name << "\n";
        std::cout << "Atomic number: " << element->atomic_number << "\n";
        std::cout << "Valence electrons: " << element->valence_electrons << "\n";
    });
    
    visualizer.on_visual_update_requested([](const auto& update_data) {
        std::cout << "Visual update requested!\n";
        std::cout << "Number of electrons to render: " << update_data.electron_positions.size() << "\n";
    });
    
    // Create nitrogen element
    auto nitrogen = std::make_shared<ElementData>(7, "N", "Nitrogen");
    nitrogen->valence_electrons = 5;
    nitrogen->electron_configuration = "1s² 2s² 2p³";
    
    // Select element (triggers callbacks)
    visualizer.select_element(nitrogen);
    
    return 0;
}
```

## Azure Quantum Integration

### Setup Steps

1. **Create Azure Account**
   - Go to https://azure.microsoft.com/
   - Create free account or sign in

2. **Create Azure Quantum Workspace**
   - Go to Azure Portal
   - Create new "Azure Quantum" resource
   - Select IonQ as provider
   - Note: workspace name, subscription ID, resource group

3. **Update Code**
   ```cpp
   auto azure_target = std::make_shared<AzureQuantumTarget>(
       "your-subscription-id",      // Azure subscription ID
       "your-resource-group",       // Resource group name
       "your-workspace-name",       // Workspace name
       "ionq.simulator",            // or "ionq.qpu" for hardware
       "your-storage-connection-string"
   );
   ```

4. **Configure Authentication**
   - Install Azure CLI: `brew install azure-cli`
   - Login: `az login`
   - Set subscription: `az account set --subscription <id>`

5. **Submit Simulation**
   ```cpp
   auto processor = std::make_shared<QuantumProcessor>(azure_target);
   auto result = processor->run_quantum_simulation(params, element);
   ```

## Troubleshooting

### CMake Configuration Fails
```bash
# Clear build directory and try again
rm -rf build
cmake -B build -S .
```

### Compilation Errors
```bash
# Check C++ standard
cmake -DCMAKE_CXX_STANDARD=17 -B build -S .

# Verbose output for debugging
cmake --build build --verbose
```

### Q# Compilation Issues
```bash
# Verify Q# installation
qsharp --version

# Rebuild Q# project
cd QuantumRD
qsharp clean
qsharp build
```

### Link Errors
```bash
# Make sure library was built
ls -la build/libPeriodicTableLib.a

# Check library exports
nm build/libPeriodicTableLib.a | grep ElementData
```

## Performance Tips

1. **Use Local Simulator for Development**
   - Faster than Azure for small circuits
   - No network latency
   - Free and immediate results

2. **Reduce Precision for Testing**
   - Lower `desiredPrecision` parameter
   - Fewer iterations needed
   - Faster overall execution

3. **Cache Results**
   - Avoid re-simulating identical elements
   - Store previous results in map
   - Clear cache periodically

4. **Use Release Build**
   ```bash
   cmake --build build --config Release
   ```

## Next Steps

1. **Implement UI Frontend**
   - Use Qt Designer to create periodic table layout
   - Add 3D visualization with OpenGL
   - Connect to ResearchAgentManager

2. **Add Element Database**
   - Load periodic table from CSV/JSON
   - Initialize all elements with proper data
   - Support custom element definitions

3. **Export Results**
   - JSON export for simulation results
   - OBJ/GLTF export for 3D models
   - Publication-ready figure generation

4. **Scale to Production**
   - Add comprehensive error handling
   - Implement logging system
   - Add configuration files
   - Create installer packages

## Additional Resources

- **C++ Documentation**: https://en.cppreference.com/
- **Qt Documentation**: https://doc.qt.io/
- **Q# Documentation**: https://learn.microsoft.com/quantum/
- **Azure Quantum**: https://quantum.microsoft.com/
- **IonQ QPU**: https://ionq.com/

## Support

For issues or questions:
1. Check ARCHITECTURE.md for system design
2. Review code comments for implementation details
3. Check Azure Quantum documentation for quantum questions
4. Review Q# examples in Microsoft documentation
