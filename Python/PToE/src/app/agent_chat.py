"""
Quantum Research Agent Chat Interface
Provides interactive chat dialog for element analysis and quantum research recommendations.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Optional, List, Callable
from datetime import datetime
from dataclasses import dataclass
import threading


@dataclass
class ChatMessage:
    """Represents a chat message."""
    timestamp: datetime
    sender: str  # 'user' or 'agent'
    message: str
    element_symbol: Optional[str] = None
    analysis_type: Optional[str] = None


class AgentChatDialog(tk.Toplevel):
    """
    Popup dialog for Quantum Research Agent interaction.
    Provides chat-based interface for element analysis and recommendations.
    """
    
    def __init__(self, parent: tk.Tk, current_element=None, on_analysis_requested: Optional[Callable] = None):
        """
        Initialize agent chat dialog.
        
        Args:
            parent: Parent tkinter window
            current_element: Currently selected element (optional)
            on_analysis_requested: Callback when user requests analysis
        """
        super().__init__(parent)
        self.parent = parent
        self.current_element = current_element
        self.on_analysis_requested = on_analysis_requested
        
        self.title("Quantum Research Agent")
        self.geometry("600x700")
        self.minsize(400, 500)
        
        # Chat history
        self.messages: List[ChatMessage] = []
        
        # Setup UI
        self._create_widgets()
        self._initialize_agent()
        self.focus()
    
    def _create_widgets(self):
        """Create chat interface widgets."""
        # Top bar with element info
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(top_frame, text="Agent Capabilities:", style='Header.TLabel').pack(side=tk.LEFT)
        
        if self.current_element:
            element_label = ttk.Label(top_frame, 
                text=f"Working with: {self.current_element.symbol} ({self.current_element.name})",
                style='Normal.TLabel')
            element_label.pack(side=tk.RIGHT)
        
        # Chat display area
        chat_frame = ttk.LabelFrame(self, text="Conversation", padding=10)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrolled text for chat history
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=('Courier', 9),
            height=20,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for styling messages
        self.chat_display.tag_config('user_msg', foreground='#0066cc', font=('Courier', 9, 'bold'))
        self.chat_display.tag_config('agent_msg', foreground='#006600', font=('Courier', 9))
        self.chat_display.tag_config('timestamp', foreground='#666666', font=('Courier', 8, 'italic'))
        self.chat_display.tag_config('element', background='#ffffcc', foreground='#000000')
        
        # Input area
        input_frame = ttk.LabelFrame(self, text="Ask the Agent", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Text input for user messages
        self.input_text = tk.Text(input_frame, height=3, wrap=tk.WORD, font=('Helvetica', 9))
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        self.input_text.bind('<Control-Return>', self._on_send_message)
        
        # Send button
        send_btn = ttk.Button(input_frame, text="Send (Ctrl+Enter)", command=self._on_send_message)
        send_btn.pack(fill=tk.X)
        
        # Quick action buttons
        buttons_frame = ttk.LabelFrame(self, text="Quick Actions", padding=10)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        if self.current_element:
            ttk.Button(buttons_frame, text="Analyze Properties",
                      command=self._analyze_properties).pack(side=tk.LEFT, padx=5)
            ttk.Button(buttons_frame, text="Suggest Visualizations",
                      command=self._suggest_visualizations).pack(side=tk.LEFT, padx=5)
            ttk.Button(buttons_frame, text="Quantum Insights",
                      command=self._quantum_insights).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buttons_frame, text="Clear History",
                  command=self._clear_history).pack(side=tk.RIGHT, padx=5)
    
    def _initialize_agent(self):
        """Initialize agent with welcome message."""
        element_info = ""
        if self.current_element:
            element_info = f" working with {self.current_element.symbol} ({self.current_element.name})"
        
        welcome_msg = f"""Welcome to the Quantum Research Agent!

I'm here to help you analyze elements, understand their properties, and recommend quantum research approaches{element_info}.

You can:
• Ask questions about element properties
• Request property analysis and comparisons
• Get visualization recommendations
• Explore quantum computation concepts
• Analyze spectral data

