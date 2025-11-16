using PeriodicTable.Models;

namespace PeriodicTable.Services;

/// <summary>
/// Provides periodic table element data.
/// </summary>
public class PeriodicTableService
{
    private readonly List<Element> _elements;

    public PeriodicTableService()
    {
        _elements = InitializeElements();
    }

    public List<Element> GetAllElements() => _elements;

    public Element? GetElementByAtomicNumber(int atomicNumber) =>
        _elements.FirstOrDefault(e => e.AtomicNumber == atomicNumber);

    public Element? GetElementBySymbol(string symbol) =>
        _elements.FirstOrDefault(e => e.Symbol == symbol);

    public List<Element> GetElementsByCategory(string category) =>
        _elements.Where(e => e.Category == category).ToList();

    private List<Element> InitializeElements()
    {
        return new List<Element>
        {
            new Element { AtomicNumber = 1, Symbol = "H", Name = "Hydrogen", AtomicMass = 1.008, Category = "Nonmetal", ElectronConfiguration = 1, ElectronShells = 1, HexColor = "#FFFFFF" },
            new Element { AtomicNumber = 2, Symbol = "He", Name = "Helium", AtomicMass = 4.003, Category = "Noble Gas", ElectronConfiguration = 2, ElectronShells = 1, HexColor = "#FFC0CB" },
            new Element { AtomicNumber = 3, Symbol = "Li", Name = "Lithium", AtomicMass = 6.941, Category = "Alkali Metal", ElectronConfiguration = 3, ElectronShells = 2, HexColor = "#FF9900" },
            new Element { AtomicNumber = 4, Symbol = "Be", Name = "Beryllium", AtomicMass = 9.012, Category = "Alkaline Earth", ElectronConfiguration = 4, ElectronShells = 2, HexColor = "#FFBFFF" },
            new Element { AtomicNumber = 5, Symbol = "B", Name = "Boron", AtomicMass = 10.811, Category = "Semimetal", ElectronConfiguration = 5, ElectronShells = 2, HexColor = "#00FF00" },
            new Element { AtomicNumber = 6, Symbol = "C", Name = "Carbon", AtomicMass = 12.011, Category = "Nonmetal", ElectronConfiguration = 6, ElectronShells = 2, HexColor = "#909090" },
            new Element { AtomicNumber = 7, Symbol = "N", Name = "Nitrogen", AtomicMass = 14.007, Category = "Nonmetal", ElectronConfiguration = 7, ElectronShells = 2, HexColor = "#3050F8" },
            new Element { AtomicNumber = 8, Symbol = "O", Name = "Oxygen", AtomicMass = 15.999, Category = "Nonmetal", ElectronConfiguration = 8, ElectronShells = 2, HexColor = "#FF0000" },
            new Element { AtomicNumber = 9, Symbol = "F", Name = "Fluorine", AtomicMass = 18.998, Category = "Halogen", ElectronConfiguration = 9, ElectronShells = 2, HexColor = "#FFFF00" },
            new Element { AtomicNumber = 10, Symbol = "Ne", Name = "Neon", AtomicMass = 20.180, Category = "Noble Gas", ElectronConfiguration = 10, ElectronShells = 2, HexColor = "#FF80FF" },
            new Element { AtomicNumber = 11, Symbol = "Na", Name = "Sodium", AtomicMass = 22.990, Category = "Alkali Metal", ElectronConfiguration = 11, ElectronShells = 3, HexColor = "#FF9900" },
            new Element { AtomicNumber = 12, Symbol = "Mg", Name = "Magnesium", AtomicMass = 24.305, Category = "Alkaline Earth", ElectronConfiguration = 12, ElectronShells = 3, HexColor = "#FFBFFF" },
            new Element { AtomicNumber = 13, Symbol = "Al", Name = "Aluminum", AtomicMass = 26.982, Category = "Metal", ElectronConfiguration = 13, ElectronShells = 3, HexColor = "#C0C0C0" },
            new Element { AtomicNumber = 14, Symbol = "Si", Name = "Silicon", AtomicMass = 28.086, Category = "Semimetal", ElectronConfiguration = 14, ElectronShells = 3, HexColor = "#CCCCCC" },
            new Element { AtomicNumber = 15, Symbol = "P", Name = "Phosphorus", AtomicMass = 30.974, Category = "Nonmetal", ElectronConfiguration = 15, ElectronShells = 3, HexColor = "#FFC800" },
            new Element { AtomicNumber = 16, Symbol = "S", Name = "Sulfur", AtomicMass = 32.065, Category = "Nonmetal", ElectronConfiguration = 16, ElectronShells = 3, HexColor = "#FFFF30" },
            new Element { AtomicNumber = 17, Symbol = "Cl", Name = "Chlorine", AtomicMass = 35.453, Category = "Halogen", ElectronConfiguration = 17, ElectronShells = 3, HexColor = "#00FF00" },
            new Element { AtomicNumber = 18, Symbol = "Ar", Name = "Argon", AtomicMass = 39.948, Category = "Noble Gas", ElectronConfiguration = 18, ElectronShells = 3, HexColor = "#FF80FF" },
            new Element { AtomicNumber = 26, Symbol = "Fe", Name = "Iron", AtomicMass = 55.845, Category = "Transition Metal", ElectronConfiguration = 26, ElectronShells = 4, HexColor = "#FFA500" },
            new Element { AtomicNumber = 29, Symbol = "Cu", Name = "Copper", AtomicMass = 63.546, Category = "Transition Metal", ElectronConfiguration = 29, ElectronShells = 4, HexColor = "#A67C52" },
            new Element { AtomicNumber = 47, Symbol = "Ag", Name = "Silver", AtomicMass = 107.868, Category = "Transition Metal", ElectronConfiguration = 47, ElectronShells = 5, HexColor = "#C0C0C0" },
            new Element { AtomicNumber = 79, Symbol = "Au", Name = "Gold", AtomicMass = 196.967, Category = "Transition Metal", ElectronConfiguration = 79, ElectronShells = 6, HexColor = "#FFD700" },
            new Element { AtomicNumber = 92, Symbol = "U", Name = "Uranium", AtomicMass = 238.029, Category = "Actinide", ElectronConfiguration = 92, ElectronShells = 7, HexColor = "#00FF00" }
        };
    }
}
