# 🔧 Setup & Troubleshooting Guide

## 🚀 Complete Setup Instructions

### Step 1: Prerequisites Check

```bash
# Check Node.js version (need 18+)
node --version

# Check npm version
npm --version

# Check Python version (need 3.9+)
python3 --version
```

**If any are missing:**
- **Node.js**: Download from https://nodejs.org/
- **Python**: Download from https://www.python.org/

---

### Step 2: Navigate to Project

```bash
cd /Users/jesse/Desktop/Company/Tools/PeriodicTable/CPK/element1
```

---

### Step 3: Install Frontend Dependencies

```bash
npm install
```

**What this does:**
- Installs Next.js, React, TypeScript
- Installs CopilotKit packages
- Installs Tailwind CSS
- Triggers postinstall script for agent setup

**Time: ~2-3 minutes** (first time)

---

### Step 4: Verify Python Environment

```bash
# Create virtual environment (optional but recommended)
python3 -m venv agent_env

# Activate virtual environment
# macOS/Linux:
source agent_env/bin/activate
# Windows:
# agent_env\Scripts\activate

# Install Python dependencies
cd agent
pip install -r requirements.txt
cd ..
```

**What this installs:**
- LangChain & LangGraph
- OpenAI client
- FastAPI & UVicorn
- Data science: NumPy, Pandas, Matplotlib, SciPy, Seaborn

**Time: ~1-2 minutes**

---

### Step 5: Set Environment Variables

Create `.env.local` file in project root:

```bash
# For development (optional)
LANGSMITH_API_KEY=your_key_here_optional

# Already configured in code:
# - LANGGRAPH_DEPLOYMENT_URL=http://localhost:8123
# - CopilotKit public API key in layout.tsx
```

---

### Step 6: Start the Application

**Option A: Unified Start (Recommended)**
```bash
npm run dev
```
This runs both frontend and agent together.

**Option B: Separate Terminals**

Terminal 1 (Frontend):
```bash
npm run dev:ui
```

Terminal 2 (Agent):
```bash
npm run dev:agent
```

**Option C: Debug Mode**
```bash
npm run dev:debug
```
Adds verbose logging.

---

### Step 7: Access the Application

Once running:

1. **Open your browser**: `http://localhost:3000`
2. **You should see**:
   - Interactive periodic table grid
   - Category filter dropdown
   - Search input field
   - CopilotKit sidebar on the right

3. **Click an element** → Details panel shows
4. **Type in sidebar** → Chat with AI

---

## ✅ Verification Checklist

After starting `npm run dev`:

- [ ] Next.js dev server started (port 3000)
- [ ] LangGraph agent started (port 8123)
- [ ] Browser loads `http://localhost:3000`
- [ ] Periodic table displays
- [ ] CopilotKit sidebar visible
- [ ] Can click elements
- [ ] Can type in chat sidebar
- [ ] No errors in terminal

---

## 🐛 Troubleshooting

### Problem: "npm: command not found"

**Solution:**
- Install Node.js from https://nodejs.org/
- Add to PATH if necessary
- Restart terminal

```bash
# Verify installation
node --version
npm --version
```

---

### Problem: "command not found: python3"

**Solution:**
- Install Python from https://www.python.org/
- Or use `python` instead of `python3`
- Make sure it's Python 3.9+

```bash
# Check Python
python3 --version
# or
python --version
```

---

### Problem: "Port 3000 is already in use"

**Solution 1: Stop other process**
```bash
# macOS/Linux
lsof -i :3000
kill -9 <PID>

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**Solution 2: Use different port**
```bash
npm run dev:ui -- -p 3001
```

Then access: `http://localhost:3001`

---

### Problem: "Port 8123 is already in use"

**Solution 1: Stop other process**
```bash
lsof -i :8123
kill -9 <PID>
```

**Solution 2: Change agent port**

Edit `agent/langgraph.json`:
```json
{
  "dev": {
    "graph_dir": ".",
    "port": 8124,  // Change this to 8124
    "no_browser": true
  }
}
```

Then update `src/app/api/copilotkit/route.ts`:
```typescript
deploymentUrl: "http://localhost:8124"
```

---

### Problem: "Module not found" errors

**Solution:**
```bash
# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# For Python issues
cd agent
pip install --upgrade -r requirements.txt
cd ..
```

---

### Problem: "TypeError: Cannot find module '@copilotkit/react-core'"

**Solution:**
```bash
npm install @copilotkit/react-core @copilotkit/react-ui @copilotkit/runtime
```

---

### Problem: "Python ModuleNotFoundError: No module named 'matplotlib'"

**Solution:**
```bash
cd agent
pip install matplotlib pandas numpy scipy seaborn pillow
cd ..
```

Or reinstall all:
```bash
cd agent
pip install -r requirements.txt
cd ..
```

---

### Problem: "CORS Error" when accessing agent

**Solution:**
Make sure agent is running:
```bash
# Check if port 8123 is listening
lsof -i :8123

# Or start agent in separate terminal
npm run dev:agent
```

