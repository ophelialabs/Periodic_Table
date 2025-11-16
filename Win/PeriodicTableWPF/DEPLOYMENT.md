# Deployment Guide

## Overview

This guide covers deployment scenarios from local development to production Azure Quantum deployment.

## Deployment Scenarios

### Scenario 1: Local Development (Default)

**Target**: Personal computer or development machine

**Configuration**:
```csharp
// QuantumProcessor.cs
public QuantumProcessor()
{
    _quantumTarget = "local-simulator";  // Default
    _useAzureQuantum = false;
}
```

**Advantages**:
- No setup required
- Instant feedback (100-500ms per simulation)
- No costs
- Full debugging support

**Limitations**:
- Single machine only
- No collaboration
- No persistence

**Build & Run**:
```bash
dotnet build
dotnet run --project PeriodicTableApp
```

### Scenario 2: Network Deployment (Teams)

**Target**: Multiple users on same network

**Configuration**:

1. **Create Data Service** (optional shared database):
```csharp
public class RemoteElementDataService
{
    private HttpClient _httpClient;
    
    public async Task<List<Element>> GetElementsAsync()
    {
        var response = await _httpClient.GetAsync("http://server/api/elements");
        // Parse and return
    }
}
```

2. **Update Startup**:
```csharp
// Inject service based on configuration
IElementDataService dataService = 
    config.UseRemoteData 
        ? (IElementDataService)new RemoteElementDataService()
        : new PeriodicTableDataService();
```

**Network Setup**:
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   User 1    │    │   User 2    │    │   User 3    │
│   Desktop   │    │   Desktop   │    │   Desktop   │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                   ┌──────▼──────┐
                   │  Shared Data│
                   │   Server    │
                   └─────────────┘
```

**Build for Network**:
```bash
# Build standalone executable
dotnet publish -c Release -r win-x64 --self-contained

# Distribute executable from bin/Release/net8.0-windows/win-x64/publish/
```

### Scenario 3: Azure Quantum Deployment

**Target**: Real quantum hardware (IonQ)

#### Prerequisites
1. Azure Account with active subscription
2. Azure Quantum Workspace created
3. IonQ provider linked
4. Credentials configured

#### Setup Steps

**Step 1: Create Azure Resources**
```bash
# Login to Azure
az login

# Create resource group
az group create --name QuantumResearch --location eastus

# Create Quantum Workspace
az quantum workspace create \
  --resource-group QuantumResearch \
  --location eastus \
  --name PeriodicTableQuantum
```

**Step 2: Configure Application**

Update `QuantumProcessor.cs`:
```csharp
public QuantumProcessor(string quantumTarget = "ionq.simulator", bool useAzure = true)
{
    _quantumTarget = quantumTarget;  // ionq.simulator or ionq.qpu
    _useAzureQuantum = useAzure;
}

public async Task<double[]> RunQuantumSimulationOnAzureAsync(
    string operationName,
    int[] parameters,
    string targetId)
{
    try
    {
        // Connect to Azure Quantum
        var workspace = new AzureQuantumWorkspace(
            subscriptionId: Environment.GetEnvironmentVariable("AZURE_SUBSCRIPTION_ID"),
            resourceGroupName: Environment.GetEnvironmentVariable("AZURE_RESOURCE_GROUP"),
            workspaceName: Environment.GetEnvironmentVariable("AZURE_QUANTUM_WORKSPACE"),
            location: Environment.GetEnvironmentVariable("AZURE_LOCATION")
        );

        // Compile Q# to QIR
        var qirCode = CompileQSharpToQIR(operationName, parameters);

        // Submit job
        var job = await workspace.SubmitJobAsync(
            qirCode,
            targetId,
            shots: 1024
        );

        // Poll for results
        while (job.Status != JobStatus.Completed)
        {
            await Task.Delay(5000);
            job = await workspace.GetJobAsync(job.Id);
        }

        // Process results
        var measurements = ParseResults(job.Result);
        return ConvertToProperties(measurements);
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Azure Quantum error: {ex.Message}");
        throw;
    }
}
```

**Step 3: Environment Configuration**

Create `.env` file:
```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=QuantumResearch
AZURE_QUANTUM_WORKSPACE=PeriodicTableQuantum
AZURE_LOCATION=eastus
AZURE_QUANTUM_TARGET=ionq.simulator
```

Load in application:
```csharp
var config = new ConfigurationBuilder()
    .AddEnvironmentVariables()
    .Build();

