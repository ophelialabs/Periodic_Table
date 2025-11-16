namespace periodictableC.Web.Services;

using periodictableC.Web.Models;

/// <summary>
/// Service for managing periodic table element data.
/// </summary>
public class ElementDataService
{
    private readonly List<Element> _elements = [];
    
    public ElementDataService()
    {
        InitializePeriodicTable();
    }
    
    /// <summary>
    /// Gets all elements in the periodic table.
    /// </summary>
    public List<Element> GetAllElements() => _elements;
    
    /// <summary>
    /// Gets a specific element by atomic number.
    /// </summary>
    public Element? GetElement(int atomicNumber) => 
        _elements.FirstOrDefault(e => e.AtomicNumber == atomicNumber);
    
    /// <summary>
    /// Gets elements in a specific category.
    /// </summary>
    public List<Element> GetElementsByCategory(string category) => 
        _elements.Where(e => e.Category == category).ToList();
    
    /// <summary>
    /// Initialize the periodic table with common elements.
    /// This demonstrates the structure; expand as needed.
    /// </summary>
    private void InitializePeriodicTable()
    {
        _elements.AddRange(new[]
        {
            new Element 
            { 
                AtomicNumber = 1, 
                Symbol = "H", 
                Name = "Hydrogen", 
                AtomicMass = 1.008m, 
                Category = "Nonmetal",
                ElectronConfiguration = "1s¹",
                PeriodRow = 1,
                GroupColumn = 1,
                Color = "#FFFFFF",
                ValenceElectrons = 1,
                OrbitalShells = [1]
            },
            new Element 
            { 
                AtomicNumber = 2, 
                Symbol = "He", 
                Name = "Helium", 
                AtomicMass = 4.003m, 
                Category = "Noble Gas",
                ElectronConfiguration = "1s²",
                PeriodRow = 1,
                GroupColumn = 18,
                Color = "#FFB3D9",
                ValenceElectrons = 2,
                OrbitalShells = [2]
            },
            new Element 
            { 
                AtomicNumber = 6, 
                Symbol = "C", 
                Name = "Carbon", 
                AtomicMass = 12.011m, 
                Category = "Nonmetal",
                ElectronConfiguration = "1s² 2s² 2p²",
                PeriodRow = 2,
                GroupColumn = 14,
                Color = "#808080",
                ValenceElectrons = 4,
                OrbitalShells = [2, 4]
            },
            new Element 
            { 
                AtomicNumber = 8, 
                Symbol = "O", 
                Name = "Oxygen", 
                AtomicMass = 15.999m, 
                Category = "Nonmetal",
                ElectronConfiguration = "1s² 2s² 2p⁴",
                PeriodRow = 2,
                GroupColumn = 16,
                Color = "#FF0000",
                ValenceElectrons = 6,
                OrbitalShells = [2, 6]
            },
            new Element 
            { 
                AtomicNumber = 26, 
                Symbol = "Fe", 
                Name = "Iron", 
                AtomicMass = 55.845m, 
                Category = "Transition Metal",
                ElectronConfiguration = "[Ar] 3d⁶ 4s²",
                PeriodRow = 4,
                GroupColumn = 8,
                Color = "#B87333",
                Electronegativity = 1.83,
                ValenceElectrons = 2,
                OrbitalShells = [2, 8, 14, 2]
            },
            new Element 
            { 
                AtomicNumber = 79, 
                Symbol = "Au", 
                Name = "Gold", 
                AtomicMass = 196.967m, 
                Category = "Transition Metal",
                ElectronConfiguration = "[Xe] 4f¹⁴ 5d¹⁰ 6s¹",
                PeriodRow = 6,
                GroupColumn = 11,
                Color = "#FFD700",
                Electronegativity = 2.54,
                ValenceElectrons = 1,
                OrbitalShells = [2, 8, 18, 32, 18, 1]
            }
        });
    }
}
