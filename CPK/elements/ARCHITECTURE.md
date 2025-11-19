# System Architecture & Data Flow

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER INTERFACE (Next.js)                    │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  │    3D Periodic   │  │   Element Card   │  │ Data Visualization
│  │     Table        │  │   Component      │  │   (Plotly)
│  │  (Three.js)      │  └──────────────────┘  └──────────────────┘
│  └──────────────────┘
│         ↑                      ↑                        ↑
│         └──────────────────────┼────────────────────────┘
│                                │
│                      ┌─────────▼─────────┐
│                      │  React State      │
│                      │  Management       │
│                      └─────────┬─────────┘
│                                │
└────────────────────────────────┼──────────────────────────────────┘
                                 │
                    ┌────────────▼───────────┐
                    │  CopilotKit Sidebar    │
                    │  (AI Assistant)        │
                    └────────────┬───────────┘
                                 │
                    ┌────────────▼───────────────────┐
                    │   Frontend Actions             │
                    │  - setThemeColor               │
                    │  - selectElementsByCategory    │
                    │  - updateVisualization         │
                    │  - showElementDetails          │
                    └────────────┬───────────────────┘
                                 │
                    ┌────────────▼───────────────────┐
                    │  /api/copilotkit Endpoint      │
                    │  (HTTP/WebSocket)              │
                    └────────────┬───────────────────┘
                                 │
┌────────────────────────────────▼──────────────────────────────────┐
│                   BACKEND (LangGraph Agent)                        │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    ChatNode (GPT-4o)                         │ │
│  │  • Analyzes user queries                                     │ │
│  │  • Routes to appropriate tools                               │ │
│  │  • Generates responses                                       │ │
│  └───────────────┬────────────────────────────────────────────┬─┘ │
│                  │                                            │    │
│  ┌───────────────▼────────────────┐  ┌────────────────────────▼──┐ │
│  │      Backend Tools             │  │   Tool Node               │ │
│  │  1. get_weather()              │  │   • Executes tools        │ │
│  │  2. select_elements_by_        │  │   • Returns results       │ │
│  │     category()                 │  │   • Routes back to chat   │ │
│  │  3. create_visualization()     │  │                           │ │
│  │  4. get_element_properties()   │  │                           │ │
│  └────────────────────────────────┘  └───────────────────────────┘ │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              Agent State (MessagesState)                      │  │
│  │  • messages: List[BaseMessage]                               │  │
│  │  • proverbs: List[str]                                       │  │
│  │  • selected_elements: List[str]                              │  │
│  │  • visualization_type: str                                   │  │
│  │  • visualization_property: str                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
                                 │
                    ┌────────────▼───────────┐
                    │   Response Message     │
                    │   (JSON)               │
                    └────────────┬───────────┘
                                 │
                    ┌────────────▼───────────┐
                    │   Streaming to UI      │
                    │   (WebSocket)          │
                    └────────────┬───────────┘
                                 │
┌────────────────────────────────▼──────────────────────────────────┐
│                      STATE UPDATE & RE-RENDER                      │
│  • Update React state with visualization type                     │
│  • Update selected elements list                                  │
│  • Trigger component re-renders                                  │
│  • Update visualization with new data                            │
└──────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

```
CopilotKitPage
├── State: themeColor
├── Actions: setThemeColor
└── YourMainContent
    ├── State: AgentState
    │   ├── selected_elements
    │   ├── visualization_type
    │   ├── visualization_property
    │   └── proverbs
    ├── Local State:
    │   ├── selectedElement
    │   └── showVisualization
    └── Children:
        ├── PeriodicTable3D
        │   ├── Three.js Scene
        │   ├── Raycaster
        │   └── Event Handlers
        │       ├── onMouseMove (hover)
        │       └── onClick (select)
        ├── ElementCard
        │   ├── Element properties
        │   └── Category badge
        └── RightPanel
            ├── Header
            ├── Legend (color codes)
            ├── SelectedElement Display
            ├── Visualization Status
            └── Instructions
```

---

## Data Flow Sequence

### User Clicks Element in 3D Table

