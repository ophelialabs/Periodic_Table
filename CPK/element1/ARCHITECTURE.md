# 🏗️ Architecture & System Design

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE (React/Next.js)               │
│                                                                     │
│  ┌───────────────────────────────┐  ┌─────────────────────────┐    │
│  │  Periodic Table Component     │  │  CopilotSidebar         │    │
│  │  - Element Grid (18x8)        │  │  - Chat Interface       │    │
│  │  - Search & Filter            │  │  - AI Commands          │    │
│  │  - Visualization Modes        │  │  - Tool Calls Display   │    │
│  │  - Property Highlighting      │  │  - Real-time Updates    │    │
│  └───────────────────────────────┘  └─────────────────────────┘    │
│                                                                     │
│  Frontend Actions:                                                  │
│  • selectElement(atomicNumber)                                      │
│  • filterByCategory(category)                                       │
│  • changeVisualization(mode)                                        │
│  • highlightProperty(property)                                      │
│  • searchElement(query)                                             │
└─────────────────────────────────────────────────────────────────────┘
                              ↕️ HTTP (JSON)
┌─────────────────────────────────────────────────────────────────────┐
│                 CopilotKit Runtime API (Next.js)                    │
│                  POST /api/copilotkit                               │
│  - Handles requests/responses                                       │
│  - Manages runtime context                                          │
│  - Routes to agent service                                          │
└─────────────────────────────────────────────────────────────────────┘
                              ↕️ HTTP
┌─────────────────────────────────────────────────────────────────────┐
│              LangGraph Agent API (Python / Port 8123)               │
│                                                                     │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │ State Machine                                              │    │
│  │ ┌──────────┐        ┌──────────┐        ┌──────────┐      │    │
│  │ │ chat_node│ ----→ │tool_node │ ----→ │chat_node │      │    │
│  │ └──────────┘        └──────────┘        └──────────┘      │    │
│  │     ↓                    ↓                    ↓             │    │
│  │   Route               Execute             Response         │    │
│  │   Decision             Tools              Output           │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  Backend Tools:                                                     │
│  • analyze_periodic_properties(property, elements)                  │
│  • generate_trend_analysis(property1, property2)                    │
│  • create_visualization_data(type, property)                        │
│                                                                     │
│  Language Model: OpenAI GPT-4o                                      │
└─────────────────────────────────────────────────────────────────────┘
                              ↕️ Python Subprocess
┌─────────────────────────────────────────────────────────────────────┐
│            Data Science & Visualization Layer (Python)              │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │    NumPy     │  │    SciPy     │  │  Matplotlib  │              │
│  │              │  │              │  │              │              │
│  │ • Statistics │  │ • Correlation│  │ • Bar Charts │              │
│  │ • Analysis   │  │ • Pearson r  │  │ • Scatter    │              │
│  │              │  │ • P-values   │  │ • Boxplot    │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │    Pandas    │  │   Seaborn    │  │   Pillow     │              │
│  │              │  │              │  │              │              │
│  │ • DataFrames │  │ • Styling    │  │ • Encoding   │              │
│  │ • Filtering  │  │ • Colors     │  │ • Base64     │              │
│  │              │  │ • Themes     │  │              │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                     │
│  Output: Base64-encoded PNG images                                  │
└─────────────────────────────────────────────────────────────────────┘
                              ↕️ Files
┌─────────────────────────────────────────────────────────────────────┐
│                 Data Layer (In-Memory & Static)                     │
│                                                                     │
│  • periodicTableData.ts - Element properties                        │
│  • PERIODIC_TABLE array - 36 elements with properties               │
│  • Categories - 11 element classifications                          │
│  • Properties - 8 measurable attributes per element                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### 1. User Selects Element

```
User clicks element
        ↓
OnClick Handler
        ↓
setSelectedElement(element)
        ↓
setState() - Updates agent state
        ↓
Element details panel renders
        ↓
UI updates immediately
```

