"""
Element Database Module
Manages the periodic table data with all elements.
"""

from typing import List, Optional, Dict
from src.element import Element, ElementState


class ElementDatabase:
    """Manages the periodic table database of all elements."""
    
    def __init__(self):
        """Initialize the element database with all periodic table elements."""
        self.elements: Dict[int, Element] = {}
        self._load_elements()
    
    def _load_elements(self):
        """Load all periodic table elements."""
        # Simplified subset - in production, load from JSON/CSV
        elements_data = [
            # Period 1
            Element(
                atomic_number=1, symbol='H', name='Hydrogen', atomic_mass=1.008,
                electron_configuration='1s1', category='Nonmetal', group=1, period=1,
                state=ElementState.GAS, electronegativity=2.20, ionization_energy=13.6,
                electron_affinity=0.754, density=0.0899, melting_point=13.8,
                boiling_point=20.3, color='#FFFFFF', discovered_year=1766,
                discoverer='Henry Cavendish', uses=['Fuel', 'Synthesis', 'Cooling'],
                properties={'oxidation_states': [-1, 1], 'covalent_radius': 0.31}
            ),
            Element(
                atomic_number=2, symbol='He', name='Helium', atomic_mass=4.003,
                electron_configuration='1s2', category='Noble Gas', group=18, period=1,
                state=ElementState.GAS, electronegativity=0.0, ionization_energy=24.59,
                electron_affinity=0.0, density=0.1785, melting_point=1.0,
                boiling_point=4.2, color='#FFCCFF', discovered_year=1868,
                discoverer='Pierre Janssen', uses=['Cooling', 'Lifting', 'Inert atmosphere'],
                properties={'oxidation_states': [0], 'covalent_radius': 0.28}
            ),
            # Period 2
            Element(
                atomic_number=3, symbol='Li', name='Lithium', atomic_mass=6.941,
                electron_configuration='[He] 2s1', category='Alkali Metal', group=1, period=2,
                state=ElementState.SOLID, electronegativity=0.98, ionization_energy=5.39,
                electron_affinity=0.618, density=0.534, melting_point=453.7,
                boiling_point=1615.0, color='#CCCCCC', discovered_year=1817,
                discoverer='Johan Arfwedson', uses=['Batteries', 'Lubricants', 'Medicine'],
                properties={'oxidation_states': [1], 'covalent_radius': 1.28}
            ),
            Element(
                atomic_number=6, symbol='C', name='Carbon', atomic_mass=12.011,
                electron_configuration='[He] 2s² 2p²', category='Nonmetal', group=14, period=2,
                state=ElementState.SOLID, electronegativity=2.55, ionization_energy=11.26,
                electron_affinity=1.263, density=2.267, melting_point=3823.0,
                boiling_point=5100.0, color='#909090', discovered_year=3750,
                discoverer='Ancient', uses=['Diamonds', 'Graphite', 'Fuel', 'Electronics'],
                properties={'oxidation_states': [-4, -3, -2, -1, 0, 1, 2, 3, 4], 'covalent_radius': 0.76}
            ),
            Element(
                atomic_number=7, symbol='N', name='Nitrogen', atomic_mass=14.007,
                electron_configuration='[He] 2s² 2p³', category='Nonmetal', group=15, period=2,
                state=ElementState.GAS, electronegativity=3.04, ionization_energy=14.53,
                electron_affinity=0.0, density=1.251, melting_point=63.1,
                boiling_point=77.4, color='#3050F8', discovered_year=1772,
                discoverer='Daniel Rutherford', uses=['Fertilizer', 'Explosives', 'Inert atmosphere'],
                properties={'oxidation_states': [-3, -2, -1, 0, 1, 2, 3, 4, 5], 'covalent_radius': 0.71}
            ),
            Element(
                atomic_number=8, symbol='O', name='Oxygen', atomic_mass=15.999,
                electron_configuration='[He] 2s² 2p⁴', category='Nonmetal', group=16, period=2,
                state=ElementState.GAS, electronegativity=3.44, ionization_energy=13.61,
                electron_affinity=1.461, density=1.429, melting_point=54.4,
                boiling_point=90.2, color='#FF0000', discovered_year=1772,
                discoverer='Carl Wilhelm Scheele', uses=['Combustion', 'Respiration', 'Water'],
                properties={'oxidation_states': [-2, -1, 0, 1, 2], 'covalent_radius': 0.66}
            ),
            # Period 3
            Element(
                atomic_number=11, symbol='Na', name='Sodium', atomic_mass=22.990,
                electron_configuration='[Ne] 3s1', category='Alkali Metal', group=1, period=3,
                state=ElementState.SOLID, electronegativity=0.93, ionization_energy=5.14,
                electron_affinity=0.548, density=0.971, melting_point=370.7,
                boiling_point=1156.0, color='#CCCCCC', discovered_year=1807,
                discoverer='Humphry Davy', uses=['Salt', 'Chemical synthesis', 'Lighting'],
                properties={'oxidation_states': [1], 'covalent_radius': 1.66}
            ),
            Element(
                atomic_number=17, symbol='Cl', name='Chlorine', atomic_mass=35.453,
                electron_configuration='[Ne] 3s² 3p⁵', category='Halogen', group=17, period=3,
                state=ElementState.GAS, electronegativity=3.16, ionization_energy=12.97,
                electron_affinity=3.617, density=3.214, melting_point=172.1,
                boiling_point=239.1, color='#1FF01F', discovered_year=1774,
                discoverer='Carl Wilhelm Scheele', uses=['Disinfection', 'PVC', 'Bleach'],
                properties={'oxidation_states': [-1, 0, 1, 3, 5, 7], 'covalent_radius': 1.02}
            ),
            # Transition metals
            Element(
                atomic_number=26, symbol='Fe', name='Iron', atomic_mass=55.845,
                electron_configuration='[Ar] 3d⁶ 4s²', category='Transition Metal', group=8, period=4,
                state=ElementState.SOLID, electronegativity=1.83, ionization_energy=7.87,
                electron_affinity=0.151, density=7.874, melting_point=1811.0,
                boiling_point=3134.0, color='#E6E6FA', discovered_year=5000,
                discoverer='Ancient', uses=['Steel', 'Construction', 'Catalysts'],
                properties={'oxidation_states': [2, 3, 4, 6], 'covalent_radius': 1.32}
            ),
            Element(
                atomic_number=29, symbol='Cu', name='Copper', atomic_mass=63.546,
                electron_configuration='[Ar] 3d¹⁰ 4s1', category='Transition Metal', group=11, period=4,
                state=ElementState.SOLID, electronegativity=1.90, ionization_energy=7.72,
                electron_affinity=1.235, density=8.96, melting_point=1357.8,
                boiling_point=2835.0, color='#FF6600', discovered_year=5000,
                discoverer='Ancient', uses=['Wiring', 'Plumbing', 'Electronics'],
                properties={'oxidation_states': [1, 2], 'covalent_radius': 1.32}
            ),
        ]
        
        for element in elements_data:
            self.elements[element.atomic_number] = element
    
    def get_element(self, atomic_number: int) -> Optional[Element]:
        """Get element by atomic number."""
        return self.elements.get(atomic_number)
    
    def get_element_by_symbol(self, symbol: str) -> Optional[Element]:
        """Get element by chemical symbol."""
        for element in self.elements.values():
            if element.symbol == symbol:
                return element
        return None
    
    def get_elements_by_category(self, category: str) -> List[Element]:
        """Get all elements in a specific category."""
        return [e for e in self.elements.values() if e.category == category]
    
    def get_elements_by_period(self, period: int) -> List[Element]:
        """Get all elements in a specific period."""
        return sorted([e for e in self.elements.values() if e.period == period],
                     key=lambda x: x.group)
    
    def get_elements_by_group(self, group: int) -> List[Element]:
        """Get all elements in a specific group."""
        return sorted([e for e in self.elements.values() if e.group == group],
                     key=lambda x: x.period)
    
    def get_all_elements(self) -> List[Element]:
        """Get all elements sorted by atomic number."""
        return sorted(self.elements.values(), key=lambda x: x.atomic_number)
    
    def get_categories(self) -> List[str]:
        """Get all unique element categories."""
        categories = set(e.category for e in self.elements.values())
        return sorted(list(categories))
    
    def search_elements(self, query: str) -> List[Element]:
        """Search elements by name or symbol."""
        query = query.lower()
        results = []
        for element in self.elements.values():
            if query in element.name.lower() or query in element.symbol.lower():
                results.append(element)
        return sorted(results, key=lambda x: x.atomic_number)
