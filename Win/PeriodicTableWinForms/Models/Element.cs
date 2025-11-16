namespace PeriodicTableWinForms.Models;

/// <summary>
/// Represents an element in the periodic table with atomic and visual data.
/// </summary>
public class Element
{
    public int AtomicNumber { get; set; }
    public string Symbol { get; set; }
    public string Name { get; set; }
    public double AtomicMass { get; set; }
    public string Category { get; set; }
    public int Period { get; set; }
    public int Group { get; set; }
    public double AtomicRadius { get; set; }
    public double ElectronegativeityPauling { get; set; }
    public int ElectronConfiguration { get; set; }
    
    /// <summary>
    /// Quantum state representation (probability amplitudes for electron states)
    /// Generated during Q# simulation
    /// </summary>
    public double[] QuantumStateAmplitudes { get; set; }
    
    /// <summary>
    /// 3D position data for electron cloud visualization
    /// </summary>
    public (double x, double y, double z)[] ElectronPositions { get; set; }
    
    /// <summary>
    /// RGB color for visual representation
    /// </summary>
    public (int R, int G, int B) DisplayColor { get; set; }

    public Element()
    {
        QuantumStateAmplitudes = Array.Empty<double>();
        ElectronPositions = Array.Empty<(double, double, double)>();
        DisplayColor = (100, 100, 100);
    }

    public override string ToString()
    {
        return $"{Symbol} - {Name} (Z={AtomicNumber})";
    }
}
