"use client";

import React, { useState, useMemo } from "react";
import { useCopilotAction, useCoAgent } from "@copilotkit/react-core";
import { CopilotKitCSSProperties } from "@copilotkit/react-ui";
import { PERIODIC_TABLE, Element, getCategories } from "@/lib/periodicTableData";

interface PeriodicTableState {
  selectedElement: Element | null;
  selectedCategory: string | null;
  visualizationMode: "table" | "trends" | "properties" | "trends3d";
  highlightedProperty: string | null;
  elementFilter: string;
}

export default function PeriodicTableViewer() {
  const [selectedElement, setSelectedElement] = useState<Element | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [visualizationMode, setVisualizationMode] = useState<"table" | "trends" | "properties" | "trends3d">("table");
  const [highlightedProperty, setHighlightedProperty] = useState<string | null>(null);
  const [elementFilter, setElementFilter] = useState("");
  const [chartData, setChartData] = useState<any>(null);

  // Agent state for shared state with the copilot
  const { state, setState } = useCoAgent<PeriodicTableState>({
    name: "sample_agent",
    initialState: {
      selectedElement: null,
      selectedCategory: null,
      visualizationMode: "table",
      highlightedProperty: null,
      elementFilter: "",
    },
  });

  // Frontend action: Select an element
  useCopilotAction({
    name: "selectElement",
    description: "Select a chemical element from the periodic table",
    parameters: [
      {
        name: "atomicNumber",
        type: "number",
        description: "The atomic number of the element to select",
        required: true,
      },
    ],
    handler: ({ atomicNumber }) => {
      const element = PERIODIC_TABLE.find((el) => el.atomicNumber === atomicNumber);
      if (element) {
        setSelectedElement(element);
        setState({
          ...state,
          selectedElement: element,
        });
      }
    },
  });

  // Frontend action: Filter by category
  useCopilotAction({
    name: "filterByCategory",
    description: "Filter elements by their category (e.g., 'Transition Metal', 'Halogen')",
    parameters: [
      {
        name: "category",
        type: "string",
        description: "The category to filter by",
        required: true,
      },
    ],
    handler: ({ category }) => {
      setSelectedCategory(category);
      setState({
        ...state,
        selectedCategory: category,
      });
    },
  });

  // Frontend action: Change visualization mode
  useCopilotAction({
    name: "changeVisualization",
    description: "Change the visualization mode to view element properties in different ways",
    parameters: [
      {
        name: "mode",
        type: "string",
        description: "The visualization mode: 'table', 'trends', 'properties', or 'trends3d'",
        required: true,
      },
    ],
    handler: (args: { mode: string }) => {
      // Narrow the incoming string to the expected union safely
      const mode = args.mode as "table" | "trends" | "properties" | "trends3d";
      const validModes: Array<"table" | "trends" | "properties" | "trends3d"> = ["table", "trends", "properties", "trends3d"];
      if (validModes.includes(mode)) {
        setVisualizationMode(mode);
        setState({
          ...state,
          visualizationMode: mode,
        });
      }
    },
  });

  // Frontend action: Highlight a property
  useCopilotAction({
    name: "highlightProperty",
    description: "Highlight a specific property across all elements (e.g., 'electronegativity', 'atomicMass')",
    parameters: [
      {
        name: "property",
        type: "string",
        description: "The property to highlight",
        required: true,
      },
    ],
    handler: ({ property }) => {
      setHighlightedProperty(property);
      setState({
        ...state,
        highlightedProperty: property,
      });
    },
  });

  // Frontend action: Search elements
  useCopilotAction({
    name: "searchElement",
    description: "Search for elements by name or symbol",
    parameters: [
      {
        name: "query",
        type: "string",
        description: "The search query (element name or symbol)",
        required: true,
      },
    ],
    handler: ({ query }) => {
      setElementFilter(query.toLowerCase());
      setState({
        ...state,
        elementFilter: query.toLowerCase(),
      });
    },
  });

  // Filtered elements
  const filteredElements = useMemo(() => {
    let result = PERIODIC_TABLE;

    if (selectedCategory) {
      result = result.filter((el) => el.category === selectedCategory);
    }

    if (elementFilter) {
      result = result.filter(
        (el) =>
          el.name.toLowerCase().includes(elementFilter) ||
          el.symbol.toLowerCase().includes(elementFilter)
      );
    }

    return result;
  }, [selectedCategory, elementFilter]);

  // Get property intensity for color coding
  const getPropertyIntensity = (element: Element, property: string | null): number => {
    if (!property) return 0.5;

    const value = (element as any)[property];
    if (typeof value !== "number") return 0.5;

    // Normalize to 0-1 range
    const allValues = PERIODIC_TABLE
      .map((el) => (el as any)[property])
      .filter((v) => typeof v === "number");

    if (allValues.length === 0) return 0.5;

    const min = Math.min(...allValues);
    const max = Math.max(...allValues);

    if (min === max) return 0.5;

    return (value - min) / (max - min);
  };

  // Get color for element based on intensity
  const getElementColor = (element: Element): string => {
    if (highlightedProperty) {
      const intensity = getPropertyIntensity(element, highlightedProperty);
      const red = Math.round(255 * intensity);
      const blue = Math.round(255 * (1 - intensity));
      return `rgb(${red}, 100, ${blue})`;
    }

    return element.categoryColor;
  };

  return (
    <div className="w-full h-full bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-5xl font-bold text-white mb-2">
            Interactive Periodic Table of Elements
          </h1>
          <p className="text-gray-300 text-lg">
            Explore elements with AI-powered analysis and visualizations
          </p>
        </div>

        {/* Control Panel */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          {/* Category Filter */}
          <div className="bg-slate-700/50 backdrop-blur p-4 rounded-lg border border-slate-600">
            <label className="block text-white font-semibold mb-2">Filter by Category</label>
            <select
              value={selectedCategory || ""}
              onChange={(e) => setSelectedCategory(e.target.value || null)}
              className="w-full px-3 py-2 bg-slate-600 text-white rounded border border-slate-500 focus:outline-none focus:border-blue-400"
            >
              <option value="">All Categories</option>
              {getCategories().map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
          </div>

          {/* Search */}
          <div className="bg-slate-700/50 backdrop-blur p-4 rounded-lg border border-slate-600">
            <label className="block text-white font-semibold mb-2">Search Elements</label>
            <input
              type="text"
              value={elementFilter}
              onChange={(e) => setElementFilter(e.target.value.toLowerCase())}
              placeholder="e.g., Gold, Au..."
              className="w-full px-3 py-2 bg-slate-600 text-white rounded border border-slate-500 focus:outline-none focus:border-blue-400 placeholder-gray-400"
            />
          </div>

          {/* Property Highlight */}
          <div className="bg-slate-700/50 backdrop-blur p-4 rounded-lg border border-slate-600">
            <label className="block text-white font-semibold mb-2">Highlight Property</label>
            <select
              value={highlightedProperty || ""}
              onChange={(e) => setHighlightedProperty(e.target.value || null)}
              className="w-full px-3 py-2 bg-slate-600 text-white rounded border border-slate-500 focus:outline-none focus:border-blue-400"
            >
              <option value="">Category Colors</option>
              <option value="atomicMass">Atomic Mass</option>
              <option value="electronegativity">Electronegativity</option>
              <option value="ionizationEnergy">Ionization Energy</option>
              <option value="atomicRadius">Atomic Radius</option>
              <option value="density">Density</option>
              <option value="meltingPoint">Melting Point</option>
              <option value="boilingPoint">Boiling Point</option>
            </select>
          </div>
        </div>

        {/* Visualization Mode Tabs */}
        <div className="flex gap-2 mb-8 flex-wrap">
          {(["table", "trends", "properties", "trends3d"] as const).map((mode) => (
            <button
              key={mode}
              onClick={() => setVisualizationMode(mode)}
              className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                visualizationMode === mode
                  ? "bg-blue-600 text-white shadow-lg"
                  : "bg-slate-700 text-gray-300 hover:bg-slate-600"
              }`}
            >
              {mode.charAt(0).toUpperCase() + mode.slice(1)}
            </button>
          ))}
        </div>

        {/* Main Content Area */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Periodic Table Grid */}
          <div className="lg:col-span-2 bg-slate-700/50 backdrop-blur p-6 rounded-lg border border-slate-600 overflow-auto max-h-[70vh]">
            {visualizationMode === "table" ? (
              <div className="grid gap-1" style={{ gridTemplateColumns: "repeat(18, minmax(0, 1fr))" }}>
                {filteredElements.length > 0 ? (
                  filteredElements.map((element) => (
                    <button
                      key={element.atomicNumber}
                      onClick={() => setSelectedElement(element)}
                      style={{
                        backgroundColor: getElementColor(element),
                        gridColumn: element.group,
                        gridRow: element.period + 1,
                      }}
                      className={`p-2 rounded text-center font-bold transition-all hover:shadow-lg hover:scale-105 cursor-pointer border-2 ${
                        selectedElement?.atomicNumber === element.atomicNumber
                          ? "border-yellow-400 shadow-xl"
                          : "border-slate-500"
                      }`}
                    >
                      <div className="text-xs text-gray-800">{element.atomicNumber}</div>
                      <div className="text-sm text-gray-900">{element.symbol}</div>
                      <div className="text-xs text-gray-800">{element.atomicMass.toFixed(2)}</div>
                    </button>
                  ))
                ) : (
                  <div className="col-span-18 text-center text-gray-400 py-8">
                    No elements found matching your filters
                  </div>
                )}
              </div>
            ) : visualizationMode === "trends" ? (
              <div className="space-y-6">
                <h3 className="text-white text-xl font-bold">Elemental Trends</h3>
                <div className="space-y-4">
                  {highlightedProperty && (
                    <div className="bg-slate-600 p-4 rounded">
                      <h4 className="text-gray-200 font-semibold mb-3">{highlightedProperty}</h4>
                      {filteredElements
                        .filter((el) => (el as any)[highlightedProperty])
                        .slice(0, 10)
                        .map((element) => (
                          <div key={element.atomicNumber} className="mb-2">
                            <div className="flex justify-between text-sm text-gray-300 mb-1">
                              <span>{element.symbol} - {element.name}</span>
                              <span>{((element as any)[highlightedProperty] || 0).toFixed(2)}</span>
                            </div>
                            <div className="w-full bg-slate-500 rounded-full h-2">
                              <div
                                className="bg-blue-500 h-2 rounded-full"
                                style={{
                                  width: `${
                                    (getPropertyIntensity(element, highlightedProperty) * 100).toFixed(0)
                                  }%`,
                                }}
                              />
                            </div>
                          </div>
                        ))}
                    </div>
                  )}
                </div>
              </div>
            ) : visualizationMode === "properties" ? (
              <div className="space-y-4">
                <h3 className="text-white text-xl font-bold mb-4">Element Properties Comparison</h3>
                <div className="grid gap-3">
                  {filteredElements.slice(0, 12).map((element) => (
                    <div
                      key={element.atomicNumber}
                      className="bg-slate-600 p-4 rounded border-l-4"
                      style={{ borderColor: element.categoryColor }}
                    >
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <h4 className="text-white font-bold">{element.name}</h4>
                          <p className="text-gray-400 text-sm">{element.symbol} - {element.category}</p>
                        </div>
                        <span className="bg-blue-600 text-white px-2 py-1 rounded text-sm font-bold">
                          #{element.atomicNumber}
                        </span>
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-xs text-gray-300">
                        <p>Mass: {element.atomicMass.toFixed(2)}</p>
                        <p>Period: {element.period}</p>
                        <p>Electronegativity: {element.electronegativity || "N/A"}</p>
                        <p>State: {element.state || "Unknown"}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-gray-400">
                <p>3D Visualization Mode</p>
                <p className="text-sm mt-2">
                  Ask the AI assistant to generate advanced 3D visualizations using matplotlib and seaborn
                </p>
              </div>
            )}
          </div>

          {/* Element Details Panel */}
          <div className="bg-slate-700/50 backdrop-blur p-6 rounded-lg border border-slate-600 max-h-[70vh] overflow-auto">
            {selectedElement ? (
              <div className="space-y-4">
                <div
                  className="p-6 rounded-lg text-center text-white font-bold"
                  style={{ backgroundColor: selectedElement.categoryColor }}
                >
                  <div className="text-5xl mb-2">{selectedElement.symbol}</div>
                  <div className="text-2xl">{selectedElement.name}</div>
                  <div className="text-sm mt-2 opacity-75">#{selectedElement.atomicNumber}</div>
                </div>

                <div className="space-y-3">
                  <div className="bg-slate-600 p-3 rounded">
                    <p className="text-gray-400 text-sm">Atomic Mass</p>
                    <p className="text-white font-bold">{selectedElement.atomicMass}</p>
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-slate-600 p-3 rounded">
                      <p className="text-gray-400 text-sm">Period</p>
                      <p className="text-white font-bold">{selectedElement.period}</p>
                    </div>
                    <div className="bg-slate-600 p-3 rounded">
                      <p className="text-gray-400 text-sm">Group</p>
                      <p className="text-white font-bold">{selectedElement.group}</p>
                    </div>
                  </div>

                  <div className="bg-slate-600 p-3 rounded">
                    <p className="text-gray-400 text-sm">Category</p>
                    <p className="text-white font-bold">{selectedElement.category}</p>
                  </div>

                  <div className="bg-slate-600 p-3 rounded">
                    <p className="text-gray-400 text-sm">State</p>
                    <p className="text-white font-bold">{selectedElement.state || "Unknown"}</p>
                  </div>

                  {selectedElement.electronegativity !== undefined && (
                    <div className="bg-slate-600 p-3 rounded">
                      <p className="text-gray-400 text-sm">Electronegativity</p>
                      <p className="text-white font-bold">{selectedElement.electronegativity}</p>
                    </div>
                  )}

                  {selectedElement.ionizationEnergy !== undefined && (
                    <div className="bg-slate-600 p-3 rounded">
                      <p className="text-gray-400 text-sm">Ionization Energy</p>
                      <p className="text-white font-bold">{selectedElement.ionizationEnergy} eV</p>
                    </div>
                  )}

                  {selectedElement.atomicRadius !== undefined && (
                    <div className="bg-slate-600 p-3 rounded">
                      <p className="text-gray-400 text-sm">Atomic Radius</p>
                      <p className="text-white font-bold">{selectedElement.atomicRadius} pm</p>
                    </div>
                  )}

                  {selectedElement.density !== undefined && (
                    <div className="bg-slate-600 p-3 rounded">
                      <p className="text-gray-400 text-sm">Density</p>
                      <p className="text-white font-bold">{selectedElement.density} g/cm³</p>
                    </div>
                  )}

                  {selectedElement.meltingPoint !== undefined && (
                    <div className="bg-slate-600 p-3 rounded">
                      <p className="text-gray-400 text-sm">Melting Point</p>
                      <p className="text-white font-bold">{selectedElement.meltingPoint}°C</p>
                    </div>
                  )}

                  {selectedElement.boilingPoint !== undefined && (
                    <div className="bg-slate-600 p-3 rounded">
                      <p className="text-gray-400 text-sm">Boiling Point</p>
                      <p className="text-white font-bold">{selectedElement.boilingPoint}°C</p>
                    </div>
                  )}

                  {selectedElement.yearDiscovered !== undefined && selectedElement.yearDiscovered > 0 && (
                    <div className="bg-slate-600 p-3 rounded">
                      <p className="text-gray-400 text-sm">Year Discovered</p>
                      <p className="text-white font-bold">{selectedElement.yearDiscovered}</p>
                    </div>
                  )}
                </div>

                <button
                  onClick={() => setSelectedElement(null)}
                  className="w-full bg-red-600 hover:bg-red-700 text-white py-2 rounded font-semibold transition-all"
                >
                  Clear Selection
                </button>
              </div>
            ) : (
              <div className="text-center py-12 text-gray-400">
                <p className="text-lg font-semibold mb-2">Select an Element</p>
                <p className="text-sm">Click on any element in the periodic table to view its detailed properties</p>
              </div>
            )}
          </div>
        </div>

        {/* Footer with Legend */}
        <div className="mt-8 grid grid-cols-2 md:grid-cols-5 gap-3">
          {getCategories().map((category) => (
            <div key={category} className="flex items-center gap-2 bg-slate-700/50 p-3 rounded border border-slate-600">
              <div
                className="w-4 h-4 rounded"
                style={{ backgroundColor: (PERIODIC_TABLE.find((el) => el.category === category)?.categoryColor || "#ccc") }}
              />
              <span className="text-gray-300 text-sm">{category}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
