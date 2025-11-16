package periodictable

// QuantumResults holds the results from a quantum simulation
type QuantumResults struct {
	ElementSymbol         string    `json:"element"`
	SimulationID          string    `json:"simulationId"`
	ElectronProbabilities []float64 `json:"electronProbabilities"`
	SpatialData           []float64 `json:"spatialData"`
	EnergyLevels          []float64 `json:"energyLevels"`
	Duration              float64   `json:"duration"`
	Success               bool      `json:"success"`
	Message               string    `json:"message"`
}

// MolecularStructure represents a molecular simulation result
type MolecularStructure struct {
	Molecule       string                 `json:"molecule"`
	Atoms          []AtomPosition         `json:"atoms"`
	Bonds          []BondInfo             `json:"bonds"`
	VibrationModes []float64              `json:"vibrationModes"`
	Properties     map[string]interface{} `json:"properties"`
}

// AtomPosition represents an atom's position in a molecule
type AtomPosition struct {
	Element       string  `json:"element"`
	X             float64 `json:"x"`
	Y             float64 `json:"y"`
	Z             float64 `json:"z"`
	PartialCharge float64 `json:"partialCharge"`
}

// BondInfo represents bond information between atoms
type BondInfo struct {
	AtomA     int     `json:"atomA"`
	AtomB     int     `json:"atomB"`
	BondOrder int     `json:"bondOrder"`
	Length    float64 `json:"length"`
}

// MaterialProperties represents simulated material properties
type MaterialProperties struct {
	Name             string                 `json:"name"`
	Conductivity     float64                `json:"conductivity"`
	BandGap          float64                `json:"bandGap"`
	RefractiveIndex  float64                `json:"refractiveIndex"`
	Density          float64                `json:"density"`
	ElasticModulus   float64                `json:"elasticModulus"`
	CustomProperties map[string]interface{} `json:"customProperties"`
}

// SimulationConfig holds configuration for quantum simulations
type SimulationConfig struct {
	ElementSymbol      string                 `json:"element"`
	SimulationType     string                 `json:"type"` // "electron_config", "molecular", "material"
	NumberOfShots      int                    `json:"shots"`
	TargetProvider     string                 `json:"provider"` // "ionq", "simulator"
	Parameters         map[string]interface{} `json:"parameters"`
	IncludeSpatialData bool                   `json:"includeSpatialData"`
}
