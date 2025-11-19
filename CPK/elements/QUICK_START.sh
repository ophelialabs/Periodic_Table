#!/bin/bash

# 🧪 Interactive 3D Periodic Table - Quick Start Guide

cat << "EOF"

╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║   🧪 Interactive 3D Periodic Table with AI Integration 🤖         ║
║                                                                    ║
║   Powered by: Three.js • CopilotKit • LangGraph • OpenAI          ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝

📋 QUICK START CHECKLIST
═════════════════════════════════════════════════════════════════════

1. 📁 PROJECT LOCATION
   Path: /Users/jesse/Desktop/Company/Tools/PeriodicTable/CPK/elements
   
2. ⚙️  PREREQUISITES
   ✓ Node.js 18+ (or higher)
   ✓ npm (comes with Node.js)
   ✓ Git (for version control)
   ✓ An OpenAI API key (FREE trial or paid)

3. 🔑 API KEYS NEEDED
   
   a) OpenAI API Key (REQUIRED)
      • Get from: https://platform.openai.com/api-keys
      • Free $5 credit for 3 months
      • Cost: ~$0.15/month for light usage
   
   b) CopilotKit Key (PROVIDED)
      • Already included: ck_pub_336d5ab8498da237aaccefc683ed17e7
   
   c) Google Maps Key (OPTIONAL)
      • Already included: AIzaSyDK7BXtZz4ypjq0yr-7FrrAcl3oCoPpxK8

4. 🚀 INSTALLATION STEPS

   Step 1: Install Dependencies
   ─────────────────────────────
   cd /Users/jesse/Desktop/Company/Tools/PeriodicTable/CPK/elements
   npm install
   
   Wait for installation to complete (~2-3 minutes)
   
   Step 2: Create Environment File
   ────────────────────────────────
   Create a file named: .env.local
   
   Content:
   ─────────
   OPENAI_API_KEY=sk_YOUR_KEY_HERE
   NEXT_PUBLIC_COPILOT_KIT_PUBLIC_API_KEY=ck_pub_336d5ab8498da237aaccefc683ed17e7
   NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=AIzaSyDK7BXtZz4ypjq0yr-7FrrAcl3oCoPpxK8
   
   ⚠️  Replace "sk_YOUR_KEY_HERE" with your actual OpenAI key
   
   Step 3: Start Development Server
   ────────────────────────────────
   npm run dev
   
   This will start:
   • UI Server: http://localhost:3000
   • Agent Server: http://localhost:8123
   
   Step 4: Open in Browser
   ───────────────────────
   Open: http://localhost:3000
   
   You should see:
   • 3D periodic table in the center
   • AI chat sidebar on the right
   • Element information panel on the right

5. 🎯 FIRST INTERACTIONS

   Try these commands in the AI chat:
   
   a) Explore Elements
      "Show me all transition metals"
      "Which elements are halogens?"
      "Tell me about Carbon"
   
   b) Visualize Data
      "Create a scatter plot of atomic mass"
      "Show me a histogram of ionization energy"
   
   c) Interact with Table
      • Click any element in the 3D table
      • See detailed information in the card
      • Hover to see element properties

6. ✅ VERIFICATION

   ✓ Page loads without errors
   ✓ 3D table is visible and interactive
   ✓ AI sidebar appears on right
   ✓ You can click on elements
   ✓ Chat works (test with simple message)
   ✓ Colors show different element types

════════════════════════════════════════════════════════════════════

📁 KEY FILES TO KNOW

Frontend:
  • src/app/page.tsx - Main application page
  • src/components/PeriodicTable3D.tsx - 3D visualization
  • src/components/ElementCard.tsx - Element details
  • src/components/DataVisualization.tsx - Charts

Backend:
  • agent/agent.py - AI agent logic
  • agent/requirements.txt - Python dependencies

Data:
  • src/lib/periodicTableData.ts - Element database

Documentation:
  • PERIODIC_TABLE_README.md - Complete feature guide
  • API_DOCUMENTATION.md - Detailed API reference
  • API_KEYS_GUIDE.md - Key setup instructions
  • ARCHITECTURE.md - System design

════════════════════════════════════════════════════════════════════

🆘 TROUBLESHOOTING

Problem: "Cannot find module 'react'"
Solution: Run: npm install

Problem: Port 3000 already in use
Solution: 
  macOS/Linux: lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9
  Windows: netstat -ano | findstr :3000

Problem: Agent not connecting
Solution: 
  1. Check port 8123 is free
  2. Restart: npm run dev:agent
  3. Check firewall settings

Problem: "Invalid API Key"
Solution:
  1. Copy key exactly (no extra spaces)
  2. Verify it starts with "sk_"
  3. Check key hasn't been revoked
  4. Restart dev server

Problem: 3D table doesn't render
Solution:
  1. Check browser WebGL support
  2. Try different browser
  3. Check browser console for errors

════════════════════════════════════════════════════════════════════

🎓 USEFUL COMMANDS

Development:
  npm run dev              # Start both UI and agent
  npm run dev:ui          # Start only UI (port 3000)
  npm run dev:agent       # Start only agent (port 8123)
  npm run dev:debug       # Start with debug logging

Building:
  npm run build           # Production build
  npm start               # Run production build

Code Quality:
  npm run lint            # Check code style

════════════════════════════════════════════════════════════════════

📚 LEARNING RESOURCES

Understand the Tech Stack:
  1. Three.js: https://threejs.org/docs/
  2. CopilotKit: https://docs.copilotkit.ai/
  3. LangGraph: https://langchain-ai.github.io/langgraph/
  4. Next.js: https://nextjs.org/docs

Explore the Code:
  1. Start with src/app/page.tsx
  2. Read src/components/PeriodicTable3D.tsx
  3. Check agent/agent.py for AI logic
  4. Review src/lib/periodicTableData.ts for data

Try Modifying:
  1. Add more elements to periodicTableData.ts
  2. Create new visualization types
  3. Add new backend tools in agent.py
  4. Customize 3D styling in PeriodicTable3D.tsx

════════════════════════════════════════════════════════════════════

🎉 YOU'RE READY!

Your Interactive 3D Periodic Table is set up and ready to explore.

Next Steps:
  1. Get your OpenAI API key from https://platform.openai.com/api-keys
  2. Create .env.local with your key
  3. Run: npm run dev
  4. Open: http://localhost:3000
  5. Start exploring!

════════════════════════════════════════════════════════════════════

💡 PRO TIPS

1. Chrome/Chromium works best for 3D performance
2. Keep the sidebar open for full AI interaction
3. Click elements to see detailed properties
4. Ask the AI for specific visualizations
5. Hover over elements for quick tooltips
6. Use debug mode for verbose logging: npm run dev:debug

════════════════════════════════════════════════════════════════════

📞 NEED HELP?

1. Check the documentation files:
   • PERIODIC_TABLE_README.md
   • API_DOCUMENTATION.md
   • API_KEYS_GUIDE.md
   • ARCHITECTURE.md

2. Look at code comments in components

3. Review browser console for errors (F12)

4. Check agent logs in terminal

════════════════════════════════════════════════════════════════════

🚀 HAPPY EXPLORING! 🔬⚛️

EOF

echo ""
echo "To get started, run:"
echo "  cd /Users/jesse/Desktop/Company/Tools/PeriodicTable/CPK/elements"
echo "  npm install"
echo "  npm run dev"
echo ""
