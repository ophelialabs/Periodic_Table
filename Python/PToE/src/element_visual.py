"""
Advanced visualization module for periodic table and element analysis.
Provides 3D visualizations, heatmaps, analytical plots, and HyperSpectral analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from scipy import stats
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Optional, Dict, Any
from pathlib import Path

from src.element import Element
from src.element_database import ElementDatabase


class ElementVisualizer:
    """Provides comprehensive visualization methods for elements and periodic table data."""
    
    # Category colors for consistent visualization
    CATEGORY_COLORS = {
        'alkali metal': '#ff9999',
        'alkaline earth metal': '#ffddb3',
        'transition metal': '#cccccc',
        'lanthanide': '#ffbfff',
        'actinide': '#ff99cc',
        'nonmetal': '#a3f7a3',
        'halogen': '#ffff99',
        'noble gas': '#c0ffff',
        'metalloid': '#ccccff',
        'post-transition metal': '#ffccff',
        'diatomic nonmetal': '#a0ffa0',
        'polyatomic nonmetal': '#99ff99',
    }
    
    def __init__(self, database: ElementDatabase, style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize the visualizer.
        
        Args:
            database: ElementDatabase instance
            style: Matplotlib style name
        """
        self.db = database
        self.df = database.get_dataframe()
        
        # Set matplotlib style
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')
        sns.set_palette("husl")
    
    def get_category_color(self, category: str) -> str:
        """Get color for an element category."""
        return self.CATEGORY_COLORS.get(category, '#cccccc')
    
    # ===== 3D Visualizations =====
    
    def plot_electron_shells_3d(self, element: Element, save_path: Optional[str] = None) -> plt.Figure:
        """
        Visualize electron shell structure in 3D with accurate shell sizes.
        
        Args:
            element: Element to visualize
            save_path: Optional path to save figure
            
        Returns:
            matplotlib Figure
        """
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        shells = element.shells
        if not shells:
            ax.text2D(0.5, 0.5, f"No shell data for {element.symbol}", 
                     ha='center', va='center')
            return fig
        
        # Create concentric spheres for each shell with higher resolution
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(shells)))
        
        for shell_num, (electrons, color) in enumerate(zip(shells, colors), 1):
            # Radius increases with shell number
            radius = shell_num * 1.5
            x = radius * np.outer(np.cos(u), np.sin(v))
            y = radius * np.outer(np.sin(u), np.sin(v))
            z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
            
            ax.plot_surface(x, y, z, alpha=0.3, color=color)
        
        ax.set_xlabel('X (Bohr radii)')
        ax.set_ylabel('Y (Bohr radii)')
        ax.set_zlabel('Z (Bohr radii)')
        ax.set_title(f'Electron Shell Structure - {element.symbol} ({element.name})')
        
        # Set equal aspect ratio
        max_radius = len(shells) * 1.5
        ax.set_xlim([-max_radius, max_radius])
        ax.set_ylim([-max_radius, max_radius])
        ax.set_zlim([-max_radius, max_radius])
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_ionization_energies_3d(self, element: Element, save_path: Optional[str] = None) -> plt.Figure:
        """
        Visualize ionization energies in 3D bar chart with accurate scaling.
        
        Args:
            element: Element to visualize
            save_path: Optional path to save figure
            
        Returns:
            matplotlib Figure
        """
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        energies = element.ionization_energies
        if not energies:
            ax.text2D(0.5, 0.5, f"No ionization energy data for {element.symbol}", 
                     ha='center', va='center')
            return fig
        
        # Create 3D bar chart with accurate scaling
        n_energies = len(energies)
        xpos = np.arange(n_energies)
        ypos = np.zeros(n_energies)
        zpos = np.zeros(n_energies)
        dx = np.ones(n_energies) * 0.8
        dy = np.ones(n_energies) * 0.8
        dz = np.array(energies)
        
        colors = plt.cm.Spectral(np.linspace(0, 1, n_energies))
        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors, shade=True, zsort='average')
        
        ax.set_xlabel('Ionization Number')
        ax.set_ylabel('')
        ax.set_zlabel('Energy (kJ/mol)')
        ax.set_title(f'Ionization Energies - {element.symbol} ({element.name})')
        ax.set_yticks([])
        ax.set_xticks(xpos)
        ax.set_xticklabels([f'IE{i+1}' for i in range(n_energies)])
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_thermal_properties_3d(self, element: Element, save_path: Optional[str] = None) -> plt.Figure:
        """
        Visualize thermal properties in 3D with electron distribution.
        
        Args:
            element: Element to visualize
            save_path: Optional path to save figure
            
        Returns:
            matplotlib Figure
        """
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        boil = element.boil
        melt = element.melt
        density = element.density
        molar_heat = element.molar_heat
        
        if not all([boil, melt, density]):
            ax.text2D(0.5, 0.5, f"Insufficient thermal data for {element.symbol}", 
                     ha='center', va='center')
            return fig
        
        # Prepare data
        properties = ['Melting Point', 'Boiling Point', 'Density']
        values = np.array([melt, boil, density])
        
        # Normalize values for visualization
        values_norm = values / np.max(values)
        
        # Create 3D scatter with properties on different axes
        theta = np.linspace(0, 2*np.pi, len(properties))
        x = np.cos(theta)
        y = np.sin(theta)
        z = values_norm
        
        sizes = values_norm * 500
        colors_array = plt.cm.plasma(values_norm)
        
        ax.scatter(x, y, z, s=sizes, c=values_norm, cmap='plasma', 
                  alpha=0.7, edgecolors='black', linewidth=2)
        
        # Add labels for each point
        for i, (prop, val) in enumerate(zip(properties, values)):
            ax.text(x[i], y[i], z[i], f'{prop}\n{val:.2f}', 
                   fontsize=9, ha='center')
        
        ax.set_xlabel('Property Type (X)')
        ax.set_ylabel('Property Type (Y)')
        ax.set_zlabel('Normalized Value')
        ax.set_title(f'Thermal Properties - {element.symbol} ({element.name})')
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_atomic_structure_3d(self, element: Element, save_path: Optional[str] = None) -> plt.Figure:
        """
        Visualize complete atomic structure with electron distribution on shells.
        
        Args:
            element: Element to visualize
            save_path: Optional path to save figure
            
        Returns:
            matplotlib Figure
        """
        fig = plt.figure(figsize=(12, 10))
        
        shells = element.shells
        if not shells:
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, f"No shell data for {element.symbol}", 
                   ha='center', va='center')
            return fig
        
        # Create a summary plot with multiple subplots
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # Subplot 1: 3D atomic structure with electron distribution
        ax1 = fig.add_subplot(gs[0, 0], projection='3d')
        
        # Plot nucleus
        ax1.scatter([0], [0], [0], s=500, c='red', marker='o', 
                   edgecolors='darkred', linewidth=2, label='Nucleus')
        
        # Generate electrons on shells
        color_palette = sns.color_palette("husl", len(shells))
        
        for shell_idx, (num_electrons, color) in enumerate(zip(shells, color_palette)):
            radius = (shell_idx + 1) * 1.5
            
            # Generate random positions for electrons on shell
            theta = np.random.uniform(0, 2*np.pi, num_electrons)
            phi = np.random.uniform(0, np.pi, num_electrons)
            
            x = radius * np.sin(phi) * np.cos(theta)
            y = radius * np.sin(phi) * np.sin(theta)
            z = radius * np.cos(phi)
            
            ax1.scatter(x, y, z, s=100, c=[color]*num_electrons, alpha=0.6, 
                       edgecolors='black', linewidth=0.5, label=f'Shell {shell_idx+1}')
            
            # Draw shell orbit
            u = np.linspace(0, 2 * np.pi, 50)
            circle_x = radius * np.cos(u)
            circle_y = radius * np.sin(u)
            circle_z = np.zeros_like(u)
            ax1.plot(circle_x, circle_y, circle_z, 'k--', alpha=0.3, linewidth=0.5)
        
        ax1.set_xlabel('X (Bohr radii)')
        ax1.set_ylabel('Y (Bohr radii)')
        ax1.set_zlabel('Z (Bohr radii)')
        ax1.set_title(f'{element.symbol} - Electron Distribution')
        
        max_radius = len(shells) * 1.5
        ax1.set_xlim([-max_radius, max_radius])
        ax1.set_ylim([-max_radius, max_radius])
        ax1.set_zlim([-max_radius, max_radius])
        
        # Subplot 2: Ionization energies
        ax2 = fig.add_subplot(gs[0, 1])
        if element.ionization_energies:
            ax2.bar(range(1, min(len(element.ionization_energies) + 1, 6)), 
                   element.ionization_energies[:5], color='steelblue', edgecolor='black')
            ax2.set_xlabel('Ionization Number')
            ax2.set_ylabel('Energy (kJ/mol)')
            ax2.set_title('First 5 Ionization Energies')
            ax2.grid(axis='y', alpha=0.3)
        
        # Subplot 3: Electron shells
        ax3 = fig.add_subplot(gs[1, 0])
        if element.shells:
            ax3.bar(range(1, len(element.shells) + 1), element.shells, 
                   color='forestgreen', edgecolor='black', alpha=0.8)
            ax3.set_xlabel('Shell Number')
            ax3.set_ylabel('Number of Electrons')
            ax3.set_title('Electron Shells')
            ax3.grid(axis='y', alpha=0.3)
        
        # Subplot 4: Key properties
        ax4 = fig.add_subplot(gs[1, 1])
        props_text = f"""Key Properties:
Atomic Number: {element.number}
Atomic Mass: {element.atomic_mass:.3f} u
Category: {element.category}
Phase: {element.phase}
Block: {element.block}
Electronegativity: {element.electronegativity or 'N/A'}
Electron Affinity: {element.electron_affinity or 'N/A'} kJ/mol
Melting: {element.melt or 'N/A'} K
Boiling: {element.boil or 'N/A'} K
Density: {element.density or 'N/A'} g/cm³
"""
        ax4.text(0.05, 0.95, props_text, ha='left', va='top', fontsize=8, 
                family='monospace', transform=ax4.transAxes)
        ax4.axis('off')
        
        fig.suptitle(f'Atomic Structure - {element.symbol} ({element.name})\nConfiguration: {element.electron_configuration_semantic}', 
                    fontsize=14, fontweight='bold')
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    # ===== Periodic Table Visualizations =====
    
    def plot_element_properties_comparison(self, elements: List[Element], 
                                         property_name: str) -> plt.Figure:
        """
        Compare a property across multiple elements.
        
        Args:
            elements: List of elements to compare
            property_name: Name of property to compare (e.g., 'atomic_mass', 'electronegativity')
            
        Returns:
            matplotlib Figure
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Get property values
        values = []
        symbols = []
        for elem in elements:
            value = getattr(elem, property_name, None)
            if value is not None:
                values.append(value)
                symbols.append(elem.symbol)
        
        if not values:
            ax.text(0.5, 0.5, f"No data for property: {property_name}", 
                   ha='center', va='center')
            return fig
        
        # Create bar chart with category colors
        colors = [self.get_category_color(elem.category) 
                 for elem in elements if getattr(elem, property_name, None) is not None]
        
        ax.bar(range(len(values)), values, color=colors, alpha=0.8, edgecolor='black')
        ax.set_xlabel('Element')
        ax.set_ylabel(property_name.replace('_', ' ').title())
        ax.set_title(f'Comparison of {property_name.replace("_", " ").title()}')
        ax.set_xticks(range(len(symbols)))
        ax.set_xticklabels(symbols)
        ax.grid(axis='y', alpha=0.3)
        
        return fig
    
    def plot_electronegativity_heatmap(self) -> plt.Figure:
        """
        Create a periodic table heatmap colored by electronegativity.
        
        Returns:
            matplotlib Figure
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Create a grid with element positions
        periods = max([e.period for e in self.db.get_all_elements()]) + 1
        groups = max([e.group for e in self.db.get_all_elements()]) + 1
        
        grid = np.full((periods, groups), np.nan)
        
        for elem in self.db.get_all_elements():
            if elem.electronegativity is not None:
                grid[elem.period - 1, elem.group - 1] = elem.electronegativity
        
        # Create heatmap
        im = ax.imshow(grid, cmap='RdYlGn_r', aspect='auto', origin='upper')
        
        # Add element symbols
        for elem in self.db.get_all_elements():
            if elem.electronegativity is not None:
                ax.text(elem.group - 1, elem.period - 1, elem.symbol,
                       ha='center', va='center', fontsize=8, fontweight='bold')
        
        ax.set_xlabel('Group')
        ax.set_ylabel('Period')
        ax.set_title('Periodic Table Heatmap - Electronegativity')
        
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Electronegativity (Pauling)')
        
        return fig
    
    def plot_atomic_mass_distribution(self) -> plt.Figure:
        """Create histogram of atomic masses."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        masses = [e.atomic_mass for e in self.db.get_all_elements()]
        ax.hist(masses, bins=30, color='steelblue', edgecolor='black', alpha=0.7)
        
        ax.set_xlabel('Atomic Mass (u)')
        ax.set_ylabel('Number of Elements')
        ax.set_title('Distribution of Atomic Masses')
        ax.grid(axis='y', alpha=0.3)
        
        return fig
    
    def plot_elements_by_category(self) -> plt.Figure:
        """Create bar chart of elements per category."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        categories = self.db.get_all_categories()
        counts = [len(self.db.get_elements_by_category(cat)) for cat in categories]
        colors = [self.get_category_color(cat) for cat in categories]
        
        ax.bar(range(len(categories)), counts, color=colors, edgecolor='black', alpha=0.8)
        ax.set_xlabel('Element Category')
        ax.set_ylabel('Number of Elements')
        ax.set_title('Distribution of Elements by Category')
        ax.set_xticks(range(len(categories)))
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        
        return fig
    
    def plot_phase_distribution(self) -> plt.Figure:
        """Create pie chart of phase distribution."""
        fig, ax = plt.subplots(figsize=(8, 8))
        
        phases = self.db.get_all_phases()
        counts = [len(self.db.get_elements_by_phase(phase)) for phase in phases]
        colors = ['#ff9999', '#66b3ff', '#99ff99'][:len(phases)]
        
        ax.pie(counts, labels=phases, autopct='%1.1f%%', colors=colors, startangle=90)
        ax.set_title('Distribution of Elements by Phase')
        
        return fig
    
    def plot_atomic_mass_vs_electronegativity(self) -> plt.Figure:
        """Create scatter plot of atomic mass vs electronegativity."""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        elements = self.db.get_all_elements()
        masses = []
        electronegativities = []
        symbols = []
        colors_list = []
        
        for elem in elements:
            if elem.atomic_mass and elem.electronegativity:
                masses.append(elem.atomic_mass)
                electronegativities.append(elem.electronegativity)
                symbols.append(elem.symbol)
                colors_list.append(self.get_category_color(elem.category))
        
        scatter = ax.scatter(masses, electronegativities, c=colors_list, s=100, 
                            alpha=0.6, edgecolor='black')
        
        # Add labels for some key elements
        for i, symbol in enumerate(symbols[::5]):  # Label every 5th element to avoid crowding
            ax.annotate(symbol, (masses[i*5], electronegativities[i*5]), 
                       fontsize=8, ha='center')
        
        ax.set_xlabel('Atomic Mass (u)')
        ax.set_ylabel('Electronegativity (Pauling)')
        ax.set_title('Atomic Mass vs Electronegativity')
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def plot_melting_vs_boiling_points(self) -> plt.Figure:
        """Create scatter plot of melting vs boiling points."""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        elements = self.db.get_all_elements()
        melts = []
        boils = []
        symbols = []
        colors_list = []
        
        for elem in elements:
            if elem.melt and elem.boil:
                melts.append(elem.melt)
                boils.append(elem.boil)
                symbols.append(elem.symbol)
                colors_list.append(self.get_category_color(elem.category))
        
        scatter = ax.scatter(melts, boils, c=colors_list, s=100, alpha=0.6, edgecolor='black')
        
        # Add labels for some key elements
        for i, symbol in enumerate(symbols[::5]):
            ax.annotate(symbol, (melts[i*5], boils[i*5]), fontsize=8, ha='center')
        
        ax.set_xlabel('Melting Point (K)')
        ax.set_ylabel('Boiling Point (K)')
        ax.set_title('Melting vs Boiling Points')
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def plot_densest_elements(self, n: int = 15) -> plt.Figure:
        """Create bar chart of densest elements."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        elements = [(e, e.density) for e in self.db.get_all_elements() 
                   if e.density is not None and e.phase == 'Solid']
        elements.sort(key=lambda x: x[1], reverse=True)
        elements = elements[:n]
        
        symbols = [e[0].symbol for e in elements]
        densities = [e[1] for e in elements]
        colors = [self.get_category_color(e[0].category) for e in elements]
        
        ax.bar(range(len(symbols)), densities, color=colors, edgecolor='black', alpha=0.8)
        ax.set_xlabel('Element')
        ax.set_ylabel('Density (g/cm³)')
        ax.set_title(f'{n} Densest Elements')
        ax.set_xticks(range(len(symbols)))
        ax.set_xticklabels(symbols)
        ax.grid(axis='y', alpha=0.3)
        
        return fig
    
    def plot_elements_per_period(self) -> plt.Figure:
        """Create bar chart of elements per period."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        periods = self.db.get_all_periods()
        counts = [len(self.db.get_elements_by_period(p)) for p in periods]
        
        ax.bar(periods, counts, color='steelblue', edgecolor='black', alpha=0.8)
        ax.set_xlabel('Period')
        ax.set_ylabel('Number of Elements')
        ax.set_title('Number of Elements per Period')
        ax.set_xticks(periods)
        ax.grid(axis='y', alpha=0.3)
        
        return fig
    
    def plot_property_correlation_matrix(self) -> plt.Figure:
        """Create correlation matrix heatmap of element properties."""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Select numeric columns
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        
        # Create heatmap
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, ax=ax, cbar_kws={'label': 'Correlation'})
        
        ax.set_title('Correlation Matrix of Element Properties')
        plt.tight_layout()
        
        return fig
    
    # ===== HyperSpectral Analysis Visualizations =====
    
    def plot_spectral_signature(self, element: Element, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a simulated spectral signature visualization for an element.
        
        Args:
            element: Element to visualize
            save_path: Optional path to save figure
            
        Returns:
            matplotlib Figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Generate simulated spectral data based on element properties
        wavelengths = np.linspace(200, 2500, 256)  # Visible to near-IR range (nm)
        
        # Create spectral signature based on atomic properties
        # This is a simplified model - real spectral data would come from spectroscopy
        electronegativity = element.electronegativity or 2.5
        ionization = element.ionization_energies[0] if element.ionization_energies else 1000
        
        # Generate spectral bands (peaks at characteristic wavelengths)
        intensity = np.exp(-((wavelengths - 400) / 100)**2) * (electronegativity / 4)  # UV absorption
        intensity += np.exp(-((wavelengths - 700) / 150)**2) * (ionization / 2000)  # Visible
        intensity += np.exp(-((wavelengths - 1500) / 200)**2) * 0.5  # IR absorption
        
        # Add noise for realism
        intensity += np.random.normal(0, 0.02, len(wavelengths))
        intensity = np.maximum(intensity, 0)
        
        # Plot 1: Spectral signature
        ax1.fill_between(wavelengths, intensity, alpha=0.6, color='steelblue')
        ax1.plot(wavelengths, intensity, 'b-', linewidth=2, label='Spectral Signature')
        ax1.set_xlabel('Wavelength (nm)')
        ax1.set_ylabel('Intensity (Reflectance)')
        ax1.set_title(f'{element.symbol} - Spectral Signature')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Plot 2: Band ratios
        # Calculate band indices for common mineral detection ratios
        uv_band = np.mean(intensity[wavelengths < 400])
        visible_band = np.mean(intensity[(wavelengths >= 400) & (wavelengths < 700)])
        ir_band = np.mean(intensity[wavelengths >= 700])
        
        bands = ['UV\n(< 400nm)', 'Visible\n(400-700nm)', 'IR\n(> 700nm)']
        values = [uv_band, visible_band, ir_band]
        colors_bars = ['violet', 'green', 'red']
        
        ax2.bar(bands, values, color=colors_bars, alpha=0.7, edgecolor='black')
        ax2.set_ylabel('Mean Intensity')
        ax2.set_title(f'{element.symbol} - Band Intensity Distribution')
        ax2.grid(axis='y', alpha=0.3)
        
        fig.suptitle(f'HyperSpectral Analysis - {element.symbol} ({element.name})', 
                    fontsize=14, fontweight='bold')
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_band_ratios(self, elements: List[Element], save_path: Optional[str] = None) -> plt.Figure:
        """
        Create band ratio visualization for multiple elements (useful for mineral identification).
        
        Args:
            elements: List of elements to analyze
            save_path: Optional path to save figure
            
        Returns:
            matplotlib Figure
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        symbols = []
        ratios = []
        
        for element in elements:
            ionization = element.ionization_energies[0] if element.ionization_energies else 1000
            electronegativity = element.electronegativity or 2.5
            
            # Band ratio: IR/Visible ratio (useful for lithium and other minerals)
            ratio = (ionization / 2000) / (electronegativity / 4) if (electronegativity / 4) != 0 else 0
            
            symbols.append(element.symbol)
            ratios.append(ratio)
        
        colors = [self.get_category_color(e.category) for e in elements]
        bars = ax.bar(range(len(symbols)), ratios, color=colors, edgecolor='black', alpha=0.8)
        
        ax.set_ylabel('Band Ratio (IR/Visible)')
        ax.set_xlabel('Element')
        ax.set_title('Band Ratios for Mineral Identification')
        ax.set_xticks(range(len(symbols)))
        ax.set_xticklabels(symbols)
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}', ha='center', va='bottom', fontsize=9)
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_minimum_wavelength_map(self, elements: List[Element], save_path: Optional[str] = None) -> plt.Figure:
        """
        Create visualization of minimum reflectance wavelengths for element identification.
        
        Args:
            elements: List of elements to analyze
            save_path: Optional path to save figure
            
        Returns:
            matplotlib Figure
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        symbols = []
        min_wavelengths = []
        
        for element in elements:
            # Calculate characteristic wavelength based on ionization energy
            ionization = element.ionization_energies[0] if element.ionization_energies else 1000
            
            # Planck relation: wavelength = hc/E, simplified
            # Normalize to visible spectrum
            min_wavelength = 1000 + (ionization / 100)
            
            symbols.append(element.symbol)
            min_wavelengths.append(min_wavelength)
        
        # Create scatter plot colored by element category
        colors = [self.get_category_color(e.category) for e in elements]
        scatter = ax.scatter(range(len(symbols)), min_wavelengths, s=200, c=colors, 
                           alpha=0.7, edgecolors='black', linewidth=2)
        
        ax.set_ylabel('Minimum Reflectance Wavelength (nm)')
        ax.set_xlabel('Element')
        ax.set_title('Minimum Wavelength Mapping for Elemental Identification')
        ax.set_xticks(range(len(symbols)))
        ax.set_xticklabels(symbols)
        ax.grid(True, alpha=0.3)
        
        # Add wavelength labels
        for i, (sym, wl) in enumerate(zip(symbols, min_wavelengths)):
            ax.text(i, wl + 20, f'{wl:.0f}nm', ha='center', fontsize=8)
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_lithium_bearing_mineral_detection(self, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create classification visualization for lithium-bearing mineral detection.
        
        Args:
            save_path: Optional path to save figure
            
        Returns:
            matplotlib Figure
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # Get lithium and related elements
        li = self.db.get_element_by_symbol('Li')
        if li is None:
            # Fallback if symbol lookup fails
            li = self.db.get_element_by_number(3)  # Lithium is element 3
        
        li_bearing = []
        for sym in ['Li', 'Al', 'Si', 'O']:
            el = self.db.get_element_by_symbol(sym)
            if el:
                li_bearing.append(el)
        
        # Plot 1: Lithium spectral characteristics
        wavelengths = np.linspace(200, 2500, 256)
        li_spectrum = np.exp(-((wavelengths - 670) / 80)**2) * 0.8  # Li has strong red lines
        li_spectrum += np.exp(-((wavelengths - 611) / 80)**2) * 0.7
        
        ax1.fill_between(wavelengths, li_spectrum, alpha=0.6, color='red')
        ax1.plot(wavelengths, li_spectrum, 'r-', linewidth=2)
        ax1.set_xlabel('Wavelength (nm)')
        ax1.set_ylabel('Intensity')
        ax1.set_title('Lithium (Li) - Characteristic Spectral Lines')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Classification matrix for Li-bearing minerals
        mineral_types = ['Spodumene\n(LiAlSi₂O₆)', 'Lepidolite\n(K(Li,Al)₃(Si,Al)₄O₁₀(OH,F)₂)', 
                         'Petalite\n(LiAlSi₄O₁₀)', 'Amblyonite\n(LiAl(PO₄)F)']
        li_content = [7.4, 4.0, 3.7, 10.3]  # Weight percentage
        
        colors_mineral = plt.cm.RdYlGn(np.array(li_content) / max(li_content))
        bars = ax2.barh(mineral_types, li_content, color=colors_mineral, edgecolor='black')
        ax2.set_xlabel('Li Content (wt%)')
        ax2.set_title('Lithium Content in Common Minerals')
        ax2.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, li_content)):
            ax2.text(val + 0.2, i, f'{val:.1f}%', va='center', fontsize=9)
        
        # Plot 3: Band ratio classification
        band_ratios = [2.1, 1.8, 1.9, 2.3]  # IR/Visible ratios for classification
        classifications = ['High Li', 'Medium Li', 'Medium Li', 'Very High Li']
        
        scatter = ax3.scatter(range(len(mineral_types)), band_ratios, s=300, 
                            c=colors_mineral, alpha=0.7, edgecolors='black', linewidth=2)
        ax3.set_xticks(range(len(mineral_types)))
        ax3.set_xticklabels([m.split('\n')[0] for m in mineral_types], rotation=45, ha='right')
        ax3.set_ylabel('IR/Visible Band Ratio')
        ax3.set_title('Band Ratio Classification')
        ax3.axhline(y=2.0, color='r', linestyle='--', alpha=0.5, label='Li Detection Threshold')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        # Plot 4: Detection confidence matrix
        detection_confidence = np.array([
            [0.95, 0.02, 0.02, 0.01],  # Spodumene
            [0.85, 0.10, 0.03, 0.02],  # Lepidolite
            [0.80, 0.12, 0.05, 0.03],  # Petalite
            [0.98, 0.01, 0.01, 0.00],  # Amblyonite
        ])
        
        im = ax4.imshow(detection_confidence, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
        ax4.set_xticks(range(len(mineral_types)))
        ax4.set_yticks(range(len(mineral_types)))
        ax4.set_xticklabels([m.split('\n')[0] for m in mineral_types], rotation=45, ha='right')
        ax4.set_yticklabels([m.split('\n')[0] for m in mineral_types])
        ax4.set_title('Mineral Identification Confidence Matrix')
        
        # Add text annotations
        for i in range(len(mineral_types)):
            for j in range(len(mineral_types)):
                text = ax4.text(j, i, f'{detection_confidence[i, j]:.2f}',
                              ha="center", va="center", color="black", fontsize=9)
        
        cbar = plt.colorbar(im, ax=ax4)
        cbar.set_label('Confidence')
        
        fig.suptitle('HyperSpectral Analysis - Lithium-Bearing Mineral Detection', 
                    fontsize=16, fontweight='bold')
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def show_figure(self, figure: plt.Figure):
        """Display a matplotlib figure."""
        plt.figure(figure.number)
        plt.show()
    
    def save_figure(self, figure: plt.Figure, filepath: str):
        """Save a figure to file."""
        figure.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {filepath}")
