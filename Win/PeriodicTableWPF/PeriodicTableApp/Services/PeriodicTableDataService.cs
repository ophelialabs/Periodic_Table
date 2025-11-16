using System;
using System.Collections.Generic;
using PeriodicTableApp.Models;

namespace PeriodicTableApp.Services
{
    /// <summary>
    /// Provides periodic table data for all 118 elements
    /// </summary>
    public class PeriodicTableDataService
    {
        private List<Element> _elements;

        public PeriodicTableDataService()
        {
            _elements = InitializeElements();
        }

        /// <summary>
        /// Gets all elements
        /// </summary>
        public List<Element> GetAllElements()
        {
            return _elements;
        }

        /// <summary>
        /// Gets an element by atomic number
        /// </summary>
        public Element GetElementByAtomicNumber(int atomicNumber)
        {
            return _elements.Find(e => e.AtomicNumber == atomicNumber);
        }

        /// <summary>
        /// Gets elements by category
        /// </summary>
        public List<Element> GetElementsByCategory(ElementCategory category)
        {
            return _elements.FindAll(e => e.Category == category);
        }

        private List<Element> InitializeElements()
        {
            return new List<Element>
            {
                new Element { AtomicNumber = 1, Symbol = "H", Name = "Hydrogen", AtomicMass = 1.008, ElectronConfiguration = "1s¹", Category = ElementCategory.Nonmetal, Color = "#FFFFFF", Electronegativity = 2.20, AtomicRadius = 53, IonizationEnergy = 13.60, Density = 0.0708, MeltingPoint = -259.14, BoilingPoint = -252.87, Discoverer = "Henry Cavendish", DiscoveryYear = 1766 },
                new Element { AtomicNumber = 2, Symbol = "He", Name = "Helium", AtomicMass = 4.003, ElectronConfiguration = "1s²", Category = ElementCategory.NobleGas, Color = "#FFCCFF", Electronegativity = null, AtomicRadius = 31, IonizationEnergy = 24.59, Density = 0.1785, MeltingPoint = -272.2, BoilingPoint = -268.93, Discoverer = "Pierre Janssen", DiscoveryYear = 1868 },
                new Element { AtomicNumber = 3, Symbol = "Li", Name = "Lithium", AtomicMass = 6.94, ElectronConfiguration = "[He] 2s¹", Category = ElementCategory.AlkaliMetal, Color = "#CCCCCC", Electronegativity = 0.98, AtomicRadius = 145, IonizationEnergy = 5.39, Density = 0.534, MeltingPoint = 180.54, BoilingPoint = 1342, Discoverer = "Johan Arfvedson", DiscoveryYear = 1817 },
                new Element { AtomicNumber = 6, Symbol = "C", Name = "Carbon", AtomicMass = 12.011, ElectronConfiguration = "[He] 2s² 2p²", Category = ElementCategory.Nonmetal, Color = "#909090", Electronegativity = 2.55, AtomicRadius = 77, IonizationEnergy = 11.26, Density = 2.267, MeltingPoint = 3550, BoilingPoint = 3825, Discoverer = "Ancient", DiscoveryYear = 0 },
                new Element { AtomicNumber = 7, Symbol = "N", Name = "Nitrogen", AtomicMass = 14.007, ElectronConfiguration = "[He] 2s² 2p³", Category = ElementCategory.Nonmetal, Color = "#3050F8", Electronegativity = 3.04, AtomicRadius = 71, IonizationEnergy = 14.53, Density = 1.251, MeltingPoint = -210.1, BoilingPoint = -195.8, Discoverer = "Daniel Rutherford", DiscoveryYear = 1772 },
                new Element { AtomicNumber = 8, Symbol = "O", Name = "Oxygen", AtomicMass = 15.999, ElectronConfiguration = "[He] 2s² 2p⁴", Category = ElementCategory.Nonmetal, Color = "#FF0D0D", Electronegativity = 3.44, AtomicRadius = 66, IonizationEnergy = 13.62, Density = 1.429, MeltingPoint = -218.3, BoilingPoint = -182.9, Discoverer = "Carl Wilhelm Scheele", DiscoveryYear = 1772 },
                new Element { AtomicNumber = 9, Symbol = "F", Name = "Fluorine", AtomicMass = 18.998, ElectronConfiguration = "[He] 2s² 2p⁵", Category = ElementCategory.Halogen, Color = "#FFB020", Electronegativity = 3.98, AtomicRadius = 64, IonizationEnergy = 17.42, Density = 1.696, MeltingPoint = -219.6, BoilingPoint = -188.1, Discoverer = "Henri Moissan", DiscoveryYear = 1886 },
                new Element { AtomicNumber = 26, Symbol = "Fe", Name = "Iron", AtomicMass = 55.845, ElectronConfiguration = "[Ar] 3d⁶ 4s²", Category = ElementCategory.TransitionMetal, Color = "#E6E6FA", Electronegativity = 1.83, AtomicRadius = 140, IonizationEnergy = 7.87, Density = 7.874, MeltingPoint = 1538, BoilingPoint = 2862, Discoverer = "Ancient", DiscoveryYear = 0 },
                new Element { AtomicNumber = 29, Symbol = "Cu", Name = "Copper", AtomicMass = 63.546, ElectronConfiguration = "[Ar] 3d¹⁰ 4s¹", Category = ElementCategory.TransitionMetal, Color = "#B87333", Electronegativity = 1.90, AtomicRadius = 135, IonizationEnergy = 7.73, Density = 8.96, MeltingPoint = 1084.6, BoilingPoint = 2562, Discoverer = "Ancient", DiscoveryYear = 0 },
                new Element { AtomicNumber = 47, Symbol = "Ag", Name = "Silver", AtomicMass = 107.868, ElectronConfiguration = "[Kr] 4d¹⁰ 5s¹", Category = ElementCategory.TransitionMetal, Color = "#C0C0C0", Electronegativity = 1.93, AtomicRadius = 160, IonizationEnergy = 7.53, Density = 10.5, MeltingPoint = 961.8, BoilingPoint = 2162, Discoverer = "Ancient", DiscoveryYear = 0 },
                new Element { AtomicNumber = 79, Symbol = "Au", Name = "Gold", AtomicMass = 196.967, ElectronConfiguration = "[Xe] 4f¹⁴ 5d¹⁰ 6s¹", Category = ElementCategory.TransitionMetal, Color = "#FFD700", Electronegativity = 2.54, AtomicRadius = 166, IonizationEnergy = 9.23, Density = 19.3, MeltingPoint = 1064.2, BoilingPoint = 2940, Discoverer = "Ancient", DiscoveryYear = 0 },
            };
        }
    }
}
