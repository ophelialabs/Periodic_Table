#!/usr/bin/env python3
"""
Generate comprehensive analysis reports and visualizations.
Run this script to create PDF reports and PNG visualizations.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.element_database import ElementDatabase
from src.analysis_report import AnalysisReportGenerator

def main():
    """Generate analysis reports."""
    print("Initializing Periodic Table Analysis...")
    
    try:
        # Load database
        db = ElementDatabase()
        print(f"Loaded {db.get_element_count()} elements")
        
        # Create report generator
        generator = AnalysisReportGenerator(db)
        
        # Print summary
        print("\n" + generator.generate_summary_statistics())
        
        # Generate reports
        print("\nGenerating reports and visualizations...")
        generator.generate_full_report(include_pdf=True, include_png=True)
        
        # Generate CSV
        print("\nGenerating CSV data file...")
        generator.generate_element_details_csv()
        
        print("\n✓ Analysis complete!")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
