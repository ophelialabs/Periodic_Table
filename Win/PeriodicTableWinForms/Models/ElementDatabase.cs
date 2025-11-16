namespace PeriodicTableWinForms.Models;

/// <summary>
/// Manages the periodic table data and element information.
/// </summary>
public static class ElementDatabase
{
    public static Dictionary<int, Element> Elements { get; } = InitializeElements();

    private static Dictionary<int, Element> InitializeElements()
    {
        var elements = new Dictionary<int, Element>
        {
            // Period 1
            { 1, new Element { AtomicNumber = 1, Symbol = "H", Name = "Hydrogen", AtomicMass = 1.008, Category = "Nonmetal", Period = 1, Group = 1, AtomicRadius = 53, ElectronegativeityPauling = 2.20, ElectronConfiguration = 1, DisplayColor = (255, 255, 255) } },
            { 2, new Element { AtomicNumber = 2, Symbol = "He", Name = "Helium", AtomicMass = 4.003, Category = "Noble Gas", Period = 1, Group = 18, AtomicRadius = 31, ElectronegativeityPauling = 0.00, ElectronConfiguration = 2, DisplayColor = (255, 192, 203) } },
            
            // Period 2
            { 3, new Element { AtomicNumber = 3, Symbol = "Li", Name = "Lithium", AtomicMass = 6.941, Category = "Alkali Metal", Period = 2, Group = 1, AtomicRadius = 167, ElectronegativeityPauling = 0.98, ElectronConfiguration = 3, DisplayColor = (204, 51, 51) } },
            { 4, new Element { AtomicNumber = 4, Symbol = "Be", Name = "Beryllium", AtomicMass = 9.012, Category = "Alkaline Earth Metal", Period = 2, Group = 2, AtomicRadius = 112, ElectronegativeityPauling = 1.57, ElectronConfiguration = 4, DisplayColor = (0, 128, 0) } },
            { 5, new Element { AtomicNumber = 5, Symbol = "B", Name = "Boron", AtomicMass = 10.811, Category = "Metalloid", Period = 2, Group = 13, AtomicRadius = 87, ElectronegativeityPauling = 2.04, ElectronConfiguration = 5, DisplayColor = (255, 165, 0) } },
            { 6, new Element { AtomicNumber = 6, Symbol = "C", Name = "Carbon", AtomicMass = 12.011, Category = "Nonmetal", Period = 2, Group = 14, AtomicRadius = 77, ElectronegativeityPauling = 2.55, ElectronConfiguration = 6, DisplayColor = (128, 128, 128) } },
            { 7, new Element { AtomicNumber = 7, Symbol = "N", Name = "Nitrogen", AtomicMass = 14.007, Category = "Nonmetal", Period = 2, Group = 15, AtomicRadius = 71, ElectronegativeityPauling = 3.04, ElectronConfiguration = 7, DisplayColor = (0, 0, 255) } },
            { 8, new Element { AtomicNumber = 8, Symbol = "O", Name = "Oxygen", AtomicMass = 15.999, Category = "Nonmetal", Period = 2, Group = 16, AtomicRadius = 66, ElectronegativeityPauling = 3.44, ElectronConfiguration = 8, DisplayColor = (255, 0, 0) } },
            { 9, new Element { AtomicNumber = 9, Symbol = "F", Name = "Fluorine", AtomicMass = 18.998, Category = "Nonmetal", Period = 2, Group = 17, AtomicRadius = 64, ElectronegativeityPauling = 3.98, ElectronConfiguration = 9, DisplayColor = (144, 238, 144) } },
            { 10, new Element { AtomicNumber = 10, Symbol = "Ne", Name = "Neon", AtomicMass = 20.180, Category = "Noble Gas", Period = 2, Group = 18, AtomicRadius = 62, ElectronegativeityPauling = 0.00, ElectronConfiguration = 10, DisplayColor = (255, 192, 203) } },
            
            // Period 3 (sampling)
            { 11, new Element { AtomicNumber = 11, Symbol = "Na", Name = "Sodium", AtomicMass = 22.990, Category = "Alkali Metal", Period = 3, Group = 1, AtomicRadius = 186, ElectronegativeityPauling = 0.93, ElectronConfiguration = 11, DisplayColor = (204, 51, 51) } },
            { 12, new Element { AtomicNumber = 12, Symbol = "Mg", Name = "Magnesium", AtomicMass = 24.305, Category = "Alkaline Earth Metal", Period = 3, Group = 2, AtomicRadius = 160, ElectronegativeityPauling = 1.31, ElectronConfiguration = 12, DisplayColor = (0, 128, 0) } },
            
            // Transition metals
            { 26, new Element { AtomicNumber = 26, Symbol = "Fe", Name = "Iron", AtomicMass = 55.845, Category = "Transition Metal", Period = 4, Group = 8, AtomicRadius = 140, ElectronegativeityPauling = 1.83, ElectronConfiguration = 26, DisplayColor = (200, 100, 50) } },
            { 29, new Element { AtomicNumber = 29, Symbol = "Cu", Name = "Copper", AtomicMass = 63.546, Category = "Transition Metal", Period = 4, Group = 11, AtomicRadius = 135, ElectronegativeityPauling = 1.90, ElectronConfiguration = 29, DisplayColor = (184, 115, 51) } },
        };

        return elements;
    }

    public static Element GetElement(int atomicNumber)
    {
        return Elements.TryGetValue(atomicNumber, out var element) ? element : null;
    }

    public static IEnumerable<Element> GetElementsByCategory(string category)
    {
        return Elements.Values.Where(e => e.Category == category);
    }

    public static IEnumerable<Element> GetElementsByPeriod(int period)
    {
        return Elements.Values.Where(e => e.Period == period).OrderBy(e => e.Group);
    }
}
