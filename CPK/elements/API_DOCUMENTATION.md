# 3D Periodic Table - Complete API Documentation

## Table of Contents
1. [Frontend Components](#frontend-components)
2. [Backend Tools](#backend-tools)
3. [State Management](#state-management)
4. [Data Structures](#data-structures)
5. [Integration Examples](#integration-examples)

---

## Frontend Components

### PeriodicTable3D Component

Interactive 3D visualization of the periodic table using Three.js.

**Props:**
```typescript
interface PeriodicTable3DProps {
  onElementClick?: (element: Element) => void;
  selectedElement?: Element | null;
}
```

**Features:**
- Mouse hover reveals element details
- Click to select element
- Real-time 3D rotation
- Color-coded by category
- Shadow and lighting effects

**Usage:**
```tsx
import { PeriodicTable3D } from '@/components/PeriodicTable3D';

<PeriodicTable3D 
  onElementClick={(element) => console.log(element)}
  selectedElement={selectedElement}
/>
```

**Events:**
- `onElementClick`: Triggered when user clicks an element
- Hover tooltip shows: Symbol, Name, Atomic #, Atomic Mass

---

### ElementCard Component

Displays detailed information about a selected element.

**Props:**
```typescript
interface ElementCardProps {
  element: Element;
  onClose?: () => void;
}
```

**Displays:**
- Large element symbol and name
- Category color badge
- Basic properties (atomic number, mass, period, group)
- Advanced properties (electronegativity, ionization energy, density, atomic radius)
- Thermal properties (melting point, boiling point)
- Discovery year

**Usage:**
```tsx
import { ElementCard } from '@/components/ElementCard';

{selectedElement && (
  <ElementCard 
    element={selectedElement}
    onClose={() => setSelectedElement(null)}
  />
)}
```

---

### DataVisualization Component

Dynamic chart rendering using Plotly.js.

**Props:**
```typescript
interface DataVisualizationProps {
  type: 'scatter' | 'histogram' | 'heatmap';
  selectedElements?: Element[];
  property?: 'atomicMass' | 'electronegativity' | 
             'ionizationEnergy' | 'density';
}
```

**Features:**
- Multiple chart types
- Interactive tooltips
- Responsive design
- Dark theme
- Category color coding

**Usage:**
```tsx
import { DataVisualization } from '@/components/DataVisualization';

<DataVisualization
  type="scatter"
  property="atomicMass"
  selectedElements={PERIODIC_TABLE}
/>
```

---

## Backend Tools

### Agent Tools (agent/agent.py)

#### 1. get_weather
Basic tool for demonstration.

```python
@tool
def get_weather(location: str):
    """Get the weather for a given location."""
    return f"The weather for {location} is 70 degrees."
```

#### 2. select_elements_by_category
Filters elements by their category.

**Parameters:**
- `category` (str): Element category name

**Returns:**
```json
{
  "category": "Transition Metal",
  "elements": ["Sc", "Ti", "V", "Cr", ...],
  "count": 10
}
```

**Usage in prompt:**
> "Show me all transition metals"

#### 3. create_visualization
Instructs frontend to create a data visualization.

**Parameters:**
- `visualization_type` (str): 'scatter', 'histogram', or 'heatmap'
- `property_name` (str): 'atomicMass', 'electronegativity', 'ionizationEnergy', 'density'
- `elements` (List[str], optional): Specific element symbols

**Returns:**
```json
{
  "visualization_type": "scatter",
  "property": "atomicMass",
  "elements": "all",
  "status": "created"
}
```

**Usage in prompt:**
> "Create a scatter plot of atomic mass"

#### 4. get_element_properties
Retrieves detailed properties of a single element.

**Parameters:**
- `element_symbol` (str): Element symbol (e.g., "Fe", "Au")

**Returns:**
```json
{
  "name": "Iron",
  "atomicNumber": 26,
  "atomicMass": 55.845,
  "category": "Transition Metal"
}
```

**Usage in prompt:**
> "Tell me about Iron"

---

## State Management

### Agent State (AgentState)

```python
class AgentState(MessagesState):
    proverbs: List[str] = []
    selected_elements: List[str] = []
    visualization_type: str = "scatter"
    visualization_property: str = "atomicMass"
    tools: List[Any]
```

### Frontend State (CopilotKit)

```typescript
type AgentState = {
  proverbs: string[];
  selected_elements: string[];
  visualization_type: string;
  visualization_property: string;
}
```

**State Updates Trigger:**
- Re-render of visualization components
- Update of UI control panels
- Chart refresh with new data

---

## Data Structures

### Element Interface

```typescript
interface Element {
  atomicNumber: number;
  symbol: string;
  name: string;
  atomicMass: number;
  category: string;
  categoryColor: string;
  period: number;
  group: number;
  electronegativity?: number;
  ionizationEnergy?: number;
  atomicRadius?: number;
  density?: number;
  meltingPoint?: number;
  boilingPoint?: number;
  yearDiscovered?: number;
  state?: string;
}
```

### Element Categories

```typescript
enum ElementCategory {
  Nonmetal = 'Nonmetal',
  ReactiveNonmetal = 'Reactive Nonmetal',
  NobleGas = 'Noble Gas',
  AlkaliMetal = 'Alkali Metal',
  AlkalineEarthMetal = 'Alkaline Earth Metal',
  Metalloid = 'Metalloid',
  TransitionMetal = 'Transition Metal',
  Lanthanide = 'Lanthanide',
  Actinide = 'Actinide',
  PostTransitionMetal = 'Post-transition Metal',
  Halogen = 'Halogen',
}
```

### Color Mapping

```typescript
const COLORS = {
  'Nonmetal': '#90EE90',
  'Reactive Nonmetal': '#FFFF99',
  'Noble Gas': '#FFB6C1',
  'Alkali Metal': '#FFB347',
  'Alkaline Earth Metal': '#FFDAB9',
  'Metalloid': '#D3D3D3',
  'Transition Metal': '#87CEEB',
  'Lanthanide': '#DDA0DD',
  'Actinide': '#F0E68C',
  'Post-transition Metal': '#C0C0C0',
  'Halogen': '#FFCCFF',
};
```

---

## Integration Examples

### Example 1: Add New Frontend Action

```tsx
useCopilotAction({
  name: "highlightElementsByDensity",
  description: "Highlight elements within a density range",
  parameters: [
    { 
      name: "minDensity", 
      type: "number", 
      required: true 
    },
    { 
      name: "maxDensity", 
      type: "number", 
      required: true 
    },
  ],
  handler: ({ minDensity, maxDensity }: any) => {
    const filtered = PERIODIC_TABLE.filter(el => 
      el.density && el.density >= minDensity && el.density <= maxDensity
    );
    setState({
      ...state,
      selected_elements: filtered.map(el => el.symbol),
    });
  },
});
```

### Example 2: Add New Backend Tool

```python
@tool
def compare_elements(element1: str, element2: str) -> str:
    """Compare properties of two elements."""
    elements = {
        "H": {"name": "Hydrogen", "mass": 1.008},
        "O": {"name": "Oxygen", "mass": 15.999},
        # ... more elements
    }
    
    el1 = elements.get(element1, {})
    el2 = elements.get(element2, {})
    
    if not el1 or not el2:
        return json.dumps({"error": "Element not found"})
    
    return json.dumps({
        "element1": el1,
        "element2": el2,
        "mass_difference": abs(el1["mass"] - el2["mass"]),
    })

# Add to backend_tools list
backend_tools = [
    get_weather,
    select_elements_by_category,
    create_visualization,
    get_element_properties,
    compare_elements,  # Add this
]
```

### Example 3: Custom Visualization

```tsx
function CustomPropertyChart() {
  const [selectedProperty, setSelectedProperty] = useState('atomicMass');
  
  return (
    <div className="w-full h-96">
      <select 
        value={selectedProperty}
        onChange={(e) => setSelectedProperty(e.target.value)}
      >
        <option value="atomicMass">Atomic Mass</option>
        <option value="electronegativity">Electronegativity</option>
        <option value="density">Density</option>
      </select>
      
      <DataVisualization
        type="scatter"
        property={selectedProperty as any}
        selectedElements={PERIODIC_TABLE.slice(0, 20)}
      />
    </div>
  );
}
```

### Example 4: Three.js Customization

```tsx
// In PeriodicTable3D.tsx, customize element rendering:

PERIODIC_TABLE.forEach((element) => {
  // ... existing code ...
  
  const geometry = new THREE.BoxGeometry(1.3, 1.3, 1.3);
  
  // Customize size by atomic mass
  const scale = Math.log10(element.atomicMass) / 2;
  geometry.scale(scale, scale, scale);
  
  // Custom material effects
  const material = new THREE.MeshStandardMaterial({
    color: color,
    metalness: 0.7,
    roughness: 0.2,
  });
  
  // ... rest of the code ...
});
```

### Example 5: Add Element Data

```typescript
// In periodicTableData.ts, add new elements:

export const PERIODIC_TABLE: Element[] = [
  // ... existing elements ...
  
  // Add new element
  {
    atomicNumber: 37,
    symbol: 'Rb',
    name: 'Rubidium',
    atomicMass: 85.468,
    category: 'Alkali Metal',
    categoryColor: COLORS['Alkali Metal'],
    period: 5,
    group: 1,
    electronegativity: 0.82,
    ionizationEnergy: 4.18,
    atomicRadius: 248,
    density: 1.532,
    meltingPoint: 39.31,
    boilingPoint: 688,
    yearDiscovered: 1861,
    state: 'Solid'
  },
  // ... more elements ...
];
```

---

## API Endpoints

### CopilotKit Route
- **Path**: `/api/copilotkit`
- **Method**: POST
- **Purpose**: Handles CopilotKit requests

### LangGraph Agent
- **Port**: 8123
- **WebSocket**: ws://localhost:8123/run
- **REST**: http://localhost:8123/

---

## Error Handling

### Frontend Error Handling
```tsx
try {
  const element = elementSymbolMap[symbol];
  if (!element) throw new Error(`Element ${symbol} not found`);
  // Process element...
} catch (error) {
  console.error('Element lookup failed:', error);
  // Show user-friendly error
}
```

### Backend Error Handling
```python
@tool
def safe_element_lookup(symbol: str) -> str:
    """Safely lookup an element with error handling."""
    try:
        element = elements_map.get(symbol.upper())
        if not element:
            return json.dumps({"error": f"Element {symbol} not found"})
        return json.dumps(element)
    except Exception as e:
        return json.dumps({"error": str(e)})
```

---

## Performance Optimization Tips

1. **Memoize Element Lists**
   ```tsx
   const filteredElements = useMemo(() => 
     PERIODIC_TABLE.filter(el => el.category === selectedCategory),
     [selectedCategory]
   );
   ```

2. **Lazy Load Visualizations**
   ```tsx
   const DataVisualization = dynamic(
     () => import('@/components/DataVisualization'),
     { ssr: false }
   );
   ```

3. **Optimize Three.js Rendering**
   ```tsx
   renderer.shadowMap.enabled = true;
   renderer.shadowMap.type = THREE.PCFShadowShadowMap;
   ```

4. **Cache API Responses**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=128)
   def get_element_data(symbol: str):
       return elements_map.get(symbol)
   ```

---

## Testing

### Frontend Component Testing
```tsx
import { render, screen } from '@testing-library/react';
import { PeriodicTable3D } from '@/components/PeriodicTable3D';

describe('PeriodicTable3D', () => {
  it('renders without crashing', () => {
    render(<PeriodicTable3D />);
  });
});
```

### Backend Tool Testing
```python
def test_select_elements_by_category():
    result = select_elements_by_category("Transition Metal")
    data = json.loads(result)
    assert data["category"] == "Transition Metal"
    assert len(data["elements"]) > 0
```

---

## Deployment

### Production Build
```bash
npm run build
npm run start
```

### Environment Variables for Production
```env
OPENAI_API_KEY=sk_prod_...
NEXT_PUBLIC_COPILOT_KIT_PUBLIC_API_KEY=ck_prod_...
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=AIza...
NODE_ENV=production
```

---

## Troubleshooting API Issues

| Issue | Solution |
|-------|----------|
| Agent not responding | Check port 8123, restart with `npm run dev:agent` |
| Elements not loading | Verify periodicTableData.ts imports |
| Visualization not showing | Check Plotly script loading, browser console |
| 3D table not rendering | Ensure WebGL support, check Three.js version |

---

**Last Updated**: November 2025
**Version**: 1.0.0
