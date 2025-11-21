#!/usr/bin/env python3
"""
Entry point for the Periodic Table Desktop Application.
Run this script to start the interactive periodic table GUI.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.app.main_app import main

if __name__ == '__main__':
    main()
