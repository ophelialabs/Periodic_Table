using PeriodicTable.Models;

namespace PeriodicTable.Services;

/// <summary>
/// Manages quantum simulations and research operations for elements.
/// This is the integration layer between the Blazor UI and quantum processors.
/// </summary>
public class ResearchAgentManager
{
    private readonly QuantumProcessor _quantumProcessor;
    private readonly ModelGenerator _modelGenerator;
    private readonly Dictionary<int, QuantumElementData> _simulationCache;

    public ResearchAgentManager(QuantumProcessor quantumProcessor, ModelGenerator modelGenerator)
    {
        _quantumProcessor = quantumProcessor;
        _modelGenerator = modelGenerator;
        _simulationCache = new Dictionary<int, QuantumElementData>();
    }

    /// <summary>
    /// Analyzes an element using quantum simulations and generates visual models.
    /// </summary>
    public async Task<ElementVisual> AnalyzeElementAsync(Element element)
    {
        // Check cache first
        if (_simulationCache.TryGetValue(element.AtomicNumber, out var cachedData))
        {
            return _modelGenerator.GenerateVisual(element, cachedData);
        }

        // Run quantum simulation
        var quantumData = await _quantumProcessor.RunQuantumSimulation(element);
        
        // Cache the results
        _simulationCache[element.AtomicNumber] = quantumData;

        // Generate 3D visual representation
        var visual = _modelGenerator.GenerateVisual(element, quantumData);
        
        return visual;
    }

    /// <summary>
    /// Batch analyze multiple elements in parallel.
    /// </summary>
    public async Task<Dictionary<int, ElementVisual>> AnalyzeElementsAsync(List<Element> elements)
    {
        var tasks = elements.Select(e => AnalyzeElementAsync(e)).ToList();
        var visuals = await Task.WhenAll(tasks);
        
        return elements.Zip(visuals, (e, v) => new { Element = e, Visual = v })
            .ToDictionary(x => x.Element.AtomicNumber, x => x.Visual);
    }

    /// <summary>
    /// Simulates bonding characteristics between two elements.
    /// </summary>
    public async Task<double> SimulateBondingAsync(Element element1, Element element2)
    {
        return await _quantumProcessor.RunBondingSimulation(element1, element2);
    }

    /// <summary>
    /// Clears the simulation cache to free memory.
    /// </summary>
    public void ClearCache()
    {
        _simulationCache.Clear();
    }

    /// <summary>
    /// Gets cache statistics for debugging.
    /// </summary>
    public int GetCacheSize() => _simulationCache.Count;
}
