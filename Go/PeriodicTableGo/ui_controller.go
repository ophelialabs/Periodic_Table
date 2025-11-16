package periodictable

import (
	"encoding/json"
	"fmt"
	"sync"
	"time"
)

// UIEvent represents an event from the UI
type UIEvent struct {
	EventType string                 `json:"eventType"`
	Timestamp time.Time              `json:"timestamp"`
	SourceID  string                 `json:"sourceId"`
	Data      map[string]interface{} `json:"data"`
}

// UIResponse represents a response to the UI
type UIResponse struct {
	Success      bool        `json:"success"`
	Message      string      `json:"message"`
	Data         interface{} `json:"data"`
	EventID      string      `json:"eventId"`
	ResponseTime float64     `json:"responseTime"`
}

// UIController handles communication between the UI and the application
type UIController struct {
	App               *PeriodicTableApp
	EventQueue        chan UIEvent
	ResponseChan      chan UIResponse
	Mutex             sync.RWMutex
	EventHandlers     map[string]func(UIEvent) UIResponse
	RunningAnimations map[string]bool
}

// NewUIController creates a new UI controller
func NewUIController(app *PeriodicTableApp) *UIController {
	uc := &UIController{
		App:               app,
		EventQueue:        make(chan UIEvent, 100),
		ResponseChan:      make(chan UIResponse, 100),
		EventHandlers:     make(map[string]func(UIEvent) UIResponse),
		RunningAnimations: make(map[string]bool),
	}

	uc.registerEventHandlers()
	return uc
}

// registerEventHandlers registers all event handlers
func (uc *UIController) registerEventHandlers() {
	uc.EventHandlers["select_element"] = uc.handleSelectElement
	uc.EventHandlers["run_simulation"] = uc.handleRunSimulation
	uc.EventHandlers["simulate_molecule"] = uc.handleSimulateMolecule
	uc.EventHandlers["simulate_material"] = uc.handleSimulateMaterial
	uc.EventHandlers["start_animation"] = uc.handleStartAnimation
	uc.EventHandlers["stop_animation"] = uc.handleStopAnimation
	uc.EventHandlers["get_dashboard"] = uc.handleGetDashboard
	uc.EventHandlers["get_scene"] = uc.handleGetScene
	uc.EventHandlers["configure_quantum"] = uc.handleConfigureQuantum
	uc.EventHandlers["export_scene"] = uc.handleExportScene
}

// ProcessEvent processes a UI event
func (uc *UIController) ProcessEvent(event UIEvent) UIResponse {
	startTime := time.Now()

	handler, exists := uc.EventHandlers[event.EventType]
	if !exists {
		return UIResponse{
			Success:      false,
			Message:      fmt.Sprintf("Unknown event type: %s", event.EventType),
			EventID:      event.SourceID,
			ResponseTime: time.Since(startTime).Seconds(),
		}
	}

	response := handler(event)
	response.ResponseTime = time.Since(startTime).Seconds()
	response.EventID = event.SourceID
	return response
}

// handleSelectElement handles element selection
func (uc *UIController) handleSelectElement(event UIEvent) UIResponse {
	symbol, ok := event.Data["symbol"].(string)
	if !ok {
		return UIResponse{Success: false, Message: "Invalid symbol"}
	}

	visual, err := uc.App.SelectElement(symbol)
	if err != nil {
		return UIResponse{Success: false, Message: err.Error()}
	}

	return UIResponse{
		Success: true,
		Message: fmt.Sprintf("Selected element: %s", symbol),
		Data: map[string]interface{}{
			"element":   visual.Element.Symbol,
			"name":      visual.Element.Name,
			"electrons": visual.Element.Electrons,
			"protons":   visual.Element.Protons,
		},
	}
}

