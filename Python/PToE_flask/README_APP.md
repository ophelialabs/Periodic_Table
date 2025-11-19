# Interactive Periodic Table of Elements

A beautiful, interactive Flask web application for exploring the periodic table with advanced 3D visualizations and element details.

## Features

✨ **Interactive Periodic Table**
- Color-coded elements by category
- Click any element to view detailed information
- Search functionality by name, symbol, or atomic number

🧬 **3D Visualizations**
- **Bohr Model (2D)**: Traditional 2D representation of electron orbitals
- **Bohr Model (3D)**: Interactive 3D model viewer (GLB format support)
- **de Broglie Wave Model**: Visualization of electron wave properties
- **Schrödinger Wave Function**: Electron probability density visualization

📊 **Element Details**
- Atomic structure and properties
- Physical characteristics (density, melting/boiling points)
- Spectral bands visualization
- Electron configuration
- Electronegativity and ionization energies
- Historical discovery information
- Element images and Wikipedia sources

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. **Clone or navigate to the project directory:**
```bash
cd /Users/jesse/Desktop/Company/Tools/PeriodicTable/Python/PToE_flask
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

Or if using the virtual environment directly:
```bash
./venv/bin/pip install -r requirements.txt
```

## Running the Application

### Using Flask CLI

```bash
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
```

### Using Python directly

```bash
python run.py
```

The application will start on `http://localhost:5001`

### Using the Virtual Environment

```bash
source venv/bin/activate
python run.py
```

## Project Structure

```
PToE_flask/
├── run.py                          # Application entry point
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables
└── src/
    └── app/
        ├── __init__.py             # Flask app factory
        ├── main.py                 # Main blueprint (routes)
        ├── api.py                  # API blueprint (data endpoints)
        ├── templates/
        │   ├── base.html           # Base template
        │   └── index.html          # Periodic table page
        └── static/                 # Static files (CSS, JS, images)
```

## Usage

1. **Navigate to the app:** Open `http://localhost:5000` in your browser

2. **Browse the periodic table:**
   - Elements are color-coded by category
   - Hover over elements to see them highlight
   - Click on any element to see detailed information

3. **Search for elements:**
   - Use the search bar to find elements by name, symbol, or atomic number
   - Results update in real-time

4. **View element details:**
   - A modal window displays comprehensive information
   - View 3D models if available
   - Check spectral bands visualization
   - Read element summaries from Wikipedia

## Data Source

The periodic table data is sourced from the **Periodic-Table-JSON** project, which includes:
- Complete element properties
- 3D Bohr models (GLB format)
- 2D spectral band images
- Historical discovery information
- Electron configurations and other quantum properties

Data file: `src/lib/Periodic-Table-JSON/PeriodicTableJSON.json`

## 3D Model Support

The application uses **Model-Viewer** from Google to display 3D atomic models in GLB format. This provides:
- Interactive rotation and zoom
- Auto-rotation capability
- Touch and mouse controls
- Cross-browser compatibility

## Customization

### Configuration

Edit `config.py` to customize:
- Cache settings
- Session configuration
- Data file location
- Debug mode

### Styling

Edit `src/app/templates/base.html` and `src/app/templates/index.html` to customize:
- Color schemes
- Layout
- Element card design
- Modal styling

### Data

Replace `src/lib/Periodic-Table-JSON/PeriodicTableJSON.json` to use different data or update the existing data.

## API Endpoints

The application provides RESTful API endpoints:

- `GET /api/elements` - Get all elements
- `GET /api/element/<atomic_number>` - Get element by atomic number
- `GET /api/element/<symbol>` - Get element by symbol

## Browser Compatibility

- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

Required for 3D models: WebGL support

## Technologies Used

- **Backend:** Flask, Python
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **UI Framework:** Bootstrap 5
- **3D Visualization:** Model-Viewer, Canvas API
- **Data Format:** JSON
- **Icons:** Unicode/Emoji

## Troubleshooting

### "Could not locate a Flask application" Error

Make sure you're running from the correct directory:
```bash
cd /Users/jesse/Desktop/Company/Tools/PeriodicTable/Python/PToE_flask
python run.py
```

Or set the Flask app explicitly:
```bash
export FLASK_APP=run.py
flask run
```

### Port Already in Use

If port 5000 is already in use, you can specify a different port:
```bash
python run.py  # Then manually change port in run.py or use:
flask run --port 5001
```

### 3D Models Not Loading

- Check browser console for errors (F12)
- Ensure WebGL is enabled in your browser
- Verify the GLB files exist in the data directory

## Future Enhancements

- [ ] Add periodic trends visualization
- [ ] Compare multiple elements side-by-side
- [ ] Export element data to PDF
- [ ] Add periodic table configuration (show/hide categories)
- [ ] Implement favorites/bookmarks
- [ ] Add quiz mode to learn element properties
- [ ] Mobile-optimized interface

## License

This project uses data from the Periodic-Table-JSON project.
See `src/lib/Periodic-Table-JSON/LICENSE.md` for details.

## Support

For issues or questions, please check:
1. The troubleshooting section above
2. Browser console logs (F12 or right-click → Inspect)
3. Terminal/console output when running the app

---

**Enjoy exploring the periodic table!** ⚛️