var subscriptionId = config["AZURE_SUBSCRIPTION_ID"];
```

**Step 4: Build and Deploy**
```bash
# Build for Azure
dotnet publish -c Release

# Deploy executable to Azure VM or Container
# Or package as Docker container (see below)
```

### Scenario 4: Docker Containerization

**Build Container**:

Create `Dockerfile`:
```dockerfile
FROM mcr.microsoft.com/dotnet/framework/aspnet:4.8-windowsservercore-ltsc2019

WORKDIR /app

# Copy published files
COPY bin/Release/net8.0-windows/publish/ .

# Set entry point
ENTRYPOINT ["PeriodicTableApp.exe"]
```

**Build Image**:
```bash
# For Linux/macOS (using cross-platform approach)
dotnet publish -c Release -r linux-x64

# Build container (adjust Dockerfile for Linux)
docker build -t periodic-table-app:latest .

# Run container
docker run -it periodic-table-app:latest
```

### Scenario 5: CI/CD Pipeline (GitHub Actions)

**Workflow File**: `.github/workflows/deploy.yml`

```yaml
name: Deploy Periodic Table App

on:
  push:
    branches: [ main, release/* ]
  pull_request:
    branches: [ main ]

env:
  DOTNET_VERSION: '8.0.x'

jobs:
  build-and-test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup .NET
        uses: actions/setup-dotnet@v3
        with:
          dotnet-version: ${{ env.DOTNET_VERSION }}
      
      - name: Restore dependencies
        run: dotnet restore
      
      - name: Build
        run: dotnet build -c Release --no-restore
      
      - name: Run tests
        run: dotnet test -c Release --no-build --verbosity normal
      
      - name: Publish
        run: dotnet publish -c Release -r win-x64 --self-contained
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: periodic-table-app-win-x64
          path: bin/Release/net8.0-windows/win-x64/publish/

  deploy-azure:
    needs: build-and-test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v3
      
      - name: Deploy to Azure
        env:
          AZURE_CREDENTIALS: ${{ secrets.AZURE_CREDENTIALS }}
        run: |
          az login --service-principal -u ${{ secrets.AZURE_CLIENT_ID }} \
            -p ${{ secrets.AZURE_CLIENT_SECRET }} \
            --tenant ${{ secrets.AZURE_TENANT_ID }}
          
          # Deploy logic here
          echo "Deploying to Azure..."
```

## Configuration Management

### Configuration Files

**appsettings.json**:
```json
{
  "Quantum": {
    "UseAzure": false,
    "Target": "local-simulator",
    "MaxQubits": 8,
    "Shots": 64
  },
  "UI": {
    "Theme": "Dark",
    "DefaultZoom": 4.0
  },
  "Performance": {
    "CacheMeshes": true,
    "MaxCacheSize": 1000
  }
}
```

**Load Configuration**:
```csharp
var config = new ConfigurationBuilder()
    .AddJsonFile("appsettings.json")
    .AddEnvironmentVariables()
    .Build();

var quantumConfig = config.GetSection("Quantum");
var useAzure = quantumConfig.GetValue<bool>("UseAzure");
```

## Performance Tuning

### Optimization Checklist

- [ ] **Enable Release Mode**: `dotnet publish -c Release`
- [ ] **Use Mesh Caching**: Reduce 3D generation overhead
- [ ] **Implement Result Caching**: Reuse simulation results
- [ ] **Optimize Qubit Allocation**: Use minimum necessary qubits
- [ ] **Batch Simulations**: Process multiple elements together
- [ ] **Async Operations**: Never block UI thread

### Profiling

**Enable Profiling**:
```csharp
using System.Diagnostics;

var stopwatch = Stopwatch.StartNew();

// Code to profile
SimulateElement(element);

stopwatch.Stop();
Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds}ms");
```

**Memory Profiling**:
```bash
dotnet run --project PeriodicTableApp -- --profile memory
```

## Monitoring and Logging

### Structured Logging

```csharp
private static readonly ILogger<ResearchAgentManager> _logger;

public async Task SimulateElementAsync(Element element)
{
    _logger.LogInformation(
        "Starting simulation for element {ElementSymbol} ({AtomicNumber})",
        element.Symbol,
        element.AtomicNumber);
    
    try
    {
        // Simulation logic
        _logger.LogInformation("Simulation completed successfully");
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Simulation failed for element {ElementSymbol}",
            element.Symbol);
        throw;
    }
}
```

### Log Aggregation (Azure)

```bash
# View logs
az monitor app-insights metrics show \
  --resource-group QuantumResearch \
  --query "[0]"
```

## Backup and Recovery

### Data Backup Strategy

1. **Configuration Backups**:
```bash
# Backup settings
cp appsettings.json appsettings.backup.json
```

2. **Results Cache**:
```csharp
// Serialize cache to disk
var json = JsonConvert.SerializeObject(_simulationCache);
File.WriteAllText("simulation_cache.json", json);
```

3. **Disaster Recovery**:
```bash
# Restore from backup
cp appsettings.backup.json appsettings.json
```

## Security Considerations

### Credential Management

**Never hardcode credentials**:
```csharp
// WRONG ❌
string password = "MySecretPassword123";

// CORRECT ✓
string password = Environment.GetEnvironmentVariable("DB_PASSWORD");
```

**Use Azure Key Vault**:
```csharp
var kvUri = "https://<vault-name>.vault.azure.net";
var client = new SecretClient(new Uri(kvUri), new DefaultAzureCredential());
KeyVaultSecret secret = client.GetSecret("QuantumApiKey");
```

### Network Security

- Use HTTPS for all Azure communications
- Enable firewall rules
- Implement VPN for remote access
- Use managed identities instead of passwords

## Troubleshooting Deployment

### Common Issues

**Issue**: "Connection timeout when accessing Azure"
**Solution**: 
```bash
# Check firewall rules
az network nsg list --resource-group QuantumResearch

# Verify network connectivity
ping <server-address>
```

**Issue**: "Out of memory during 3D rendering"
**Solution**:
```csharp
// Reduce mesh quality
const int MAX_SUBDIVISIONS = 12;  // Was 32
AddSphereMesh(mesh, center, radius, MAX_SUBDIVISIONS, MAX_SUBDIVISIONS);
```

**Issue**: "Q# compilation fails"
**Solution**:
```bash
# Check Q# SDK version
qsharp --version

# Reinstall workload
dotnet workload restore
dotnet workload update
```

## Production Checklist

- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Azure credentials secured
- [ ] Performance optimized
- [ ] UI responsive on target hardware
- [ ] Documentation updated
- [ ] Tests passing
- [ ] Load testing completed
- [ ] Backup strategy implemented
- [ ] Monitoring alerts configured
- [ ] Team trained on deployment
- [ ] Rollback plan documented

## Maintenance

### Regular Tasks

**Weekly**:
- Monitor Azure Quantum usage and costs
- Check error logs for issues
- Verify backups completed

**Monthly**:
- Update dependencies: `dotnet package update`
- Review performance metrics
- Test disaster recovery

**Quarterly**:
- Major version updates
- Security audits
- Feature enhancements

## Support Resources

- **Azure Support**: https://support.microsoft.com/azure
- **Microsoft Quantum Support**: https://quantumcomp.uservoice.com/
- **GitHub Issues**: Report bugs and request features
- **Community Forum**: Connect with other users

## Version Management

### Versioning Strategy

Use Semantic Versioning (MAJOR.MINOR.PATCH):

```csharp
public static class AppVersion
{
    public const string Version = "1.0.0";
    public const string Build = "1.0.0.0";
}
```

**Release Process**:
1. Update version numbers
2. Update CHANGELOG.md
3. Tag release in Git
4. Build release artifacts
5. Create GitHub release
6. Deploy to production

## Next Steps

1. Choose deployment scenario appropriate for your use case
2. Follow setup instructions carefully
3. Test in staging environment first
4. Monitor production deployment
5. Gather feedback and iterate

For additional help, consult the README.md, DEVELOPMENT.md, and QSH_INTEGRATION.md files.