// handleRunSimulation handles quantum simulation requests
func (uc *UIController) handleRunSimulation(event UIEvent) UIResponse {
	symbol, ok := event.Data["symbol"].(string)
	if !ok {
		return UIResponse{Success: false, Message: "Invalid symbol"}
	}

	results, err := uc.App.RunQuantumSimulation(symbol)
	if err != nil {
		return UIResponse{Success: false, Message: err.Error()}
	}

	return UIResponse{
		Success: true,
		Message: "Simulation completed",
		Data: map[string]interface{}{
			"element":      results.ElementSymbol,
			"simulationId": results.SimulationID,
			"success":      results.Success,
			"duration":     results.Duration,
			"numElectrons": len(results.ElectronProbabilities),
			"energyLevels": results.EnergyLevels,
		},
	}
}

// handleSimulateMolecule handles molecular simulation requests
func (uc *UIController) handleSimulateMolecule(event UIEvent) UIResponse {
	molecule, ok := event.Data["molecule"].(string)
	if !ok {
		return UIResponse{Success: false, Message: "Invalid molecule name"}
	}

	atoms, ok := event.Data["atoms"].([]interface{})
	if !ok {
		return UIResponse{Success: false, Message: "Invalid atoms list"}
	}

	atomStrings := make([]string, len(atoms))
	for i, a := range atoms {
		if str, ok := a.(string); ok {
			atomStrings[i] = str
		}
	}

	scene, err := uc.App.SimulateMolecule(molecule, atomStrings)
	if err != nil {
		return UIResponse{Success: false, Message: err.Error()}
	}

	return UIResponse{
		Success: true,
		Message: fmt.Sprintf("Molecular simulation for %s completed", molecule),
		Data: map[string]interface{}{
			"molecule":    scene.Name,
			"objectCount": len(scene.Objects),
			"sceneId":     scene.ID,
		},
	}
}

// handleSimulateMaterial handles material property simulation requests
func (uc *UIController) handleSimulateMaterial(event UIEvent) UIResponse {
	material, ok := event.Data["material"].(string)
	if !ok {
		return UIResponse{Success: false, Message: "Invalid material name"}
	}

	composition, ok := event.Data["composition"].(map[string]float64)
	if !ok {
		// Try to parse composition from generic map
		compInterface, ok := event.Data["composition"].(map[string]interface{})
		if !ok {
			return UIResponse{Success: false, Message: "Invalid composition"}
		}

		composition = make(map[string]float64)
		for k, v := range compInterface {
			if f, ok := v.(float64); ok {
				composition[k] = f
			}
		}
	}

	props, err := uc.App.SimulateMaterialProperties(material, composition)
	if err != nil {
		return UIResponse{Success: false, Message: err.Error()}
	}

	return UIResponse{
		Success: true,
		Message: fmt.Sprintf("Material simulation for %s completed", material),
		Data: map[string]interface{}{
			"material":        props.Name,
			"conductivity":    props.Conductivity,
			"bandGap":         props.BandGap,
			"refractiveIndex": props.RefractiveIndex,
			"density":         props.Density,
		},
	}
}

// handleStartAnimation handles animation start requests
func (uc *UIController) handleStartAnimation(event UIEvent) UIResponse {
	element, ok := event.Data["element"].(string)
	if !ok {
		return UIResponse{Success: false, Message: "Invalid element"}
	}

	uc.Mutex.Lock()
	if uc.RunningAnimations[element] {
		uc.Mutex.Unlock()
		return UIResponse{Success: false, Message: "Animation already running"}
	}
	uc.RunningAnimations[element] = true
	uc.Mutex.Unlock()

	go uc.animationLoop(element)

	return UIResponse{
		Success: true,
		Message: fmt.Sprintf("Animation started for %s", element),
		Data: map[string]interface{}{
			"element": element,
			"status":  "running",
		},
	}
}

// handleStopAnimation handles animation stop requests
func (uc *UIController) handleStopAnimation(event UIEvent) UIResponse {
	element, ok := event.Data["element"].(string)
	if !ok {
		return UIResponse{Success: false, Message: "Invalid element"}
	}

	uc.Mutex.Lock()
	uc.RunningAnimations[element] = false
	uc.Mutex.Unlock()

	return UIResponse{
		Success: true,
		Message: fmt.Sprintf("Animation stopped for %s", element),
	}
}

