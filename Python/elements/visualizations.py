"""
Advanced 3D visualization module for elements.
Provides various 3D plots and analyses using matplotlib, plotly, and scipy.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from scipy import stats
import plotly.graph_objects as go
import plotly.express as px


class ElementVisualizer:
    """Create advanced 3D visualizations for periodic table elements."""
    
    def __init__(self, style='seaborn-v0_8-darkgrid'):
        """
        Initialize visualizer with matplotlib style.
        
        Args:
            style (str): Matplotlib style name
        """
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')
        sns.set_palette("husl")
    
    def plot_electron_shells_3d(self, element, save_path=None):
        """
        Create 3D visualization of electron shells.
        
        Args:
            element (dict): Element data
            save_path (str): Optional path to save figure
        """
        shells = element.get('shells', [])
        if not shells:
            print("No shell data available")
            return
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Create concentric spheres for each shell
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(shells)))
        
        for i, (electrons, color) in enumerate(zip(shells, colors)):
            radius = (i + 1) * 2
            x = radius * np.outer(np.cos(u), np.sin(v))
            y = radius * np.outer(np.sin(u), np.sin(v))
            z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
            
            ax.plot_surface(x, y, z, alpha=0.3, color=color, 
                          label=f'Shell {i+1}: {electrons} electrons')
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'{element["name"]} ({element["symbol"]}) - Electron Shell Structure')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_ionization_energies_3d(self, element, save_path=None):
        """
        Create 3D visualization of ionization energies.
        
        Args:
            element (dict): Element data
            save_path (str): Optional path to save figure
        """
        energies = element.get('ionization_energies', [])
        if not energies:
            print("No ionization energy data available")
            return
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Create 3D bar representation
        n_energies = len(energies)
        xpos = np.arange(n_energies)
        ypos = np.zeros(n_energies)
        zpos = np.zeros(n_energies)
        dx = np.ones(n_energies) * 0.8
        dy = np.ones(n_energies) * 0.8
        dz = np.array(energies) / 100  # Scale for better visualization
        
        colors = plt.cm.Spectral(np.linspace(0, 1, n_energies))
        
        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors, zsort='average')
        
        ax.set_xlabel('Ionization Level')
        ax.set_ylabel('Intensity')
        ax.set_zlabel('Energy (kJ/mol)')
        ax.set_title(f'{element["name"]} ({element["symbol"]}) - Ionization Energies')
        ax.set_xticks(xpos)
        ax.set_xticklabels([f'IE{i+1}' for i in range(n_energies)])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_thermal_properties_3d(self, element, save_path=None):
        """
        Create 3D visualization of thermal properties.
        
        Args:
            element (dict): Element data
            save_path (str): Optional path to save figure
        """
        boil = element.get('boil')
        melt = element.get('melt')
        molar_heat = element.get('molar_heat')
        density = element.get('density')
        
        if not all([boil, melt, density]):
            print("Insufficient thermal data available")
            return
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Prepare data
        properties = ['Melting Point', 'Boiling Point', 'Density']
        values = [melt, boil, density]
        
        # Normalize values for visualization
        values_norm = np.array(values) / np.max(values)
        
        # Create 3D scatter plot with additional dimension
        theta = np.linspace(0, 2*np.pi, len(properties))
        x = np.cos(theta)
        y = np.sin(theta)
        z = values_norm
        
        sizes = values_norm * 500
        colors = plt.cm.plasma(values_norm)
        
        ax.scatter(x, y, z, s=sizes, c=values_norm, cmap='plasma', 
                  alpha=0.6, edgecolors='black', linewidth=2)
        
        # Add labels for each point
        for i, prop in enumerate(properties):
            ax.text(x[i], y[i], z[i], f'{prop}\n{values[i]:.2f}', 
                   fontsize=9, ha='center')
        
        ax.set_xlabel('Property Type (X)')
        ax.set_ylabel('Property Type (Y)')
        ax.set_zlabel('Normalized Value')
        ax.set_title(f'{element["name"]} ({element["symbol"]}) - Thermal Properties')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_atomic_structure_3d(self, element, save_path=None):
        """
        Create 3D visualization of atomic structure based on electron configuration.
        
        Args:
            element (dict): Element data
            save_path (str): Optional path to save figure
        """
        shells = element.get('shells', [])
        if not shells:
            print("No shell data available")
            return
        
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')
        
        # Generate random points for electrons on shells
        total_electrons = sum(shells)
        colors_list = []
        x_coords = []
        y_coords = []
        z_coords = []
        
        electron_idx = 0
        color_palette = sns.color_palette("husl", len(shells))
        
        for shell_idx, num_electrons in enumerate(shells):
            radius = (shell_idx + 1) * 1.5
            
            # Generate random angles for electron distribution
            theta = np.random.uniform(0, 2*np.pi, num_electrons)
            phi = np.random.uniform(0, np.pi, num_electrons)
            
            x = radius * np.sin(phi) * np.cos(theta)
            y = radius * np.sin(phi) * np.sin(theta)
            z = radius * np.cos(phi)
            
            x_coords.extend(x)
            y_coords.extend(y)
            z_coords.extend(z)
            colors_list.extend([color_palette[shell_idx]] * num_electrons)
            
            # Draw shell orbit
            u = np.linspace(0, 2 * np.pi, 50)
            circle_x = radius * np.cos(u)
            circle_y = radius * np.sin(u)
            circle_z = np.zeros_like(u)
            ax.plot(circle_x, circle_y, circle_z, 'k--', alpha=0.3, linewidth=0.5)
        
        # Plot nucleus
        ax.scatter([0], [0], [0], s=500, c='red', marker='o', 
                  edgecolors='darkred', linewidth=2, label='Nucleus')
        
        # Plot electrons
        scatter = ax.scatter(x_coords, y_coords, z_coords, s=100, c=colors_list, 
                            alpha=0.6, edgecolors='black', linewidth=0.5, label='Electrons')
        
        ax.set_xlabel('X (Bohr radii)')
        ax.set_ylabel('Y (Bohr radii)')
        ax.set_zlabel('Z (Bohr radii)')
        ax.set_title(f'{element["name"]} ({element["symbol"]}) - Atomic Structure\n'
                    f'Electron Configuration: {element.get("electron_configuration_semantic", "N/A")}')
        ax.legend()
        
        # Set equal aspect ratio
        max_range = np.max([np.abs(x_coords).max(), np.abs(y_coords).max(), 
                           np.abs(z_coords).max()])
        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([-max_range, max_range])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_element_properties_comparison(self, elements, property_name, save_path=None):
        """
        Create 3D surface plot comparing element properties.
        
        Args:
            elements (list): List of element dictionaries
            property_name (str): Property to compare
            save_path (str): Optional path to save figure
        """
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Extract data
        atomic_numbers = []
        values = []
        names = []
        
        for elem in elements:
            num = elem.get('number')
            val = elem.get(property_name)
            if num is not None and val is not None:
                atomic_numbers.append(num)
                values.append(val)
                names.append(elem.get('symbol', 'Unknown'))
        
        if not atomic_numbers:
            print(f"No data available for property: {property_name}")
            return
        
        atomic_numbers = np.array(atomic_numbers)
        values = np.array(values)
        
        # Create surface
        periods = np.array([elem.get('period', 0) for elem in elements 
                           if elem.get('number') in atomic_numbers])
        groups = np.array([elem.get('group', 0) for elem in elements 
                          if elem.get('number') in atomic_numbers])
        
        colors = plt.cm.viridis(values / values.max())
        
        ax.scatter(atomic_numbers, periods[:len(atomic_numbers)], values, 
                  c=colors, s=100, alpha=0.6, edgecolors='black')
        
        ax.set_xlabel('Atomic Number')
        ax.set_ylabel('Period')
        ax.set_zlabel(property_name.replace('_', ' ').title())
        ax.set_title(f'Element Properties Comparison: {property_name.replace("_", " ").title()}')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_electronegativity_heatmap(self, elements_df, save_path=None):
        """
        Create interactive heatmap of electronegativity across periodic table.
        
        Args:
            elements_df (pd.DataFrame): DataFrame with element data
            save_path (str): Optional path to save figure
        """
        # Create periodic table matrix
        max_period = elements_df['period'].max()
        max_group = elements_df['group'].max()
        
        matrix = np.full((int(max_period), int(max_group)), np.nan)
        
        for _, row in elements_df.iterrows():
            period = int(row['period']) - 1
            group = int(row['group']) - 1
            electronegativity = row.get('electronegativity_pauling')
            if not np.isnan(electronegativity) if electronegativity is not None else False:
                matrix[period, group] = electronegativity
        
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.heatmap(matrix, cmap='RdYlGn', ax=ax, cbar_kws={'label': 'Electronegativity (Pauling)'})
        ax.set_title('Periodic Table - Electronegativity Distribution', fontsize=16, fontweight='bold')
        ax.set_xlabel('Group')
        ax.set_ylabel('Period')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
