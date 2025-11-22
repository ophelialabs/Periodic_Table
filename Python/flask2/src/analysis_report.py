"""
Analysis Report Generator - Create visualizations and reports for elements.
"""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


class AnalysisReportGenerator:
    """Generate analysis reports and visualizations for periodic table."""
    
    def __init__(self, element_database):
        """
        Initialize the report generator.
        
        Args:
            element_database: ElementDatabase instance
        """
        self.db = element_database
        self.output_dir = Path(__file__).parent / 'reports'
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_summary_statistics(self) -> str:
        """Generate summary statistics about elements in the database."""
        elements = self.db.get_all_elements()
        categories = self.db.get_categories()
        
        summary = f"""
╔════════════════════════════════════════════════════════════╗
║         Periodic Table Analysis Summary                    ║
╠════════════════════════════════════════════════════════════╣
║ Total Elements:        {len(elements):>35} ║
║ Total Categories:      {len(categories):>35} ║
║ Database Status:       {('✓ Loaded' if elements else '✗ Empty'):>35} ║
╚════════════════════════════════════════════════════════════╝

Categories:
"""
        for category in categories:
            count = len(self.db.get_elements_by_category(category))
            summary += f"  • {category.title():<30} ({count:>3} elements)\n"
        
        return summary
    
    def generate_heatmap_data(self, property_name: str) -> Dict[str, Any]:
        """
        Generate heatmap data for a specific element property.
        
        Args:
            property_name: Name of the property (e.g., 'atomic_mass')
        
        Returns:
            Dictionary with heatmap data
        """
        elements = self.db.get_all_elements()
        min_val, max_val = self.db.get_property_range(property_name)
        
        data = {
            'property': property_name,
            'min': min_val,
            'max': max_val,
            'elements': []
        }
        
        for element in elements:
            value = element.get(property_name)
            if value is not None:
                try:
                    normalized = (float(value) - min_val) / (max_val - min_val) if max_val > min_val else 0
                    data['elements'].append({
                        'symbol': element.get('symbol'),
                        'name': element.get('name'),
                        'number': element.get('number'),
                        'value': float(value),
                        'normalized': normalized
                    })
                except (ValueError, TypeError):
                    pass
        
        return data
    
    def generate_property_distribution(self, property_name: str) -> Dict[str, Any]:
        """
        Generate property distribution data for histogram visualization.
        
        Args:
            property_name: Name of the property
        
        Returns:
            Dictionary with distribution data
        """
        elements = self.db.get_all_elements()
        values = []
        
        for element in elements:
            value = element.get(property_name)
            if value is not None:
                try:
                    values.append(float(value))
                except (ValueError, TypeError):
                    pass
        
        if not values:
            return {'property': property_name, 'bins': [], 'counts': []}
        
        bins = np.histogram_bin_edges(values, bins=10)
        counts, _ = np.histogram(values, bins=bins)
        
        return {
            'property': property_name,
            'bins': [float(b) for b in bins[:-1]],
            'counts': [int(c) for c in counts],
            'mean': float(np.mean(values)),
            'median': float(np.median(values)),
            'std': float(np.std(values))
        }
    
    def generate_element_details_csv(self) -> str:
        """
        Generate CSV file with all element details.
        
        Returns:
            Path to generated CSV file
        """
        elements = self.db.get_all_elements()
        
        if not elements:
            return ""
        
        # Get all unique keys
        all_keys = set()
        for element in elements:
            all_keys.update(element.keys())
        
        all_keys = sorted(list(all_keys))
        
        csv_path = self.output_dir / 'elements_data.csv'
        
        with open(csv_path, 'w', encoding='utf-8') as f:
            # Write header
            f.write(','.join(all_keys) + '\n')
            
            # Write data
            for element in elements:
                row = []
                for key in all_keys:
                    value = element.get(key, '')
                    # Escape quotes in CSV values
                    if isinstance(value, str):
                        value = f'"{value.replace('"', '""')}"'
                    row.append(str(value))
                f.write(','.join(row) + '\n')
        
        return str(csv_path)
    
    def generate_full_report(self, include_pdf: bool = False, include_png: bool = False) -> Dict[str, str]:
        """
        Generate comprehensive analysis report.
        
        Args:
            include_pdf: Whether to generate PDF report
            include_png: Whether to generate PNG visualizations
        
        Returns:
            Dictionary with paths to generated files
        """
        results = {
            'csv': self.generate_element_details_csv()
        }
        
        if include_png:
            results['visualizations'] = self._generate_visualizations()
        
        return results
    
    def _generate_visualizations(self) -> Dict[str, str]:
        """Generate PNG visualizations."""
        visualizations = {}
        
        # Atomic mass distribution
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            dist_data = self.generate_property_distribution('atomic_mass')
            if dist_data['bins']:
                ax.bar(dist_data['bins'], dist_data['counts'], width=1)
                ax.set_xlabel('Atomic Mass')
                ax.set_ylabel('Frequency')
                ax.set_title('Atomic Mass Distribution')
                
                png_path = self.output_dir / 'atomic_mass_distribution.png'
                plt.savefig(png_path, dpi=100, bbox_inches='tight')
                plt.close()
                visualizations['atomic_mass'] = str(png_path)
        except Exception as e:
            print(f"Error generating atomic mass visualization: {e}")
        
        return visualizations
    
    def get_element_comparison(self, symbols: List[str]) -> List[Dict[str, Any]]:
        """
        Get comparison data for multiple elements.
        
        Args:
            symbols: List of element symbols to compare
        
        Returns:
            List of element data for comparison
        """
        results = []
        for symbol in symbols:
            element = self.db.get_element_by_symbol(symbol)
            if element:
                results.append(element)
        return results
