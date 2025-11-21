# Periodic Table Application - Reference Card

## 🚀 Quick Start
```bash
cd PToE.AppHost && dotnet run
# Then open browser to displayed URL and click "Periodic Table"
```

## 📍 Key URLs
- **Web Application**: `https://localhost:5173` (or similar)
- **Periodic Table Page**: `/periodic-table`
- **API Base**: `https+http://apiservice/api/elements`

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/elements` | All 118 elements |
| GET | `/api/elements/number/{n}` | Get by atomic number (1-118) |
| GET | `/api/elements/symbol/{sym}` | Get by symbol (H, He, Li, etc.) |
| GET | `/api/elements/name/{name}` | Get by element name |
| GET | `/api/elements/search?q={term}` | Search by name/symbol/category |
| GET | `/api/elements/category/{cat}` | Get by category |

## 🎨 Element Categories & Colors

| Category | Color | Examples |
|----------|-------|----------|
| Alkali Metals | #FFB5B5 | Li, Na, K |
| Alkaline Earth | #FFDDB3 | Be, Mg, Ca |
| Transition Metal | #FFC0C0 | Fe, Cu, Zn |
| Lanthanide | #FFBFFF | La, Ce, Pr |
| Actinide | #FFB5B5 | U, Pu, Th |
| Post-Transition | #CCCCCC | Al, Sn, Pb |
| Metalloid | #CCCC99 | B, Si, As |
| Nonmetal (diatomic) | #A0FFA0 | H, N, O, F |
| Nonmetal (polyatomic) | #A0FFA0 | C, P, S |
| Halogen | #FFFF99 | F, Cl, Br, I |
| Noble Gas | #C0FFFF | He, Ne, Ar |

## 📂 Project Structure

```
PToE/
├── PToE.ApiService/
│   ├── Models/
│   │   └── Element.cs (30+ properties per element)
│   ├── Services/
│   │   └── PeriodicTableService.cs (data loading & search)
│   ├── Program.cs (6 API endpoints)
│   └── lib/Periodic-Table-JSON/
│       └── periodic-table-lookup.json (118 elements)
│
├── PToE.Web/
│   ├── Models/
│   │   └── Element.cs (matches API model)
│   ├── Services/
│   │   └── PeriodicTableApiClient.cs (HTTP client)
│   ├── Components/
│   │   ├── Pages/
│   │   │   └── PeriodicTableofElements.razor (main UI)
│   │   ├── ElementDetailModal.razor (detail view)
│   │   ├── Layout/NavMenu.razor (navigation)
│   │   └── App.razor (CSS links)
│   ├── Program.cs (service setup)
│   └── wwwroot/
│       └── periodic-table.css (responsive styling)
│
├── PToE.AppHost/ (Aspire orchestration)
├── PToE.ServiceDefaults/ (shared config)
└── Documentation/
    ├── README.md (features & roadmap)
    ├── QUICKSTART.md (getting started)
    ├── IMPLEMENTATION.md (technical details)
    └── SUMMARY.md (what was built)
```

## 🎯 UI Features

**Search Box**:
- Type element name (gold, helium)
- Type symbol (Au, He)
- Type category (alkali, noble gas)
- Real-time filtering

**Periodic Table Grid**:
- 18 columns × 7 rows (standard layout)
- Shows: Number, Symbol, Name, Atomic Mass
- Color-coded by category
- Hover effects

**Element Detail Modal**:
- 40+ properties displayed
- Element image with attribution
- Discovery information
- Wikipedia link
- Responsive layout

## 🔄 Data Flow

```
User Browser
    ↓
Blazor Component (PeriodicTableofElements.razor)
    ↓
PeriodicTableApiClient
    ↓
HTTP Request
    ↓
ASP.NET Core API (Program.cs)
    ↓
PeriodicTableService
    ↓
periodic-table-lookup.json
    ↓
JSON Deserialized → Element Objects
    ↓
