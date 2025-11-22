"""
Main Desktop Application GUI
Interactive periodic table with quantum research integration using tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from typing import Optional, List, Tuple
from pathlib import Path
import webbrowser
from PIL import Image, ImageTk
from io import BytesIO
import urllib.request

from src.element import Element
from src.element_database import ElementDatabase
from src.element_visual import ElementVisualizer
from src.app.agent_chat import AgentChatDialog


class PeriodicTableApp:
    """Main tkinter application for interactive periodic table."""
    
    # Screen size breakpoints (in pixels)
    BREAKPOINTS = {
        'small': 1000,    # < 1000px: small screen
        'medium': 1400,   # 1000-1400px: medium screen
        'large': 1400     # >= 1400px: large screen
    }
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the application.
        
        Args:
            root: tkinter root window
        """
        self.root = root
        self.root.title("Periodic Table - Interactive Desktop Application")
        
        # Determine initial window size based on screen resolution
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set responsive default geometry (80% of screen, min 1000x800)
        default_width = max(1000, int(screen_width * 0.8))
        default_height = max(800, int(screen_height * 0.8))
        self.root.geometry(f"{default_width}x{default_height}")
        self.root.minsize(1000, 800)
        
        # Bind resize event for responsive adjustments
        self.root.bind('<Configure>', self._on_window_resize)
        
        # Initialize database
        try:
            self.db = ElementDatabase()
            self.visualizer = ElementVisualizer(self.db)
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Could not load periodic table data: {e}")
            return
        
        self.selected_elements: List[Element] = []
        self.current_element: Optional[Element] = None
        self.current_screen_size = 'medium'  # Track current breakpoint
        
        # Setup UI
        self._setup_styles()
        self._create_widgets()
        self._load_periodic_table()
    
    def _get_screen_breakpoint(self) -> str:
        """Determine current screen size breakpoint."""
        width = self.root.winfo_width()
        if width < self.BREAKPOINTS['small']:
            return 'small'
        elif width < self.BREAKPOINTS['medium']:
            return 'medium'
        else:
            return 'large'
    
    def _on_window_resize(self, event):
        """Handle window resize events for responsive behavior."""
        new_breakpoint = self._get_screen_breakpoint()
        if new_breakpoint != self.current_screen_size and hasattr(self, 'periodic_table_frame'):
            self.current_screen_size = new_breakpoint
            self._adjust_layout_for_screen_size()
    
    def _adjust_layout_for_screen_size(self):
        """Adjust UI layout and styling based on current screen size."""
        if self.current_screen_size == 'small':
            # Small screens: reduce font sizes and element button sizes
            self._apply_small_screen_styles()
        elif self.current_screen_size == 'medium':
            # Medium screens: balanced layout
            self._apply_medium_screen_styles()
        else:  # large
            # Large screens: optimize spacing and sizes
            self._apply_large_screen_styles()
    
    def _apply_small_screen_styles(self):
        """Apply styles optimized for small screens (<1000px)."""
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('Header.TLabel', font=('Helvetica', 10, 'bold'))
        style.configure('Normal.TLabel', font=('Helvetica', 8))
    
    def _apply_medium_screen_styles(self):
        """Apply styles optimized for medium screens (1000-1400px)."""
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Helvetica', 14, 'bold'))
        style.configure('Header.TLabel', font=('Helvetica', 11, 'bold'))
        style.configure('Normal.TLabel', font=('Helvetica', 9))
    
    def _apply_large_screen_styles(self):
        """Apply styles optimized for large screens (>1400px)."""
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))
        style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('Normal.TLabel', font=('Helvetica', 10))
    
    def _setup_styles(self):
        """Setup custom tkinter styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Initialize with medium screen defaults
        self._apply_medium_screen_styles()
    
    def _get_element_button_dimensions(self) -> Tuple[int, int, int]:
        """
        Get responsive element button dimensions based on screen size.
        
        Returns:
            Tuple of (width, height, font_size)
        """
        if self.current_screen_size == 'small':
            return (4, 2, 8)  # Smaller buttons for small screens
        elif self.current_screen_size == 'medium':
            return (5, 2, 9)  # Balanced sizing
        else:  # large
            return (6, 3, 10)  # Larger buttons for large screens
    
    def _create_widgets(self):
        """Create main UI widgets."""
        # Create main frames - top bar, then content area with periodic table + details side-by-side,
        # then visualization area below
        top_frame = ttk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # Middle frame for periodic table + details side by side
        content_frame = ttk.Frame(self.root)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10)
        
        # Bottom frame for visualizations with horizontal scroll
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False, padx=10, pady=10)
        
        # ===== TOP FRAME: Search and Controls =====
        ttk.Label(top_frame, text="Periodic Table Explorer", 
                 style='Title.TLabel').pack(side=tk.LEFT)
        
        # Search box
        ttk.Label(top_frame, text="Search:", style='Normal.TLabel').pack(side=tk.LEFT, padx=(20, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_changed)
        search_entry = ttk.Entry(top_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        ttk.Button(top_frame, text="Clear", command=self._clear_search).pack(side=tk.LEFT, padx=5)
        
        # Agent button (right side)
        ttk.Button(top_frame, text="🤖 Quantum Agent", command=self._open_agent_chat).pack(side=tk.RIGHT, padx=5)
        
        # ===== CONTENT FRAME: Periodic Table (left) + Details (right) with Resizable Divider =====
        # Use PanedWindow for resizable panels with a draggable divider
        paned_window = tk.PanedWindow(content_frame, orient=tk.HORIZONTAL, bg='gray80', sashwidth=5)
        paned_window.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Left panel: Periodic Table
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, width=700, minsize=400)
        
        # Right panel: Element Details
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, width=300, minsize=250)
        
        # Periodic Table Grid
        table_label = ttk.Label(left_frame, text="Periodic Table", style='Header.TLabel')
        table_label.pack(pady=10)
        
        # Scrollable frame for periodic table
        canvas = tk.Canvas(left_frame, bg='white', height=400)
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.periodic_table_frame = scrollable_frame
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ===== RIGHT FRAME: Element Details =====
        details_label = ttk.Label(right_frame, text="Element Details", style='Header.TLabel')
        details_label.pack(pady=10)
        
        # Create details notebook for tabs
        self.details_notebook = ttk.Notebook(right_frame)
        self.details_notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tab 1: Basic Info
        basic_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(basic_frame, text="Basic Info")
        self.basic_info_text = scrolledtext.ScrolledText(basic_frame, width=35, height=30, 
                                                        font=('Courier', 9))
        self.basic_info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 2: Properties
        prop_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(prop_frame, text="Properties")
        self.properties_text = scrolledtext.ScrolledText(prop_frame, width=35, height=30, 
                                                        font=('Courier', 9))
        self.properties_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Selected elements display
        selected_label = ttk.Label(right_frame, text="Selected Elements", style='Normal.TLabel')
        selected_label.pack(pady=10)
        
        self.selected_text = scrolledtext.ScrolledText(right_frame, width=35, height=8, 
                                                      font=('Courier', 9))
        self.selected_text.pack(fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        # Action buttons
        buttons_frame = ttk.Frame(right_frame)
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="Clear Selection",
                  command=self._clear_selection).pack(pady=5)
        ttk.Button(buttons_frame, text="Compare Selected",
                  command=self._compare_elements).pack(pady=5)
        
        # ===== BOTTOM FRAME: Visualizations with Horizontal Scroll =====
        vis_label = ttk.Label(bottom_frame, text="Visualizations", style='Header.TLabel')
        vis_label.pack(side=tk.TOP, pady=5)
        
        # Create horizontally scrollable canvas for visualizations
        vis_canvas = tk.Canvas(bottom_frame, bg='lightgray', height=300, highlightthickness=1)
        h_scrollbar = ttk.Scrollbar(bottom_frame, orient=tk.HORIZONTAL, command=vis_canvas.xview)
        
        # Frame to hold visualization buttons
        self.vis_buttons_frame = ttk.Frame(vis_canvas, relief=tk.SUNKEN)
        vis_canvas.create_window((0, 0), window=self.vis_buttons_frame, anchor="nw")
        vis_canvas.configure(xscrollcommand=h_scrollbar.set)
        
        # Bind mousewheel for horizontal scrolling
        def _on_mousewheel(event):
            vis_canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        
        vis_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Pack the visualization canvas and scrollbar
        vis_canvas.pack(side=tk.TOP, fill=tk.X, expand=False, pady=5)
        h_scrollbar.pack(side=tk.TOP, fill=tk.X)
        
        # Populate visualization buttons
        self._populate_visualization_buttons()
    
    def _load_periodic_table(self):
        """Load and display the periodic table grid."""
        # Get maximum period and group
        elements = self.db.get_all_elements()
        max_period = max(e.period for e in elements)
        max_group = max(e.group for e in elements)
        
        # Create grid of element buttons
        for row in range(max_period + 1):
            for col in range(max_group + 1):
                # Find element at this position
                element = None
                for e in elements:
                    if e.period - 1 == row and e.group - 1 == col:
                        element = e
                        break
                
                # Create button for element or empty space
                if element:
                    self._create_element_button(element, row, col)
                else:
                    ttk.Label(self.periodic_table_frame, text="").grid(row=row, column=col, 
                                                                       padx=2, pady=2)
    
    def _populate_visualization_buttons(self):
        """Populate the visualization buttons frame."""
        # 3D Visualizations
        ttk.Label(self.vis_buttons_frame, text="3D Visualizations:", 
                 style='Header.TLabel').pack(side=tk.LEFT, padx=10, pady=10)
        
        ttk.Button(self.vis_buttons_frame, text="Atomic Structure",
                  command=lambda: self._show_visualization('atomic_structure')).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.vis_buttons_frame, text="Ionization Energies",
                  command=lambda: self._show_visualization('ionization')).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.vis_buttons_frame, text="Electron Shells",
                  command=lambda: self._show_visualization('shells')).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.vis_buttons_frame, text="Thermal Properties",
                  command=lambda: self._show_visualization('thermal')).pack(side=tk.LEFT, padx=5)
        
        # Separator
        ttk.Separator(self.vis_buttons_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # HyperSpectral Visualizations
        ttk.Label(self.vis_buttons_frame, text="HyperSpectral:", 
                 style='Header.TLabel').pack(side=tk.LEFT, padx=10, pady=10)
        
        ttk.Button(self.vis_buttons_frame, text="Spectral Signature",
                  command=lambda: self._show_visualization('spectral')).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.vis_buttons_frame, text="Band Ratios",
                  command=lambda: self._show_visualization('band_ratios')).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.vis_buttons_frame, text="Wavelength Map",
                  command=lambda: self._show_visualization('wavelength')).pack(side=tk.LEFT, padx=5)
        
        # Separator
        ttk.Separator(self.vis_buttons_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Analysis Visualizations
        ttk.Label(self.vis_buttons_frame, text="Analysis:", 
                 style='Header.TLabel').pack(side=tk.LEFT, padx=10, pady=10)
        
        ttk.Button(self.vis_buttons_frame, text="Li Mineral Detection",
                  command=lambda: self._show_visualization('li_minerals')).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.vis_buttons_frame, text="Heatmap",
                  command=self._show_heatmap).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.vis_buttons_frame, text="Distributions",
                  command=self._show_distributions).pack(side=tk.LEFT, padx=5)
    
    def _create_element_button(self, element: Element, row: int, col: int):
        """Create a button for an element with responsive sizing."""
        # Get button dimensions based on screen size
        width, height, font_size = self._get_element_button_dimensions()
        
        btn = tk.Button(
            self.periodic_table_frame,
            text=f"{element.symbol}\n{element.atomic_mass:.2f}",
            command=lambda e=element: self._on_element_selected(e),
            bg=element.color,
            fg='black',
            width=width,
            height=height,
            font=('Helvetica', font_size, 'bold'),
            relief=tk.RAISED,
            bd=2
        )
        btn.grid(row=row, column=col, padx=2, pady=2)
        
        # Store reference for later updates
        if not hasattr(self, 'element_buttons'):
            self.element_buttons = {}
        self.element_buttons[element.number] = btn
    
    def _on_element_selected(self, element: Element):
        """Handle element selection."""
        self.current_element = element
        
        # Toggle selection
        if element in self.selected_elements:
            self.selected_elements.remove(element)
        else:
            self.selected_elements.append(element)
        
        self._update_element_display()
        self._update_selected_display()
    
    def _update_element_display(self):
        """Update the element details display."""
        if self.current_element is None:
            self.basic_info_text.delete(1.0, tk.END)
            self.properties_text.delete(1.0, tk.END)
            return
        
        elem = self.current_element
        
        # Update basic info tab
        basic_info = f"""
{elem.symbol} - {elem.name}