```
1. PeriodicTable3D Component
   └─> Mouse Click Event
       └─> Raycaster Detection
           └─> Element Identified
               └─> userData.element retrieved

2. onElementClick Handler
   └─> setSelectedElement(element)
       └─> Local State Update

3. Component Re-render
   └─> ElementCard becomes visible
   └─> Right panel updates
   └─> PeriodicTable3D highlights selected
```

### User Asks AI to Visualize Data

```
1. User Input in Sidebar
   └─> CopilotKit sends to agent

2. ChatNode processes query
   └─> Detects visualization request
   └─> Calls create_visualization tool
       ├─> Tool: type = "scatter"
       ├─> Tool: property = "atomicMass"
       └─> Tool: elements = "all"

3. Tool Node executes
   └─> Returns visualization config

4. Response sent back to frontend
   └─> updateVisualization action triggered

5. Frontend Action Handler
   └─> setState({
       visualization_type: "scatter",
       visualization_property: "atomicMass"
   })

6. Component Re-renders
   └─> showVisualization = true
   └─> DataVisualization loads
   └─> Plotly renders chart
```

### User Asks for Element Information

```
1. User Query
   └─> "Tell me about Iron"

2. Agent Analysis
   └─> Extracts: element_symbol = "Fe"
   └─> Calls get_element_properties("Fe")

3. Backend Tool
   └─> Looks up element data
   └─> Returns properties

4. Agent Response
   └─> Formats data for display
   └─> Sends showElementDetails action

5. Frontend Renders
   └─> ElementCard displays with data
```

---

## Three.js Scene Graph

```
Scene
├── Lighting
│   ├── AmbientLight (0xffffff, 0.6)
│   └── DirectionalLight (0xffffff, 0.8)
│       ├── CastShadow: true
│       └── ShadowMap: 2048x2048
├── Camera
│   ├── FOV: 75
│   ├── Position: (15, 10, 15)
│   └── LookAt: (8, 3, 0)
└── Objects (36 Element Cubes)
    ├── Cube 1 (Hydrogen)
    │   ├── Geometry: BoxGeometry(1.3, 1.3, 1.3)
    │   ├── Material: MeshPhongMaterial
    │   │   ├── color: #90EE90 (Nonmetal)
    │   │   ├── emissive: 0x000000
    │   │   └── shininess: 100
    │   ├── Position: (0, 6, 0) [Period 1, Group 1]
    │   ├── CastShadow: true
    │   └── userData: {element: Element, originalColor: Color}
    ├── Cube 2 (Helium)
    │   ├── Position: (1.5, 6, 0) [Period 1, Group 18]
    │   └── ...
    └── ... [34 more element cubes]
```

---

## Data Structure Relationships

```
┌─────────────────────────────────────┐
│          PERIODIC_TABLE: Element[]   │
├─────────────────────────────────────┤
│ [                                    │
│   {                                  │
│     atomicNumber: 1                  │
│     symbol: "H"                      │
│     name: "Hydrogen"                 │
│     ├─ Basic: atomicMass, period     │
│     ├─ Chemical: electronegativity   │
│     ├─ Physical: density, state      │
│     ├─ Thermal: meltingPoint, etc.   │
│     └─ Historical: yearDiscovered    │
│   },                                 │
│   ... 35 more elements ...           │
│ ]                                    │
└─────────────────────────────────────┘
        │
        ├─→ elementSymbolMap (Index)
        │   K: "H" → V: Element
        │
        ├─→ CategoryColor Map
        │   K: "Nonmetal" → V: "#90EE90"
        │
        └─→ Utility Functions
            ├─ getElementByAtomicNumber()
            ├─ getElementsByCategory()
            └─ getCategories()
```

---

## State Synchronization

### Frontend State ↔ Agent State

```
Frontend AgentState
├── selected_elements: string[]
│   ↓ (via backend tool)
Agent State selected_elements
│   ↓ (via response)
Frontend AgentState
├── visualization_type: string
│   ↓ (via handler)
updateVisualization Action
│   ↓
Frontend AgentState updated
├── visualization_property: string
│   ↓
Component Re-render Triggered
```

---

## Tool Execution Pipeline

