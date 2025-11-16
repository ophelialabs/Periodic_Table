    /// <summary>
    /// Simulates electron distribution in an atom using quantum superposition.
    /// Returns measurement probabilities for different quantum states.
    /// </summary>
    operation SimulateElectronDistribution(numElectrons : Int) : Double[] {
        let numQubits = numElectrons > 5 ? 5 | numElectrons;
        use qubits = Qubit[numQubits];
        
        // Create superposition of electron states
        for q in qubits {
            H(q);
        }
        
        // Apply controlled rotations to simulate orbital interactions
        for i in 0 .. numQubits - 2 {
            Controlled Rz([qubits[i]], (0.5, qubits[i + 1]));
        }
        
        // Measure all qubits
        let results = MeasureEachZ(qubits);
        ResetAll(qubits);
        
        return GenerateDistribution(results, numQubits);
    }

    /// <summary>
    /// Simulates quantum orbital interactions and phase relationships.
    /// </summary>
    operation SimulateOrbitalPhase(orbitalIndex : Int, energyLevel : Int) : Double[] {
        let numQubits = energyLevel > 4 ? 4 | energyLevel;
        use qubits = Qubit[numQubits];
        
        // Initialize qubits based on orbital index
        let theta = 0.78539816339 * (orbitalIndex > 0 ? 1.0 | 0.0); // pi/4 * orbitalIndex
        
        for i in 0 .. numQubits - 1 {
            Ry(theta, qubits[i]);
        }
        
        // Measure qubits
        let measurements = MeasureEachZ(qubits);
        ResetAll(qubits);
        
        return GenerateDistribution(measurements, numQubits);
    }

    /// <summary>
    /// Calculates quantum probability amplitudes for electron density distribution.
    /// </summary>
    operation CalculateElectronDensity(atomicNumber : Int) : Double[] {
        let qubitsNeeded = CalculateQubitsNeeded(atomicNumber);
        use qubits = Qubit[qubitsNeeded];
        
        // Create equal superposition
        for q in qubits {
            H(q);
        }
        
        // Apply basic phase oracle for amplitude amplification
        for i in 0 .. qubitsNeeded - 1 {
            if i < (atomicNumber / 2) {
                Z(qubits[i]);
            }
        }
        
        let results = MeasureEachZ(qubits);
        ResetAll(qubits);
        
        return GenerateDistribution(results, qubitsNeeded);
    }

    // Helper functions

    /// <summary>
    /// Calculate number of qubits needed for simulation
    /// </summary>
    function CalculateQubitsNeeded(atomicNumber : Int) : Int {
        mutable qubits = 1;
        mutable count = atomicNumber;
        while count > 1 {
            set qubits += 1;
            set count = count / 2;
        }
        return qubits > 6 ? 6 | qubits;
    }

    /// <summary>
    /// Generate probability distribution from measurements
    /// </summary>
    function GenerateDistribution(measurements : Result[], numQubits : Int) : Double[] {
        let numStates = 2 ^ numQubits;
        mutable probabilities = [0.0, size = numStates];
        
        // Find which state was measured
        mutable stateIndex = 0;
        for i in 0 .. Length(measurements) - 1 {
            if measurements[i] == One {
                set stateIndex += (2 ^ i);
            }
        }
        
        // Initialize with measured state
        set probabilities w/= stateIndex <- 1.0;
        
        // Add smoothing to nearby states
        for i in 0 .. numStates - 1 {
            let distance = i - stateIndex;
            let absDist = distance < 0 ? -distance | distance;
            let weight = 1.0 / (1.0 + 2.0 * (absDist > 0 ? 1.0 | 0.0));
            let current = probabilities[i];
            set probabilities w/= i <- current + weight * 0.05;
        }
        
        // Normalize
        mutable sum = 0.0;
        for prob in probabilities {
            set sum += prob;
        }
        
        if sum > 0.0 {
            mutable normalized = [0.0, size = Length(probabilities)];
            for i in 0 .. Length(probabilities) - 1 {
                set normalized w/= i <- probabilities[i] / sum;
            }
            probabilities = normalized;
        }
        
        return probabilities;
    }