// handleGetDashboard handles dashboard data requests
func (uc *UIController) handleGetDashboard(event UIEvent) UIResponse {
	dashboardData := uc.App.GetDashboardData()

	return UIResponse{
		Success: true,
		Message: "Dashboard data retrieved",
		Data:    dashboardData,
	}
}

// handleGetScene handles scene data requests
func (uc *UIController) handleGetScene(event UIEvent) UIResponse {
	symbol, ok := event.Data["symbol"].(string)
	if !ok {
		return UIResponse{Success: false, Message: "Invalid symbol"}
	}

	scene, err := uc.App.GetElementVisualScene(symbol)
	if err != nil {
		return UIResponse{Success: false, Message: err.Error()}
	}

	return UIResponse{
		Success: true,
		Message: "Scene data retrieved",
		Data:    scene,
	}
}

// handleConfigureQuantum handles quantum provider configuration
func (uc *UIController) handleConfigureQuantum(event UIEvent) UIResponse {
	provider, ok := event.Data["provider"].(string)
	if !ok {
		return UIResponse{Success: false, Message: "Invalid provider"}
	}

	workspace := ""
	token := ""

	if w, ok := event.Data["workspace"].(string); ok {
		workspace = w
	}
	if t, ok := event.Data["token"].(string); ok {
		token = t
	}

	err := uc.App.ConfigureQuantumProvider(provider, workspace, token)
	if err != nil {
		return UIResponse{Success: false, Message: err.Error()}
	}

	return UIResponse{
		Success: true,
		Message: fmt.Sprintf("Quantum provider configured to: %s", provider),
		Data: map[string]interface{}{
			"provider":  provider,
			"workspace": workspace,
		},
	}
}

// handleExportScene handles scene export requests
func (uc *UIController) handleExportScene(event UIEvent) UIResponse {
	symbol, ok := event.Data["symbol"].(string)
	if !ok {
		return UIResponse{Success: false, Message: "Invalid symbol"}
	}

	sceneJSON, err := uc.App.ExportCurrentScene(symbol)
	if err != nil {
		return UIResponse{Success: false, Message: err.Error()}
	}

	// Parse back to get the scene object for the response
	var scene Scene
	json.Unmarshal([]byte(sceneJSON), &scene)

	return UIResponse{
		Success: true,
		Message: "Scene exported successfully",
		Data: map[string]interface{}{
			"scene": scene,
			"json":  sceneJSON,
		},
	}
}

// animationLoop runs the animation for an element
func (uc *UIController) animationLoop(element string) {
	frameNum := 0
	ticker := time.NewTicker(time.Millisecond * 33) // ~30 FPS
	defer ticker.Stop()

	for {
		uc.Mutex.RLock()
		isRunning := uc.RunningAnimations[element]
		uc.Mutex.RUnlock()

		if !isRunning {
			break
		}

		err := uc.App.AnimateCurrentElement(frameNum)
		if err != nil {
			// Element might have changed
			break
		}

		frameNum++
		<-ticker.C
	}
}

// QueueEvent queues a UI event for processing
func (uc *UIController) QueueEvent(event UIEvent) {
	select {
	case uc.EventQueue <- event:
	default:
		// Queue is full, log warning
		fmt.Println("Event queue full, dropping event:", event.EventType)
	}
}

// StartEventProcessor starts processing events from the queue
func (uc *UIController) StartEventProcessor() {
	go func() {
		for event := range uc.EventQueue {
			response := uc.ProcessEvent(event)
			select {
			case uc.ResponseChan <- response:
			default:
				fmt.Println("Response channel full")
			}
		}
	}()
}

// GetResponse retrieves a response from the response channel
func (uc *UIController) GetResponse(timeout time.Duration) (UIResponse, bool) {
	select {
	case response := <-uc.ResponseChan:
		return response, true
	case <-time.After(timeout):
		return UIResponse{Success: false, Message: "Response timeout"}, false
	}
}
