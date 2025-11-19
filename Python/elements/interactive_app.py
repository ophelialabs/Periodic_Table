"""
Interactive Periodic Table Application.
Provides an interactive UI for exploring elements and viewing 3D visualizations.
"""

import sys
from pathlib import Path
import pandas as pd
from data_loader import PeriodicTableDataLoader
from visualizations import ElementVisualizer


class InteractivePeriodicTable:
    """Interactive application for exploring the periodic table."""
    
    def __init__(self, json_file_path):
        """
        Initialize the interactive periodic table.
        
        Args:
            json_file_path (str): Path to PeriodicTableJSON.json
        """
        self.loader = PeriodicTableDataLoader(json_file_path)
        self.visualizer = ElementVisualizer()
        self.df = self.loader.get_dataframe()
        self.current_element = None
    
    def display_welcome(self):
        """Display welcome message and instructions."""
        print("\n" + "="*70)
        print("     INTERACTIVE PERIODIC TABLE OF ELEMENTS")
        print("="*70)
        print("\nWelcome to the Interactive Periodic Table Explorer!")
        print("Visualize advanced 3D atomic structures and element properties.")
        print("\nAvailable Commands:")
        print("  - 'search [element]'  : Search for element by name or symbol")
        print("  - 'number [N]'        : Get element by atomic number")
        print("  - 'category'          : List all element categories")
        print("  - 'category [name]'   : View elements in a category")
        print("  - 'list'              : List all elements")
        print("  - 'element [symbol]'  : Select element for visualization")
        print("  - 'visualize'         : Show 3D visualizations for current element")
        print("  - 'info'              : Display detailed info for current element")
        print("  - 'help'              : Show this help message")
        print("  - 'quit' or 'exit'    : Exit the application")
        print("="*70 + "\n")
    
    def search_element(self, query):
        """
        Search for element by name or symbol.
        
        Args:
            query (str): Search query
        """
        query_lower = query.lower()
        
        results = []
        for elem in self.loader.get_all_elements():
            if (query_lower in elem.get('name', '').lower() or 
                query_lower in elem.get('symbol', '').lower()):
                results.append(elem)
        
        if results:
            print(f"\nFound {len(results)} element(s):")
            for elem in results:
                print(f"  {elem['number']:3d}. {elem['name']:15s} ({elem['symbol']:2s}) - {elem['category']}")
            return results[0]
        else:
            print(f"No elements found matching '{query}'")
            return None
    
    def get_element_by_number(self, number):
        """Get element by atomic number."""
        try:
            num = int(number)
            elem = self.loader.get_element_by_number(num)
            if elem:
                return elem
            else:
                print(f"No element found with atomic number {num}")
                return None
        except ValueError:
            print("Invalid atomic number. Please enter a number.")
            return None
    
    def get_element_by_symbol(self, symbol):
        """Get element by symbol."""
        elem = self.loader.get_element_by_symbol(symbol.strip())
        if elem:
            return elem
        else:
            print(f"Element '{symbol}' not found")
            return None
    
    def display_element_info(self, element):
        """Display detailed information about an element."""
        if not element:
            print("No element selected. Use 'element [symbol]' to select one.")
            return
        
        print("\n" + "="*70)
        print(f"  {element['name'].upper()} ({element['symbol']})")
        print("="*70)
        
        info_fields = [
            ('Atomic Number', 'number'),
            ('Atomic Mass', 'atomic_mass'),
            ('Category', 'category'),
            ('Period', 'period'),
            ('Group', 'group'),
            ('Phase at Room Temp', 'phase'),
            ('Appearance', 'appearance'),
            ('Electron Configuration', 'electron_configuration_semantic'),
            ('Electronegativity (Pauling)', 'electronegativity_pauling'),
            ('Density', 'density'),
            ('Melting Point (K)', 'melt'),
            ('Boiling Point (K)', 'boil'),
            ('Molar Heat (J/mol·K)', 'molar_heat'),
            ('Discovered By', 'discovered_by'),
            ('Named By', 'named_by'),
        ]
        
        for label, key in info_fields:
            value = element.get(key)
            if value is not None:
                print(f"  {label:.<30s} {value}")
        
        # Ionization energies
        ie = element.get('ionization_energies', [])
        if ie:
            print(f"  {'Ionization Energies (kJ/mol)':.<30s}")
            for i, energy in enumerate(ie[:5], 1):
                print(f"    IE{i}: {energy:.2f}")
            if len(ie) > 5:
                print(f"    ... and {len(ie)-5} more")
        
        # Summary
        summary = element.get('summary')
        if summary:
            print(f"\n  Summary:")
            print(f"  {summary[:100]}..." if len(summary) > 100 else f"  {summary}")
        
        # Source
        source = element.get('source')
        if source:
            print(f"\n  Source: {source}")
        
        print("="*70 + "\n")
    
    def display_categories(self):
        """Display all element categories."""
        categories = sorted(self.loader.get_all_categories())
        print(f"\nAvailable Categories ({len(categories)}):")
        for i, category in enumerate(categories, 1):
            count = len(self.loader.get_elements_by_category(category))
            print(f"  {i:2d}. {category:.<40s} ({count} elements)")
        print()
    
    def display_category_elements(self, category_name):
        """Display all elements in a category."""
        elements = self.loader.get_elements_by_category(category_name)
        if elements:
            print(f"\nElements in '{category_name}' ({len(elements)} total):")
            for elem in sorted(elements, key=lambda x: x['number']):
                print(f"  {elem['number']:3d}. {elem['name']:15s} ({elem['symbol']:2s})")
            print()
        else:
            print(f"Category '{category_name}' not found or has no elements.")
    
    def display_all_elements(self):
        """Display a formatted list of all elements."""
        elements = sorted(self.loader.get_all_elements(), key=lambda x: x['number'])
        print(f"\nAll Elements ({len(elements)} total):")
        print(f"{'Num':<5} {'Name':<15} {'Symbol':<5} {'Category':<25} {'Phase':<10}")
        print("-"*70)
        for elem in elements:
            print(f"{elem['number']:<5} {elem['name']:<15} {elem['symbol']:<5} "
                  f"{elem['category']:<25} {elem['phase']:<10}")
        print()
    
    def show_visualizations(self, element):
        """Display 3D visualizations for the selected element."""
        if not element:
            print("No element selected. Use 'element [symbol]' to select one.")
            return
        
        print(f"\nGenerating 3D visualizations for {element['name']} ({element['symbol']})...")
        print("\nSelect visualization type:")
        print("  1. Electron Shell Structure")
        print("  2. Ionization Energies")
        print("  3. Thermal Properties")
        print("  4. Atomic Structure")
        print("  5. All visualizations")
        print("  0. Cancel")
        
        choice = input("\nEnter choice (0-5): ").strip()
        
        if choice == '1':
            self.visualizer.plot_electron_shells_3d(element)
        elif choice == '2':
            if element.get('ionization_energies'):
                self.visualizer.plot_ionization_energies_3d(element)
            else:
                print("No ionization energy data available for this element.")
        elif choice == '3':
            self.visualizer.plot_thermal_properties_3d(element)
        elif choice == '4':
            self.visualizer.plot_atomic_structure_3d(element)
        elif choice == '5':
            self.visualizer.plot_electron_shells_3d(element)
            if element.get('ionization_energies'):
                self.visualizer.plot_ionization_energies_3d(element)
            self.visualizer.plot_thermal_properties_3d(element)
            self.visualizer.plot_atomic_structure_3d(element)
        elif choice == '0':
            print("Cancelled.")
        else:
            print("Invalid choice.")
    
    def run(self):
        """Run the interactive application."""
        self.display_welcome()
        
        while True:
            try:
                user_input = input("periodic-table> ").strip()
                
                if not user_input:
                    continue
                
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                if command in ['quit', 'exit']:
                    print("\nThank you for using the Interactive Periodic Table. Goodbye!")
                    break
                
                elif command == 'help':
                    self.display_welcome()
                
                elif command == 'search':
                    if args:
                        elem = self.search_element(args)
                        if elem:
                            self.current_element = elem
                    else:
                        print("Usage: search [element_name_or_symbol]")
                
                elif command == 'number':
                    if args:
                        elem = self.get_element_by_number(args)
                        if elem:
                            self.current_element = elem
                    else:
                        print("Usage: number [atomic_number]")
                
                elif command == 'element':
                    if args:
                        elem = self.get_element_by_symbol(args)
                        if elem:
                            self.current_element = elem
                            self.display_element_info(elem)
                    else:
                        print("Usage: element [symbol]")
                
                elif command == 'category':
                    if args:
                        self.display_category_elements(args)
                    else:
                        self.display_categories()
                
                elif command == 'list':
                    self.display_all_elements()
                
                elif command == 'info':
                    self.display_element_info(self.current_element)
                
                elif command == 'visualize':
                    self.show_visualizations(self.current_element)
                
                else:
                    print(f"Unknown command: '{command}'. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\n\nInterrupted. Type 'quit' or 'exit' to exit.")
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Main entry point."""
    # Find the JSON file
    json_path = Path(__file__).parent / "Periodic-Table-JSON" / "PeriodicTableJSON.json"
    
    if not json_path.exists():
        print(f"Error: Could not find PeriodicTableJSON.json at {json_path}")
        print("Please ensure the file is in the correct location.")
        sys.exit(1)
    
    app = InteractivePeriodicTable(str(json_path))
    app.run()


if __name__ == "__main__":
    main()
