"use client";

import { useCoAgent, useCopilotAction } from "@copilotkit/react-core";
import { CopilotKitCSSProperties, CopilotSidebar } from "@copilotkit/react-ui";
import { useState, useMemo } from "react";
import { Element, PERIODIC_TABLE } from "@/lib/periodicTableData";
import { PeriodicTable3D } from "@/components/PeriodicTable3D";
import { ElementCard } from "@/components/ElementCard";
import dynamic from 'next/dynamic';

const DataVisualization = dynamic(() => import('@/components/DataVisualization').then(mod => mod.DataVisualization), { ssr: false });

// Create a map of element symbols for quick lookup
const elementSymbolMap = PERIODIC_TABLE.reduce((acc, el) => {
  acc[el.symbol] = el;
  return acc;
}, {} as Record<string, Element>);

export default function CopilotKitPage() {
  const [themeColor, setThemeColor] = useState("#6366f1");

  useCopilotAction({
    name: "setThemeColor",
    parameters: [{
      name: "themeColor",
      description: "The theme color to set. Make sure to pick nice colors.",
      required: true, 
    }],
    handler({ themeColor }: any) {
      setThemeColor(themeColor);
    },
  });

  return (
    <main style={{ "--copilot-kit-primary-color": themeColor } as CopilotKitCSSProperties}>
      <YourMainContent themeColor={themeColor} />
      <CopilotSidebar
        clickOutsideToClose={false}
        defaultOpen={true}
        labels={{
          title: "Chemistry Assistant",
          initial: "👋 Welcome to the Interactive 3D Periodic Table!\n\nI'm your chemistry assistant. You can:\n- **Explore Elements**: Click on elements in the 3D periodic table\n- **Visualize Data**: \"Show me a scatter plot of atomic mass\"\n- **Find Elements**: \"Which elements are transition metals?\"\n- **Compare Properties**: \"Compare the ionization energy of noble gases\"\n- **Create Charts**: \"Make a histogram of element density\"\n\nTry asking me about elements or requesting visualizations!"
        }}
      />
    </main>
  );
}

// State of the agent, make sure this aligns with your agent's state.
type AgentState = {
  proverbs: string[];
  selected_elements: string[];
  visualization_type: string;
  visualization_property: string;
}

