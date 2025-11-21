"""
Periodic Table Desktop Application
Interactive periodic table with quantum research integration.
"""

__version__ = "1.0.0"
__author__ = "Periodic Table Team"

from src.element import Element
from src.element_database import ElementDatabase
from src.element_visual import ElementVisualizer
from agent.agent import ResearchAgentManager, QuantumProcessor
from src.analysis_report import AnalysisReportGenerator

__all__ = [
    'Element',
    'ElementDatabase',
    'ElementVisualizer',
    'ResearchAgentManager',
    'QuantumProcessor',
    'AnalysisReportGenerator',
]
