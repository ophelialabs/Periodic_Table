#!/usr/bin/env python3
"""
Verification script to test all application components.
Run this to ensure the application is working correctly.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_database():
    """Test element database."""
    print("Testing Element Database...")
    from src.element_database import ElementDatabase
    
    db = ElementDatabase()
    assert db.get_element_count() > 0, "No elements loaded"
    
    # Test element retrieval
    hydrogen = db.get_element_by_symbol('H')
    assert hydrogen is not None, "Could not load hydrogen"
    assert hydrogen.number == 1, "Hydrogen atomic number incorrect"
    
    # Test search
    results = db.search_elements('noble')
    assert len(results) > 0, "Search failed"
    
    print(f"  ✓ Database loaded {db.get_element_count()} elements")
    print(f"  ✓ Element retrieval working")
    print(f"  ✓ Search functionality working")
    return db

def test_visualizations(db):
    """Test visualization module."""
    print("\nTesting Visualizations...")
    from src.element_visual import ElementVisualizer
    
    viz = ElementVisualizer(db)
    
    # Test some visualization methods exist
    methods = [
        'plot_atomic_structure_3d',
        'plot_ionization_energies_3d',
        'plot_electron_shells_3d',
        'plot_atomic_mass_distribution',
        'plot_elements_by_category',
        'plot_phase_distribution',
        'plot_electronegativity_heatmap',
    ]
    
    for method in methods:
        assert hasattr(viz, method), f"Missing method: {method}"
    
    print(f"  ✓ ElementVisualizer has {len(methods)}+ methods")
    print(f"  ✓ All visualization methods available")
    return viz

def test_gui(db, viz):
    """Test GUI initialization."""
    print("\nTesting GUI Application...")
    import tkinter as tk
    from src.app.main_app import PeriodicTableApp
    
    root = tk.Tk()
    try:
        app = PeriodicTableApp(root)
        assert app.db is not None, "Database not initialized in GUI"
        assert app.visualizer is not None, "Visualizer not initialized in GUI"
        print("  ✓ PeriodicTableApp initialized")
        print("  ✓ Database loaded in GUI")
        print("  ✓ Visualizer loaded in GUI")
        root.destroy()
    except Exception as e:
        root.destroy()
        raise e

def test_analysis(db):
    """Test analysis report generator."""
    print("\nTesting Analysis Report Generator...")
    from src.analysis_report import AnalysisReportGenerator
    
    generator = AnalysisReportGenerator(db)
    
    # Test summary generation
    summary = generator.generate_summary_statistics()
    assert len(summary) > 0, "Summary generation failed"
    assert "PERIODIC TABLE ANALYSIS SUMMARY" in summary, "Summary format incorrect"
    
    print("  ✓ AnalysisReportGenerator initialized")
    print("  ✓ Summary statistics generation working")
    print("  ✓ Ready to generate PDF/PNG reports")

def test_quantum(db):
    """Test quantum integration."""
    print("\nTesting Quantum Integration...")
    from src.research_agent import QuantumIntegration, ResearchTaskType
    
    quantum = QuantumIntegration(use_azure=False)
    
    # Test job submission
    job_id = quantum.analyze_element_quantum_properties('Fe')
    assert job_id is not None, "Job submission failed"
    assert 'QJ_' in job_id, "Invalid job ID format"
    
    print("  ✓ QuantumIntegration initialized")
    print("  ✓ Job submission working")
    print("  ✓ Framework ready for Azure integration")

def main():
    """Run all tests."""
    print("=" * 70)
    print("PERIODIC TABLE APPLICATION - VERIFICATION TEST")
    print("=" * 70)
    
    try:
        # Test database
        db = test_database()
        
        # Test visualizations
        viz = test_visualizations(db)
        
        # Test GUI
        test_gui(db, viz)
        
        # Test analysis
        test_analysis(db)
        
        # Test quantum
        test_quantum(db)
        
        print("\n" + "=" * 70)
        print("✓ ALL TESTS PASSED!")
        print("=" * 70)
        print("\nYou can now run the application with:")
        print("  python run_app.py")
        print("\nOr generate analysis reports with:")
        print("  python generate_analysis.py")
        print("=" * 70)
        
        return 0
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
