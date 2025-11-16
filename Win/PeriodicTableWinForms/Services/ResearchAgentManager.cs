namespace PeriodicTableWinForms.Services;

using PeriodicTableWinForms.Models;
using System.Diagnostics;

/// <summary>
/// Orchestrates research agent operations for element analysis.
/// Coordinates with the quantum processor and model generator.
/// </summary>
public class ResearchAgentManager
{
    private readonly QuantumProcessor _quantumProcessor;
    private readonly DynamicModelGenerator _modelGenerator;
    private readonly ILogger<ResearchAgentManager> _logger;

    public event EventHandler<AgentEventArgs> OnAnalysisStarted;
    public event EventHandler<AgentEventArgs> OnAnalysisCompleted;
    public event EventHandler<AgentEventArgs> OnError;

    public ResearchAgentManager(ILogger<ResearchAgentManager> logger)
    {
        _logger = logger;
        _quantumProcessor = new QuantumProcessor();
        _modelGenerator = new DynamicModelGenerator();
    }

    /// <summary>
    /// Initiates quantum simulation and 3D model generation for an element.
    /// </summary>
    public async Task<Element> AnalyzeElementAsync(Element element, CancellationToken cancellationToken = default)
    {
        try
        {
            _logger.LogInformation($"Starting analysis for {element.Name} (Z={element.AtomicNumber})");
            OnAnalysisStarted?.Invoke(this, new AgentEventArgs { Element = element });

            // Step 1: Run quantum simulation
            _logger.LogInformation("Running quantum simulation...");
            var quantumResults = await _quantumProcessor.RunQuantumSimulationAsync(element, cancellationToken);

            if (quantumResults == null || quantumResults.Length == 0)
            {
                throw new InvalidOperationException("Quantum simulation returned no results");
            }

            // Step 2: Update element with quantum state data
            element.QuantumStateAmplitudes = quantumResults;
            _logger.LogInformation($"Quantum state amplitudes: {quantumResults.Length} samples");

            // Step 3: Generate 3D model based on quantum results
            _logger.LogInformation("Generating 3D model...");
            var positions = _modelGenerator.GenerateElectronPositions(element, quantumResults);
            element.ElectronPositions = positions;

            _logger.LogInformation($"Generated {positions.Length} electron positions");
            OnAnalysisCompleted?.Invoke(this, new AgentEventArgs { Element = element });

            return element;
        }
        catch (Exception ex)
        {
            _logger.LogError($"Analysis failed: {ex.Message}");
            OnError?.Invoke(this, new AgentEventArgs { Element = element, ErrorMessage = ex.Message });
            throw;
        }
    }

    /// <summary>
    /// Batch analyze multiple elements.
    /// </summary>
    public async Task<List<Element>> AnalyzeElementsAsync(IEnumerable<Element> elements, CancellationToken cancellationToken = default)
    {
        var results = new List<Element>();

        foreach (var element in elements)
        {
            try
            {
                var analyzed = await AnalyzeElementAsync(element, cancellationToken);
                results.Add(analyzed);
            }
            catch (Exception ex)
            {
                _logger.LogWarning($"Failed to analyze {element.Name}: {ex.Message}");
            }
        }

        return results;
    }

    /// <summary>
    /// Generate a research report for an element based on analysis results.
    /// </summary>
    public string GenerateResearchReport(Element element)
    {
        var report = new System.Text.StringBuilder();

        report.AppendLine($"=== Research Report: {element.Name} ({element.Symbol}) ===");
        report.AppendLine($"Atomic Number: {element.AtomicNumber}");
        report.AppendLine($"Atomic Mass: {element.AtomicMass:F3}");
        report.AppendLine($"Category: {element.Category}");
        report.AppendLine($"Electron Configuration: {element.ElectronConfiguration}");
        report.AppendLine($"Electronegativity (Pauling): {element.ElectronegativeityPauling:F2}");
        report.AppendLine();

        if (element.QuantumStateAmplitudes.Length > 0)
        {
            report.AppendLine("Quantum State Analysis:");
            report.AppendLine($"- State Amplitudes: {element.QuantumStateAmplitudes.Length} samples");
            report.AppendLine($"- Max Amplitude: {element.QuantumStateAmplitudes.Max():F4}");
            report.AppendLine($"- Mean Amplitude: {element.QuantumStateAmplitudes.Average():F4}");
            report.AppendLine();
        }

        if (element.ElectronPositions.Length > 0)
        {
            report.AppendLine("3D Model Data:");
            report.AppendLine($"- Generated Positions: {element.ElectronPositions.Length}");
            report.AppendLine($"- Center of Mass: ({element.ElectronPositions.Average(p => p.x):F2}, " +
                            $"{element.ElectronPositions.Average(p => p.y):F2}, " +
                            $"{element.ElectronPositions.Average(p => p.z):F2})");
        }

        return report.ToString();
    }
}

public class AgentEventArgs : EventArgs
{
    public Element Element { get; set; }
    public string ErrorMessage { get; set; }
}
