# 🧪 Interactive Periodic Table of Elements with CopilotKit

An interactive, AI-powered periodic table of elements integrated with CopilotKit and advanced data visualization capabilities.

## ✨ Features

### 🎨 Interactive UI
- **Beautiful Periodic Table Grid**: Color-coded by element category with hover effects
- **Real-time Element Selection**: Click any element to view detailed properties
- **Multiple Visualization Modes**: 
  - Table view with grid layout
  - Trends view with comparative analysis
  - Properties view with detailed cards
  - 3D visualization ready (via AI)

### 🤖 AI-Powered Assistant
- Integrated CopilotKit with GPT-4o for intelligent responses
- **Data Analysis Tools**:
  - `analyze_periodic_properties` - Statistical analysis of element properties
  - `generate_trend_analysis` - Correlation analysis using SciPy
  - `create_visualization_data` - Chart generation with Matplotlib & Seaborn

### 📊 Advanced Visualizations
- **Matplotlib**: Professional charts and graphs
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **SciPy**: Statistical analysis and correlations
- **Seaborn**: Statistical data visualization

### 🎯 Frontend Actions (AI-Controlled UI)
- `selectElement` - Select an element by atomic number
- `filterByCategory` - Filter elements by category
- `changeVisualization` - Switch between visualization modes
- `highlightProperty` - Highlight specific elemental properties
- `searchElement` - Search elements by name or symbol

### 🔍 Interactive Controls
- **Category Filter**: Filter elements by type (Metal, Nonmetal, etc.)
- **Search**: Find elements by name or symbol
- **Property Highlighting**: Color elements based on selected property values
- **Category Legend**: Visual reference for element categories

## 🛠️ Technology Stack

### Frontend
- **Next.js 16** - React framework
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **CopilotKit** - AI integration framework

### Backend
- **Python/LangGraph** - Agentic workflows
- **OpenAI GPT-4o** - Language model
- **FastAPI** - API server
- **UVicorn** - ASGI server

### Data Science & Visualization
- **Matplotlib** - Static visualizations
- **Seaborn** - Statistical graphics
- **Pandas** - Data analysis
- **NumPy** - Numerical computing
- **SciPy** - Scientific computing

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- npm or yarn

### Installation

1. **Install Dependencies**
```bash
npm install
```

This will automatically install both frontend and backend dependencies via the postinstall script.

2. **Environment Setup**
Create a `.env.local` file in the root directory:
```env
LANGSMITH_API_KEY=your_langsmith_key
```

### Running the Application

**Development Mode** (UI + Agent):
```bash
npm run dev
```

This runs both the Next.js frontend and the LangGraph agent in parallel:
- Frontend: `http://localhost:3000`
- Agent API: `http://localhost:8123`

**Debug Mode** (with logging):
```bash
npm run dev:debug
```

**UI Only**:
```bash
npm run dev:ui
```

**Agent Only**:
```bash
npm run dev:agent
```

## 📖 Usage Guide

### 1. **Exploring the Periodic Table**
- Click any element to view its detailed properties
- Use the category filter to focus on specific element types
- Search for elements by name (e.g., "Gold") or symbol (e.g., "Au")

### 2. **Analyzing Element Properties**
Try these AI prompts:
- "Compare the atomic masses of transition metals"
- "Show me elements with electronegativity above 3"
- "What's the correlation between atomic radius and density?"
- "Analyze melting points for Period 3 elements"

### 3. **Generating Visualizations**
Ask the AI:
- "Create a bar chart of atomic masses"
- "Generate a scatter plot of ionization energy vs atomic number"
- "Show the distribution of melting points by period"
- "Create a 3D visualization of atomic radius trends"

### 4. **Data Analysis**
The AI can:
- Calculate statistical measures (mean, median, std dev)
- Find correlations between properties using SciPy
- Identify trends across periods and groups
- Generate professional visualizations

## 🧬 API Endpoints

### CopilotKit Runtime
- `POST /api/copilotkit` - Main runtime endpoint

### LangGraph Agent
- Default deployment: `http://localhost:8123`
- Graph ID: `sample_agent`

## 📊 Available Properties for Analysis

- `atomic_mass` - Mass of the atom
- `electronegativity` - Ability to attract electrons
- `ionization_energy` - Energy to remove an electron
- `atomic_radius` - Size of the atom
- `density` - Mass per unit volume
- `melting_point` - Temperature at which solid becomes liquid
- `boiling_point` - Temperature at which liquid becomes gas

## 🔧 Architecture

### Frontend Flow
1. User interacts with periodic table component
2. Frontend actions triggered by user or AI
3. UI state updates in real-time
4. CopilotKit sidebar manages AI conversations

### Backend Flow
1. User message sent to agent
2. Agent determines needed tools
3. Data analysis tools executed (numpy, pandas, scipy)
4. Visualizations generated (matplotlib, seaborn)
5. Results returned to frontend

## 📚 Project Structure

```
.
├── src/
│   ├── app/
│   │   ├── api/copilotkit/route.ts      # API endpoint
│   │   ├── layout.tsx                    # Root layout with CopilotKit
│   │   ├── page.tsx                      # Main page
│   │   └── globals.css                   # Global styles
│   ├── components/
│   │   └── PeriodicTableViewer.tsx       # Main periodic table component
│   └── lib/
│       └── periodicTableData.ts          # Element data
├── agent/
│   ├── agent.py                          # LangGraph agent definition
│   ├── langgraph.json                    # Agent configuration
│   └── requirements.txt                  # Python dependencies
├── package.json                          # npm dependencies
└── tsconfig.json                         # TypeScript configuration
```

## 🎓 Learning Resources

### CopilotKit Documentation
- https://docs.copilotkit.ai/

### Data Science Libraries
- **NumPy**: https://numpy.org/doc/
- **Pandas**: https://pandas.pydata.org/docs/
- **Matplotlib**: https://matplotlib.org/stable/
- **SciPy**: https://docs.scipy.org/doc/scipy/
- **Seaborn**: https://seaborn.pydata.org/

### LangGraph
- https://langchain-ai.github.io/langgraph/

## 🤝 Contributing

Feel free to enhance the application by:
1. Adding more elements to the periodic table
2. Creating new analysis tools
3. Implementing new visualization types
4. Adding more AI capabilities

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Periodic table data sourced from scientific databases
- Built with CopilotKit for AI integration
- Powered by OpenAI's GPT-4o
- Visualization by Matplotlib and Seaborn communities

---

**Built with ❤️ for chemistry and AI enthusiasts**
