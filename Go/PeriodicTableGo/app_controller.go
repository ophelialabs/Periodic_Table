package periodictable

import (
	"fmt"
	"sync"
)

// PeriodicTableApp is the main application controller
type PeriodicTableApp struct {
	ElementDatabase    *ElementDatabase
	ResearchAgent      *ResearchAgent
	ModelGenerator     *DynamicModelGenerator
	ActiveVisuals      map[string]*ElementVisual
	AppState           map[string]interface{}
	QuantumIntegration *QuantumIntegration
	Mutex              sync.RWMutex
}

// QuantumIntegration handles Q# interoperability
type QuantumIntegration struct {
	TargetProvider  string
	AzureWorkspace  string
	AuthToken       string
	EnableHardware  bool
	SimulationCache map[string]*QuantumResults
	MolecularCache  map[string]*MolecularStructure
	MaterialCache   map[string]*MaterialProperties
}

// NewPeriodicTableApp creates and initializes the main application
func NewPeriodicTableApp() *PeriodicTableApp {
	db := NewElementDatabase()
	processor := &MockQuantumProcessor{Name: "Mock Quantum Backend"}
	agent := NewResearchAgent("agent-1", "Research Agent", processor, db)
	generator := NewDynamicModelGenerator(db)

	return &PeriodicTableApp{
		ElementDatabase: db,
		ResearchAgent:   agent,
		ModelGenerator:  generator,
		ActiveVisuals:   make(map[string]*ElementVisual),
		AppState: map[string]interface{}{
			"current_element":   nil,
			"simulation_mode":   "electron_config",
			"rendering_enabled": true,
			"animation_enabled": true,
		},
		QuantumIntegration: &QuantumIntegration{
			TargetProvider:  "simulator",
			EnableHardware:  false,
			SimulationCache: make(map[string]*QuantumResults),
			MolecularCache:  make(map[string]*MolecularStructure),
			MaterialCache:   make(map[string]*MaterialProperties),
		},
	}
}

// SelectElement selects an element and generates its visual model
func (app *PeriodicTableApp) SelectElement(symbol string) (*ElementVisual, error) {
	app.Mutex.Lock()
	defer app.Mutex.Unlock()

	elem := app.ElementDatabase.GetElement(symbol)
	if elem == nil {
		return nil, fmt.Errorf("element not found: %s", symbol)
	}

	// Generate visual model
	visual, err := app.ModelGenerator.GenerateElementModel(symbol)
	if err != nil {
		return nil, err
	}

	app.ActiveVisuals[symbol] = visual
	app.AppState["current_element"] = symbol

	return visual, nil
}

// RunQuantumSimulation runs a quantum simulation for the selected element
func (app *PeriodicTableApp) RunQuantumSimulation(symbol string) (*QuantumResults, error) {
	results, err := app.ResearchAgent.RunElementSimulation(symbol)
	if err != nil {
		return nil, err
	}

	// Cache results
	app.QuantumIntegration.SimulationCache[symbol] = results

	// Update visual if element is active
	if visual, exists := app.ActiveVisuals[symbol]; exists {
		visual.UpdateFromQuantumResults(*results)
	}

	return results, nil
}

// GetElementVisualScene returns the current element as a scene for rendering
func (app *PeriodicTableApp) GetElementVisualScene(symbol string) (*Scene, error) {
	app.Mutex.RLock()
	visual, exists := app.ActiveVisuals[symbol]
	app.Mutex.RUnlock()

	if !exists {
		_, err := app.SelectElement(symbol)
		if err != nil {
			return nil, err
		}
		app.Mutex.RLock()
		visual = app.ActiveVisuals[symbol]
		app.Mutex.RUnlock()
	}

	scene := app.ModelGenerator.ConvertVisualToScene(visual)
	return scene, nil
}

// SimulateMolecule simulates molecular structure and generates scene
func (app *PeriodicTableApp) SimulateMolecule(molecule string, atoms []string) (*Scene, error) {
	app.Mutex.Lock()
	app.AppState["current_molecule"] = molecule
	app.Mutex.Unlock()

	molecularStruct, err := app.ResearchAgent.RunMolecularSimulation(molecule, atoms)
	if err != nil {
		return nil, err
	}

	// Cache molecule
	app.QuantumIntegration.MolecularCache[molecule] = molecularStruct

	scene := app.ModelGenerator.GenerateMolecularScene(molecularStruct)
	return scene, nil
}

