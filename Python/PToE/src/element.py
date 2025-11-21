"""
Element data structure for the periodic table.
Represents a single chemical element with all its properties.
"""

from typing import Optional, List, Dict, Any


class Element:
    """Represents a chemical element with all its properties."""
    
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize an Element from a data dictionary.
        
        Args:
            data: Dictionary containing element properties from PeriodicTableJSON
        """
        self._data = data
    
    @property
    def number(self) -> int:
        """Atomic number."""
        return self._data.get('number', 0)
    
    @property
    def symbol(self) -> str:
        """Chemical symbol."""
        return self._data.get('symbol', '')
    
    @property
    def name(self) -> str:
        """Element name."""
        return self._data.get('name', '')
    
    @property
    def atomic_mass(self) -> float:
        """Atomic mass in u."""
        return self._data.get('atomic_mass', 0.0)
    
    @property
    def category(self) -> str:
        """Element category (e.g., 'alkali metal', 'noble gas')."""
        return self._data.get('category', '')
    
    @property
    def phase(self) -> str:
        """Phase at room temperature (Gas, Liquid, Solid)."""
        return self._data.get('phase', '')
    
    @property
    def group(self) -> int:
        """Group number (column)."""
        return self._data.get('group', 0)
    
    @property
    def period(self) -> int:
        """Period number (row)."""
        return self._data.get('period', 0)
    
    @property
    def block(self) -> str:
        """Block (s, p, d, f)."""
        return self._data.get('block', '')
    
    @property
    def electron_configuration(self) -> str:
        """Full electron configuration."""
        return self._data.get('electron_configuration', '')
    
    @property
    def electron_configuration_semantic(self) -> str:
        """Semantic (short-hand) electron configuration."""
        return self._data.get('electron_configuration_semantic', '')
    
    @property
    def shells(self) -> List[int]:
        """Electron shells (number of electrons per shell)."""
        return self._data.get('shells', [])
    
    @property
    def electronegativity(self) -> Optional[float]:
        """Electronegativity (Pauling scale)."""
        return self._data.get('electronegativity_pauling')
    
    @property
    def ionization_energies(self) -> List[float]:
        """Successive ionization energies in kJ/mol."""
        return self._data.get('ionization_energies', [])
    
    @property
    def electron_affinity(self) -> Optional[float]:
        """First electron affinity in kJ/mol."""
        return self._data.get('electron_affinity')
    
    @property
    def melt(self) -> Optional[float]:
        """Melting point in Kelvin."""
        return self._data.get('melt')
    
    @property
    def boil(self) -> Optional[float]:
        """Boiling point in Kelvin."""
        return self._data.get('boil')
    
    @property
    def density(self) -> Optional[float]:
        """Density in g/cm³ (solids/liquids) or g/L (gases)."""
        return self._data.get('density')
    
    @property
    def molar_heat(self) -> Optional[float]:
        """Molar heat capacity in J/(mol*K)."""
        return self._data.get('molar_heat')
    
    @property
    def appearance(self) -> str:
        """Visual appearance description."""
        return self._data.get('appearance', '')
    
    @property
    def summary(self) -> str:
        """Summary from Wikipedia."""
        return self._data.get('summary', '')
    
    @property
    def bohr_model_image(self) -> Optional[str]:
        """URL to Bohr model image."""
        return self._data.get('bohr_model_image')
    
    @property
    def bohr_model_3d(self) -> Optional[str]:
        """URL to 3D Bohr model (GLB file)."""
        return self._data.get('bohr_model_3d')
    
    @property
    def spectral_img(self) -> Optional[str]:
        """URL to spectral image."""
        return self._data.get('spectral_img')
    
    @property
    def image_url(self) -> Optional[str]:
        """URL to element image."""
        return self._data.get('image', {}).get('url')
    
    @property
    def image_title(self) -> str:
        """Image title/description."""
        return self._data.get('image', {}).get('title', '')
    
    @property
    def cpk_hex(self) -> str:
        """CPK color (hex code without #)."""
        return self._data.get('cpk-hex', 'cccccc')
    
    @property
    def color(self) -> str:
        """Returns CPK color as hex with # prefix for tkinter."""
        hex_color = self.cpk_hex
        if hex_color is None or hex_color == '':
            hex_color = 'cccccc'
        if not hex_color.startswith('#'):
            hex_color = '#' + hex_color
        return hex_color
    
    @property
    def discovered_by(self) -> Optional[str]:
        """Person/entity that discovered the element."""
        return self._data.get('discovered_by')
    
    @property
    def named_by(self) -> Optional[str]:
        """Person/entity that named the element."""
        return self._data.get('named_by')
    
    @property
    def source(self) -> Optional[str]:
        """URL to source (usually Wikipedia)."""
        return self._data.get('source')
    
    @property
    def xpos(self) -> int:
        """X position in periodic table."""
        return self._data.get('xpos', 0)
    
    @property
    def ypos(self) -> int:
        """Y position in periodic table."""
        return self._data.get('ypos', 0)
    
    @property
    def wxpos(self) -> int:
        """Wide periodic table X position."""
        return self._data.get('wxpos', 0)
    
    @property
    def wypos(self) -> int:
        """Wide periodic table Y position."""
        return self._data.get('wypos', 0)
    
    def get_raw_data(self) -> Dict[str, Any]:
        """Get the raw data dictionary."""
        return self._data.copy()
    
    def __repr__(self) -> str:
        return f"Element({self.symbol} - {self.name})"
    
    def __str__(self) -> str:
        return f"{self.symbol}: {self.name} (Z={self.number})"
