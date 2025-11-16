/**
 * Quantum Simulation API Route
 * Handles quantum simulation requests and returns 3D probability data
 * 
 * POST /api/quantum
 * Body: { atomicNumber: number, elementSymbol: string, gridSize: number, energyThreshold: number }
 * Response: { elementSymbol: string, atomicNumber: number, probabilityMap: number[][], groundStateEnergy: number, spatialData: SpatialPoint[] }
 */

import { NextRequest, NextResponse } from "next/server";
import { SimulationResult, SpatialPoint, Vector3 } from "@/lib/elements";

export const maxDuration = 60; // 60 seconds for computation

interface QuantumRequest {
  atomicNumber: number;
  elementSymbol: string;
  gridSize: number;
  energyThreshold: number;
  useSimulator?: boolean;
  target?: string;
}

export async function POST(request: NextRequest) {
  try {
    const body: QuantumRequest = await request.json();

    // Validate input
    if (!body.atomicNumber || !body.elementSymbol || !body.gridSize) {
      return NextResponse.json(
        { error: "Missing required parameters" },
        { status: 400 }
      );
    }

    // Generate mock quantum simulation data
    const simulationResult = generateQuantumSimulation(body);

    return NextResponse.json(simulationResult, { status: 200 });
  } catch (error) {
    console.error("Quantum API error:", error);
    return NextResponse.json(
      { error: "Failed to process quantum simulation" },
      { status: 500 }
    );
  }
}

/**
 * Generate mock quantum simulation based on hydrogen-like atom model
 * In production, this would call the Q# Azure Quantum service
 */
function generateQuantumSimulation(config: QuantumRequest): SimulationResult {
  const { atomicNumber, elementSymbol, gridSize, energyThreshold } = config;

  // Calculate ground state energy using Rydberg formula: E_n = -13.6 * Z² / n²
  const groundStateEnergy = (-13.6 * atomicNumber * atomicNumber) / 1;

  // Generate 2D probability map (slice through center)
  const probabilityMap: number[][] = [];
  for (let i = 0; i < gridSize; i++) {
    const row: number[] = [];
    for (let j = 0; j < gridSize; j++) {
      // Normalized coordinates (-1 to 1)
      const x = (i - gridSize / 2) / (gridSize / 2);
      const y = (j - gridSize / 2) / (gridSize / 2);

      // Gaussian distribution with atomic number scaling
      const radius = Math.sqrt(x * x + y * y);
      const bohrRadius = 0.529 / atomicNumber; // in units of grid normalization
      const probability = Math.exp(
        -(radius * radius) / (2 * bohrRadius * bohrRadius)
      );

      row.push(Math.max(0, probability));
    }
    probabilityMap.push(row);
  }

  // Generate 3D spatial data points
  const spatialData: SpatialPoint[] = [];
  const spacing = 4 / gridSize; // 4 Å total size

  for (let i = 0; i < gridSize; i += 1) {
    for (let j = 0; j < gridSize; j += 1) {
      for (let k = 0; k < gridSize; k += 1) {
        // Convert grid indices to physical coordinates
        const x = (i - gridSize / 2) * spacing;
        const y = (j - gridSize / 2) * spacing;
        const z = (k - gridSize / 2) * spacing;

        // Calculate probability at this point (hydrogen-like orbital)
        const r = Math.sqrt(x * x + y * y + z * z);
        const bohrRadius = 0.529 / atomicNumber;

        // 1s orbital probability density: |ψ|² ∝ exp(-2r/a₀)
        const probability =
          (1 / (Math.PI * bohrRadius ** 3)) *
          Math.exp(-2 * r / bohrRadius);

        // Only include points above threshold for efficiency
        if (probability > energyThreshold * 0.01) {
          spatialData.push({
            position: { x, y, z },
            probability: Math.min(probability, 1.0),
            phase: Math.atan2(y, x),
          });
        }
      }
    }
  }

  return {
    elementSymbol,
    atomicNumber,
    probabilityMap,
    groundStateEnergy,
    spatialData,
    molecularBonds: generateMockBonds(elementSymbol),
  };
}

/**
 * Generate mock bond data for visualization
 */
function generateMockBonds(elementSymbol: string) {
  // Example bonds - in production would come from Q# simulation
  const commonBonds: Record<string, any[]> = {
    H: [
      { element1: "H", element2: "O", bondType: "covalent", bondEnergy: 4.5, bondLength: 96 },
      { element1: "H", element2: "C", bondType: "covalent", bondEnergy: 4.3, bondLength: 109 },
    ],
    C: [
      { element1: "C", element2: "O", bondType: "covalent", bondEnergy: 7.7, bondLength: 123 },
      { element1: "C", element2: "C", bondType: "covalent", bondEnergy: 6.1, bondLength: 154 },
    ],
    O: [
      { element1: "O", element2: "O", bondType: "covalent", bondEnergy: 5.1, bondLength: 121 },
    ],
    Fe: [
      { element1: "Fe", element2: "C", bondType: "metallic", bondEnergy: 3.2, bondLength: 200 },
    ],
    Au: [
      { element1: "Au", element2: "Au", bondType: "metallic", bondEnergy: 2.3, bondLength: 288 },
    ],
  };

  return commonBonds[elementSymbol] || [];
}

/**
 * Health check endpoint
 */
export async function GET() {
  return NextResponse.json(
    {
      status: "ok",
      message: "Quantum simulation API is running",
      version: "1.0.0",
    },
    { status: 200 }
  );
}
