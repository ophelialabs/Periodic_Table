import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Use port 5001 by default to avoid conflicts with AirPlay Receiver on macOS
    # Change PORT environment variable to use a different port
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)