using PeriodicTableWeb.Models;

namespace PeriodicTableWeb.Services;

/// <summary>
/// Generates 3D models and visualization data from quantum simulation results
/// </summary>
public class DynamicModelGenerator
{
    private readonly ILogger<DynamicModelGenerator> _logger;

    public DynamicModelGenerator(ILogger<DynamicModelGenerator> logger)
    {
        _logger = logger;
    }

    /// <summary>
    /// Generate 3D electron sphere positions from model and quantum results
    /// </summary>
    public ElectronSphereData[] Generate3DElectronSpheres(
        Element3DModelData model,
        QuantumSimulationResult quantumResult)
    {
        _logger.LogInformation($"Generating 3D electron spheres for element {model.AtomicNumber}");

        var spheres = new List<ElectronSphereData>();
        var spatialData = quantumResult.SpatialData;
        var probabilities = quantumResult.MeasurementProbabilities;

        if (spatialData.Length == 0)
        {
            _logger.LogWarning("No spatial data in quantum result");
            return Array.Empty<ElectronSphereData>();
        }

        // Map spatial data to 3D electron spheres
        int electronIndex = 0;
        foreach (var cloud in model.ElectronClouds)
        {
            for (int i = 0; i < cloud.ElectronCount; i++)
            {
                if (electronIndex * 3 + 2 < spatialData.Length)
                {
                    var x = spatialData[electronIndex * 3];
                    var y = spatialData[electronIndex * 3 + 1];
                    var z = spatialData[electronIndex * 3 + 2];

                    var probability = probabilities.Length > electronIndex 
                        ? probabilities[electronIndex] 
                        : 0.1;

                    spheres.Add(new ElectronSphereData
                    {
                        X = x,
                        Y = y,
                        Z = z,
                        Radius = 0.15 + probability * 0.35,
                        Opacity = 0.5 + probability * 0.5,
                        Color = InterpolateColor(cloud.ShellNumber, model.ElectronClouds.Count)
                    });

                    electronIndex++;
                }
            }
        }

        _logger.LogInformation($"Generated {spheres.Count} electron spheres");

        return spheres.ToArray();
    }

    /// <summary>
    /// Generate material properties for 3D rendering
    /// </summary>
    public MaterialProperties GenerateMaterialProperties(
        Element element,
        QuantumSimulationResult quantumResult)
    {
        _logger.LogInformation($"Generating material properties for {element.Name}");

        var avgProbability = quantumResult.MeasurementProbabilities.Length > 0
            ? quantumResult.MeasurementProbabilities.Average()
            : 0.5;

        return new MaterialProperties
        {
            DiffuseColor = element.Color,
            Metalness = element.Category.Contains("Metal") ? 0.8 : 0.3,
            Roughness = 1.0 - avgProbability,
            Opacity = 0.7 + avgProbability * 0.3
        };
    }

    /// <summary>
    /// Generate data visualization plot
    /// </summary>
    public DataPlot GenerateDataPlot(QuantumSimulationResult quantumResult)
    {
        _logger.LogInformation("Generating data visualization plot");

        var probabilities = quantumResult.MeasurementProbabilities;
        var states = quantumResult.QuantumStates;

        var plot = new DataPlot
        {
            Title = "Quantum State Probability Distribution",
            XAxisLabel = "Quantum State",
            YAxisLabel = "Probability",
            XValues = states.Cast<double>().ToArray(),
            YValues = probabilities
        };

        return plot;
    }

    /// <summary>
    /// Interpolate color based on shell number
    /// </summary>
    private string InterpolateColor(int shellNumber, int totalShells)
    {
        var colors = new[]
        {
            "#FF6B6B", // Red for first shell
            "#4ECDC4", // Teal for second
            "#45B7D1", // Blue for third
            "#FFA07A", // Light salmon for fourth
            "#98D8C8"  // Mint for fifth
        };

        var colorIndex = Math.Min(shellNumber - 1, colors.Length - 1);
        return colors[colorIndex];
    }
}
