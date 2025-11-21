"""
Element database for loading and managing periodic table data.
"""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
import pandas as pd

from src.element import Element


class ElementDatabase:
    """Manages loading and accessing element data."""
    
    def __init__(self, json_file_path: Optional[str] = None):
        """
        Initialize the element database.
        
        Args:
            json_file_path: Path to PeriodicTableJSON.json file.
                          If None, uses default location relative to this file.
        """
        if json_file_path is None:
            # Default path relative to this file
            current_dir = Path(__file__).parent
            json_file_path = current_dir / 'lib' / 'Periodic-Table-JSON' / 'PeriodicTableJSON.json'
        
        self.json_file_path = Path(json_file_path)
        self.elements: Dict[int, Element] = {}
        self.elements_by_symbol: Dict[str, Element] = {}
        self.dataframe: Optional[pd.DataFrame] = None
        
        self._load_data()
    
    def _load_data(self):
        """Load element data from JSON file."""
        if not self.json_file_path.exists():
            raise FileNotFoundError(f"Periodic table JSON not found at {self.json_file_path}")
        
        with open(self.json_file_path, 'r') as f:
            data = json.load(f)
        
        # Load elements into dictionaries
        for element_data in data.get('elements', []):
            element = Element(element_data)
            self.elements[element.number] = element
            self.elements_by_symbol[element.symbol] = element
        
        # Create DataFrame for analytical operations
        self._create_dataframe()
    
    def _create_dataframe(self):
        """Create pandas DataFrame from element data."""
        data_list = [elem.get_raw_data() for elem in self.elements.values()]
        self.dataframe = pd.DataFrame(data_list)
    
    def get_element_by_number(self, atomic_number: int) -> Optional[Element]:
        """Get element by atomic number."""
        return self.elements.get(atomic_number)
    
    def get_element_by_symbol(self, symbol: str) -> Optional[Element]:
        """Get element by chemical symbol."""
        return self.elements_by_symbol.get(symbol.upper())
    
    def get_element_by_name(self, name: str) -> Optional[Element]:
        """Get element by name."""
        for element in self.elements.values():
            if element.name.lower() == name.lower():
                return element
        return None
    
    def get_all_elements(self) -> List[Element]:
        """Get all elements sorted by atomic number."""
        return sorted(self.elements.values(), key=lambda e: e.number)
    
    def get_elements_by_category(self, category: str) -> List[Element]:
        """Get all elements in a specific category."""
        return [e for e in self.elements.values() if e.category == category]
    
    def get_elements_by_period(self, period: int) -> List[Element]:
        """Get all elements in a specific period (row)."""
        return [e for e in self.elements.values() if e.period == period]
    
    def get_elements_by_group(self, group: int) -> List[Element]:
        """Get all elements in a specific group (column)."""
        return [e for e in self.elements.values() if e.group == group]
    
    def get_elements_by_block(self, block: str) -> List[Element]:
        """Get all elements in a specific block (s, p, d, f)."""
        return [e for e in self.elements.values() if e.block == block]
    
    def get_elements_by_phase(self, phase: str) -> List[Element]:
        """Get all elements in a specific phase (Gas, Liquid, Solid)."""
        return [e for e in self.elements.values() if e.phase == phase]
    
    def get_all_categories(self) -> List[str]:
        """Get all unique element categories."""
        return sorted(list(set(e.category for e in self.elements.values() if e.category)))
    
    def get_all_periods(self) -> List[int]:
        """Get all periods."""
        return sorted(list(set(e.period for e in self.elements.values() if e.period)))
    
    def get_all_groups(self) -> List[int]:
        """Get all groups."""
        return sorted(list(set(e.group for e in self.elements.values() if e.group)))
    
    def get_all_blocks(self) -> List[str]:
        """Get all blocks."""
        return sorted(list(set(e.block for e in self.elements.values() if e.block)))
    
    def get_all_phases(self) -> List[str]:
        """Get all phases."""
        return sorted(list(set(e.phase for e in self.elements.values() if e.phase)))
    
    def search_elements(self, query: str) -> List[Element]:
        """
        Search for elements by name, symbol, or category.
        
        Args:
            query: Search string
            
        Returns:
            List of matching elements
        """
        query_lower = query.lower()
        results = []
        
        for element in self.elements.values():
            if (query_lower in element.name.lower() or 
                query_lower in element.symbol.lower() or 
                query_lower in element.category.lower()):
                results.append(element)
        
        return sorted(results, key=lambda e: e.number)
    
    def get_element_count(self) -> int:
        """Get total number of elements."""
        return len(self.elements)
    
    def get_dataframe(self) -> pd.DataFrame:
        """Get the full dataframe for analysis."""
        return self.dataframe.copy() if self.dataframe is not None else None