---

### Problem: "CopilotKit sidebar not showing"

**Solution:**
1. Check browser console (F12) for errors
2. Verify API key in `layout.tsx`
3. Clear browser cache: Cmd+Shift+Del
4. Try incognito window

---

### Problem: "npm ERR! peer dep missing"

**Solution:**
```bash
# Install specific versions
npm install --save-exact next@16.0.1 react@19.2.0 typescript@5
```

---

### Problem: "Agent times out or doesn't respond"

**Solution:**
1. Check if agent is running: `npm run dev:agent`
2. Verify OpenAI API key is set
3. Check network connectivity
4. Try simpler queries first
5. Restart agent: Stop and `npm run dev:agent`

---

## 🔍 Debugging Tips

### View Terminal Logs

**Frontend (Next.js):**
- Shows compilation info
- React errors and warnings
- Network requests

**Agent (LangGraph):**
- Shows tool execution
- Model API calls
- Routing decisions

### Enable Debug Logging

```bash
# Run with debug mode
npm run dev:debug

# Or set log level
LOG_LEVEL=debug npm run dev
```

### Check Specific Services

```bash
# Is frontend running?
curl http://localhost:3000

# Is agent API running?
curl http://localhost:8123

# Check API response
curl -X POST http://localhost:3000/api/copilotkit \
  -H "Content-Type: application/json"
```

---

## 🧪 Test the Application

### Manual Testing Flow

1. **Open app**: `http://localhost:3000`

2. **Test Periodic Table**:
   - Click element → Details should show
   - Filter by category → Grid updates
   - Search for element → Grid filters
   - Highlight property → Colors change

3. **Test AI Integration**:
   - Type in sidebar
   - Try: "Select Gold"
   - Try: "Show all halogens"
   - Try: "Create a bar chart"

4. **Test Data Tools**:
   - Try: "Compare atomic masses"
   - Try: "Find correlation between atomic radius and density"
   - Check for visualizations in sidebar

---

## 📋 Development Workflow

### Running Tests

```bash
# Lint code
npm run lint

# Build for production
npm run build

# Start production build
npm start
```

### Making Changes

**Frontend changes:**
1. Edit files in `src/`
2. Next.js hot-reloads automatically
3. Check browser for updates

**Agent changes:**
1. Edit `agent/agent.py`
2. Agent auto-reloads
3. Restart chat for new tools

**Style changes:**
1. Edit `src/app/globals.css` or component styles
2. Tailwind recompiles
3. Changes appear immediately

---

## 📦 Dependency Management

### Add New npm Package

```bash
npm install package-name
npm run dev
```

### Add New Python Package

```bash
cd agent
pip install package-name
pip freeze > requirements.txt
cd ..
```

---

## 🚀 Production Deployment

### Build for Production

```bash
npm run build
npm start
```

### Deploy Frontend (Vercel)

```bash
# Login to Vercel
npm i -g vercel
vercel login

# Deploy
vercel
```

### Deploy Agent (Choose Platform)

- **Railway**: Push to Railway
- **Heroku**: `heroku create`, `git push heroku main`
- **AWS Lambda**: Use serverless framework
- **Google Cloud**: Deploy to Cloud Functions

---

## 🔐 Security Checklist

- [ ] API key in `.env.local` (not committed)
- [ ] No sensitive data in frontend code
- [ ] HTTPS enabled in production
- [ ] Rate limiting configured
- [ ] Input validation on backend
- [ ] CORS properly configured
- [ ] Dependencies kept up-to-date

---

## 📞 Getting Help

### Resources

1. **CopilotKit Docs**: https://docs.copilotkit.ai/
2. **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
3. **Next.js Docs**: https://nextjs.org/docs
4. **Python Data Science**:
   - NumPy: https://numpy.org/doc/
   - Pandas: https://pandas.pydata.org/docs/
   - Matplotlib: https://matplotlib.org/

### Common Issues Quick Links

| Issue | Solution |
|-------|----------|
| Port in use | Kill process or use different port |
| Module not found | Run `npm install` and `pip install -r requirements.txt` |
| Agent not responding | Verify port 8123, restart agent |
| Sidebar not showing | Clear cache, check API key |
| Slow performance | Restart app, check resources |

---

## 🎯 Next Steps After Setup

1. ✅ Verify everything works
2. ✅ Try a few AI prompts
3. ✅ Explore the periodic table
4. ✅ Generate visualizations
5. ✅ Customize element data
6. ✅ Add more analysis tools
7. ✅ Deploy to production

---

## 📝 Quick Reference

```bash
# Start everything
npm run dev

# Frontend only
npm run dev:ui

# Agent only
npm run dev:agent

# Debug mode
npm run dev:debug

# Build production
npm run build

# Run production build
npm start

# Lint code
npm run lint

# Stop all services
Ctrl+C (in terminal)
```

---

**If you're still having issues, check the console output carefully - it usually shows exactly what's wrong! 🔍**
