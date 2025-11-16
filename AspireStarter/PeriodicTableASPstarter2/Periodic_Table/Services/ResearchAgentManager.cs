using PeriodicTableWeb.Models;

namespace PeriodicTableWeb.Services;

/// <summary>
/// Manages research operations and coordinates between UI and quantum processor
/// </summary>
public class ResearchAgentManager
{
    private readonly IQuantumProcessor _quantumProcessor;
    private readonly ElementDataService _elementService;
    private readonly ILogger<ResearchAgentManager> _logger;

    public ResearchAgentManager(
        IQuantumProcessor quantumProcessor,
        ElementDataService elementService,
        ILogger<ResearchAgentManager> logger)
    {
        _quantumProcessor = quantumProcessor;
        _elementService = elementService;
        _logger = logger;
    }

    /// <summary>
    /// Generate 3D atomic model for an element
    /// </summary>
    public async Task<Element3DModelData> GenerateElement3DModel(int atomicNumber)
    {
        _logger.LogInformation($"Generating 3D model for element {atomicNumber}");

        var element = _elementService.GetElement(atomicNumber);
        if (element == null)
        {
            throw new ArgumentException($"Element with atomic number {atomicNumber} not found");
        }

        var model = new Element3DModelData
        {
            AtomicNumber = atomicNumber,
            NucleusRadius = 0.5,
        };

        // Generate electron shells based on electron configuration
        var shells = CalculateElectronShells(atomicNumber);
        foreach (var shell in shells)
        {
            model.ElectronClouds.Add(shell);
            if (shell.OrbitalRadius > model.MaxRadius)
            {
                model.MaxRadius = shell.OrbitalRadius;
            }
        }

        _logger.LogInformation($"Generated 3D model with {model.ElectronClouds.Count} shells");

        return model;
    }

    /// <summary>
    /// Run quantum simulation for an element
    /// </summary>
    public async Task<QuantumSimulationResult> RunQuantumSimulation(int atomicNumber, string simulationType)
    {
        _logger.LogInformation($"Running quantum simulation for element {atomicNumber}");

        return await _quantumProcessor.RunQuantumSimulationAsync(atomicNumber, simulationType);
    }

    /// <summary>
    /// Calculate electron shell configuration
    /// </summary>
    private List<ElectronCloud> CalculateElectronShells(int atomicNumber)
    {
        var shells = new List<ElectronCloud>();
        var remaining = atomicNumber;
        int shellNumber = 1;

        while (remaining > 0)
        {
            int maxElectrons = 2 * shellNumber * shellNumber;
            int electronsInShell = Math.Min(remaining, maxElectrons);
            
            shells.Add(new ElectronCloud
            {
                ShellNumber = shellNumber,
                ElectronCount = electronsInShell,
                OrbitalRadius = 1.0 + (shellNumber - 1) * 1.5,
                OrbitalType = GetOrbitalType(shellNumber)
            });

            remaining -= electronsInShell;
            shellNumber++;
        }

        return shells;
    }

    private string GetOrbitalType(int shellNumber)
    {
        return shellNumber switch
        {
            1 => "s",
            2 => "s,p",
            3 => "s,p,d",
            _ => "s,p,d,f"
        };
    }
}
