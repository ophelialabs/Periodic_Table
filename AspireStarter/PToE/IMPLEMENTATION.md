# Periodic Table of Elements - Implementation Guide

## Overview
This project implements an interactive web-based Periodic Table of Elements using .NET Aspire with a microservices architecture consisting of an API service backend and a Blazor web frontend.

## Architecture

### Backend (PToE.ApiService)
**Language**: C# (.NET)
**Framework**: ASP.NET Core Minimal APIs
**Port**: Default Aspire service discovery

#### API Endpoints

The API provides the following RESTful endpoints for element data:

- **GET `/api/elements`** - Retrieve all 118 elements from the periodic table
- **GET `/api/elements/number/{atomicNumber}`** - Get element by atomic number (1-118)
- **GET `/api/elements/symbol/{symbol}`** - Get element by chemical symbol (e.g., "H", "He")
- **GET `/api/elements/name/{name}`** - Get element by full name
- **GET `/api/elements/search?q={query}`** - Search elements by name, symbol, or category
- **GET `/api/elements/category/{category}`** - Get all elements in a specific category

#### Key Components

**Models (`PToE.ApiService/Models/Element.cs`)**:
- `Element` - Represents a periodic table element with 30+ properties including atomic mass, melting point, electron configuration, etc.
- `ElementImage` - Contains image metadata for elements
- `PeriodicTableData` - Container for the full periodic table JSON data

**Services (`PToE.ApiService/Services/PeriodicTableService.cs`)**:
- `IPeriodicTableService` - Interface for all periodic table operations
- `PeriodicTableService` - Implementation that loads from `periodic-table-lookup.json` and provides filtering/search functionality

**Data Source**:
- Location: `PToE.ApiService/lib/Periodic-Table-JSON/periodic-table-lookup.json`
- Format: JSON with element order array and individual element objects
- Contains comprehensive data for all 118 elements including:
  - Basic properties (atomic number, mass, symbol, phase)
  - Physical properties (density, melting point, boiling point)
  - Electronic properties (electron configuration, electronegativity, ionization energies)
  - Category classification
  - Wikipedia links
  - 3D model URLs (Bohr models)
  - Element images with attribution

### Frontend (PToE.Web)
**Framework**: Blazor Server (Interactive Server Components)
**Language**: C# with Razor markup

#### Pages & Components

**PeriodicTableofElements.razor** (`PToE.Web/Components/Pages/PeriodicTableofElements.razor`):
- Main interactive periodic table interface
- Features:
  - 18-column grid layout matching standard periodic table structure
  - Elements positioned by xpos/ypos coordinates
  - Color-coded by category
  - Click to view details
  - Real-time search filtering
  - Category legend
  - Responsive design (desktop, tablet, mobile)

**ElementDetailModal.razor** (`PToE.Web/Components/ElementDetailModal.razor`):
- Modal dialog showing detailed element information
- Displays:
  - Symbol, atomic number, and category color
  - Basic properties (mass, period, group, block, phase)
  - Summary description
  - Physical properties (density, melting/boiling points)
  - Electronic properties (electronegativity, electron affinity, configuration)
  - Element images with attribution
  - Discovery information
  - Wikipedia link

**Navigation Update** (`PToE.Web/Components/Layout/NavMenu.razor`):
- Added "Periodic Table" navigation link to main menu

#### HTTP Client

**PeriodicTableApiClient** (`PToE.Web/Services/PeriodicTableApiClient.cs`):
- Service for communicating with the API backend
- Methods:
  - `GetAllElementsAsync()` - Fetch all elements
  - `GetElementByNumberAsync(int)` - Get by atomic number
  - `GetElementBySymbolAsync(string)` - Get by symbol
  - `SearchElementsAsync(string)` - Search by query
  - `GetElementsByCategoryAsync(string)` - Filter by category
- Uses proper JSON deserialization with case-insensitive property matching

#### Styling

**periodic-table.css** (`PToE.Web/wwwroot/periodic-table.css`):
- Comprehensive styling for the periodic table UI
- Grid-based layout using CSS Grid
- Category color scheme:
  - Alkali metals: #FFB5B5 (light red)
  - Alkaline earth metals: #FFDDB3 (light orange)
  - Transition metals: #FFC0C0 (light pink)
  - Lanthanides/Actinides: #FFBFFF (light purple)
  - Nonmetals: #A0FFA0 (light green)
  - Halogens: #FFFF99 (light yellow)
  - Noble gases: #C0FFFF (light cyan)
  - And more...
- Responsive breakpoints for tablets and mobile devices
- Hover effects and transitions for better UX
- Modal styling for element details

## Features Implemented

### ✅ Phase 1: Basic Interactive Table
- [x] Web-based interactive grid layout
- [x] Elements positioned in periodic table structure
- [x] Color-coded by category
- [x] Click elements to view details
- [x] Search functionality (name, symbol, category)
- [x] Responsive design
- [x] Category legend

