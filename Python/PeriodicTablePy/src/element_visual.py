"""
Element Visual Module
Handles visual representation and interaction of individual elements.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Dict, Any
from src.element import Element, ElementState
import math


class ElementVisual(tk.Frame):
    """
    Widget for displaying and interacting with individual elements.
    Shows element information, properties, and quantum data visualizations.
    """
    
    def __init__(self, parent: tk.Widget, element: Element, 
                 on_select: Optional[Callable] = None, **kwargs):
        """
        Initialize element visual.
        
        Args:
            parent: Parent widget
            element: Element object to display
            on_select: Callback function when element is selected
            **kwargs: Additional frame arguments
        """
        super().__init__(parent, **kwargs)
        self.element = element
        self.on_select = on_select
        self.is_selected = False
        self.quantum_data: Optional[Dict[str, Any]] = None
        
        self._create_widgets()
        self._setup_bindings()
        self._apply_styling()
    
    def _create_widgets(self):
        """Create all visual widgets."""
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Element symbol (large, prominent)
        symbol_frame = ttk.Frame(main_frame)
        symbol_frame.pack(fill=tk.BOTH, expand=True)
        
        self.symbol_label = tk.Label(
            symbol_frame,
            text=self.element.symbol,
            font=("Arial", 28, "bold"),
            fg=self.element.color,
            bg="white",
            height=2
        )
        self.symbol_label.pack(fill=tk.BOTH, expand=True)
        
        # Element info section
        info_frame = ttk.LabelFrame(main_frame, text="Element Info", padding=5)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        info_text = (
            f"Name: {self.element.name}\n"
            f"Atomic #: {self.element.atomic_number}\n"
            f"Mass: {self.element.atomic_mass:.3f} u\n"
            f"Category: {self.element.category}"
        )
        
        self.info_label = tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 9),
            justify=tk.LEFT
        )
        self.info_label.pack(fill=tk.BOTH, expand=True)
        
        # Properties section
        prop_frame = ttk.LabelFrame(main_frame, text="Properties", padding=5)
        prop_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        prop_text = (
            f"EN: {self.element.electronegativity:.2f}\n"
            f"IE: {self.element.ionization_energy:.2f} eV\n"
            f"State: {self.element.state.value}"
        )
        
        self.prop_label = tk.Label(
            prop_frame,
            text=prop_text,
            font=("Arial", 8),
            justify=tk.LEFT
        )
        self.prop_label.pack(fill=tk.BOTH, expand=True)
        
        # Quantum visualization area
        self.quantum_frame = ttk.LabelFrame(main_frame, text="Quantum Data", padding=5)
        self.quantum_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.quantum_canvas = tk.Canvas(
            self.quantum_frame,
            width=150,
            height=100,
            bg="white",
            highlightthickness=1
        )
        self.quantum_canvas.pack(fill=tk.BOTH, expand=True)
        self._draw_bohr_model()
    
    def _setup_bindings(self):
        """Setup event bindings."""
        self.symbol_label.bind("<Button-1>", self._on_click)
        self.bind("<Button-1>", self._on_click)
    
    def _apply_styling(self):
        """Apply visual styling."""
        if self.is_selected:
            self.config(bg="#E0E0E0", relief=tk.SUNKEN, bd=2)
        else:
            self.config(bg="white", relief=tk.RAISED, bd=1)
    
    def _on_click(self, event=None):
        """Handle click event."""
        self.select()
        if self.on_select:
            self.on_select(self.element)
    
    def select(self):
        """Select this element."""
        self.is_selected = True
        self._apply_styling()
    
    def deselect(self):
        """Deselect this element."""
        self.is_selected = False
        self._apply_styling()
    
    def _draw_bohr_model(self):
        """Draw simplified Bohr model for element."""
        canvas = self.quantum_canvas
        canvas.delete("all")
        
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w <= 1 or h <= 1:
            w, h = 150, 100
        
        cx, cy = w / 2, h / 2
        nucleus_radius = 4
        
        # Draw nucleus
        canvas.create_oval(
            cx - nucleus_radius, cy - nucleus_radius,
            cx + nucleus_radius, cy + nucleus_radius,
            fill="red", outline="darkred", width=2
        )
        
        # Draw electron shells
        shells = min(3, self.element.period)  # Show up to 3 shells
        colors = ["blue", "green", "purple"]
        
        for shell in range(1, shells + 1):
            radius = 15 + shell * 15
            canvas.create_oval(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                outline=colors[shell - 1], width=1, dash=(2, 2)
            )
            
            # Draw electrons as dots
            electron_count = min(8, self.element.get_electron_count())
            angle_step = 360 / electron_count
            
            for i in range(electron_count):
                angle = math.radians(i * angle_step)
                ex = cx + radius * math.cos(angle)
                ey = cy + radius * math.sin(angle)
                canvas.create_oval(
                    ex - 2, ey - 2,
                    ex + 2, ey + 2,
                    fill=colors[shell - 1], outline=colors[shell - 1]
                )
    
    def update_quantum_data(self, data: Dict[str, Any]):
        """
        Update with quantum simulation results.
        
        Args:
            data: Dictionary containing quantum simulation results
        """
        self.quantum_data = data
        self._update_visualization()
    
    def _update_visualization(self):
        """Update visualization with quantum data."""
        if not self.quantum_data:
            return
        
        canvas = self.quantum_canvas
        canvas.delete("orbital")
        
        # Visualize probability distributions or electron density
        if 'probabilities' in self.quantum_data:
            probs = self.quantum_data['probabilities']
            self._draw_probability_distribution(probs)
        
        if 'orbital_data' in self.quantum_data:
            orbital = self.quantum_data['orbital_data']
            self._draw_orbital(orbital)
    
    def _draw_probability_distribution(self, probabilities: list):
        """Draw probability distribution visualization."""
        canvas = self.quantum_canvas
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w <= 1:
            w = 150
        
        # Simple bar chart
        bar_width = max(1, w // len(probabilities))
        max_prob = max(probabilities) if probabilities else 1
        
        for i, prob in enumerate(probabilities):
            x1 = i * bar_width
            x2 = x1 + bar_width
            bar_height = (prob / max_prob) * h * 0.8
            y1 = h - bar_height
            y2 = h
            
            canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="cyan", outline="blue", tags="orbital"
            )
    
    def _draw_orbital(self, orbital_data: Dict):
        """Draw orbital visualization."""
        canvas = self.quantum_canvas
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w <= 1 or h <= 1:
            w, h = 150, 100
        
        # Draw orbital shape (simplified)
        if 'type' in orbital_data:
            orbital_type = orbital_data['type']
            cx, cy = w / 2, h / 2
            
            if orbital_type == 's':
                # s-orbital: sphere
                radius = min(w, h) * 0.3
                canvas.create_oval(
                    cx - radius, cy - radius,
                    cx + radius, cy + radius,
                    outline="purple", width=2, tags="orbital"
                )
            elif orbital_type == 'p':
                # p-orbital: dumbbell
                radius = min(w, h) * 0.2
                canvas.create_oval(
                    cx - radius, cy - radius * 2,
                    cx + radius, cy - radius,
                    outline="blue", width=2, tags="orbital"
                )
                canvas.create_oval(
                    cx - radius, cy + radius,
                    cx + radius, cy + radius * 2,
                    outline="blue", width=2, tags="orbital"
                )
            elif orbital_type == 'd':
                # d-orbital: cloverleaf pattern
                radius = min(w, h) * 0.15
                for angle in [0, 90, 180, 270]:
                    rad = math.radians(angle)
                    ox = cx + math.cos(rad) * min(w, h) * 0.25
                    oy = cy + math.sin(rad) * min(w, h) * 0.25
                    canvas.create_oval(
                        ox - radius, oy - radius,
                        ox + radius, oy + radius,
                        outline="green", width=2, tags="orbital"
                    )
    
    def get_element(self) -> Element:
        """Return the element object."""
        return self.element
    
    def refresh(self):
        """Refresh the visual representation."""
        self._draw_bohr_model()
        if self.quantum_data:
            self._update_visualization()


class ElementDetailView(ttk.Frame):
    """Detailed view of element properties with extensive information."""
    
    def __init__(self, parent: tk.Widget, element: Optional[Element] = None, **kwargs):
        """
        Initialize detail view.
        
        Args:
            parent: Parent widget
            element: Element to display details for
            **kwargs: Additional frame arguments
        """
        super().__init__(parent, **kwargs)
        self.element = element
        self._create_widgets()
    
    def _create_widgets(self):
        """Create detail view widgets."""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Basic info tab
        basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(basic_frame, text="Basic Info")
        self._create_basic_tab(basic_frame)
        
        # Properties tab
        prop_frame = ttk.Frame(self.notebook)
        self.notebook.add(prop_frame, text="Properties")
        self._create_properties_tab(prop_frame)
        
        # Configuration tab
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="Configuration")
        self._create_configuration_tab(config_frame)
    
    def _create_basic_tab(self, parent):
        """Create basic information tab."""
        if not self.element:
            return
        
        text = tk.Text(parent, height=15, width=50, font=("Courier", 9))
        text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        info = (
            f"Element: {self.element.name}\n"
            f"Symbol: {self.element.symbol}\n"
            f"Atomic Number: {self.element.atomic_number}\n"
            f"Atomic Mass: {self.element.atomic_mass:.4f} u\n"
            f"Category: {self.element.category}\n"
            f"Period: {self.element.period}\n"
            f"Group: {self.element.group}\n"
            f"State: {self.element.state.value}\n"
            f"\nDiscovered: {self.element.discovered_year}\n"
            f"Discoverer: {self.element.discoverer}\n"
            f"\nCommon Uses:\n"
        )
        
        for use in self.element.uses:
            info += f"  • {use}\n"
        
        text.insert(1.0, info)
        text.config(state=tk.DISABLED)
    
    def _create_properties_tab(self, parent):
        """Create properties tab."""
        if not self.element:
            return
        
        text = tk.Text(parent, height=15, width=50, font=("Courier", 9))
        text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        props = (
            f"Electronegativity: {self.element.electronegativity:.2f}\n"
            f"Ionization Energy: {self.element.ionization_energy:.2f} eV\n"
            f"Electron Affinity: {self.element.electron_affinity:.2f} eV\n"
            f"Density: {self.element.density:.2f} g/cm³\n"
            f"Melting Point: {self.element.melting_point:.1f} K\n"
            f"Boiling Point: {self.element.boiling_point:.1f} K\n"
            f"\nValence Electrons: {self.element.get_valence_electrons()}\n"
            f"Total Electrons: {self.element.get_electron_count()}\n"
            f"Estimated Bohr Radius: {self.element.get_bohr_radius_estimation():.2f} Å\n"
            f"\nIs Metal: {self.element.is_metal()}\n"
            f"Is Nonmetal: {self.element.is_nonmetal()}\n"
        )
        
        text.insert(1.0, props)
        text.config(state=tk.DISABLED)
    
    def _create_configuration_tab(self, parent):
        """Create electron configuration tab."""
        if not self.element:
            return
        
        text = tk.Text(parent, height=15, width=50, font=("Courier", 9))
        text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        config = f"Electron Configuration:\n{self.element.electron_configuration}\n"
        text.insert(1.0, config)
        text.config(state=tk.DISABLED)
    
    def set_element(self, element: Element):
        """Set element to display."""
        self.element = element
        # Rebuild tabs
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)
        self._create_widgets()
