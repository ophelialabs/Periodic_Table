namespace periodictableC.Web.Models;

/// <summary>
/// Represents a chemical element with properties used for visualization and quantum simulation.
/// </summary>
public class Element
{
    public int AtomicNumber { get; set; }
    public string Symbol { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public decimal AtomicMass { get; set; }
    public string Category { get; set; } = string.Empty;
    public string ElectronConfiguration { get; set; } = string.Empty;
    public int PeriodRow { get; set; }
    public int GroupColumn { get; set; }
    
    // Visual properties
    public string Color { get; set; } = "#FF6B6B";
    public double Radius { get; set; } = 1.0;
    
    // Quantum properties for simulation
    public int ValenceElectrons { get; set; }
    public double IonicRadius { get; set; }
    public double Electronegativity { get; set; }
    
    /// <summary>
    /// Orbital shell structure represented as a list of electron counts per shell.
    /// Example: [2, 8, 8, 2] for a 4-shell atom
    /// </summary>
    public List<int> OrbitalShells { get; set; } = [];
}
