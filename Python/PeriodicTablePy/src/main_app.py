"""
Main Application GUI
Desktop application for interactive periodic table with quantum research integration.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import Optional, Dict, Any
import logging

from src.element import Element
from src.element_database import ElementDatabase
from src.element_visual import ElementVisual, ElementDetailView
from src.research_agent import (
    ResearchAgentManager, ResearchTaskType, QuantumProcessor
)
from src.model_generator import (
    MolecularModel, OrbitalVisualizer, OrbitalType, Vector3D, MolecularGeometry
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PeriodicTableApp(tk.Tk):
    """Main application window."""
    
    def __init__(self):
        """Initialize the application."""
        super().__init__()
        
        self.title("Interactive Periodic Table with Quantum Research Agent")
        self.geometry("1600x1000")
        self.minsize(1400, 900)
        
        # Initialize data
        self.element_db = ElementDatabase()
        self.quantum_processor = QuantumProcessor()
        self.research_agent = ResearchAgentManager(self.quantum_processor)
        
        self.selected_element: Optional[Element] = None
        self.active_tasks: Dict[str, str] = {}  # task_id -> element_symbol
        
        self._setup_style()
        self._create_menu_bar()
        self._create_main_layout()
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _setup_style(self):
        """Setup application styling."""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', font=("Arial", 16, "bold"))
        style.configure('Subtitle.TLabel', font=("Arial", 12, "bold"))
        style.configure('Status.TLabel', font=("Arial", 9))
    
    def _create_menu_bar(self):
        """Create application menu bar."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self._on_closing)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Reset View", command=self._reset_view)
        view_menu.add_separator()
        view_menu.add_command(label="Show All Elements", command=self._show_all_elements)
        
        # Research menu
        research_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Research", menu=research_menu)
        research_menu.add_command(label="Analyze Orbital", command=self._analyze_orbital)
        research_menu.add_command(label="Molecular Simulation", command=self._run_molecular_sim)
        research_menu.add_separator()
        research_menu.add_command(label="Task Status", command=self._show_task_status)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _create_main_layout(self):
        """Create main application layout."""
        # Main container with paned window
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left sidebar
        self.left_frame = ttk.Frame(paned)
        paned.add(self.left_frame, weight=2)
        self._create_left_sidebar()
        
        # Center: periodic table view
        self.center_frame = ttk.Frame(paned)
        paned.add(self.center_frame, weight=3)
        self._create_periodic_table()
        
        # Right sidebar: details and controls
        self.right_frame = ttk.Frame(paned)
        paned.add(self.right_frame, weight=2)
        self._create_right_sidebar()
    
    def _create_left_sidebar(self):
        """Create left sidebar with search and filters."""
        # Title
        title = ttk.Label(self.left_frame, text="Search & Filter", style='Title.TLabel')
        title.pack(padx=5, pady=10)
        
        # Search frame
        search_frame = ttk.LabelFrame(self.left_frame, text="Search Elements", padding=5)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Name/Symbol:").pack()
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(fill=tk.X)
        
        # Category filter
        filter_frame = ttk.LabelFrame(self.left_frame, text="Filter by Category", padding=5)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.category_var = tk.StringVar(value="All")
        categories = ["All"] + self.element_db.get_categories()
        
        for category in categories:
            ttk.Radiobutton(
                filter_frame, text=category, value=category,
                variable=self.category_var,
                command=self._on_category_change
            ).pack(anchor=tk.W)
        
        # Selected element info
        self.info_frame = ttk.LabelFrame(self.left_frame, text="Selected Element", padding=5)
        self.info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.info_text = tk.Text(self.info_frame, height=15, width=30, font=("Courier", 9))
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Control buttons
        button_frame = ttk.Frame(self.left_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Analyze", command=self._analyze_orbital).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="3D Model", command=self._show_3d_model).pack(fill=tk.X, pady=2)
    
    def _create_periodic_table(self):
        """Create interactive periodic table."""
        title = ttk.Label(self.center_frame, text="Periodic Table of Elements", style='Title.TLabel')
        title.pack(padx=5, pady=10)
        
        # Create canvas with scrollbar
        canvas_frame = ttk.Frame(self.center_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.table_canvas = tk.Canvas(canvas_frame, yscrollcommand=scrollbar.set, bg="white")
        self.table_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.table_canvas.yview)
        
        # Create scrollable frame
        self.table_frame = ttk.Frame(self.table_canvas)
        self.canvas_window = self.table_canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        
        self.table_frame.bind("<Configure>", lambda e: self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all")))
        
        # Populate with elements
        self._populate_periodic_table()
    
    def _populate_periodic_table(self):
        """Populate periodic table with elements."""
        # Clear existing
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        # Create grid layout
        elements = self.element_db.get_all_elements()
        
        if self.category_var.get() != "All":
            elements = [e for e in elements if e.category == self.category_var.get()]
        
        search_query = self.search_var.get()
        if search_query:
            elements = self.element_db.search_elements(search_query)
        
        # Create element tiles
        for i, element in enumerate(elements):
            row = i // 8
            col = i % 8
            
            visual = ElementVisual(
                self.table_frame,
                element,
                on_select=self._on_element_selected,
                width=100,
                height=140,
                bg="white"
            )
            visual.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        
        self.table_frame.update_idletasks()
    
    def _create_right_sidebar(self):
        """Create right sidebar with details and visualization."""
        title = ttk.Label(self.right_frame, text="Details & Analysis", style='Title.TLabel')
        title.pack(padx=5, pady=10)
        
        # Notebook for tabs
        self.details_notebook = ttk.Notebook(self.right_frame)
        self.details_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Element details tab
        details_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(details_frame, text="Properties")
        self.element_details = ElementDetailView(details_frame)
        self.element_details.pack(fill=tk.BOTH, expand=True)
        
        # Quantum data tab
        quantum_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(quantum_frame, text="Quantum Data")
        self._create_quantum_tab(quantum_frame)
        
        # Task status tab
        task_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(task_frame, text="Tasks")
        self._create_task_tab(task_frame)
    
    def _create_quantum_tab(self, parent):
        """Create quantum data tab."""
        # Status
        self.quantum_status_var = tk.StringVar(value="No active simulation")
        status_label = ttk.Label(parent, textvariable=self.quantum_status_var, style='Status.TLabel')
        status_label.pack(padx=5, pady=5)
        
        # Control frame
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Run Simulation", command=self._run_quantum_sim).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Clear Results", command=self._clear_quantum_results).pack(side=tk.LEFT, padx=2)
        
        # Results display
        self.quantum_text = tk.Text(parent, height=15, width=40, font=("Courier", 8))
        self.quantum_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(parent, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=5, pady=5)
    
    def _create_task_tab(self, parent):
        """Create task status tab."""
        # Task list
        list_frame = ttk.LabelFrame(parent, text="Active Tasks", padding=5)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create listbox
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.task_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Courier", 9))
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Refresh button
        ttk.Button(parent, text="Refresh Tasks", command=self._refresh_task_list).pack(fill=tk.X, padx=5, pady=5)
    
    def _on_element_selected(self, element: Element):
        """Handle element selection."""
        self.selected_element = element
        
        # Update left sidebar info
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        
        info = (
            f"Name: {element.name}\n"
            f"Symbol: {element.symbol}\n"
            f"Atomic #: {element.atomic_number}\n"
            f"Atomic Mass: {element.atomic_mass:.3f} u\n"
            f"Category: {element.category}\n"
            f"Period: {element.period}\n"
            f"Group: {element.group}\n"
            f"State: {element.state.value}\n"
            f"\nElectron Config:\n{element.electron_configuration}\n"
            f"\nElectronegativity: {element.electronegativity:.2f}\n"
            f"IE: {element.ionization_energy:.2f} eV\n"
            f"Density: {element.density:.3f} g/cm³\n"
            f"\nValence e⁻: {element.get_valence_electrons()}\n"
            f"Bohr Radius: {element.get_bohr_radius_estimation():.3f} Å\n"
        )
        
        self.info_text.insert(1.0, info)
        self.info_text.config(state=tk.DISABLED)
        
        # Update right sidebar
        self.element_details.set_element(element)
    
    def _on_search(self, *args):
        """Handle search input."""
        self._populate_periodic_table()
    
    def _on_category_change(self):
        """Handle category filter change."""
        self._populate_periodic_table()
    
    def _analyze_orbital(self):
        """Analyze electron orbital of selected element."""
        if not self.selected_element:
            messagebox.showwarning("Warning", "Please select an element first")
            return
        
        element = self.selected_element
        
        # Create research task
        task_id = self.research_agent.create_research_task(
            ResearchTaskType.ELECTRON_ORBITAL,
            element,
            {
                'n': element.period,
                'l': 0,
                'ml': 0,
                'ms': 0.5
            }
        )
        
        self.active_tasks[task_id] = element.symbol
        self.quantum_status_var.set(f"Analyzing {element.symbol}...")
        self.progress.start()
        
        # Execute asynchronously
        self.research_agent.execute_task_async(task_id, self._on_orbital_analysis_complete)
    
    def _on_orbital_analysis_complete(self, task):
        """Handle orbital analysis completion."""
        self.progress.stop()
        
        if task.status == "completed":
            result = task.result
            self.quantum_status_var.set(f"Analysis complete: {task.element.symbol}")
            
            # Display results
            self.quantum_text.config(state=tk.NORMAL)
            self.quantum_text.delete(1.0, tk.END)
            
            result_text = (
                f"Element: {result['element']}\n"
                f"Task ID: {result['task_id']}\n"
                f"Orbital Type: {result['orbital_data']['type']}\n"
                f"Quantum Numbers:\n"
                f"  n = {result['orbital_data']['n']}\n"
                f"  l = {result['orbital_data']['l']}\n"
                f"  ml = {result['orbital_data']['ml']}\n"
                f"  ms = {result['orbital_data']['ms']}\n"
                f"Energy Level: {result['energy_level']:.3f} eV\n"
                f"\nProbability Distribution:\n"
            )
            
            for i, prob in enumerate(result['probabilities']):
                result_text += f"  R[{i}]: {prob:.4f}\n"
            
            self.quantum_text.insert(1.0, result_text)
            self.quantum_text.config(state=tk.DISABLED)
        
        else:
            self.quantum_status_var.set(f"Analysis failed: {task.error}")
            messagebox.showerror("Error", f"Analysis failed: {task.error}")
        
        self._refresh_task_list()
    
    def _run_quantum_sim(self):
        """Run quantum simulation."""
        if not self.selected_element:
            messagebox.showwarning("Warning", "Please select an element first")
            return
        
        self._analyze_orbital()
    
    def _run_molecular_sim(self):
        """Run molecular simulation."""
        if not self.selected_element:
            messagebox.showwarning("Warning", "Please select an element first")
            return
        
        element = self.selected_element
        task_id = self.research_agent.create_research_task(
            ResearchTaskType.MOLECULAR_SIMULATION,
            element,
            {'molecule': f"{element.symbol}2"}
        )
        
        self.active_tasks[task_id] = element.symbol
        self.progress.start()
        self.research_agent.execute_task_async(task_id, self._on_simulation_complete)
    
    def _on_simulation_complete(self, task):
        """Handle simulation completion."""
        self.progress.stop()
        if task.status == "completed":
            messagebox.showinfo("Success", f"Simulation completed for {task.element.symbol}")
        else:
            messagebox.showerror("Error", f"Simulation failed: {task.error}")
        self._refresh_task_list()
    
    def _show_3d_model(self):
        """Show 3D model of element."""
        if not self.selected_element:
            messagebox.showwarning("Warning", "Please select an element first")
            return
        
        element = self.selected_element
        
        # Create molecular model
        model = MolecularModel(f"{element.symbol}2")
        
        # Add atoms
        geometry = "linear" if element.symbol in ['H', 'N', 'O'] else "tetrahedral"
        positions = MolecularGeometry.generate_positions(geometry, 2)
        
        for i, pos in enumerate(positions):
            model.add_atom(element.symbol, pos, element.atomic_number)
        
        model.add_bond(0, 1, 1.0)
        
        # Get mesh data
        mesh_data = model.get_mesh_data()
        props = model.calculate_properties()
        
        # Show in message
        info = (
            f"Molecule: {element.symbol}₂\n"
            f"Geometry: {geometry}\n"
            f"Molecular Mass: {props['molecular_mass']:.2f} u\n"
            f"Molecular Size: {props['molecular_size']:.2f} Å\n"
            f"Number of Atoms: {props['num_atoms']}\n"
            f"Number of Bonds: {props['num_bonds']}\n"
        )
        
        messagebox.showinfo("3D Model Info", info)
    
    def _clear_quantum_results(self):
        """Clear quantum results display."""
        self.quantum_text.config(state=tk.NORMAL)
        self.quantum_text.delete(1.0, tk.END)
        self.quantum_text.config(state=tk.DISABLED)
        self.quantum_status_var.set("No active simulation")
    
    def _refresh_task_list(self):
        """Refresh task list display."""
        self.task_listbox.delete(0, tk.END)
        
        for task in self.research_agent.get_all_tasks():
            status_icon = {
                'pending': '○',
                'running': '◐',
                'completed': '●',
                'failed': '✗'
            }.get(task.status, '?')
            
            item = f"{status_icon} {task.task_id}: {task.status}"
            self.task_listbox.insert(tk.END, item)
    
    def _show_task_status(self):
        """Show task status dialog."""
        self._refresh_task_list()
    
    def _reset_view(self):
        """Reset view to show all elements."""
        self.search_var.set("")
        self.category_var.set("All")
        self._populate_periodic_table()
    
    def _show_all_elements(self):
        """Show all elements."""
        self._reset_view()
    
    def _show_about(self):
        """Show about dialog."""
        about_text = (
            "Interactive Periodic Table with Quantum Research Agent\n\n"
            "Version 1.0\n\n"
            "An advanced desktop application featuring:\n"
            "• Interactive periodic table of elements\n"
            "• Real-time element information\n"
            "• Quantum orbital simulation\n"
            "• Molecular structure modeling\n"
            "• 3D visualization of atomic structures\n"
            "• Integration with Azure Quantum\n\n"
            "© 2025 Quantum Research Lab"
        )
        messagebox.showinfo("About", about_text)
    
    def _on_closing(self):
        """Handle application closing."""
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.destroy()


def main():
    """Main entry point."""
    app = PeriodicTableApp()
    app.mainloop()


if __name__ == "__main__":
    main()
