/**
 * Interactive Periodic Table Component with 3D Element Visualization
 * Integrates quantum simulations and research tools
 */

"use client";

import React, { useState, useCallback, useEffect } from "react";
import {
  ElementData,
  PERIODIC_TABLE,
  getElement,
  createMockModelData,
} from "@/lib/elements";
import {
  QuantumResearchManager,
  QuantumSimulationConfig,
  ProcessedVisualizationData,
} from "@/lib/quantumHost";

interface PeriodicTableProps {
  onElementSelect?: (element: ElementData) => void;
  onSimulationComplete?: (data: ProcessedVisualizationData) => void;
}

interface Element3DViewProps {
  element: ElementData;
  visualizationData?: ProcessedVisualizationData;
  isLoading: boolean;
}

/**
 * 3D Element Visualization Component
 * Displays electron cloud, orbital structure, and quantum data
 */
function Element3DView({ element, visualizationData, isLoading }: Element3DViewProps) {
  const canvasRef = React.useRef<HTMLCanvasElement>(null);
  const [rotation, setRotation] = useState({ x: 0, y: 0 });

  // Simple 3D sphere visualization for electron cloud
  useEffect(() => {
    if (!canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Clear canvas
    ctx.fillStyle = "#0f1419";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (isLoading) {
      ctx.fillStyle = "#fff";
      ctx.font = "16px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("Simulating...", canvas.width / 2, canvas.height / 2);
      return;
    }

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    // Draw nucleus
    ctx.fillStyle = element.color;
    ctx.beginPath();
    ctx.arc(centerX, centerY, 8, 0, Math.PI * 2);
    ctx.fill();

    if (visualizationData) {
      // Draw electron cloud based on quantum data
      const radius = visualizationData.effectiveRadius * 30; // Scale for display

      // Multiple shells for visual effect
      for (let i = 0; i < 3; i++) {
        const shellRadius = (radius * (i + 1)) / 3;
        const opacity = 0.3 - i * 0.08;

        ctx.strokeStyle = `rgba(100, 200, 255, ${opacity})`;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(centerX, centerY, shellRadius, 0, Math.PI * 2);
        ctx.stroke();
      }

      // Draw densest points
      const pointRadius = radius * 0.8;
      visualizationData.densestPoints.slice(0, 12).forEach((point, idx) => {
        const angle = (idx / 12) * Math.PI * 2;
        const distance = pointRadius * (0.5 + point.probability * 0.5);

        const x = centerX + Math.cos(angle) * distance;
        const y = centerY + Math.sin(angle) * distance;

        ctx.fillStyle = `rgba(100, 200, 255, ${0.5 + point.probability * 0.5})`;
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fill();
      });

      // Draw orbital path
      ctx.strokeStyle = "rgba(100, 200, 255, 0.2)";
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let i = 0; i <= 100; i++) {
        const angle = (i / 100) * Math.PI * 2;
        const x = centerX + Math.cos(angle) * pointRadius;
        const y = centerY + Math.sin(angle) * pointRadius;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
    }

    // Draw orbital shells (basic Bohr model)
    const modelData = element.modelData || createMockModelData(element);
    modelData.orbitalRadii.slice(0, 3).forEach((bohrRadius, idx) => {
      const screenRadius = bohrRadius * 30; // Scale factor
      const opacity = (0.4 - idx * 0.15).toString();

      ctx.strokeStyle = `rgba(150, 150, 200, ${opacity})`;
      ctx.lineWidth = 1;
      ctx.setLineDash([5, 5]);
      ctx.beginPath();
      ctx.arc(centerX, centerY, screenRadius, 0, Math.PI * 2);
      ctx.stroke();
      ctx.setLineDash([]);
    });
  }, [element, visualizationData, isLoading]);

  return (
    <div className="flex flex-col gap-4">
      <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-lg p-4">
        <canvas
          ref={canvasRef}
          width={320}
          height={320}
          className="w-full border border-slate-700 rounded"
        />
      </div>

      {visualizationData && (
        <div className="grid grid-cols-2 gap-2 text-sm text-slate-300 bg-slate-800/50 p-3 rounded">
          <div>
            <p className="text-slate-400 text-xs">Effective Radius</p>
            <p className="font-mono text-lg">
              {visualizationData.effectiveRadius.toFixed(2)} Å
            </p>
          </div>
          <div>
            <p className="text-slate-400 text-xs">Ground State Energy</p>
            <p className="font-mono text-lg">
              {visualizationData.groundStateEnergy.toFixed(2)} eV
            </p>
          </div>
          <div className="col-span-2">
            <p className="text-slate-400 text-xs">Peak Probability</p>
            <p className="font-mono">
              {(visualizationData.peakProbability * 100).toFixed(1)}%
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

/**
 * Element Card Component
 * Shows element properties and integrates with research tools
 */
function ElementCard({
  element,
  isSelected,
  onClick,
  visualizationData,
  isLoading,
}: {
  element: ElementData;
  isSelected: boolean;
  onClick: () => void;
  visualizationData?: ProcessedVisualizationData;
  isLoading: boolean;
}) {
  return (
    <div
      onClick={onClick}
      className={`
        p-3 rounded-lg cursor-pointer transition-all duration-200
        border-2 ${
          isSelected
            ? "border-blue-500 bg-blue-900/20 shadow-lg shadow-blue-500/50"
            : "border-slate-700 bg-slate-900/50 hover:border-slate-500"
        }
      `}
    >
      <div className="text-center">
        <div className="text-2xl font-bold" style={{ color: element.color }}>
          {element.symbol}
        </div>
        <div className="text-xs text-slate-400">{element.atomicNumber}</div>
        <div className="text-xs text-slate-500 truncate">{element.name}</div>
        {isLoading && <div className="text-xs text-blue-400 mt-1">Simulating...</div>}
      </div>
    </div>
  );
}

/**
 * Element Details Panel
 */
function ElementDetailsPanel({ element }: { element: ElementData }) {
  return (
    <div className="space-y-4 text-sm">
      <div>
        <h3 className="text-white font-semibold mb-2">{element.name}</h3>
        <p className="text-slate-400">{element.category}</p>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="bg-slate-800/50 p-2 rounded">
          <p className="text-slate-400 text-xs">Atomic Mass</p>
          <p className="text-white font-mono">{element.atomicMass.toFixed(3)}</p>
        </div>
        <div className="bg-slate-800/50 p-2 rounded">
          <p className="text-slate-400 text-xs">Electronegativity</p>
          <p className="text-white font-mono">
            {element.electronegativity === 0 ? "N/A" : element.electronegativity}
          </p>
        </div>
        <div className="bg-slate-800/50 p-2 rounded">
          <p className="text-slate-400 text-xs">Ionization Energy</p>
          <p className="text-white font-mono">{element.ionizationEnergy.toFixed(2)} eV</p>
        </div>
        <div className="bg-slate-800/50 p-2 rounded">
          <p className="text-slate-400 text-xs">Atomic Radius</p>
          <p className="text-white font-mono">{element.atomicRadius} pm</p>
        </div>
      </div>

      <div>
        <p className="text-slate-400 text-xs mb-1">Electron Configuration</p>
        <p className="text-white font-mono text-xs">{element.electronConfig}</p>
      </div>

      <div>
        <p className="text-slate-400 text-xs mb-1">Oxidation States</p>
        <p className="text-white font-mono">
          {element.oxidationStates.map(s => (s > 0 ? `+${s}` : s)).join(", ")}
        </p>
      </div>
    </div>
  );
}

/**
 * Main Periodic Table Component
 */
export function PeriodicTable3D({
  onElementSelect,
  onSimulationComplete,
}: PeriodicTableProps) {
  const [selectedElement, setSelectedElement] = useState<ElementData | null>(
    PERIODIC_TABLE[0]
  );
  const [visualizationData, setVisualizationData] = useState<ProcessedVisualizationData>();
  const [isLoading, setIsLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");

  const researchManager = React.useRef(new QuantumResearchManager(true)).current;

  const handleElementClick = useCallback(
    async (element: ElementData) => {
      setSelectedElement(element);
      onElementSelect?.(element);

      // Trigger quantum simulation
      setIsLoading(true);
      try {
        const config: QuantumSimulationConfig = {
          atomicNumber: element.atomicNumber,
          elementSymbol: element.symbol,
          gridSize: 16,
          energyThreshold: 1.0,
        };

        const response = await researchManager.simulateElement(config);

        if (response.success && response.result) {
          const vizData = researchManager.getProcessedVisualization(response.result);
          setVisualizationData(vizData);
          onSimulationComplete?.(vizData);
        }
      } catch (error) {
        console.error("Simulation error:", error);
      } finally {
        setIsLoading(false);
      }
    },
    [researchManager, onElementSelect, onSimulationComplete]
  );

  const filteredElements = PERIODIC_TABLE.filter(
    el =>
      el.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      el.symbol.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="flex flex-col lg:flex-row gap-6 h-full">
      {/* Periodic Table Grid */}
      <div className="flex-1 space-y-4">
        <div>
          <input
            type="text"
            placeholder="Search elements..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
          />
        </div>

        <div className="grid grid-cols-4 sm:grid-cols-6 gap-2 overflow-y-auto max-h-96">
          {filteredElements.map(element => (
            <ElementCard
              key={element.atomicNumber}
              element={element}
              isSelected={selectedElement?.atomicNumber === element.atomicNumber}
              onClick={() => handleElementClick(element)}
              isLoading={
                isLoading && selectedElement?.atomicNumber === element.atomicNumber
              }
            />
          ))}
        </div>
      </div>

      {/* Selected Element Details and 3D View */}
      {selectedElement && (
        <div className="lg:w-96 space-y-4">
          <div className="bg-slate-900 border border-slate-700 rounded-lg p-4 space-y-4">
            {/* 3D Visualization */}
            <Element3DView
              element={selectedElement}
              visualizationData={visualizationData}
              isLoading={isLoading}
            />

            {/* Element Details */}
            <div className="border-t border-slate-700 pt-4">
              <ElementDetailsPanel element={selectedElement} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