```
User Query
    │
    ├─→ [Agent Analysis]
    │   └─→ Tool Identified
    │       └─→ Tool Called
    │
    ├─→ [Parameter Binding]
    │   ├─ category: "Transition Metal"
    │   └─ property: "atomicMass"
    │
    ├─→ [Tool Execution]
    │   ├─ Backend Processing
    │   └─ Result Generation
    │
    ├─→ [Response Formatting]
    │   └─→ JSON Result
    │
    ├─→ [Agent Processing]
    │   ├─ Analyze result
    │   └─ Generate response
    │
    └─→ [Frontend Action]
        └─→ Update UI State
            └─→ Re-render Components
```

---

## Event Flow Diagram

```
User Interaction
    │
    ├─→ Click on Element
    │   └─→ PeriodicTable3D
    │       ├─ Raycaster detects
    │       └─ onElementClick fired
    │           └─ setSelectedElement()
    │               └─ State Update
    │                   └─ Re-render
    │
    ├─→ Type Message
    │   └─→ CopilotKit Sidebar
    │       ├─ Message sent to agent
    │       └─ Agent processes
    │           ├─ Tool identified
    │           └─ Tool executed
    │               └─ Frontend action called
    │                   └─ UI updated
    │
    └─→ Hover on Element
        └─→ PeriodicTable3D
            ├─ Raycaster detects
            └─ onMouseMove fired
                └─ setHoveredElement()
                    └─ Tooltip displayed
```

---

## API Contract

### Frontend → Agent

```json
{
  "type": "query",
  "message": "Show me all transition metals",
  "actions": {
    "selectElementsByCategory": {
      "category": "Transition Metal"
    }
  }
}
```

### Agent → Frontend

```json
{
  "type": "response",
  "content": "Here are all transition metals...",
  "actions": [
    {
      "name": "updateVisualization",
      "args": {
        "type": "scatter",
        "property": "atomicMass",
        "elements": ["Sc", "Ti", "V", ...]
      }
    }
  ]
}
```

---

## Memory Management

### Three.js Resources
```
Scene Memory Allocation
├── Geometries: 36 BoxGeometry (shared)
├── Materials: 10+ MeshPhongMaterial
├── Meshes: 36 Mesh objects
├── Textures: 0 (color-based)
└── Total: ~50-100 MB
```

### React Components
```
Component Tree Memory
├── Page Component: ~1 KB
├── YourMainContent: ~5 KB
├── PeriodicTable3D: ~2 MB (WebGL context)
├── ElementCard: ~1 KB
├── DataVisualization: ~1 MB (Plotly)
└── Total: ~3-4 MB
```

---

## Performance Optimization Strategies

```
┌──────────────────────────────────────────────────┐
│          Performance Optimization               │
├──────────────────────────────────────────────────┤
│ 1. Code Splitting                               │
│    └─→ Dynamic imports for DataVisualization    │
│                                                  │
│ 2. Memoization                                  │
│    └─→ useMemo for expensive computations       │
│                                                  │
│ 3. Lazy Loading                                 │
│    └─→ Plotly loaded on-demand                  │
│                                                  │
│ 4. Geometry Caching                             │
│    └─→ Shared BoxGeometry for elements          │
│                                                  │
│ 5. Event Debouncing                             │
│    └─→ Throttle mouse move events               │
│                                                  │
│ 6. State Optimization                           │
│    └─→ Only update changed elements             │
└──────────────────────────────────────────────────┘
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│          Production Deployment           │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────────────────────┐  │
│  │     Vercel/Production Host       │  │
│  │  ├─ Next.js Build (optimized)    │  │
│  │  ├─ Static Files CDN             │  │
│  │  └─ Environment Variables        │  │
│  │      ├─ OPENAI_API_KEY (secret)  │  │
│  │      └─ PUBLIC_KEYS              │  │
│  └───────────────┬────────────────────┘  │
│                  │                       │
│  ┌───────────────▼────────────────────┐  │
│  │     LangGraph Agent Server         │  │
│  │  ├─ Python Runtime                │  │
│  │  ├─ OpenAI API Client             │  │
│  │  └─ Tool Execution Engine         │  │
│  └────────────────────────────────────┘  │
│                                         │
│  ┌────────────────────────────────────┐ │
│  │      External APIs                 │ │
│  │  ├─ OpenAI (GPT-4o)               │ │
│  │  ├─ CopilotKit Backend            │ │
│  │  └─ Google Maps (optional)        │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

**Architecture Version**: 1.0.0
**Last Updated**: November 2025
