using System;
using System.Collections.Generic;

namespace PeriodicTableApp.Models
{
    /// <summary>
    /// Represents a chemical element with comprehensive data and properties
    /// </summary>
    public class Element
    {
        /// <summary>
        /// Unique atomic number (1-118)
        /// </summary>
        public int AtomicNumber { get; set; }

        /// <summary>
        /// Element symbol (e.g., "H", "He", "Li")
        /// </summary>
        public string Symbol { get; set; }

        /// <summary>
        /// Full element name
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// Atomic mass in atomic mass units (amu)
        /// </summary>
        public double AtomicMass { get; set; }

        /// <summary>
        /// Electron configuration
        /// </summary>
        public string ElectronConfiguration { get; set; }

        /// <summary>
        /// Oxidation states
        /// </summary>
        public List<int> OxidationStates { get; set; } = new();

        /// <summary>
        /// Electronegativity (Pauling scale)
        /// </summary>
        public double? Electronegativity { get; set; }

        /// <summary>
        /// Atomic radius in picometers
        /// </summary>
        public double? AtomicRadius { get; set; }

        /// <summary>
        /// Ionization energy (first ionization energy in eV)
        /// </summary>
        public double? IonizationEnergy { get; set; }

        /// <summary>
        /// Electron affinity in eV
        /// </summary>
        public double? ElectronAffinity { get; set; }

        /// <summary>
        /// Melting point in Celsius
        /// </summary>
        public double? MeltingPoint { get; set; }

        /// <summary>
        /// Boiling point in Celsius
        /// </summary>
        public double? BoilingPoint { get; set; }

        /// <summary>
        /// Density at standard conditions (g/cm³)
        /// </summary>
        public double? Density { get; set; }

        /// <summary>
        /// Specific heat capacity (J/g·K)
        /// </summary>
        public double? SpecificHeatCapacity { get; set; }

        /// <summary>
        /// Thermal conductivity (W/m·K)
        /// </summary>
        public double? ThermalConductivity { get; set; }

        /// <summary>
        /// Element category (Metal, Nonmetal, Metalloid, Halogen, Noble Gas, Lanthanide, Actinide)
        /// </summary>
        public ElementCategory Category { get; set; }

        /// <summary>
        /// Color for visualization
        /// </summary>
        public string Color { get; set; } = "#808080";

        /// <summary>
        /// Historical discovery year
        /// </summary>
        public int? DiscoveryYear { get; set; }

        /// <summary>
        /// Discoverer name
        /// </summary>
        public string Discoverer { get; set; }

        /// <summary>
        /// Brief description of the element
        /// </summary>
        public string Description { get; set; }

        /// <summary>
        /// Common uses and applications
        /// </summary>
        public List<string> CommonUses { get; set; } = new();

        /// <summary>
        /// Quantum simulation results for electron orbital
        /// </summary>
        public double[] OrbitalProbabilities { get; set; }

        /// <summary>
        /// Material properties predicted by quantum simulation
        /// </summary>
        public MaterialProperties QuantumProperties { get; set; }

        public Element()
        {
            QuantumProperties = new MaterialProperties();
        }

        public override string ToString()
        {
            return $"{AtomicNumber} - {Symbol} ({Name})";
        }
    }

    /// <summary>
    /// Element classification categories
    /// </summary>
    public enum ElementCategory
    {
        Metal,
        Nonmetal,
        Metalloid,
        Halogen,
        NobleGas,
        Lanthanide,
        Actinide,
        AlkaliMetal,
        AlkalineEarthMetal,
        TransitionMetal
    }

    /// <summary>
    /// Material properties derived from quantum simulations
    /// </summary>
    public class MaterialProperties
    {
        /// <summary>
        /// Electrical conductivity (0-1 normalized scale)
        /// </summary>
        public double Conductivity { get; set; }

        /// <summary>
        /// Material density prediction
        /// </summary>
        public double Density { get; set; }

        /// <summary>
        /// Material hardness estimation
        /// </summary>
        public double Hardness { get; set; }

        /// <summary>
        /// Chemical reactivity prediction
        /// </summary>
        public double Reactivity { get; set; }

        /// <summary>
        /// Timestamp of last quantum simulation
        /// </summary>
        public DateTime LastSimulationTime { get; set; }

        /// <summary>
        /// Flag indicating if simulation is running
        /// </summary>
        public bool IsSimulating { get; set; }
    }
}
