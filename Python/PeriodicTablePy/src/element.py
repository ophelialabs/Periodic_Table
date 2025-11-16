"""
Element Data Structure Module
Holds and manages element data for the periodic table.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum


class ElementState(Enum):
    """Enumeration for element states."""
    SOLID = "Solid"
    LIQUID = "Liquid"
    GAS = "Gas"
    PLASMA = "Plasma"
    UNKNOWN = "Unknown"


@dataclass
class Element:
    """
    Represents a chemical element with all relevant properties.
    
    Attributes:
        atomic_number: Unique identifier for the element
        symbol: Chemical symbol (e.g., 'H', 'He')
        name: Full name of the element
        atomic_mass: Standard atomic weight
        electron_configuration: Electronic configuration string
        category: Category of element (Metal, Nonmetal, etc.)
        group: Group number in periodic table
        period: Period number in periodic table
        state: Physical state at room temperature
        electronegativity: Pauling electronegativity value
        ionization_energy: First ionization energy (eV)
        electron_affinity: Electron affinity (eV)
        density: Density at STP (g/cm³)
        melting_point: Melting point (K)
        boiling_point: Boiling point (K)
        color: Color representation (hex code)
        discovered_year: Year of discovery
        discoverer: Name of discoverer
        uses: List of common uses
        properties: Additional properties dictionary
    """
    
    atomic_number: int
    symbol: str
    name: str
    atomic_mass: float
    electron_configuration: str
    category: str
    group: int
    period: int
    state: ElementState
    electronegativity: float
    ionization_energy: float
    electron_affinity: float
    density: float
    melting_point: float
    boiling_point: float
    color: str = "#CCCCCC"
    discovered_year: int = 0
    discoverer: str = "Unknown"
    uses: List[str] = field(default_factory=list)
    properties: Dict[str, any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate element data after initialization."""
        if self.atomic_number < 1:
            raise ValueError("Atomic number must be positive")
        if not self.symbol or not self.name:
            raise ValueError("Symbol and name are required")
    
    def get_electron_count(self) -> int:
        """Returns the electron count (equals atomic number for neutral atoms)."""
        return self.atomic_number
    
    def get_valence_electrons(self) -> int:
        """
        Extract valence electron count from electron configuration.
        
        Returns:
            Number of valence electrons
        """
        # Simple heuristic: extract outermost shell electrons
        # This is a simplified approach; real implementation would parse more carefully
        config_parts = self.electron_configuration.split()
        if config_parts:
            last_part = config_parts[-1]
            # Extract number from strings like "3s2", "4p6", etc.
            digit_sum = sum(int(c) for c in last_part if c.isdigit())
            return digit_sum
        return 0
    
    def is_metal(self) -> bool:
        """Check if element is a metal."""
        return self.category in ["Metal", "Transition Metal", "Alkaline Earth Metal", 
                                  "Alkali Metal", "Lanthanide", "Actinide"]
    
    def is_nonmetal(self) -> bool:
        """Check if element is a nonmetal."""
        return self.category in ["Nonmetal", "Halogen", "Noble Gas"]
    
    def get_bohr_radius_estimation(self) -> float:
        """
        Estimate the Bohr radius for the element's valence electrons.
        
        Returns:
            Estimated radius in Angstroms
        """
        # Simplified Bohr model estimation
        # Real Bohr radius = 0.529 Å * n² / Z_eff
        valence = self.get_valence_electrons()
        period = self.period
        return 0.529 * (period ** 2) / self.atomic_number
    
    def to_dict(self) -> Dict:
        """Convert element to dictionary representation."""
        return {
            'atomic_number': self.atomic_number,
            'symbol': self.symbol,
            'name': self.name,
            'atomic_mass': self.atomic_mass,
            'electron_configuration': self.electron_configuration,
            'category': self.category,
            'group': self.group,
            'period': self.period,
            'state': self.state.value,
            'electronegativity': self.electronegativity,
            'ionization_energy': self.ionization_energy,
            'electron_affinity': self.electron_affinity,
            'density': self.density,
            'melting_point': self.melting_point,
            'boiling_point': self.boiling_point,
            'color': self.color,
            'discovered_year': self.discovered_year,
            'discoverer': self.discoverer,
            'uses': self.uses,
            'properties': self.properties
        }
    
    def __repr__(self) -> str:
        """String representation of element."""
        return f"{self.name} ({self.symbol}, Z={self.atomic_number})"
    
    def __str__(self) -> str:
        """Readable string representation."""
        return (f"{self.name}\n"
                f"Symbol: {self.symbol}, Atomic #: {self.atomic_number}\n"
                f"Mass: {self.atomic_mass:.2f} u\n"
                f"Config: {self.electron_configuration}")
