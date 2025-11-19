# 🧪 Interactive 3D Periodic Table with CopilotKit Integration

An advanced chemistry visualization tool featuring a fully interactive 3D periodic table of elements with AI-powered insights and data visualization capabilities.

## Features

### 🎯 Core Features
- **3D Periodic Table**: Fully rendered 3D periodic table using Three.js
- **Interactive Elements**: Click to view detailed element information
- **Real-time Visualization**: Dynamic data charts powered by Plotly
- **AI Assistant**: CopilotKit-powered chemistry assistant
- **Element Properties**: Complete atomic data including mass, electronegativity, ionization energy, and more

### 🤖 AI Capabilities
The integrated chemistry assistant can:
- Identify and filter elements by category (Transition Metals, Nonmetals, etc.)
- Generate visualizations (scatter plots, histograms, heatmaps)
- Compare element properties
- Provide detailed information about any element
- Help explore relationships between elements

### 📊 Data Visualization Tools
- **Scatter Plots**: Analyze element distributions
- **Histograms**: View property frequency distributions  
- **Heatmaps**: Compare multiple properties across elements
- **Properties**: Atomic Mass, Electronegativity, Ionization Energy, Density, and more

## Setup Instructions

### Prerequisites
- Node.js 18+
- npm or yarn
- OpenAI API key (for the assistant)

### Installation

1. **Install Dependencies**
```bash
npm install
```

This will automatically set up both the frontend and agent backend.

2. **Environment Setup**
Create a `.env.local` file in the project root:
```env
OPENAI_API_KEY=your_openai_key_here
NEXT_PUBLIC_COPILOT_KIT_PUBLIC_API_KEY=ck_pub_336d5ab8498da237aaccefc683ed17e7
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=AIzaSyDK7BXtZz4ypjq0yr-7FrrAcl3oCoPpxK8
```

### Running the Application

**Development Mode**:
```bash
npm run dev
```

This starts both:
- Next.js UI on `http://localhost:3000`
- LangGraph agent on `http://localhost:8123`

**Debug Mode** (with verbose logging):
```bash
npm run dev:debug
```

### Agent Development

The agent is built with LangGraph and supports:
- Tool-calling capabilities
- Multi-step reasoning
- State management for user interactions
- Backend tool execution (element analysis, visualization)

To view the agent graph:
```bash
cd agent && npm run dev
```

## Project Structure

```
├── src/
│   ├── app/
│   │   ├── page.tsx              # Main page with 3D table
│   │   ├── layout.tsx            # App layout
│   │   └── api/
│   │       └── copilotkit/       # CopilotKit API route
│   ├── components/
│   │   ├── PeriodicTable3D.tsx   # 3D visualization
│   │   ├── ElementCard.tsx       # Element details
│   │   └── DataVisualization.tsx # Chart rendering
│   └── lib/
│       └── periodicTableData.ts  # Element database
├── agent/
│   ├── agent.py                  # LangGraph workflow
│   └── requirements.txt          # Python dependencies
└── public/                       # Static assets
```

## Available AI Commands

### Element Exploration
- "Show me all transition metals"
- "What elements are halogens?"
- "Find noble gases"

### Data Analysis
- "Create a scatter plot of atomic mass"
- "Show me a histogram of ionization energy"
- "Compare density of different elements"

### Property Queries
- "What's the electronegativity of Carbon?"
- "Tell me about the element Iron"
- "Compare Hydrogen and Oxygen"

### Visualization
- "Make a chart of element density"
- "Show atomic radius distribution"
- "Visualize ionization energy trends"

## Technology Stack

### Frontend
- **Next.js 16** - React framework
- **TypeScript** - Type safety
- **Three.js** - 3D graphics
- **Plotly.js** - Data visualization
- **Tailwind CSS** - Styling
- **CopilotKit** - AI integration

### Backend
- **LangGraph** - Agent orchestration
- **LangChain** - LLM framework
- **OpenAI GPT-4o** - Language model
- **Python 3.10+** - Backend runtime

## API Keys Required

1. **OpenAI** - Get from https://platform.openai.com/api-keys
2. **CopilotKit** - Get from https://copilotkit.ai
3. **Google Maps** - Get from https://cloud.google.com/maps-platform (optional)

## Component Details

### PeriodicTable3D
- WebGL rendering using Three.js
- Mouse interaction for element selection
- Color-coded by element category
- Real-time rotation and hover effects
- Touch-friendly controls

### ElementCard
- Displays comprehensive element information
- Shows all available properties
- Color-coded category badge
- Clean, modern design
- Responsive layout

### DataVisualization
- Plotly-based interactive charts
- Multiple visualization modes
- Responsive sizing
- Dark theme support
- Hover tooltips and zoom

## Periodic Table Data

The application includes complete data for 36 elements (first 4 periods):
- Atomic number and mass
- Electron configuration group/period
- Category classification
- Physical properties (density, melting/boiling points)
- Chemical properties (electronegativity, ionization energy)
- Historical information (year discovered)
- Physical state

## Performance Optimization

- **Code Splitting**: Components loaded dynamically
- **SSR Disabled**: 3D rendering requires client-side execution
- **Memoization**: React useMemo for expensive computations
- **Lazy Loading**: Plotly loaded on-demand
- **Canvas Optimization**: WebGL memory management

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Kill process on port 8123
lsof -i :8123 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Missing Dependencies
```bash
npm install
npm run install:agent
```

### Agent Connection Issues
Ensure the agent is running on port 8123 and check firewall settings.

## Browser Support

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Future Enhancements

- [ ] Extended periodic table (all 118 elements)
- [ ] 3D molecular structure visualization
- [ ] Reaction prediction
- [ ] Temperature/pressure effects
- [ ] Isotope information
- [ ] Electron configuration visualization
- [ ] Chemical equation balancing
- [ ] Interactive experiment simulations

## Contributing

To add new features:
1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

MIT License - Feel free to use this project

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Check GitHub issues
4. Consult the documentation

---

**Happy Exploring! 🔬⚛️**
