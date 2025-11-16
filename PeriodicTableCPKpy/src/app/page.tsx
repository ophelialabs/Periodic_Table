"use client";

import { useCoAgent, useCopilotAction } from "@copilotkit/react-core";
import { CopilotKitCSSProperties, CopilotSidebar } from "@copilotkit/react-ui";
import { useState } from "react";
import { PeriodicTable3D } from "@/components/PeriodicTable3D";
import { ElementData } from "@/lib/elements";
import { ProcessedVisualizationData } from "@/lib/quantumHost";

export default function CopilotKitPage() {
  const [themeColor, setThemeColor] = useState("#0f172a");
  const [selectedElement, setSelectedElement] = useState<ElementData | null>(null);
  const [visualizationData, setVisualizationData] = useState<ProcessedVisualizationData | null>(null);

  // 🪁 Frontend Actions: https://docs.copilotkit.ai/guides/frontend-actions
  useCopilotAction({
    name: "setThemeColor",
    parameters: [{
      name: "themeColor",
      description: "The theme color to set. Use hex colors like #FF5733, #3498DB, etc.",
      required: true, 
    }],
    handler({ themeColor }) {
      setThemeColor(themeColor);
    },
  });

  useCopilotAction({
    name: "selectElement",
    description: "Select an element from the periodic table for detailed analysis and quantum simulation.",
    parameters: [{
      name: "elementSymbol",
      description: "Chemical symbol of the element (e.g., H, He, C, O, Fe, Au)",
      required: true,
    }],
    handler({ elementSymbol }) {
      // This would trigger element selection in the UI
      console.log(`Selected element: ${elementSymbol}`);
    },
  });

  return (
    <main style={{ "--copilot-kit-primary-color": themeColor } as CopilotKitCSSProperties}>
      <YourMainContent 
        themeColor={themeColor}
        onElementSelect={setSelectedElement}
        onVisualizationComplete={setVisualizationData}
      />
      <CopilotSidebar
        clickOutsideToClose={false}
        defaultOpen={true}
        labels={{
          title: "Quantum Research Assistant",
          initial: "👋 Welcome to the Interactive Periodic Table!\n\nI'm your quantum research assistant. I can help you:\n\n**Explore Elements:**\n- \"Tell me about Hydrogen\"\n- \"What's the ionization energy of Carbon?\"\n- \"Show me the orbital structure of Iron\"\n\n**Run Simulations:**\n- \"Simulate the electron cloud for Gold\"\n- \"Generate a 3D visualization for Oxygen\"\n\n**Research & Analysis:**\n- \"Research element properties for materials science\"\n- \"Compare the reactivity of different elements\"\n- \"Suggest elements for nanotechnology applications\"\n\n**Customize:**\n- \"Set the theme to blue\"\n- \"Change the background color to purple\"\n\nClick on elements in the table on the left to start exploring! 🔬"
        }}
      />
    </main>
  );
}

// State of the agent, make sure this aligns with your agent's state.
type AgentState = {
  elementHistory: string[];
  researchData: Record<string, unknown>;
}

function YourMainContent({ 
  themeColor,
  onElementSelect,
  onVisualizationComplete,
}: { 
  themeColor: string;
  onElementSelect: (el: ElementData | null) => void;
  onVisualizationComplete: (data: ProcessedVisualizationData | null) => void;
}) {
  // 🪁 Shared State: https://docs.copilotkit.ai/coagents/shared-state
  const { state, setState } = useCoAgent<AgentState>({
    name: "sample_agent",
    initialState: {
      elementHistory: [],
      researchData: {},
    },
  })

  return (
    <div
      style={{ backgroundColor: themeColor }}
      className="h-screen w-screen flex justify-center items-center flex-col transition-colors duration-300 p-4"
    >
      <div className="bg-white/5 backdrop-blur-md p-6 rounded-2xl shadow-xl max-w-7xl w-full h-full flex flex-col gap-4">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-2">Interactive Periodic Table</h1>
          <p className="text-gray-300 text-sm">3D Quantum Orbital Visualization & Research Tools</p>
        </div>
        
        <div className="flex-1 overflow-hidden">
          <PeriodicTable3D
            onElementSelect={(element) => {
              onElementSelect(element);
              setState({
                ...state,
                elementHistory: [...state.elementHistory, element.symbol],
              });
            }}
            onSimulationComplete={(data) => {
              onVisualizationComplete(data);
              setState({
                ...state,
                researchData: {
                  ...state.researchData,
                  lastSimulation: data,
                },
              });
            }}
          />
        </div>

        {state.elementHistory.length > 0 && (
          <div className="bg-white/10 rounded-lg p-3 text-sm text-white/80">
            <p className="text-xs text-white/60 mb-1">Recently viewed: {state.elementHistory.join(", ")}</p>
          </div>
        )}
      </div>
    </div>
  );
}
