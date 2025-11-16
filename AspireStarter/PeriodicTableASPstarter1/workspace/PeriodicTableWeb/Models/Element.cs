namespace PeriodicTableWeb.Models;

/// <summary>
/// Represents a chemical element with its properties
/// </summary>
public class Element
{
    public int AtomicNumber { get; set; }
    public string Symbol { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public double AtomicMass { get; set; }
    public string Category { get; set; } = string.Empty;
    public string ElectronConfiguration { get; set; } = string.Empty;
    public int ValenceElectrons { get; set; }
    public string Color { get; set; } = "#999999";
}

/// <summary>
/// Represents electron cloud data for 3D atomic model
/// </summary>
public class ElectronCloud
{
    public int ShellNumber { get; set; }
    public int ElectronCount { get; set; }
    public double OrbitalRadius { get; set; }
    public string OrbitalType { get; set; } = string.Empty; // s, p, d, f
}

/// <summary>
/// 3D model data for atomic representation
/// </summary>
public class Element3DModelData
{
    public int AtomicNumber { get; set; }
    public double NucleusRadius { get; set; } = 0.5;
    public List<ElectronCloud> ElectronClouds { get; set; } = new();
    public double MaxRadius { get; set; }
}

/// <summary>
/// Result of quantum simulation
/// </summary>
public class QuantumSimulationResult
{
    public string SimulationType { get; set; } = "electron-distribution";
    public double[] MeasurementProbabilities { get; set; } = Array.Empty<double>();
    public int[] QuantumStates { get; set; } = Array.Empty<int>();
    public double[] SpatialData { get; set; } = Array.Empty<double>();
    public long ExecutionTimeMs { get; set; }
}

/// <summary>
/// 3D spatial data for electron spheres
/// </summary>
public class ElectronSphereData
{
    public double X { get; set; }
    public double Y { get; set; }
    public double Z { get; set; }
    public double Radius { get; set; }
    public double Opacity { get; set; }
    public string Color { get; set; } = "#667eea";
}

/// <summary>
/// Material properties for 3D rendering
/// </summary>
public class MaterialProperties
{
    public string DiffuseColor { get; set; } = "#667eea";
    public double Metalness { get; set; } = 0.5;
    public double Roughness { get; set; } = 0.7;
    public double Opacity { get; set; } = 0.8;
}

/// <summary>
/// Data visualization plot data
/// </summary>
public class DataPlot
{
    public string Title { get; set; } = string.Empty;
    public double[] XValues { get; set; } = Array.Empty<double>();
    public double[] YValues { get; set; } = Array.Empty<double>();
    public string XAxisLabel { get; set; } = string.Empty;
    public string YAxisLabel { get; set; } = string.Empty;
}