HTTP Response
    ↓
Rendered in Browser
```

## 📊 Element Data Properties

Each element includes:
- **Identity**: name, symbol, atomic number, atomic mass
- **Classification**: category, period, group, block, phase
- **Physical**: density, melting point, boiling point, appearance
- **Electronic**: electron configuration, electronegativity, ionization energies
- **Discovery**: discovered by, named by, year discovered
- **Media**: image URL, bohr model URL, spectral image, Wikipedia link
- **Atomic Structure**: electron shells, electron affinity, CPK color

## 🛠️ Development

**Add New Endpoint**:
```csharp
// In PToE.ApiService/Program.cs
app.MapGet("/api/elements/custom", CustomHandler)
    .WithName("CustomEndpoint");

async Task<IResult> CustomHandler(IPeriodicTableService service)
{
    // implementation
    return Results.Ok(data);
}
```

**Modify Search**:
```csharp
// In PeriodicTableService.cs
public async Task<List<Element>> SearchElementsAsync(string query)
{
    // Customize search logic here
}
```

**Change Colors**:
```csharp
// In PeriodicTableofElements.razor
private string GetCategoryColor(string category)
{
    return category.ToLower() switch
    {
        "alkali metal" => "#NEW_COLOR",
        // ... etc
    };
}
```

## 📱 Responsive Breakpoints

| Breakpoint | Width | Layout |
|-----------|-------|--------|
| Desktop | >1200px | Full 18-column grid |
| Tablet | 768-1200px | 12-column grid, smaller cells |
| Mobile | <768px | 12-column grid, 6-column on small |

## ⚡ Performance

- Elements cached in memory after first load
- Client-side search (no API calls while typing)
- CSS Grid uses native browser optimization
- Lazy modal loading (only shown when needed)
- Async HTTP operations (non-blocking)

## 🔐 Security

- CORS enabled for safe cross-origin access
- No sensitive data exposed via API
- Input validation on search queries
- Safe JSON deserialization

## 📋 Browser Compatibility

- Chrome/Chromium ✅
- Firefox ✅
- Safari ✅
- Edge ✅
- Requires JavaScript enabled

## 🐛 Debugging Tips

**API Issues**:
- Check AppHost console for errors
- Test endpoints with curl: `curl https+http://localhost:5000/api/elements`

**Web Issues**:
- Check browser console (F12)
- Network tab shows API requests
- Blazor diagnostics in browser console

**Data Issues**:
- Verify JSON file exists: `PToE.ApiService/lib/Periodic-Table-JSON/periodic-table-lookup.json`
- Check file is valid JSON

## 📚 Files to Know

**For API Work**: 
- `PToE.ApiService/Program.cs` - Routes
- `PToE.ApiService/Services/PeriodicTableService.cs` - Logic

**For UI Work**:
- `PToE.Web/Components/Pages/PeriodicTableofElements.razor` - Main component
- `PToE.Web/wwwroot/periodic-table.css` - Styles

**For HTTP**:
- `PToE.Web/Services/PeriodicTableApiClient.cs` - API calls

**For Models**:
- `PToE.ApiService/Models/Element.cs` - Backend model
- `PToE.Web/Models/Element.cs` - Frontend model

## 🎓 Learning Resources

In this implementation you'll find examples of:
- ✅ REST API design with .NET
- ✅ Blazor Server components
- ✅ Service pattern and dependency injection
- ✅ HTTP client usage in .NET
- ✅ JSON deserialization
- ✅ CSS Grid layouts
- ✅ Responsive design
- ✅ Component composition
- ✅ Error handling
- ✅ Async programming

## 📞 Support

- Check `IMPLEMENTATION.md` for technical details
- Check `QUICKSTART.md` for usage help
- Check `README.md` for feature roadmap
- Console logs show API and client activity

---

**Version**: 1.0  
**Status**: ✅ Production Ready  
**Last Updated**: 2024