### 📋 Future Phases (From Roadmap)
- [ ] 3D Visualizations (Bohr model viewer, orbital visualizations)
- [ ] Data visualization charts (atomic mass distribution, ionization energies, etc.)
- [ ] Spectral analysis and hyperspectral visualization
- [ ] Element similarity recommendations
- [ ] Wikipedia integration (currently linked)
- [ ] Database integration for extended properties
- [ ] Quantum integration and simulations
- [ ] Research agent for molecular analysis
- [ ] PDF report generation with visualizations

## How to Run

### Prerequisites
- .NET 9.0 or later
- Visual Studio 2022 or VS Code with C# extension

### Running Locally

1. **Start the AppHost** (Aspire):
   ```bash
   cd PToE.AppHost
   dotnet run
   ```
   This will launch both the API service and web frontend through Aspire orchestration.

2. **Access the application**:
   - Open browser to `https://localhost:5173` (or the port shown in console)
   - Navigate to "Periodic Table" in the menu

3. **API Documentation**:
   - API endpoints available at `https+http://apiservice/api/elements`

### Building

```bash
dotnet build
dotnet publish
```

## Project Structure

```
PToE/
├── PToE.ApiService/                 # Backend API
│   ├── Models/
│   │   └── Element.cs              # Data models
│   ├── Services/
│   │   └── PeriodicTableService.cs # Business logic
│   ├── Program.cs                  # API setup & endpoints
│   └── lib/
│       └── Periodic-Table-JSON/    # Data files
│
├── PToE.Web/                        # Frontend Blazor
│   ├── Components/
│   │   ├── Pages/
│   │   │   ├── PeriodicTableofElements.razor
│   │   │   ├── Home.razor
│   │   │   └── Counter.razor
│   │   ├── ElementDetailModal.razor
│   │   ├── Layout/
│   │   │   └── NavMenu.razor
│   │   ├── App.razor
│   │   └── Routes.razor
│   ├── Models/
│   │   └── Element.cs              # Mirror of API models
│   ├── Services/
│   │   └── PeriodicTableApiClient.cs
│   ├── Program.cs                  # Web setup
│   └── wwwroot/
│       ├── app.css
│       ├── periodic-table.css
│       └── lib/bootstrap/
│
├── PToE.ServiceDefaults/            # Shared service defaults
├── PToE.AppHost/                    # Aspire orchestration
└── README.md
```

## Data Model

Each element contains the following fields:

```csharp
public class Element
{
    public string Name { get; set; }                    // e.g., "Hydrogen"
    public string Symbol { get; set; }                  // e.g., "H"
    public int AtomicNumber { get; set; }              // 1-118
    public double AtomicMass { get; set; }             // e.g., 1.008
    public string Category { get; set; }               // Element type
    public int Period { get; set; }                    // Row in periodic table
    public int Group { get; set; }                     // Column in periodic table
    public string Phase { get; set; }                  // Solid/Liquid/Gas
    public double? Density { get; set; }               // g/cm³
    public double? MeltingPoint { get; set; }          // Kelvin
    public double? BoilingPoint { get; set; }          // Kelvin
    public double? Electronegativity { get; set; }     // Pauling scale
    public string? ElectronConfiguration { get; set; } // e.g., "1s2 2s1"
    public string? Summary { get; set; }               // Element description
    public string? BohrModel3D { get; set; }          // GLB model URL
    public ElementImage? Image { get; set; }           // Element photo
    // ... and more properties
}
```

## Key Design Decisions

1. **Minimal APIs**: Used ASP.NET Core Minimal APIs for a clean, modern API design
2. **Service Pattern**: Centralized `PeriodicTableService` for data access and operations
3. **Component Reusability**: ElementDetailModal is a reusable component
4. **Responsive CSS Grid**: Grid layout automatically adapts to screen size
5. **Lazy Loading**: Elements loaded asynchronously from backend
6. **Color Coding**: Visual categories help users identify element types at a glance
7. **Search First Design**: Prominent search box for quick element lookup

## Performance Considerations

- Elements loaded once and cached in service
- Efficient JSON deserialization with property name mapping
- Search performed client-side (safe for 118 elements)
- CSS Grid provides native browser optimization
- Minimal re-renders through proper Blazor component design

## Extensibility

The architecture supports easy addition of:
- New API endpoints for additional data
- New visualization components
- Database integration (replace JSON file loading)
- Authentication/authorization layers
- API versioning
- Advanced search/filtering
- Element comparison tools

## Credits

- Periodic table data from the Periodic-Table-JSON library
- Element images and 3D models sourced from Wikimedia Commons and other open sources
- Bootstrap for responsive utilities
- Blazor framework for interactive web components

## Future Enhancements

See the Features Roadmap in the main README.md for planned additions including:
- 3D visualizations and interactive models
- Advanced data analysis and visualization
- Quantum computing integration
- Research agent capabilities