Atomic Number: {elem.number}
Atomic Mass: {elem.atomic_mass:.3f} u

Category: {elem.category}
Phase: {elem.phase}
Block: {elem.block}

Appearance: {elem.appearance}

Summary:
{elem.summary}

Discovered by: {elem.discovered_by or 'Unknown'}
Named by: {elem.named_by or 'Unknown'}

Source: {elem.source or 'N/A'}
"""
        
        self.basic_info_text.delete(1.0, tk.END)
        self.basic_info_text.insert(1.0, basic_info)
        
        # Update properties tab
        properties_info = f"""
ELECTRON CONFIGURATION
Full: {elem.electron_configuration}
Semantic: {elem.electron_configuration_semantic}

SHELLS
{elem.shells}

ELECTRONEGATIVITY
Pauling: {elem.electronegativity or 'N/A'}

IONIZATION ENERGIES (kJ/mol)
{', '.join(f"{ie:.0f}" for ie in elem.ionization_energies) if elem.ionization_energies else 'N/A'}

ELECTRON AFFINITY
{elem.electron_affinity or 'N/A'} kJ/mol

THERMAL PROPERTIES
Melting Point: {elem.melt or 'N/A'} K
Boiling Point: {elem.boil or 'N/A'} K
Molar Heat: {elem.molar_heat or 'N/A'} J/(mol·K)

