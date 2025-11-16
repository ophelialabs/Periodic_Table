# INSTALLATION & SETUP GUIDE

## System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.9 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB for application + dependencies

## Step-by-Step Installation

### Step 1: Verify Python Installation

```bash
python --version
# Should output: Python 3.9.x or higher
```

If Python is not installed:
- **Windows**: Download from https://www.python.org/downloads/
- **macOS**: `brew install python3`
- **Linux**: `sudo apt-get install python3`

### Step 2: Clone or Download Project

```bash
# Option A: Using git (if available)
git clone https://github.com/yourrepo/PeriodicTableCP.git
cd PeriodicTableCP

# Option B: Download and extract ZIP file
unzip PeriodicTableCP.zip
cd PeriodicTableCP
```

### Step 3: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 4: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Verify Tkinter Installation

```bash
python -m tkinter
```

This should open a test window. If it fails:
- **Windows**: Tkinter is included with Python
- **macOS**: Usually included, run `brew install python-tk3`
- **Linux**: `sudo apt-get install python3-tk`

### Step 6: (Optional) Install Q# SDK

For quantum operation compilation:

```bash
# Install .NET SDK first (if needed)
# https://dotnet.microsoft.com/download

# Install Q# tool
dotnet tool install -g Microsoft.Quantum.IQSharp

# Verify installation
qsharp --version
```

### Step 7: Launch Application

```bash
python main.py
```

The application window should open immediately.

## Configuration

### Local Mode (Default)

No configuration needed! Works out of the box with local quantum simulation.

### Azure Quantum Mode

To enable quantum hardware access:

1. **Create Azure Account**
   - Visit https://azure.microsoft.com
   - Create free account or sign in

2. **Create Quantum Workspace**
   - Navigate to Azure Quantum
   - Create new workspace
   - Note workspace ID, subscription ID, resource group

3. **Configure Credentials**
   - Copy `config.json.example` to `config.json`
   - Fill in your Azure credentials:
   ```json
   {
     "azure_quantum": {
       "enabled": true,
       "workspace_id": "your-workspace-id",
       "subscription_id": "your-subscription-id",
       "resource_group": "your-resource-group",
       "location": "westus",
       "provider": "ionq",
       "target": "ionq.simulator"
     }
   }
   ```

4. **Install Azure SDK**
   ```bash
   pip install azure-quantum
   ```

5. **Authenticate**
   ```bash
   az login
   ```

## Troubleshooting Installation

### Issue: "Python not found"
**Solution**: Python not in PATH
- **Windows**: Reinstall Python, check "Add Python to PATH" option
- **macOS/Linux**: Use `python3` instead of `python`

### Issue: "ModuleNotFoundError: No module named 'tkinter'"
**Solution**: Install tkinter
```bash
# Windows - Usually included
# macOS
brew install python-tk@3.9

# Linux (Ubuntu/Debian)
sudo apt-get install python3-tk

# Linux (Fedora)
sudo dnf install python3-tkinter

# Linux (Arch)
sudo pacman -S tk
```

### Issue: "Permission denied" on macOS/Linux
**Solution**: Make script executable
```bash
chmod +x main.py
```

### Issue: Application won't start
**Solution**: Check Python compatibility
```bash
python --version  # Must be 3.9+
pip list          # Verify packages installed
python -m tkinter  # Test tkinter
```

### Issue: "ImportError" when launching
**Solution**: Reinstall dependencies
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Issue: Quantum simulations fail
**Solution**: Verify Q# installation
```bash
qsharp --version
dotnet --version
```

## Verification

After installation, verify everything works:

```bash
# Test 1: Check Python
python --version

# Test 2: Check imports
python -c "import tkinter; print('Tkinter OK')"
python -c "from src.element import Element; print('Element module OK')"

# Test 3: Start application
python main.py

# Test 4: Search for element
# In app, type "hydrogen" or "H" in search box

# Test 5: Run simulation
# Select element, click "Analyze" button
```

## Platform-Specific Notes

### Windows

**Installation**
```bash
py -3.9 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
py main.py
```

**Common Issues**:
- Ensure Python added to PATH during installation
- Use `py` instead of `python` if needed
- Visual C++ build tools may be required for some packages

### macOS

**Installation**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

**Common Issues**:
- Use `python3` and `pip3` explicitly
- May need Xcode Command Line Tools: `xcode-select --install`
- Tkinter: `brew install python-tk@3.x`

### Linux

**Installation (Ubuntu/Debian)**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-tk
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

**Installation (Fedora)**
```bash
sudo dnf install python3 python3-pip python3-tkinter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Advanced Configuration

### Custom Data

Add more elements to `src/element_database.py`:

```python
elements_data = [
    # ... existing elements ...
    Element(
        atomic_number=119,
        symbol='Uue',
        name='Ununennium',
        # ... properties
    ),
]
```

### Performance Tuning

Edit `config.json` to optimize:

```json
{
  "simulation": {
    "num_qubits": 4,
    "max_iterations": 100,
    "precision": "double"
  }
}
```

### UI Customization

Modify GUI appearance in `config.json`:

```json
{
  "ui": {
    "window_width": 1600,
    "window_height": 1000,
    "font_size": 10,
    "theme": "clam"
  }
}
```

## Uninstallation

### Remove Application

```bash
# Deactivate virtual environment
deactivate

# Remove project folder
rm -rf PeriodicTableCP

# Remove virtual environment (if created)
rm -rf venv
```

### Clean Python Installation

```bash
pip uninstall -r requirements.txt
pip cache purge
```

## Getting Help

1. **Check README.md**: Full documentation
2. **Check QUICKSTART.md**: Common tasks
3. **Check DEVELOPER.md**: Technical details
4. **Check Q# docs**: https://docs.microsoft.com/quantum

## Next Steps After Installation

1. **Launch Application**: `python main.py`
2. **Read QUICKSTART.md**: Learn basic usage
3. **Explore Periodic Table**: Browse elements
4. **Run Simulations**: Analyze quantum properties
5. **Configure Azure** (optional): Enable real quantum hardware

## Environment Variables

Optional environment configuration:

```bash
# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Enable debug logging
export DEBUG=1

# Set log level
export LOG_LEVEL=DEBUG
```

## Accessing Help

From within the application:
- Click "Help" → "About" for information
- Hover over buttons for tooltips
- Check "Tasks" tab for execution status

## System Health Check

Verify installation completeness:

```bash
# Create diagnostic script
cat > check_install.py << 'EOF'
import sys
print(f"Python: {sys.version}")

try:
    import tkinter
    print("✓ Tkinter installed")
except:
    print("✗ Tkinter NOT installed")

try:
    from src.element import Element
    print("✓ Element module loaded")
except Exception as e:
    print(f"✗ Element module error: {e}")

try:
    from src.research_agent import ResearchAgentManager
    print("✓ Research agent loaded")
except Exception as e:
    print(f"✗ Research agent error: {e}")

print("\nInstallation check complete!")
EOF

python check_install.py
```

---

**Installation Complete!** 🎉

You're ready to use the Interactive Periodic Table with Quantum Research Agent.

For detailed usage instructions, see **QUICKSTART.md** or **README.md**.