### 2. User Asks for Analysis

```
User types: "Create a bar chart of atomic masses"
        ↓
Message sent to CopilotKit Runtime
        ↓
Runtime routes to LangGraph Agent
        ↓
Agent receives message
        ↓
GPT-4o determines needed tools
        ↓
Route to tool_node
        ↓
Execute tools in parallel (if applicable):
    • analyze_periodic_properties("atomic_mass")
    • create_visualization_data("bar", "atomic_mass")
        ↓
Collect results
        ↓
Route back to chat_node
        ↓
Generate natural language response
        ↓
Send back to frontend with results
        ↓
Display in CopilotSidebar
```

### 3. AI Triggers Frontend Action

```
User: "Filter to show only transition metals"
        ↓
Agent determines action: filterByCategory
        ↓
Call: filterByCategory("Transition Metal")
        ↓
Frontend receives action
        ↓
Handler executes:
    setSelectedCategory("Transition Metal")
    setState({...state, selectedCategory})
        ↓
Component re-renders with filter applied
        ↓
Only transition metals displayed in grid
        ↓
Agent sees UI updated and responds
```

### 4. Property Analysis Flow

```
Tool Call: analyze_periodic_properties
        ↓
Extract parameter: "electronegativity"
        ↓
Filter PERIODIC_TABLE_DATA
        ↓
Extract all electronegativity values
        ↓
NumPy calculations:
    • np.mean()   - average
    • np.median() - middle value
    • np.std()    - spread
    • np.min()    - minimum
    • np.max()    - maximum
        ↓
Return JSON with statistics
```

### 5. Correlation Analysis Flow

```
Tool Call: generate_trend_analysis
        ↓
Extract parameters: "atomic_radius", "density"
        ↓
Collect paired data:
    For each element:
        Add (atomic_radius, density) to lists
        ↓
SciPy correlation:
    stats.pearsonr(data1, data2)
        ↓
Calculate:
    • Pearson r coefficient (-1 to 1)
    • P-value (significance)
        ↓
Return JSON with correlation results
```

### 6. Visualization Generation Flow

```
Tool Call: create_visualization_data
        ↓
Extract parameters: "bar", "atomic_mass"
        ↓
Setup Matplotlib figure:
    plt.subplots(figsize=(12, 6))
        ↓
Prepare data from PERIODIC_TABLE_DATA
        ↓
Create visualization:
    ├─ Bar chart: ax.bar()
    ├─ Scatter: ax.scatter()
    └─ Boxplot: ax.boxplot()
        ↓
Style with Seaborn theme
        ↓
Add labels and formatting
        ↓
Save to BytesIO buffer
        ↓
Encode to Base64
        ↓
Return JSON with image_base64
        ↓
Frontend displays PNG in sidebar
```

---

## Component Interaction Map

```
┌──────────────────┐
│   App (page)     │
└────────┬─────────┘
         │
         ├────────────────────┬─────────────────────┐
         ↓                    ↓                     ↓
    ┌─────────────────┐  ┌──────────────┐  ┌─────────────────┐
    │ PeriodicTable   │  │CopilotSidebar│  │  CopilotKit     │
    │    Viewer       │  │  Component   │  │  Provider       │
    └────────┬────────┘  └──────┬───────┘  └────────┬────────┘
             │                  │                   │
    ┌────────┴──────────────────┴───────────────────┴────────┐
    │                                                          │
    │  useCoAgent("sample_agent")                             │
    │    ↓                                                    │
    │  Agent State Management:                               │
    │    • selectedElement                                   │
    │    • selectedCategory                                  │
    │    • visualizationMode                                 │
    │    • highlightedProperty                               │
    │    • elementFilter                                     │
    │                                                          │
    ├───────────────────────────────────────────────────────┤
    │                                                          │
    │  useCopilotAction x 5:                                 │
    │    • selectElement → setState                          │
    │    • filterByCategory → setState                       │
    │    • changeVisualization → setState                    │
    │    • highlightProperty → setState                      │
    │    • searchElement → setState                          │
    │                                                          │
    └──────────────────────────────────────────────────────┘
```

