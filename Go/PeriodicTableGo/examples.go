package periodictable

import (
	"encoding/json"
	"fmt"
)

// Example usage of the periodic table application
func Example_BasicUsage() {
	// Initialize the application
	app := NewPeriodicTableApp()

	// Select an element
	visual, _ := app.SelectElement("C")
	fmt.Printf("Selected: %s (%s)\n", visual.Element.Symbol, visual.Element.Name)

	// Run quantum simulation
	results, _ := app.RunQuantumSimulation("C")
	fmt.Printf("Simulation completed: %s\n", results.SimulationID)

	// Get visualization scene
	scene, _ := app.GetElementVisualScene("C")
	fmt.Printf("Scene created with %d objects\n", len(scene.Objects))
}

// Example of molecular simulation
func Example_MolecularSimulation() {
	app := NewPeriodicTableApp()

	// Simulate a water molecule (H2O)
	scene, _ := app.SimulateMolecule("H2O", []string{"H", "O", "H"})
	fmt.Printf("Molecular scene: %s\n", scene.Name)
	fmt.Printf("Objects in scene: %d\n", len(scene.Objects))

	// Export to JSON for frontend rendering
	jsonData, _ := app.ModelGenerator.ExportSceneToJSON(scene)
	fmt.Printf("Scene JSON length: %d bytes\n", len(jsonData))
}

// Example of material properties simulation
func Example_MaterialSimulation() {
	app := NewPeriodicTableApp()

	composition := map[string]float64{
		"Si": 1.0,
	}

	props, _ := app.SimulateMaterialProperties("Silicon", composition)
	fmt.Printf("Material: %s\n", props.Name)
	fmt.Printf("Band Gap: %.2f eV\n", props.BandGap)
	fmt.Printf("Conductivity: %.2e S/m\n", props.Conductivity)
}

// Example of quantum integration
func Example_QuantumIntegration() {
	app := NewPeriodicTableApp()

	// Configure for Azure Quantum with IonQ
	_ = app.ConfigureQuantumProvider("ionq", "workspace-id", "auth-token")

	// Create quantum proxy
	proxy := NewQuantumRDProxy("workspace", "subscription", "location", "resource-group", "ionq", true)

	// Run electron configuration simulation
	results, _ := proxy.RunElectronConfigurationSimulation("O", 8, 8)
	fmt.Printf("Quantum simulation results: %s\n", results.SimulationID)
	fmt.Printf("Success: %v\n", results.Success)
}

// Example of UI event handling
func Example_UIEventHandling() {
	app := NewPeriodicTableApp()
	uiController := NewUIController(app)
	uiController.StartEventProcessor()

	// Create UI event to select element
	event := UIEvent{
		EventType: "select_element",
		SourceID:  "ui_1",
		Data: map[string]interface{}{
			"symbol": "Au",
		},
	}

	response := uiController.ProcessEvent(event)
	fmt.Printf("Response: %s\n", response.Message)
	fmt.Printf("Success: %v\n", response.Success)
}

// Example of animation
func Example_Animation() {
	app := NewPeriodicTableApp()
	app.SelectElement("Fe")

	// Run animation for a few frames
	for i := 0; i < 5; i++ {
		_ = app.AnimateCurrentElement(i)
	}

	fmt.Println("Animation frames processed")
}

// Example of dashboard
func Example_Dashboard() {
	app := NewPeriodicTableApp()
	app.SelectElement("H")
	app.RunQuantumSimulation("H")

	dashboard := app.GetDashboardData()

	// Convert to JSON for display
	jsonData, _ := json.MarshalIndent(dashboard, "", "  ")
	fmt.Printf("Dashboard JSON:\n%s\n", string(jsonData))
}

// Example of complete R&D workflow
func Example_RDWorkflow() {
	// Initialize app and components
	app := NewPeriodicTableApp()
	proxy := NewQuantumRDProxy("ws", "sub", "loc", "rg", "simulator", false)
	workflow := NewIntegrationWorkflow()

	// Step 1: Select element
	workflow.AddStep("element_selection", "Select carbon element", map[string]string{"element": "C"})
	visual, _ := app.SelectElement("C")
	workflow.CompleteStep(0, visual, 0.1)

	// Step 2: Run quantum simulation
	workflow.AddStep("quantum_simulation", "Run electron config simulation", nil)
	results, _ := proxy.RunElectronConfigurationSimulation("C", 6, 6)
	workflow.CompleteStep(1, results, 0.542)

	// Step 3: Generate 3D model
	workflow.AddStep("model_generation", "Generate 3D visualization", nil)
	visual.UpdateFromQuantumResults(*results)
	scene := app.ModelGenerator.ConvertVisualToScene(visual)
	workflow.CompleteStep(2, scene, 0.2)

	// Display workflow summary
	summary := workflow.GetWorkflowSummary()
	fmt.Printf("Workflow Summary:\n")
	fmt.Printf("  Total Steps: %d\n", summary["total_steps"])
	fmt.Printf("  Completed: %d\n", summary["completed"])
	fmt.Printf("  Total Time: %.2f seconds\n", summary["total_time_sec"])
}

// Example of caching and performance
func Example_CachingPerformance() {
	app := NewPeriodicTableApp()

	// First run - no cache
	app.RunQuantumSimulation("C")
	stats1 := app.ResearchAgent.GetCacheStats()
	fmt.Printf("After first simulation - Cached: %d\n", stats1["cached_simulations"])

	// Second run - from cache
	app.RunQuantumSimulation("C")
	stats2 := app.ResearchAgent.GetCacheStats()
	fmt.Printf("After second simulation - Cached: %d\n", stats2["cached_simulations"])

	// Clear cache
	app.ClearCache()
	stats3 := app.ResearchAgent.GetCacheStats()
	fmt.Printf("After clear - Cached: %d\n", stats3["cached_simulations"])
}
