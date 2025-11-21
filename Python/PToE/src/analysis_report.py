"""
Analysis report generator for periodic table data.
Generates PDF reports and PNG visualizations.
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
from pathlib import Path
from typing import Optional
from datetime import datetime

from src.element_database import ElementDatabase
from src.element_visual import ElementVisualizer


class AnalysisReportGenerator:
    """Generate comprehensive analysis reports and visualizations."""
    
    def __init__(self, database: ElementDatabase, output_dir: Optional[str] = None):
        """
        Initialize the report generator.
        
        Args:
            database: ElementDatabase instance
            output_dir: Directory to save reports. Defaults to 'periodic_table_analysis/'
        """
        self.db = database
        self.visualizer = ElementVisualizer(database)
        
        if output_dir is None:
            output_dir = 'periodic_table_analysis'
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_full_report(self, include_pdf: bool = True, include_png: bool = True):
        """
        Generate a complete analysis report with all visualizations.
        
        Args:
            include_pdf: Generate PDF report
            include_png: Generate PNG visualizations
        """
        print("Generating comprehensive periodic table analysis report...")
        
        if include_pdf:
            self._generate_pdf_report()
        
        if include_png:
            self._generate_png_visualizations()
        
        print(f"Report generation complete. Files saved to {self.output_dir}")
    
    def _generate_pdf_report(self):
        """Generate a PDF report with statistical analysis."""
        pdf_path = self.output_dir / 'periodic_table_analysis.pdf'
        
        with PdfPages(pdf_path) as pdf:
            # Page 1: Title and Summary Statistics
            self._add_title_page(pdf)
            
            # Page 2: Basic Statistics
            self._add_statistics_page(pdf)
            
            # Page 3-4: Element Categories
            self._add_categories_page(pdf)
            
            # Additional pages with visualizations
            self._add_visualization_pages(pdf)
        
        print(f"PDF report saved: {pdf_path}")
    
    def _add_title_page(self, pdf):
        """Add title page to PDF."""
        fig = plt.figure(figsize=(8.5, 11))
        ax = fig.add_subplot(111)
        
        ax.text(0.5, 0.9, "Periodic Table Analysis", 
               ha='center', va='top', fontsize=28, fontweight='bold',
               transform=ax.transAxes)
        
        ax.text(0.5, 0.75, "Comprehensive Statistical Report", 
               ha='center', va='top', fontsize=16,
               transform=ax.transAxes)
        
        ax.text(0.5, 0.65, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
               ha='center', va='top', fontsize=12,
               transform=ax.transAxes)
        
        summary_text = f"""
Total Elements: {self.db.get_element_count()}
Periods: {len(self.db.get_all_periods())}
Groups: {len(self.db.get_all_groups())}
Categories: {len(self.db.get_all_categories())}
Phases: {len(self.db.get_all_phases())}
        """
        
        ax.text(0.5, 0.45, summary_text, 
               ha='center', va='top', fontsize=12, family='monospace',
               transform=ax.transAxes)
        
        ax.axis('off')
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _add_statistics_page(self, pdf):
        """Add statistics page to PDF."""
        fig = plt.figure(figsize=(8.5, 11))
        
        # Create grid for statistics
        gs = fig.add_gridspec(3, 1, hspace=0.4)
        
        # Atomic mass statistics
        ax1 = fig.add_subplot(gs[0])
        ax1.axis('off')
        
        masses = [e.atomic_mass for e in self.db.get_all_elements()]
        mass_stats = f"""