---

## State Management

### Frontend Component State
```typescript
interface PeriodicTableState {
  selectedElement: Element | null           // Currently selected
  selectedCategory: string | null           // Filter by category
  visualizationMode: "table" | "trends"     // View mode
  highlightedProperty: string | null        // Color-by property
  elementFilter: string                     // Search query
}

// Managed by:
// 1. useCoAgent() - Shared with AI
// 2. useState() - Local state
// 3. useMemo() - Computed filtered list
```

### Agent State
```python
class AgentState(MessagesState):
    tools: List[Any]           # Available tools
    
# Messages from LangChain
# Inherits from MessagesState
```

---

## Tool Invocation Chain

```
User Message
    ↓
GPT-4o Model (with tools bound)
    ↓
Decision: Tool call needed?
    ├─ YES → route_to_tool_node()
    │    ↓
    │  ToolNode executes:
    │    ├─ analyze_periodic_properties()
    │    ├─ generate_trend_analysis()
    │    └─ create_visualization_data()
    │    ↓
    │  Return to chat_node
    │    ↓
    │  Generate response with results
    │
    └─ NO → route=END
         ↓
       Return response directly
```

---

## Frontend Action Handler Pattern

```typescript
useCopilotAction({
  name: "actionName",
  description: "Human-readable description",
  parameters: [
    {
      name: "paramName",
      type: "string",
      description: "Parameter description",
      required: true,
    }
  ],
  handler: ({ paramName }) => {
    // Update local state
    setLocalState(newValue);
    
    // Update agent state
    setState({
      ...state,
      fieldName: newValue,
    });
  },
});
```

All 5 actions follow this pattern.

---

## API Response Pattern

### Tool Output Format
```json
{
  "success": true/false,
  "data": {
    "property": "value",
    "statistics": {...},
    "elements": {...}
  },
  "message": "Human-readable summary"
}
```

### Visualization Output Format
```json
{
  "success": true,
  "visualization_type": "bar",
  "property": "atomic_mass",
  "image_base64": "iVBORw0KGgoAAAANS...",
  "message": "Generated bar visualization"
}
```

---

## Error Handling Strategy

```
Try Block
    ↓
Execute tool logic
    ↓
Catch exception
    ↓
Return JSON error:
{
  "error": "Description of what went wrong",
  "context": "Additional context"
}
    ↓
Agent receives error
    ↓
GPT-4o generates user-friendly response
    ↓
Display in sidebar
```

---

## Performance Considerations

### Frontend Optimization
- ✅ Memoized filtered elements list
- ✅ CSS transitions (GPU-accelerated)
- ✅ Event delegation on grid
- ✅ No unnecessary re-renders

### Backend Optimization
- ✅ In-memory data (fast access)
- ✅ Vectorized NumPy operations
- ✅ SciPy built-in efficiency
- ✅ Matplotlib caching enabled

### Network Optimization
- ✅ Base64 encoding (no extra requests)
- ✅ Minimal JSON payloads
- ✅ Tool-specific routing (no unused calls)

---

## Security Layers

```
┌─ User Input Validation
│
├─ Frontend
│  └─ React component prop validation
│  └─ TypeScript type safety
│
├─ API
│  └─ Next.js API route validation
│  └─ CopilotKit runtime protection
│
├─ Agent
│  └─ Tool parameter validation
│  └─ Type hints and checks
│
└─ Execution
   └─ Sandboxed tool execution
   └─ No file system access
```

---

**This architecture ensures:**
- ✅ Real-time responsiveness
- ✅ Scalable AI capabilities
- ✅ Professional visualizations
- ✅ Robust error handling
- ✅ Extensible design
