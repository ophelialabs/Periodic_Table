# Quick Reference - Periodic Table Quantum Project

## 🚀 Quick Start (30 seconds)

```bash
cd /Users/jesse/periodictable/workspace
chmod +x quickstart.sh
./quickstart.sh
# Opens: https://localhost:5001/periodic-table
```

## 📋 Essential Commands

### Build & Run
```bash
# Build project
dotnet build

# Run once
dotnet run --project PeriodicTableWeb/PeriodicTableWeb.csproj

# Run with auto-reload (recommended)
dotnet watch run --project PeriodicTableWeb/PeriodicTableWeb.csproj

# Clean and rebuild
dotnet clean && dotnet build
```

### Package Management
```bash
# Restore dependencies
dotnet restore

# List installed packages
dotnet list package

# Update specific package
dotnet add PeriodicTableWeb.csproj package PackageName
```

### Testing & Debugging
```bash
# Build specific project
dotnet build PeriodicTableQuantum/PeriodicTableQuantum.csproj

# Run with debug info
dotnet run --configuration Debug

# Check Q# compilation
dotnet build PeriodicTableQuantum/
```

## 📁 Important Files

| File | Purpose | Edit For |
|------|---------|----------|
| `PeriodicTableWeb/Components/Pages/PeriodicTable.razor` | Main UI component | UI changes, layout |
| `PeriodicTableWeb/Services/ElementDataService.cs` | Element data | Add/modify elements |
| `PeriodicTableQuantum/src/QuantumRD.qs` | Quantum algorithms | Quantum logic |
| `PeriodicTableWeb/Services/ResearchAgentManager.cs` | Business logic | Orchestration |
| `PeriodicTableWeb/Program.cs` | App startup | Dependencies, services |
| `.github/copilot-instructions.md` | Development guidelines | Project standards |

## 🔧 VS Code Tasks

**Cmd+Shift+P** → type "Run Task" then select:
- **Build Periodic Table Project** - Compile entire solution
- **Run Periodic Table (Watch Mode)** - Start dev server with auto-reload
- **Restore NuGet Packages** - Download dependencies
- **Clean Build** - Remove artifacts

## 🎯 Project Structure at a Glance

```
PeriodicTableWeb/          ← 🌐 Blazor web app (C#, Razor)
  Components/
    Pages/PeriodicTable.razor  ← Main interactive component
    _Imports.razor             ← Global usings
  Services/                     ← Business logic
  Models/                       ← Data classes
  
PeriodicTableQuantum/      ← ⚛️ Quantum library (Q#)
  src/QuantumRD.qs            ← Quantum operations

.vscode/                   ← VS Code configuration
  tasks.json                 ← Build tasks
  launch.json                ← Debug settings
```

## 🧪 Testing Workflow

1. **Open Application**
   ```bash
   https://localhost:5001/periodic-table
   ```

2. **Select Element** - Click any element button

3. **View Properties** - Check right panel for details

4. **View 3D Model** - See orbital shells listed

5. **Run Simulation** - Click "🚀 Run Quantum Simulation"

6. **Review Results** - Check probability bars and metrics

## 🔍 Code Navigation

### Add a New Element
**File**: `ElementDataService.cs` → `InitializeElements()`
```csharp
new Element { 
    AtomicNumber = 21, 
    Symbol = "Sc", 
    Name = "Scandium",
    // ... add properties
}
```

### Modify Quantum Algorithm
**File**: `QuantumRD.qs` → `SimulateElectronDistribution()`
```q#
// Change gate sequence or add new operations
H(q);  // Hadamard gate
Ry(theta, q);  // Rotation gate
Z(q);  // Phase gate
```

### Update UI Layout
**File**: `PeriodicTable.razor` → CSS section at bottom
```html
<style>
    /* Modify colors, spacing, fonts here */
</style>
```

### Add Service to DI
**File**: `Program.cs`
```csharp
builder.Services.AddSingleton<MyService>();
```

## 🐛 Common Issues

| Problem | Fix |
|---------|-----|
| Port 5001 taken | `lsof -i :5001` → `kill -9 <PID>` |
| Q# errors | `dotnet build PeriodicTableQuantum/` |
| CSS not loading | `dotnet build` + Refresh browser |
| DI resolution error | Check namespace imports in Program.cs |
| Component not found | Verify file in Components folder + @using |

## 📊 Architecture Quick View

```
Browser (UI)
    ↓
PeriodicTable.razor (Component)
    ↓
ResearchAgentManager (Orchestrator)
    ↓
├─ ElementDataService (Data)
├─ DynamicModelGenerator (Visualization)
└─ LocalQuantumProcessor (Quantum)
    ↓
QuantumRD.qs (Q# Operations)
    ↓
Quantum Measurement Results
    ↓
Browser (Updated UI)
```

## 🎨 Element Colors (Category-based)

```csharp
// Modify in ElementDataService.InitializeElements()
"#FFFFFF"  // Nonmetal (White)
"#FFB3B3"  // Noble Gas (Light Red)
"#FF99CC"  // Alkali Metal (Pink)
"#FFFF99"  // Alkaline Earth (Light Yellow)
"#90EE90"  // Metalloid (Light Green)
"#CCCCCC"  // Metal (Gray)
"#3333FF"  // Nonmetal (Blue)
"#FF3333"  // Nonmetal (Red)
// etc.
```

## ⚛️ Q# Operations Reference

```q#
// Allocation
use qubits = Qubit[n];

// Gates
H(qubit);           // Hadamard (superposition)
X(qubit);           // Pauli-X (NOT gate)
Y(qubit);           // Pauli-Y
Z(qubit);           // Pauli-Z (phase)
Rx(angle, qubit);   // Rotation X
Ry(angle, qubit);   // Rotation Y
Rz(angle, qubit);   // Rotation Z

// Multi-qubit
Controlled Op([control], target);

// Measurement & Reset
let result = Measure(basis, qubit);
ResetAll(qubits);
```

## 📈 Performance Tips

- **Minimize DOM updates** in Razor components
- **Cache element data** in ElementDataService
- **Batch quantum operations** when possible
- **Use async/await** for service calls
- **Optimize Q# circuits** to reduce gate count

## 🔗 Useful Links

- **Project GitHub**: Your local folder
- **Q# Documentation**: https://learn.microsoft.com/quantum/
- **Blazor Docs**: https://learn.microsoft.com/aspnet/core/blazor/
- **Azure Quantum**: https://azure.microsoft.com/services/quantum/
- **.NET 8 Docs**: https://learn.microsoft.com/dotnet/

## 💡 Pro Tips

1. **Use VS Code snippets** for faster coding
2. **Enable IntelliSense** for Q# with QDK extension
3. **Debug with breakpoints** using F5
4. **Use browser DevTools** (F12) to inspect network
5. **Check application logs** in browser console
6. **Profile performance** with browser performance tab

## 🚀 Deployment Checklist

- [ ] Test locally: `dotnet run`
- [ ] Build release: `dotnet build -c Release`
- [ ] Test in release mode: `dotnet run -c Release`
- [ ] Check for console errors
- [ ] Verify all elements display correctly
- [ ] Test quantum simulation
- [ ] Check mobile responsiveness
- [ ] Deploy to Azure App Service or IIS

---

**Keep this reference handy for quick access to common tasks!**
