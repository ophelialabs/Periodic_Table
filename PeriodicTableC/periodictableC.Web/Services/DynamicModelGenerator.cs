namespace periodictableC.Web.Services;

using periodictableC.Web.Models;

/// <summary>
/// Generates dynamic 3D scene data and visualization configurations.
/// Processes quantum simulation results and converts them into renderable 3D coordinates.
/// </summary>
public class DynamicModelGenerator
{
    private readonly ILogger<DynamicModelGenerator> _logger;
    
    public DynamicModelGenerator(ILogger<DynamicModelGenerator> logger)
    {
        _logger = logger;
    }
    
    /// <summary>
    /// Generates 3D sphere positions for electron visualization based on quantum results.
    /// </summary>
    public ElectronSphereData[] Generate3DElectronSpheres(
        Element3DModelData modelData, 
        QuantumSimulationResult quantumResult)
    {
        _logger.LogInformation($"Generating 3D electron spheres for {modelData.Element.Symbol}");
        
        var spheres = new List<ElectronSphereData>();
        var probabilityIndex = 0;
        
        foreach (var cloudData in modelData.ElectronClouds)
        {
            for (int i = 0; i < cloudData.ElectronCount && probabilityIndex < quantumResult.MeasurementProbabilities.Length; i++)
            {
                var probability = quantumResult.MeasurementProbabilities[probabilityIndex];
                var position = GenerateOrbitalPosition(cloudData.OrbitalRadius, i, cloudData.ElectronCount, probability);
                
                spheres.Add(new ElectronSphereData
                {
                    Position = position,
                    Radius = 0.15f,
                    Color = cloudData.Color,
                    Opacity = cloudData.Opacity,
                    ProbabilityAmplitude = probability,
                    OrbitalShell = modelData.ElectronClouds.IndexOf(cloudData)
                });
                
                probabilityIndex++;
            }
        }
        
        return spheres.ToArray();
    }
    
    /// <summary>
    /// Generates a 3D position within an orbital based on probability amplitudes.
    /// </summary>
    private float[] GenerateOrbitalPosition(float radius, int electronIndex, int totalElectrons, double probability)
    {
        // Distribute electrons around the orbital using golden angle for aesthetic arrangement
        var angle = (2.0 * Math.PI * electronIndex) / totalElectrons;
        var phi = Math.Acos(-1.0 + (2.0 * electronIndex) / totalElectrons);
        
        // Apply probability-based modulation to radius
        var modulatedRadius = (float)(radius * (0.8 + 0.4 * probability));
        
        var x = (float)(modulatedRadius * Math.Sin(phi) * Math.Cos(angle));
        var y = (float)(modulatedRadius * Math.Sin(phi) * Math.Sin(angle));
        var z = (float)(modulatedRadius * Math.Cos(phi));
        
        return [x, y, z];
    }
    
    /// <summary>
    /// Generates material properties for 3D rendering based on element properties.
    /// </summary>
    public MaterialProperties GenerateMaterialProperties(Element element, QuantumSimulationResult quantum)
    {
        var avgProbability = quantum.MeasurementProbabilities.Length > 0 
            ? quantum.MeasurementProbabilities.Average() 
            : 0.1;
        
        return new MaterialProperties
        {
            BaseColor = element.Color,
            Metalness = (float)element.Electronegativity / 4.0f,
            Roughness = (float)(1.0 - avgProbability),
            Emissive = ScaleColorByValue(element.Color, (float)(0.2 + avgProbability * 0.3)),
            AlphaOpacity = 0.85f
        };
    }
    
    /// <summary>
    /// Generates a data visualization plot configuration for quantum results.
    /// </summary>
    public DataVisualizationPlot GenerateDataPlot(QuantumSimulationResult quantum)
    {
        var probabilities = quantum.MeasurementProbabilities;
        
        return new DataVisualizationPlot
        {
            Title = $"Quantum Measurement Results - {quantum.ElementSymbol}",
            XAxisLabel = "Measurement Index",
            YAxisLabel = "Probability Amplitude",
            DataPoints = probabilities
                .Select((p, i) => new DataPoint { X = i, Y = p })
                .ToArray(),
            AverageValue = probabilities.Average(),
            MaxValue = probabilities.Max(),
            MinValue = probabilities.Min()
        };
    }
    
    private string ScaleColorByValue(string hexColor, float value)
    {
        // Simple color intensity scaling (for basic visualization)
        // In a real implementation, this would do proper HSL/HSV adjustments
        value = Math.Clamp(value, 0f, 1f);
        var intensity = (int)(255 * value);
        return $"rgba({intensity}, {intensity}, {intensity}, 0.5)";
    }
}

/// <summary>
/// Represents a single electron sphere for 3D rendering.
/// </summary>
public class ElectronSphereData
{
    public float[] Position { get; set; } = [];
    public float Radius { get; set; }
    public string Color { get; set; } = string.Empty;
    public float Opacity { get; set; }
    public double ProbabilityAmplitude { get; set; }
    public int OrbitalShell { get; set; }
}

/// <summary>
/// Material properties for 3D mesh rendering.
/// </summary>
public class MaterialProperties
{
    public string BaseColor { get; set; } = string.Empty;
    public float Metalness { get; set; }
    public float Roughness { get; set; }
    public string Emissive { get; set; } = string.Empty;
    public float AlphaOpacity { get; set; }
}

/// <summary>
/// Represents a data visualization plot for quantum results.
/// </summary>
public class DataVisualizationPlot
{
    public string Title { get; set; } = string.Empty;
    public string XAxisLabel { get; set; } = string.Empty;
    public string YAxisLabel { get; set; } = string.Empty;
    public DataPoint[] DataPoints { get; set; } = [];
    public double AverageValue { get; set; }
    public double MaxValue { get; set; }
    public double MinValue { get; set; }
}

/// <summary>
/// Single data point for plotting.
/// </summary>
public class DataPoint
{
    public int X { get; set; }
    public double Y { get; set; }
}