Use the Quick Actions buttons or type your questions below.
Type Ctrl+Enter to send your message."""
        
        self._add_agent_message(welcome_msg)
    
    def _on_send_message(self, event=None):
        """Handle user message submission."""
        user_input = self.input_text.get("1.0", tk.END).strip()
        
        if not user_input:
            return
        
        # Add user message to chat
        self._add_user_message(user_input)
        self.input_text.delete("1.0", tk.END)
        
        # Process message and generate response (threaded to prevent UI freeze)
        threading.Thread(target=self._process_user_message, args=(user_input,), daemon=True).start()
    
    def _process_user_message(self, message: str):
        """Process user message and generate agent response."""
        # Simulate processing
        response = self._generate_agent_response(message)
        self._add_agent_message(response)
    
    def _generate_agent_response(self, user_input: str) -> str:
        """
        Generate agent response based on user input.
        
        Args:
            user_input: User's message
            
        Returns:
            Agent's response
        """
        # Simple response logic - can be enhanced with NLP/ML
        user_input_lower = user_input.lower()
        
        if not self.current_element:
            return "Please select an element first to get specific analysis and recommendations."
        
        # Check for specific keywords and generate contextual responses
        if any(word in user_input_lower for word in ['property', 'properties', 'characteristics']):
            return self._analyze_properties_response()
        elif any(word in user_input_lower for word in ['visualize', 'visualization', 'plot', 'show']):
            return self._visualization_response()
        elif any(word in user_input_lower for word in ['quantum', 'compute', 'calculation']):
            return self._quantum_response()
        elif any(word in user_input_lower for word in ['compare', 'similar', 'like']):
            return self._comparison_response()
        elif any(word in user_input_lower for word in ['spectrum', 'spectral', 'wavelength']):
            return self._spectral_response()
        else:
            return self._general_response(user_input)
    
    def _analyze_properties_response(self) -> str:
        """Generate analysis of current element's properties."""
        elem = self.current_element
        return f"""Analysis of {elem.symbol} ({elem.name}):

Key Properties:
• Atomic Number: {elem.number}
• Atomic Mass: {elem.atomic_mass:.3f} u
• Electron Configuration: {elem.electron_configuration_semantic}
• Category: {elem.category}
• Block: {elem.block}
• Phase: {elem.phase}

Physical Properties:
• Electronegativity: {elem.electronegativity or 'N/A'}
• Density: {elem.density or 'N/A'} g/cm³
• Melting Point: {elem.melt or 'N/A'} K
• Boiling Point: {elem.boil or 'N/A'} K

Ionization Energy (first 3):
{self._format_ionization_energies(elem)}

Would you like me to suggest specific visualizations or quantum analyses?"""
    
    def _visualization_response(self) -> str:
        """Suggest visualizations for current element."""
        elem = self.current_element
        return f"""Recommended Visualizations for {elem.symbol}:

3D Visualizations:
• Atomic Structure - View electron distribution in 3D
• Ionization Energies - Compare energy levels
• Electron Shells - Understand shell configuration
• Thermal Properties - Analyze thermal characteristics

Spectroscopic Analysis:
• Spectral Signature - Element's characteristic spectrum (200-2500nm)
• Band Ratios - IR and visible wavelength comparison
• Wavelength Map - Identify element by wavelength

Analysis Tools:
• Property Heatmap - Compare across periodic table
• Property Distribution - Statistical visualization
• Mineral Detection - Identify minerals containing this element

Click any visualization button in the panel below to explore!"""
    
    def _quantum_response(self) -> str:
        """Provide quantum computation insights."""
        elem = self.current_element
        return f"""Quantum Insights for {elem.symbol}:

Electron Configuration Quantum Numbers:
• Valence Electrons: {sum(elem.shells[-1:]) if elem.shells else 'N/A'}
• Total Electrons: {elem.number}
• Orbital Structure: {elem.electron_configuration_semantic}

Quantum Properties:
• This element has potential for quantum state analysis
• Ionization energy indicates orbital stability
• Electronic structure enables quantum modeling

Potential Quantum Research:
• Electron orbital simulations
• Quantum state transitions
• Binding energy calculations
• Molecular interaction analysis

Would you like to submit a quantum computation job to Azure Quantum?"""
    
    def _comparison_response(self) -> str:
        """Suggest element comparisons."""
        elem = self.current_element
        return f"""Comparison Analysis for {elem.symbol}:

Similar Elements (same category):
{elem.category} elements share similar chemical properties.

You can compare {elem.symbol} with other elements by:
1. Selecting another element from the periodic table
2. Using the Quick Actions buttons
3. Requesting specific property comparisons

Would you like me to suggest elements with similar properties?"""
    
    def _spectral_response(self) -> str:
        """Provide spectral analysis information."""
        elem = self.current_element
        return f"""Spectroscopic Analysis for {elem.symbol}:

Available Spectral Visualizations:
• Spectral Signature (200-2500 nm range)
  - Shows characteristic absorption/emission lines
  - Useful for remote sensing and mineral identification
  
• Band Ratio Analysis
  - Visible and IR wavelength comparison
  - Essential for multispectral imaging
  
• Wavelength Map
  - Characteristic wavelengths for identification
  - Applications in mineralogy and astronomy

HyperSpectral Applications:
• Remote sensing analysis
• Mineral composition detection
• Atmospheric analysis
• Material characterization

Click "Spectral Signature" in the Visualizations panel to see {elem.symbol}'s spectrum!"""
    
    def _general_response(self, user_input: str) -> str:
        """Generate general response."""
        return f"""I understand you're asking about: "{user_input}"

For {self.current_element.symbol}, I can help you with:
• Detailed property analysis
• Visualization recommendations
• Quantum computation insights
• Element comparisons
• Spectroscopic information

Please try:
- "Tell me about the properties of this element"
- "What visualizations would help me understand this element?"
- "Give me quantum insights"
- "Show me similar elements"
- "Explain the spectral data"

Or use the Quick Action buttons for immediate analysis!"""
    
    def _format_ionization_energies(self, element) -> str:
        """Format ionization energies for display."""
        if not element.ionization_energies:
            return "Not available"
        
        energies = element.ionization_energies[:3]
        lines = []
        for i, energy in enumerate(energies, 1):
            lines.append(f"  {i}: {energy:.0f} kJ/mol")
        return "\n".join(lines)
    
    def _analyze_properties(self):
        """Quick action: Analyze properties."""
        self._add_user_message(f"Analyze the properties of {self.current_element.symbol}")
        response = self._analyze_properties_response()
        self._add_agent_message(response)
    
    def _suggest_visualizations(self):
        """Quick action: Suggest visualizations."""
        self._add_user_message(f"What visualizations would help me understand {self.current_element.symbol}?")
        response = self._visualization_response()
        self._add_agent_message(response)
    
    def _quantum_insights(self):
        """Quick action: Quantum insights."""
        self._add_user_message(f"Give me quantum insights for {self.current_element.symbol}")
        response = self._quantum_response()
        self._add_agent_message(response)
    
    def _add_user_message(self, message: str):
        """Add user message to chat display."""
        self.chat_display.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        self.chat_display.insert(tk.END, "You:\n", 'user_msg')
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
        self.messages.append(ChatMessage(
            timestamp=datetime.now(),
            sender='user',
            message=message,
            element_symbol=self.current_element.symbol if self.current_element else None
        ))
    
    def _add_agent_message(self, message: str):
        """Add agent message to chat display."""
        self.chat_display.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        self.chat_display.insert(tk.END, "Agent:\n", 'agent_msg')
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
        self.messages.append(ChatMessage(
            timestamp=datetime.now(),
            sender='agent',
            message=message
        ))
    
    def _clear_history(self):
        """Clear chat history."""
        if messagebox.askyesno("Clear History", "Clear all conversation history?"):
            self.messages = []
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.config(state=tk.DISABLED)
            self._initialize_agent()
