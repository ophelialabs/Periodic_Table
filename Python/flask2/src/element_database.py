"""
Element Database - Load and query periodic table data.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Any


class ElementDatabase:
    """Load and provide access to periodic table element data."""
    
    def __init__(self):
        """Initialize the database by loading periodic table data."""
        self.elements = {}
        self.categories = set()
        self._load_periodic_table()
    
    def _load_periodic_table(self):
        """Load periodic table JSON data."""
        json_file = Path(__file__).parent / 'lib' / 'Periodic-Table-JSON' / 'PeriodicTableJSON.json'
        
        if not json_file.exists():
            raise FileNotFoundError(f"Periodic table JSON not found at {json_file}")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both dictionary and list formats
            if isinstance(data, dict) and 'elements' in data:
                elements_list = data['elements']
            else:
                elements_list = data if isinstance(data, list) else []
            
            # Index elements by symbol and number
            for element in elements_list:
                symbol = element.get('symbol', '').upper()
                if symbol:
                    self.elements[symbol] = element
                    category = element.get('category', 'unknown')
                    self.categories.add(category)
        
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in periodic table file: {e}")
    
    def get_element_by_symbol(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get element data by chemical symbol."""
        return self.elements.get(symbol.upper())
    
    def get_element_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get element data by element name."""
        name_lower = name.lower()
        for element in self.elements.values():
            if element.get('name', '').lower() == name_lower:
                return element
        return None
    
    def get_all_elements(self) -> List[Dict[str, Any]]:
        """Get all elements sorted by atomic number."""
        return sorted(self.elements.values(), 
                     key=lambda x: x.get('number', 0))
    
    def get_elements_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all elements of a specific category."""
        return [e for e in self.elements.values() 
                if e.get('category', '').lower() == category.lower()]
    
    def get_categories(self) -> List[str]:
        """Get all unique element categories."""
        return sorted(list(self.categories))
    
    def search(self, query: str, category: str = '') -> List[Dict[str, Any]]:
        """
        Search elements by name, symbol, or category.
        
        Args:
            query: Search string (name or symbol)
            category: Optional category filter
        
        Returns:
            List of matching elements
        """
        query_lower = query.lower()
        results = []
        
        for element in self.elements.values():
            # Check if matches query
            matches_query = (
                query_lower in element.get('name', '').lower() or
                query_lower in element.get('symbol', '').lower()
            )
            
            # Check if matches category
            matches_category = (
                not category or 
                element.get('category', '').lower() == category.lower()
            )
            
            if matches_query and matches_category:
                results.append(element)
        
        return sorted(results, key=lambda x: x.get('number', 0))
    
    def get_element_count(self) -> int:
        """Get total number of elements in database."""
        return len(self.elements)
    
    def get_property_range(self, property_name: str) -> tuple:
        """
        Get the min and max values for a given property across all elements.
        
        Args:
            property_name: Name of the property (e.g., 'atomic_mass', 'density')
        
        Returns:
            Tuple of (min_value, max_value)
        """
        values = []
        for element in self.elements.values():
            value = element.get(property_name)
            if value is not None:
                try:
                    values.append(float(value))
                except (ValueError, TypeError):
                    pass
        
        if values:
            return (min(values), max(values))
        return (0, 0)