ATOMIC MASS STATISTICS
Average: {sum(masses)/len(masses):.2f} u
Minimum: {min(masses):.2f} u ({self.db.get_element_by_number(1).symbol})
Maximum: {max(masses):.2f} u ({max((e for e in self.db.get_all_elements()), key=lambda x: x.atomic_mass).symbol})
Median: {sorted(masses)[len(masses)//2]:.2f} u
        """
        ax1.text(0.05, 0.9, mass_stats, ha='left', va='top', fontsize=10, 
                family='monospace', transform=ax1.transAxes)
        
        # Electronegativity statistics
        ax2 = fig.add_subplot(gs[1])
        ax2.axis('off')
        
        electroneg = [e.electronegativity for e in self.db.get_all_elements() 
                     if e.electronegativity is not None]
        electroneg_stats = f"""
ELECTRONEGATIVITY STATISTICS (Pauling Scale)
Average: {sum(electroneg)/len(electroneg):.2f}
Minimum: {min(electroneg):.2f}
Maximum: {max(electroneg):.2f}
Count with data: {len(electroneg)}
        """
        ax2.text(0.05, 0.9, electroneg_stats, ha='left', va='top', fontsize=10, 
                family='monospace', transform=ax2.transAxes)
        
        # Temperature statistics
        ax3 = fig.add_subplot(gs[2])
        ax3.axis('off')
        
        melts = [e.melt for e in self.db.get_all_elements() if e.melt is not None]
        boils = [e.boil for e in self.db.get_all_elements() if e.boil is not None]
        
        temp_stats = f"""
TEMPERATURE STATISTICS
Melting Points (K):
  Average: {sum(melts)/len(melts):.1f} K
  Min: {min(melts):.1f} K
  Max: {max(melts):.1f} K

Boiling Points (K):
  Average: {sum(boils)/len(boils):.1f} K
  Min: {min(boils):.1f} K
  Max: {max(boils):.1f} K
        """
        ax3.text(0.05, 0.9, temp_stats, ha='left', va='top', fontsize=10, 
                family='monospace', transform=ax3.transAxes)
        
        fig.suptitle('Statistical Analysis', fontsize=16, fontweight='bold')
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _add_categories_page(self, pdf):
        """Add element categories page to PDF."""
        fig, ax = plt.subplots(figsize=(8.5, 11))
        
        categories = self.db.get_all_categories()
        counts = [len(self.db.get_elements_by_category(cat)) for cat in categories]
        colors = [self.visualizer.get_category_color(cat) for cat in categories]
        
        y_pos = range(len(categories))
        ax.barh(y_pos, counts, color=colors, edgecolor='black', alpha=0.8)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(categories)
        ax.set_xlabel('Number of Elements')
        ax.set_title('Elements by Category')
        ax.grid(axis='x', alpha=0.3)
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _add_visualization_pages(self, pdf):
        """Add visualization pages to PDF."""
        # Add atomic mass distribution
        fig = self.visualizer.plot_atomic_mass_distribution()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
        
        # Add phase distribution
        fig = self.visualizer.plot_phase_distribution()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
        
        # Add elements per period
        fig = self.visualizer.plot_elements_per_period()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
        
        # Add atomic mass vs electronegativity
        fig = self.visualizer.plot_atomic_mass_vs_electronegativity()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
        
        # Add melting vs boiling points
        fig = self.visualizer.plot_melting_vs_boiling_points()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
        
        # Add densest elements
        fig = self.visualizer.plot_densest_elements()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
        
        # Add electronegativity heatmap
        fig = self.visualizer.plot_electronegativity_heatmap()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _generate_png_visualizations(self):
        """Generate individual PNG files for each visualization."""
        visualizations = {
            'atomic_mass_distribution.png': self.visualizer.plot_atomic_mass_distribution,
            'elements_by_category.png': self.visualizer.plot_elements_by_category,
            'phase_distribution.png': self.visualizer.plot_phase_distribution,
            'atomic_mass_vs_electronegativity.png': self.visualizer.plot_atomic_mass_vs_electronegativity,
            'melting_vs_boiling_points.png': self.visualizer.plot_melting_vs_boiling_points,
            'densest_elements.png': lambda: self.visualizer.plot_densest_elements(15),
            'elements_per_period.png': self.visualizer.plot_elements_per_period,
            'electronegativity_heatmap.png': self.visualizer.plot_electronegativity_heatmap,
            'property_correlation_matrix.png': self.visualizer.plot_property_correlation_matrix,
        }
        
        for filename, plot_func in visualizations.items():
            try:
                fig = plot_func()
                filepath = self.output_dir / filename
                self.visualizer.save_figure(fig, str(filepath))
                plt.close(fig)
            except Exception as e:
                print(f"Warning: Could not generate {filename}: {e}")
    
    def generate_element_details_csv(self):
        """Generate CSV file with all element details."""
        csv_path = self.output_dir / 'elements_data.csv'
        
        df = self.db.get_dataframe()
        df.to_csv(csv_path, index=False)
        
        print(f"CSV file saved: {csv_path}")
    
    def generate_summary_statistics(self) -> str:
        """
        Generate a text summary of periodic table statistics.
        
        Returns:
            Summary text
        """
        summary = f"""
{'='*70}
PERIODIC TABLE ANALYSIS SUMMARY
{'='*70}

BASIC INFORMATION
Total Elements: {self.db.get_element_count()}
Periods: {len(self.db.get_all_periods())}
Groups: {len(self.db.get_all_groups())}
Blocks: {len(self.db.get_all_blocks())}

CATEGORIES
"""
        
        for cat in self.db.get_all_categories():
            count = len(self.db.get_elements_by_category(cat))
            summary += f"  {cat:.<50} {count:>3d}\n"
        
        summary += f"""
PHASES
"""
        
        for phase in self.db.get_all_phases():
            count = len(self.db.get_elements_by_phase(phase))
            percentage = (count / self.db.get_element_count()) * 100
            summary += f"  {phase:.<50} {count:>3d} ({percentage:>5.1f}%)\n"
        
        summary += f"""
{'='*70}
"""
        
        return summary


if __name__ == '__main__':
    # Example usage
    db = ElementDatabase()
    generator = AnalysisReportGenerator(db)
    
    # Print summary
    print(generator.generate_summary_statistics())
    
    # Generate reports
    generator.generate_full_report(include_pdf=True, include_png=True)
    generator.generate_element_details_csv()