// SimulateMaterialProperties simulates material properties
func (app *PeriodicTableApp) SimulateMaterialProperties(material string, composition map[string]float64) (*MaterialProperties, error) {
	props, err := app.ResearchAgent.RunMaterialPropertySimulation(material, composition)
	if err != nil {
		return nil, err
	}

	// Cache properties
	app.QuantumIntegration.MaterialCache[material] = props

	return props, nil
}

// AnimateCurrentElement animates the current element
func (app *PeriodicTableApp) AnimateCurrentElement(frameNum int) error {
	app.Mutex.RLock()
	currentElem := app.AppState["current_element"]
	app.Mutex.RUnlock()

	if currentElem == nil {
		return fmt.Errorf("no element selected")
	}

	symbol := currentElem.(string)
	visual, exists := app.ActiveVisuals[symbol]
	if !exists {
		return fmt.Errorf("visual not found for element: %s", symbol)
	}

	app.ModelGenerator.AnimateElectrons(visual, frameNum)
	return nil
}

// GetAppStatus returns current application status
func (app *PeriodicTableApp) GetAppStatus() map[string]interface{} {
	app.Mutex.RLock()
	defer app.Mutex.RUnlock()

	return map[string]interface{}{
		"app_state":    app.AppState,
		"agent_status": app.ResearchAgent.GetCacheStats(),
		"model_stats":  app.ModelGenerator.GetModelStatistics(),
		"quantum_integration": map[string]interface{}{
			"target_provider":    app.QuantumIntegration.TargetProvider,
			"hardware_enabled":   app.QuantumIntegration.EnableHardware,
			"cached_simulations": len(app.QuantumIntegration.SimulationCache),
			"cached_molecules":   len(app.QuantumIntegration.MolecularCache),
			"cached_materials":   len(app.QuantumIntegration.MaterialCache),
		},
	}
}

// ConfigureQuantumProvider configures the quantum provider
func (app *PeriodicTableApp) ConfigureQuantumProvider(provider string, workspace string, token string) error {
	app.Mutex.Lock()
	defer app.Mutex.Unlock()

	app.QuantumIntegration.TargetProvider = provider
	app.QuantumIntegration.AzureWorkspace = workspace
	app.QuantumIntegration.AuthToken = token

	if provider == "ionq" {
		app.QuantumIntegration.EnableHardware = true
	}

	return nil
}

// ExportCurrentScene exports the current scene as JSON
func (app *PeriodicTableApp) ExportCurrentScene(symbol string) (string, error) {
	scene, err := app.GetElementVisualScene(symbol)
	if err != nil {
		return "", err
	}

	return app.ModelGenerator.ExportSceneToJSON(scene)
}

// GetElementList returns all available elements
func (app *PeriodicTableApp) GetElementList() []*Element {
	return app.ElementDatabase.GetAllElements()
}

// GetDashboardData returns comprehensive dashboard data
func (app *PeriodicTableApp) GetDashboardData() map[string]interface{} {
	app.Mutex.RLock()
	defer app.Mutex.RUnlock()

	elements := app.ElementDatabase.GetAllElements()
	elementSummary := make([]map[string]interface{}, 0)

	for _, elem := range elements {
		elementSummary = append(elementSummary, map[string]interface{}{
			"symbol":       elem.Symbol,
			"name":         elem.Name,
			"atomicNumber": elem.AtomicNumber,
			"electrons":    elem.Electrons,
			"category":     elem.Category,
		})
	}

	return map[string]interface{}{
		"app_status":     app.AppState,
		"elements":       elementSummary,
		"agent_stats":    app.ResearchAgent.GetCacheStats(),
		"model_stats":    app.ModelGenerator.GetModelStatistics(),
		"quantum_status": app.QuantumIntegration.TargetProvider,
		"active_visuals": len(app.ActiveVisuals),
	}
}

// ClearCache clears all caches
func (app *PeriodicTableApp) ClearCache() {
	app.Mutex.Lock()
	defer app.Mutex.Unlock()

	app.ResearchAgent.ClearCache()
	app.QuantumIntegration.SimulationCache = make(map[string]*QuantumResults)
	app.QuantumIntegration.MolecularCache = make(map[string]*MolecularStructure)
	app.QuantumIntegration.MaterialCache = make(map[string]*MaterialProperties)
}
