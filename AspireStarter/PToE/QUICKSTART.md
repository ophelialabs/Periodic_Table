# Periodic Table Application - Quick Start Guide

## What Was Built

A fully functional **Interactive Periodic Table of Elements** web application using modern .NET architecture with:

- **API Backend** (ASP.NET Core with Minimal APIs)
- **Web Frontend** (Blazor Server with interactive components)
- **Complete Data** (All 118 elements with comprehensive properties)

## Features

✅ **Interactive Grid Layout** - Elements arranged in standard periodic table structure  
✅ **Color-Coded Categories** - 11 distinct element categories with unique colors  
✅ **Element Details** - Click any element to see comprehensive information  
✅ **Search & Filter** - Find elements by name, symbol, or category  
✅ **Responsive Design** - Works on desktop, tablet, and mobile  
✅ **RESTful API** - 6 different API endpoints for data access  
✅ **Modern Architecture** - .NET Aspire microservices orchestration  

## Running the Application

### Prerequisites
- **.NET 9.0 or later** installed
- Visual Studio 2022, VS Code, or JetBrains Rider

### Start the Application

1. Open a terminal in the `PToE` directory:
   ```bash
   cd /Users/jesse/Desktop/Company/Tools/PeriodicTable/AspireStarter/PToE
   ```

2. Start the Aspire host (orchestrates both API and Web):
   ```bash
   cd PToE.AppHost
   dotnet run
   ```

3. The console will show the URLs. Open your browser to the web application URL (typically `https://localhost:5173` or similar)

4. Click **"Periodic Table"** in the navigation menu

### Using the Application

**View the Periodic Table:**
- Elements are arranged in the standard periodic table grid
- Each element shows its symbol, number, name, and atomic mass
- Elements are color-coded by category

**Search for Elements:**
- Use the search box at the top to find elements by:
  - Name (e.g., "gold", "helium")
  - Symbol (e.g., "Au", "He")
  - Category (e.g., "alkali metal", "noble gas")

**View Element Details:**
- Click any element to open a detailed information panel showing:
  - Atomic mass and configuration
  - Physical properties (density, melting/boiling points)
  - Electronic properties (electronegativity, electron affinity)
  - Element photographs with attribution
  - Discovery information
  - Link to Wikipedia for more information

## API Endpoints

You can also access the API directly at `https+http://apiservice/api/elements`:

```bash
# Get all elements
GET /api/elements

# Get element by atomic number
GET /api/elements/number/1

# Get element by symbol
GET /api/elements/symbol/Au

# Get element by name
GET /api/elements/name/gold

# Search elements
GET /api/elements/search?q=alkali

# Get by category
GET /api/elements/category/noble%20gas
```

## Project Structure

```
PToE/
├── PToE.ApiService/          ← Backend API with element data
├── PToE.Web/                 ← Blazor frontend with UI
├── PToE.ServiceDefaults/     ← Shared configuration
├── PToE.AppHost/             ← Aspire orchestration
└── IMPLEMENTATION.md         ← Detailed technical documentation
```

## Key Files to Know

**Backend:**
- `PToE.ApiService/Program.cs` - API routes and configuration
- `PToE.ApiService/Services/PeriodicTableService.cs` - Data loading and operations
- `PToE.ApiService/Models/Element.cs` - Element data model

**Frontend:**
- `PToE.Web/Components/Pages/PeriodicTableofElements.razor` - Main table UI
- `PToE.Web/Components/ElementDetailModal.razor` - Element detail popup
- `PToE.Web/Services/PeriodicTableApiClient.cs` - API communication
- `PToE.Web/wwwroot/periodic-table.css` - Table styling

**Data:**
- `PToE.ApiService/lib/Periodic-Table-JSON/periodic-table-lookup.json` - All element data (118 elements)

## Color Categories

| Color | Category |
|-------|----------|
| Light Red | Alkali Metals |
| Light Orange | Alkaline Earth Metals |
| Light Pink | Transition Metals |
| Light Purple | Lanthanides & Actinides |
| Light Green | Nonmetals |
| Yellow | Halogens |
| Cyan | Noble Gases |
| Gray | Post-Transition Metals |
| Olive | Metalloids |

## Technical Stack

- **Language**: C#
- **Backend Framework**: ASP.NET Core 10
- **Frontend Framework**: Blazor Server
- **Orchestration**: .NET Aspire
- **Build System**: .NET CLI
- **Styling**: CSS3 (with Bootstrap utilities)
- **Data Format**: JSON

## Browser Support

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Any modern browser with JavaScript enabled

## Troubleshooting

**"Unable to connect to backend":**
- Ensure both services are running via `dotnet run` in PToE.AppHost
- Check that ports are not in use
- Clear browser cache and reload

**"No elements loading":**
- Verify the periodic-table-lookup.json file exists in the correct location
- Check API console for any loading errors

**"Styling looks broken":**
- Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
- Check that CSS files are loading (check network tab in browser dev tools)

## Next Steps

The foundation is complete! Future enhancements could include:
- 3D visualization of atomic structures
- Data analysis charts and graphs
- Quantum computing simulations
- Element comparison tools
- Advanced search with filters
- User accounts and favorites
- Mobile app version

See `IMPLEMENTATION.md` and `README.md` for the complete roadmap.

## Support

For detailed technical information, see:
- `IMPLEMENTATION.md` - Architecture and design decisions
- `README.md` - Features roadmap and project vision
