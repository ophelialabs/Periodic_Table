# Quick Start Guide

## 🚀 5-Minute Setup

### 1. Install Dependencies (1 min)
```bash
cd /Users/jesse/periodic-table
pnpm install
```

### 2. Set Environment Variables (1 min)
```bash
# Create .env.local file in project root
echo "OPENAI_API_KEY=your-api-key-here" > .env.local
```

### 3. Start Development Servers (1 min)
```bash
pnpm dev
```

This starts:
- 🎨 **Frontend**: http://localhost:3000
- 🤖 **Agent Server**: http://localhost:8123

### 4. Open Application (1 min)
- Visit http://localhost:3000 in your browser
- Click any element to visualize its electron orbital
- Chat with the quantum research assistant in the sidebar

### 5. Try Examples (1 min)

**In the Chat Sidebar:**
- "Tell me about Hydrogen"
- "Simulate the electron cloud for Gold"
- "What's the ionization energy of Carbon?"
- "Research element properties for Iron"
- "Set the theme to blue"

---

## 📋 Troubleshooting

### Issue: "Port 3000 already in use"
```bash
# Kill existing process
lsof -ti:3000 | xargs kill -9
# Or use different port
PORT=3001 pnpm dev:ui
```

### Issue: "OPENAI_API_KEY not set"
```bash
# Verify .env.local exists and has the key
cat .env.local

# Or set inline:
OPENAI_API_KEY=sk-... pnpm dev
```

### Issue: "Agent not responding"
```bash
# Check agent server is running
curl http://localhost:8123

# Restart agent only:
pnpm dev:agent
```

### Issue: "Visualizations not showing"
1. Check browser console for errors (F12)
2. Ensure JavaScript is enabled
3. Try refreshing the page
4. Clear browser cache

---

## 🎯 Interactive Features to Try

### Element Exploration
1. **Search**: Type element names or symbols in the search box
2. **Select**: Click any element card
3. **Visualize**: Watch 3D orbital render
4. **Compare**: Select multiple elements to compare properties

### Chat with Agent
- **Ask about elements**: "What is the atomic structure of Carbon?"
- **Request simulations**: "Generate a 3D orbital for Oxygen"
- **Research topics**: "What are the applications of Gold in nanotechnology?"
- **Get math**: "Calculate the ground state energy for Iron"
- **Customize UI**: "Change theme to purple"

### View Quantum Data
- **Orbital radius**: Shown in Angstroms (Å)
- **Ground state energy**: Displayed in eV
- **Peak probability**: Shows electron density concentration
- **Bohr model shells**: Dashed circles show classical orbits

---

## 📚 Key Concepts

### Elements Included
- **H** (Hydrogen) - Simplest atom
- **He** (Helium) - Noble gas
- **C** (Carbon) - Organic chemistry
- **O** (Oxygen) - Life essential
- **Fe** (Iron) - Transition metal
- **Au** (Gold) - Precious metal

### Physics Models
- **Bohr Model**: Orbital shells and radii
- **Rydberg Formula**: Ground state energy calculation
- **Hydrogen Wavefunctions**: Probability distributions

### Quantum Concepts
- **Electron Cloud**: Probability density visualization
- **Quantum Numbers**: n, l, ml, ms definitions
- **Ground State**: Lowest energy orbital (1s)
- **Ionization Energy**: Energy to remove electron

---

## 🔧 Development Workflow

### Run Frontend Only
```bash
pnpm dev:ui
# Access: http://localhost:3000
```

### Run Agent Only
```bash
pnpm dev:agent
# Access: http://localhost:8123
```

### Development Mode
```bash
# Enable debug logging
LOG_LEVEL=debug pnpm dev
```

### Build for Production
```bash
pnpm build
pnpm start
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `src/app/page.tsx` | Main page & UI layout |
| `src/components/PeriodicTable3D.tsx` | Interactive periodic table |
| `src/lib/elements.ts` | Element data & calculations |
| `src/lib/quantumHost.ts` | Quantum simulation manager |
| `src/app/api/quantum/route.ts` | API endpoint for simulations |
| `src/quantum/QuantumRD.qs` | Q# quantum operations |
| `agent/agent.py` | LangGraph research agent |

---

## 🔗 Useful Links

- **Documentation**: See `RESEARCH_AGENT_README.md`
- **Q# Guide**: See `Q_SHARP_INTEGRATION.md`
- **Implementation**: See `IMPLEMENTATION_SUMMARY.md`
- **CopilotKit Docs**: https://copilotkit.ai
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **Q# Docs**: https://learn.microsoft.com/en-us/azure/quantum/

---

## 💡 Tips & Tricks

### Faster Development
- Use `pnpm` instead of `npm` (faster)
- Enable HMR in browser for live updates
- Use VS Code for excellent TypeScript support

### Better Visualizations
- Try elements with different atomic numbers
- Notice how orbital size changes with Z
- Observe energy level differences

### Advanced Exploration
- Examine Q# code in `src/quantum/QuantumRD.qs`
- Study element data in `src/lib/elements.ts`
- Review agent tools in `agent/agent.py`

### Extend the System
1. Add more elements to `PERIODIC_TABLE` array
2. Create new Q# operations
3. Add agent tools for custom analysis
4. Design custom UI components

---

## 📞 Getting Help

1. **Check logs**: `LOG_LEVEL=debug pnpm dev`
2. **Review docs**: See README files in project root
3. **Check endpoints**: Verify servers running with `curl`
4. **Browser console**: Check for JavaScript errors (F12)
5. **Terminal output**: Look for error messages

---

## ✅ Verification Checklist

Before considering setup complete:

- [ ] `pnpm install` completed successfully
- [ ] `.env.local` file created with API key
- [ ] `pnpm dev` started both servers
- [ ] Frontend loads at http://localhost:3000
- [ ] Agent server responds at http://localhost:8123
- [ ] Can click element and see visualization
- [ ] Can type in chat sidebar
- [ ] Page doesn't show errors in console

---

## 🎉 Next Steps

Once setup is complete:

1. **Explore Elements**: Click different elements and observe orbital patterns
2. **Chat with Agent**: Ask questions about element properties
3. **Run Simulations**: Request quantum orbital visualizations
4. **Read Documentation**: Deep dive into how everything works
5. **Extend System**: Add features or new elements
6. **Deploy**: Prepare for production deployment

---

## 📝 Notes

- First load may take a moment for all systems to initialize
- Agent responses use OpenAI GPT-4 (requires API calls)
- Quantum simulations use mock data by default
- Azure Quantum integration available for production
- System designed for educational and research use

**Enjoy exploring quantum mechanics! 🔬✨**
