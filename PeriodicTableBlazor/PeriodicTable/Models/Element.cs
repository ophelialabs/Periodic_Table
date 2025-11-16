namespace PeriodicTable.Models;

/// <summary>
/// Represents a chemical element with its properties and quantum data.
/// </summary>
public class Element
{
    public int AtomicNumber { get; set; }
    public string Symbol { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public double AtomicMass { get; set; }
    public string Category { get; set; } = string.Empty;
    public int ElectronConfiguration { get; set; }
    public double ElectronShells { get; set; }
    
    /// <summary>
    /// Color representation for UI display
    /// </summary>
    public string HexColor { get; set; } = "#808080";
    
    /// <summary>
    /// Quantum simulation data for this element
    /// </summary>
    public QuantumElementData? QuantumData { get; set; }
}

/// <summary>
/// Contains quantum simulation results for an element.
/// </summary>
public class QuantumElementData
{
    public string ElementSymbol { get; set; } = string.Empty;
    public DateTime GeneratedAt { get; set; }
    
    /// <summary>
    /// Electron probability distribution (0.0 to 1.0)
    /// </summary>
    public double[] ElectronProbabilities { get; set; } = Array.Empty<double>();
    
    /// <summary>
    /// Orbital radius estimates in Angstroms
    /// </summary>
    public double[] OrbitalRadii { get; set; } = Array.Empty<double>();
    
    /// <summary>
    /// Energy levels in eV
    /// </summary>
    public double[] EnergyLevels { get; set; } = Array.Empty<double>();
    
    /// <summary>
    /// 3D coordinates for electron cloud visualization
    /// </summary>
    public Vector3D[]? ElectronCloudPoints { get; set; }
    
    /// <summary>
    /// Molecular bonding characteristics
    /// </summary>
    public double BondingPotential { get; set; }
    
    /// <summary>
    /// Stability index (higher = more stable)
    /// </summary>
    public double StabilityIndex { get; set; }
}

/// <summary>
/// Represents a 3D point for visualizations.
/// </summary>
public class Vector3D
{
    public double X { get; set; }
    public double Y { get; set; }
    public double Z { get; set; }
    
    public Vector3D() { }
    
    public Vector3D(double x, double y, double z)
    {
        X = x;
        Y = y;
        Z = z;
    }
}

/// <summary>
/// Represents a 3D model visual for an element.
/// </summary>
public class ElementVisual
{
    public string ElementSymbol { get; set; } = string.Empty;
    public List<Sphere> ElectronSpheres { get; set; } = new();
    public List<Ring> OrbitalRings { get; set; } = new();
    public Vector3D NucleusPosition { get; set; } = new(0, 0, 0);
    public string MaterialColor { get; set; } = "#FFFFFF";
}

/// <summary>
/// Represents a sphere in 3D space (for electron cloud)
/// </summary>
public class Sphere
{
    public Vector3D Position { get; set; } = new();
    public double Radius { get; set; }
    public double Opacity { get; set; }
    public string Color { get; set; } = "#0088FF";
}

/// <summary>
/// Represents an orbital ring in 3D space
/// </summary>
public class Ring
{
    public Vector3D Center { get; set; } = new();
    public double Radius { get; set; }
    public string Axis { get; set; } = "Z"; // X, Y, or Z
    public string Color { get; set; } = "#88FF00";
}