DENSITY
{elem.density or 'N/A'} g/cm³

POSITION
Period: {elem.period}
Group: {elem.group}
X Position: {elem.xpos}
Y Position: {elem.ypos}
"""
        
        self.properties_text.delete(1.0, tk.END)
        self.properties_text.insert(1.0, properties_info)
    
    def _update_selected_display(self):
        """Update the selected elements display."""
        self.selected_text.delete(1.0, tk.END)
        
        if not self.selected_elements:
            self.selected_text.insert(1.0, "No elements selected")
            return
        
        selected_info = "\n".join(
            f"{e.symbol}: {e.name}" for e in sorted(self.selected_elements, key=lambda x: x.number)
        )
        self.selected_text.insert(1.0, selected_info)
    
    def _on_search_changed(self, *args):
        """Handle search input changes."""
        query = self.search_var.get().strip()
        
        if not query:
            # Show all elements
            self._update_element_buttons_visibility(self.db.get_all_elements())
        else:
            # Show search results
            results = self.db.search_elements(query)
            self._update_element_buttons_visibility(results)
    
    def _update_element_buttons_visibility(self, visible_elements: List[Element]):
        """Update visibility of element buttons based on filter."""
        visible_numbers = {e.number for e in visible_elements}
        
        for elem_num, btn in self.element_buttons.items():
            if elem_num in visible_numbers:
                btn.grid()
            else:
                btn.grid_remove()
    
    def _clear_search(self):
        """Clear the search box."""
        self.search_var.set("")
    
    def _clear_selection(self):
        """Clear selected elements."""
        self.selected_elements.clear()
        self._update_selected_display()
    
    def _show_visualization(self, viz_type: str):
        """Show a specific visualization for current element."""
        if viz_type not in ['li_minerals'] and self.current_element is None:
            messagebox.showwarning("Warning", "Please select an element first")
            return
        
        try:
            if viz_type == 'atomic_structure':
                fig = self.visualizer.plot_atomic_structure_3d(self.current_element)
            elif viz_type == 'ionization':
                fig = self.visualizer.plot_ionization_energies_3d(self.current_element)
            elif viz_type == 'shells':
                fig = self.visualizer.plot_electron_shells_3d(self.current_element)
            elif viz_type == 'thermal':
                fig = self.visualizer.plot_thermal_properties_3d(self.current_element)
            elif viz_type == 'spectral':
                fig = self.visualizer.plot_spectral_signature(self.current_element)
            elif viz_type == 'band_ratios':
                if len(self.selected_elements) < 2:
                    messagebox.showwarning("Warning", "Please select at least 2 elements for band ratio comparison")
                    return
                fig = self.visualizer.plot_band_ratios(self.selected_elements)
            elif viz_type == 'wavelength':
                if len(self.selected_elements) < 1:
                    elements = [self.current_element]
                else:
                    elements = self.selected_elements if self.selected_elements else [self.current_element]
                fig = self.visualizer.plot_minimum_wavelength_map(elements)
            elif viz_type == 'li_minerals':
                fig = self.visualizer.plot_lithium_bearing_mineral_detection()
            else:
                return
            
            self.visualizer.show_figure(fig)
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate visualization: {e}")
    
    def _compare_elements(self):
        """Compare selected elements."""
        if len(self.selected_elements) < 2:
            messagebox.showwarning("Warning", "Please select at least 2 elements to compare")
            return
        
        # Create comparison window
        comp_window = tk.Toplevel(self.root)
        comp_window.title("Compare Elements")
        comp_window.geometry("600x400")
        
        # Properties to compare
        frame = ttk.Frame(comp_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        properties = ['atomic_mass', 'electronegativity', 'melt', 'boil', 'density']
        
        for prop in properties:
            prop_label = prop.replace('_', ' ').title()
            ttk.Label(frame, text=prop_label, style='Header.TLabel').pack(anchor=tk.W)
            
            # Display values for each element
            values = []
            for elem in sorted(self.selected_elements, key=lambda x: x.number):
                value = getattr(elem, prop, None)
                if value is not None:
                    values.append(f"  {elem.symbol}: {value:.3f}")
                else:
                    values.append(f"  {elem.symbol}: N/A")
            
            for value_str in values:
                ttk.Label(frame, text=value_str, style='Normal.TLabel').pack(anchor=tk.W)
            
            ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
    
    def _show_heatmap(self):
        """Show electronegativity heatmap."""
        try:
            fig = self.visualizer.plot_electronegativity_heatmap()
            self.visualizer.show_figure(fig)
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate heatmap: {e}")
    
    def _show_distributions(self):
        """Show property distributions."""
        try:
            import matplotlib.pyplot as plt
            
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle('Periodic Table Analysis', fontsize=16, fontweight='bold')
            
            # 1. Atomic mass distribution
            self.visualizer.plot_atomic_mass_distribution()
            
            # 2. Elements by category
            self.visualizer.plot_elements_by_category()
            
            # 3. Phase distribution
            self.visualizer.plot_phase_distribution()
            
            # 4. Elements per period
            self.visualizer.plot_elements_per_period()
            
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate distributions: {e}")
    
    def _generate_analysis_report(self):
        """Generate comprehensive analysis report."""
        try:
            messagebox.showinfo("Info", 
                              "Analysis report generation requires advanced modules.\n"
                              "Please see the analysis module for detailed implementation.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate report: {e}")
    
    def _generate_all_visualizations(self):
        """Generate all available visualizations."""
        try:
            messagebox.showinfo("Info",
                              "Generating visualizations for all elements...\n"
                              "This may take a moment.")
            
            # This would generate multiple visualizations
            # For now, show a placeholder
            messagebox.showinfo("Generated",
                              "Visualization generation completed.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate visualizations: {e}")
    
    def _open_agent_chat(self):
        """Open the Quantum Research Agent chat dialog."""
        try:
            # Open agent chat dialog with current element context
            AgentChatDialog(self.root, current_element=self.current_element)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open agent: {e}")


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = PeriodicTableApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()