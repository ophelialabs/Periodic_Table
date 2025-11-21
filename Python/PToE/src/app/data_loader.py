"""
Data loader module for the Periodic Table application.
Loads and processes element data from JSON files.
"""

import json
import pandas as pd
from pathlib import Path


class PeriodicTableDataLoader:
    """Load and process periodic table data from JSON format."""
    
    def __init__(self, json_file_path):
        """
        Initialize the data loader.
        
        Args:
            json_file_path (str): Path to the PeriodicTableJSON.json file
        """
        self.json_file_path = json_file_path
        self.elements_data = None
        self.df = None
        self._load_data()
    
    def _load_data(self):
        """Load JSON data from file."""
        with open(self.json_file_path, 'r') as f:
            data = json.load(f)
            self.elements_data = data.get('elements', [])
    
    def get_dataframe(self):
        """
        Convert elements data to pandas DataFrame.
        
        Returns:
            pd.DataFrame: DataFrame with all element properties
        """
        if self.df is None:
            self.df = pd.DataFrame(self.elements_data)
        return self.df
    
    def get_element_by_symbol(self, symbol):
        """
        Get element data by chemical symbol.
        
        Args:
            symbol (str): Chemical symbol (e.g., 'H', 'He', 'O')
            
        Returns:
            dict: Element data or None if not found
        """
        for element in self.elements_data:
            if element.get('symbol') == symbol:
                return element
        return None
    
    def get_element_by_number(self, atomic_number):
        """
        Get element data by atomic number.
        
        Args:
            atomic_number (int): Atomic number
            
        Returns:
            dict: Element data or None if not found
        """
        for element in self.elements_data:
            if element.get('number') == atomic_number:
                return element
        return None
    
    def get_element_by_name(self, name):
        """
        Get element data by name.
        
        Args:
            name (str): Element name
            
        Returns:
            dict: Element data or None if not found
        """
        for element in self.elements_data:
            if element.get('name').lower() == name.lower():
                return element
        return None
    
    def get_all_elements(self):
        """
        Get all elements data.
        
        Returns:
            list: List of all element dictionaries
        """
        return self.elements_data
    
    def get_elements_by_category(self, category):
        """
        Get all elements in a specific category.
        
        Args:
            category (str): Element category (e.g., 'alkali metal', 'noble gas')
            
        Returns:
            list: List of matching elements
        """
        return [e for e in self.elements_data if e.get('category') == category]
    
    def get_all_categories(self):
        """
        Get all unique categories.
        
        Returns:
            set: Set of unique element categories
        """
        return set(e.get('category') for e in self.elements_data if e.get('category'))