function YourMainContent({ themeColor }: { themeColor: string }) {
  const { state, setState } = useCoAgent<AgentState>({
    name: "sample_agent",
    initialState: {
      proverbs: [],
      selected_elements: [],
      visualization_type: "scatter",
      visualization_property: "atomicMass",
    },
  })

  const [selectedElement, setSelectedElement] = useState<Element | null>(null);
  const [showVisualization, setShowVisualization] = useState(false);

  // Frontend action: Select elements by category
  useCopilotAction({
    name: "selectElementsByCategory",
    description: "Select and highlight elements by their category",
    parameters: [{
      name: "category",
      type: "string",
      description: "Element category (Transition Metal, Nonmetal, etc)",
      required: true,
    }],
    handler: ({ category }: any) => {
      setState({
        ...state,
        visualization_type: "scatter",
      });
    },
  });

  // Frontend action: Update visualization
  useCopilotAction({
    name: "updateVisualization",
    description: "Update the data visualization",
    parameters: [
      { name: "type", type: "string", description: "scatter, histogram, or heatmap", required: true },
      { name: "property", type: "string", description: "Element property to visualize", required: true },
    ],
    handler: ({ type, property }: any) => {
      setState({
        ...state,
        visualization_type: type,
        visualization_property: property,
      });
      setShowVisualization(true);
    },
  });

  // Frontend action: Display element details
  useCopilotAction({
    name: "showElementDetails",
    description: "Show detailed information about an element",
    parameters: [{
      name: "symbol",
      type: "string",
      description: "Element symbol (e.g., H, He, C)",
      required: true,
    }],
    render: ({ args }: any) => {
      const element = elementSymbolMap[args.symbol];
      if (!element) return <div className="text-white">Element not found</div>;
      return (
        <div className="bg-white/10 rounded-lg p-4 text-white">
          <div className="text-2xl font-bold">{element.symbol} - {element.name}</div>
          <div className="mt-2 space-y-1 text-sm">
            <div>Atomic Number: {element.atomicNumber}</div>
            <div>Atomic Mass: {element.atomicMass.toFixed(3)}</div>
            <div>Category: {element.category}</div>
            <div>Period: {element.period}, Group: {element.group}</div>
          </div>
        </div>
      );
    },
  });

  return (
    <div className="h-screen w-screen flex overflow-hidden" style={{ backgroundColor: themeColor }}>
      {/* 3D Periodic Table */}
      <div className="flex-1 relative">
        <PeriodicTable3D 
          onElementClick={setSelectedElement}
          selectedElement={selectedElement}
        />
        
        {/* Selected Element Card */}
        {selectedElement && (
          <div className="absolute bottom-4 right-4 z-10">
            <ElementCard 
              element={selectedElement}
              onClose={() => setSelectedElement(null)}
            />
          </div>
        )}
      </div>

      {/* Right Panel - Info and Controls */}
      <div className="w-80 bg-slate-900 border-l border-slate-700 flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-slate-700">
          <h2 className="text-xl font-bold text-white">Interactive Periodic Table</h2>
          <p className="text-xs text-gray-400 mt-1">3D Chemistry Visualization</p>
        </div>

        {/* Legend */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          <div className="bg-slate-800 rounded p-3">
            <h3 className="font-semibold text-white text-sm mb-2">Element Categories</h3>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded" style={{ backgroundColor: '#90EE90' }}></div>
                <span className="text-gray-300">Nonmetal</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded" style={{ backgroundColor: '#FFB347' }}></div>
                <span className="text-gray-300">Alkali Metal</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded" style={{ backgroundColor: '#87CEEB' }}></div>
                <span className="text-gray-300">Transition</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded" style={{ backgroundColor: '#FFB6C1' }}></div>
                <span className="text-gray-300">Noble Gas</span>
              </div>
            </div>
          </div>

          {selectedElement && (
            <div className="bg-slate-800 rounded p-3">
              <h3 className="font-semibold text-white text-sm mb-2">Selected Element</h3>
              <div className="text-white text-lg font-bold">{selectedElement.symbol}</div>
              <div className="text-gray-300 text-sm">{selectedElement.name}</div>
              <div className="mt-2 text-xs text-gray-400 space-y-1">
                <div>Atomic #: {selectedElement.atomicNumber}</div>
                <div>Mass: {selectedElement.atomicMass.toFixed(3)}</div>
                <div>Category: {selectedElement.category}</div>
              </div>
            </div>
          )}

          {showVisualization && (
            <div className="bg-slate-800 rounded p-3">
              <div className="flex justify-between items-center mb-2">
                <h3 className="font-semibold text-white text-sm">Current Visualization</h3>
                <button
                  onClick={() => setShowVisualization(false)}
                  className="text-gray-400 hover:text-white text-xs"
                >
                  ✕
                </button>
              </div>
              <div className="text-xs text-gray-300">
                <div>Type: {state.visualization_type}</div>
                <div>Property: {state.visualization_property}</div>
              </div>
            </div>
          )}

          <div className="bg-slate-800 rounded p-3">
            <h3 className="font-semibold text-white text-sm mb-2">Instructions</h3>
            <ul className="text-xs text-gray-300 space-y-1">
              <li>• Click elements in the table to see details</li>
              <li>• Ask the assistant to visualize data</li>
              <li>• Request element comparisons</li>
              <li>• Explore atomic properties</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

// Simple sun icon for the weather card
function SunIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-14 h-14 text-yellow-200">
      <circle cx="12" cy="12" r="5" />
      <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" strokeWidth="2" stroke="currentColor" />
    </svg>
  );
}

// Weather card component where the location and themeColor are based on what the agent
// sets via tool calls.
function WeatherCard({ location, themeColor }: { location?: string, themeColor: string }) {
  return (
    <div
    style={{ backgroundColor: themeColor }}
    className="rounded-xl shadow-xl mt-6 mb-4 max-w-md w-full"
  >
    <div className="bg-white/20 p-4 w-full">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-xl font-bold text-white capitalize">{location}</h3>
          <p className="text-white">Current Weather</p>
        </div>
        <SunIcon />
      </div>
      
      <div className="mt-4 flex items-end justify-between">
        <div className="text-3xl font-bold text-white">70°</div>
        <div className="text-sm text-white">Clear skies</div>
      </div>
      
      <div className="mt-4 pt-4 border-t border-white">
        <div className="grid grid-cols-3 gap-2 text-center">
          <div>
            <p className="text-white text-xs">Humidity</p>
            <p className="text-white font-medium">45%</p>
          </div>
          <div>
            <p className="text-white text-xs">Wind</p>
            <p className="text-white font-medium">5 mph</p>
          </div>
          <div>
            <p className="text-white text-xs">Feels Like</p>
            <p className="text-white font-medium">72°</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  );
}
