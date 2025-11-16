using PeriodicTableWeb.Models;

namespace PeriodicTableWeb.Services;

/// <summary>
/// Service for managing periodic table element data
/// </summary>
public class ElementDataService
{
    private readonly List<Element> _elements = new();

    public ElementDataService()
    {
        InitializeElements();
    }

    /// <summary>
    /// Get all elements
    /// </summary>
    public IEnumerable<Element> GetAllElements() => _elements.OrderBy(e => e.AtomicNumber);

    /// <summary>
    /// Get element by atomic number
    /// </summary>
    public Element? GetElement(int atomicNumber) => 
        _elements.FirstOrDefault(e => e.AtomicNumber == atomicNumber);

    private void InitializeElements()
    {
        // First 20 elements for demonstration
        _elements.AddRange(new[]
        {
            new Element { AtomicNumber = 1, Symbol = "H", Name = "Hydrogen", AtomicMass = 1.008, Category = "Nonmetal", ElectronConfiguration = "1s¹", ValenceElectrons = 1, Color = "#FFFFFF" },
            new Element { AtomicNumber = 2, Symbol = "He", Name = "Helium", AtomicMass = 4.003, Category = "Noble Gas", ElectronConfiguration = "1s²", ValenceElectrons = 2, Color = "#FFB3B3" },
            new Element { AtomicNumber = 3, Symbol = "Li", Name = "Lithium", AtomicMass = 6.941, Category = "Alkali Metal", ElectronConfiguration = "[He]2s¹", ValenceElectrons = 1, Color = "#FF99CC" },
            new Element { AtomicNumber = 4, Symbol = "Be", Name = "Beryllium", AtomicMass = 9.012, Category = "Alkaline Earth", ElectronConfiguration = "[He]2s²", ValenceElectrons = 2, Color = "#FFFF99" },
            new Element { AtomicNumber = 5, Symbol = "B", Name = "Boron", AtomicMass = 10.811, Category = "Metalloid", ElectronConfiguration = "[He]2s²2p¹", ValenceElectrons = 3, Color = "#90EE90" },
            new Element { AtomicNumber = 6, Symbol = "C", Name = "Carbon", AtomicMass = 12.011, Category = "Nonmetal", ElectronConfiguration = "[He]2s²2p²", ValenceElectrons = 4, Color = "#CCCCCC" },
            new Element { AtomicNumber = 7, Symbol = "N", Name = "Nitrogen", AtomicMass = 14.007, Category = "Nonmetal", ElectronConfiguration = "[He]2s²2p³", ValenceElectrons = 5, Color = "#3333FF" },
            new Element { AtomicNumber = 8, Symbol = "O", Name = "Oxygen", AtomicMass = 15.999, Category = "Nonmetal", ElectronConfiguration = "[He]2s²2p⁴", ValenceElectrons = 6, Color = "#FF3333" },
            new Element { AtomicNumber = 9, Symbol = "F", Name = "Fluorine", AtomicMass = 18.998, Category = "Halogen", ElectronConfiguration = "[He]2s²2p⁵", ValenceElectrons = 7, Color = "#FFFF66" },
            new Element { AtomicNumber = 10, Symbol = "Ne", Name = "Neon", AtomicMass = 20.180, Category = "Noble Gas", ElectronConfiguration = "[He]2s²2p⁶", ValenceElectrons = 8, Color = "#FF6666" },
            new Element { AtomicNumber = 11, Symbol = "Na", Name = "Sodium", AtomicMass = 22.990, Category = "Alkali Metal", ElectronConfiguration = "[Ne]3s¹", ValenceElectrons = 1, Color = "#FF99CC" },
            new Element { AtomicNumber = 12, Symbol = "Mg", Name = "Magnesium", AtomicMass = 24.305, Category = "Alkaline Earth", ElectronConfiguration = "[Ne]3s²", ValenceElectrons = 2, Color = "#FFFF99" },
            new Element { AtomicNumber = 13, Symbol = "Al", Name = "Aluminum", AtomicMass = 26.982, Category = "Metal", ElectronConfiguration = "[Ne]3s²3p¹", ValenceElectrons = 3, Color = "#CCCCCC" },
            new Element { AtomicNumber = 14, Symbol = "Si", Name = "Silicon", AtomicMass = 28.086, Category = "Metalloid", ElectronConfiguration = "[Ne]3s²3p²", ValenceElectrons = 4, Color = "#CCCC99" },
            new Element { AtomicNumber = 15, Symbol = "P", Name = "Phosphorus", AtomicMass = 30.974, Category = "Nonmetal", ElectronConfiguration = "[Ne]3s²3p³", ValenceElectrons = 5, Color = "#FF6633" },
            new Element { AtomicNumber = 16, Symbol = "S", Name = "Sulfur", AtomicMass = 32.065, Category = "Nonmetal", ElectronConfiguration = "[Ne]3s²3p⁴", ValenceElectrons = 6, Color = "#FFFF33" },
            new Element { AtomicNumber = 17, Symbol = "Cl", Name = "Chlorine", AtomicMass = 35.453, Category = "Halogen", ElectronConfiguration = "[Ne]3s²3p⁵", ValenceElectrons = 7, Color = "#99FF99" },
            new Element { AtomicNumber = 18, Symbol = "Ar", Name = "Argon", AtomicMass = 39.948, Category = "Noble Gas", ElectronConfiguration = "[Ne]3s²3p⁶", ValenceElectrons = 8, Color = "#FF6666" },
            new Element { AtomicNumber = 19, Symbol = "K", Name = "Potassium", AtomicMass = 39.098, Category = "Alkali Metal", ElectronConfiguration = "[Ar]4s¹", ValenceElectrons = 1, Color = "#FF99CC" },
            new Element { AtomicNumber = 20, Symbol = "Ca", Name = "Calcium", AtomicMass = 40.078, Category = "Alkaline Earth", ElectronConfiguration = "[Ar]4s²", ValenceElectrons = 2, Color = "#FFFF99" },
        });
    }
}
