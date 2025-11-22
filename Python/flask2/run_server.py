#!/usr/bin/env python3
"""
Run the Periodic Table Flask server.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000, host='127.0.0.1')
