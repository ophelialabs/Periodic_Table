package main

import (
	"encoding/json"
	"fmt"

	pt "github.com/jesse/periodictable"
)

func main() {
	fmt.Println("=" * 60)
	fmt.Println("Interactive Periodic Table - Desktop Application")
	fmt.Println("With Quantum Computing Integration")
	fmt.Println("=" * 60)
	fmt.Println()

	// Initialize the application
	fmt.Println("Initializing application...")
	app := pt.NewPeriodicTableApp()
	uiController := pt.NewUIController(app)
	uiController.StartEventProcessor()

	// Demo 1: Element Selection and Visualization
	fmt.Println("\n--- Demo 1: Element Selection ---")
	demonstrateElementSelection(app)

	// Demo 2: Quantum Simulation
	fmt.Println("\n--- Demo 2: Quantum Simulation ---")
	demonstrateQuantumSimulation(app)

	// Demo 3: Scene Generation
	fmt.Println("\n--- Demo 3: 3D Scene Generation ---")
	demonstrateSceneGeneration(app)

	// Demo 4: Molecular Simulation
	fmt.Println("\n--- Demo 4: Molecular Simulation ---")
	demonstrateMolecularSimulation(app)

	// Demo 5: Material Properties
	fmt.Println("\n--- Demo 5: Material Properties ---")
	demonstrateMaterialProperties(app)

	// Demo 6: UI Event Handling
	fmt.Println("\n--- Demo 6: UI Event Handling ---")
	demonstrateUIEvents(uiController)

	// Demo 7: Dashboard and Statistics
	fmt.Println("\n--- Demo 7: Dashboard & Statistics ---")
	demonstrateDashboard(app)

	// Demo 8: Quantum Integration
	fmt.Println("\n--- Demo 8: Quantum Integration Layer ---")
	demonstrateQuantumIntegration(app)

	fmt.Println("\n" + "="*60)
	fmt.Println("Application Demo Complete!")
	fmt.Println("=" * 60)
}

func demonstrateElementSelection(app *pt.PeriodicTableApp) {
	elements := []string{"H", "C", "O", "Fe", "Au"}

	for _, symbol := range elements {
		visual, err := app.SelectElement(symbol)
		if err != nil {
			fmt.Printf("Error selecting %s: %v\n", symbol, err)
			continue
		}

		fmt.Printf("✓ Selected: %s (%s)\n", visual.Element.Symbol, visual.Element.Name)
		fmt.Printf("  Atomic #: %d, Electrons: %d\n", visual.Element.AtomicNumber, visual.Element.Electrons)
		fmt.Printf("  Electron Orbitals: %d\n", len(visual.ElectronOrbitals))
	}
}

func demonstrateQuantumSimulation(app *pt.PeriodicTableApp) {
	symbols := []string{"C", "O", "Fe"}

	for _, symbol := range symbols {
		results, err := app.RunQuantumSimulation(symbol)
		if err != nil {
			fmt.Printf("Error simulating %s: %v\n", symbol, err)
			continue
		}

		fmt.Printf("✓ Simulation for %s completed\n", symbol)
		fmt.Printf("  Simulation ID: %s\n", results.SimulationID)
		fmt.Printf("  Duration: %.3f seconds\n", results.Duration)
		fmt.Printf("  Electron Probabilities: %d values\n", len(results.ElectronProbabilities))
		fmt.Printf("  Energy Levels: %d values\n", len(results.EnergyLevels))
	}
}

func demonstrateSceneGeneration(app *pt.PeriodicTableApp) {
	scenes := []string{"C", "O", "Au"}

	for _, symbol := range scenes {
		scene, err := app.GetElementVisualScene(symbol)
		if err != nil {
			fmt.Printf("Error generating scene for %s: %v\n", symbol, err)
			continue
		}

		fmt.Printf("✓ Scene generated for %s\n", symbol)
		fmt.Printf("  Scene ID: %s\n", scene.ID)
		fmt.Printf("  Objects: %d\n", len(scene.Objects))

		// Count objects by type
		typeCount := make(map[string]int)
		for _, obj := range scene.Objects {
			typeCount[obj.Type]++
		}
		fmt.Printf("  Object breakdown: %+v\n", typeCount)
	}
}

func demonstrateMolecularSimulation(app *pt.PeriodicTableApp) {
	molecules := []struct {
		name  string
		atoms []string
	}{
		{"Water", []string{"H", "O", "H"}},
		{"Carbon Dioxide", []string{"C", "O", "O"}},
		{"Methane", []string{"C", "H", "H", "H"}},
	}

	for _, mol := range molecules {
		scene, err := app.SimulateMolecule(mol.name, mol.atoms)
		if err != nil {
			fmt.Printf("Error simulating %s: %v\n", mol.name, err)
			continue
		}

		fmt.Printf("✓ %s simulation completed\n", mol.name)
		fmt.Printf("  Scene: %s\n", scene.Name)
		fmt.Printf("  Objects: %d (atoms + bonds)\n", len(scene.Objects))
	}
}

func demonstrateMaterialProperties(app *pt.PeriodicTableApp) {
	materials := []struct {
		name        string
		composition map[string]float64
	}{
		{"Silicon", map[string]float64{"Si": 1.0}},
		{"Silicon Carbide", map[string]float64{"Si": 0.5, "C": 0.5}},
		{"Gallium Arsenide", map[string]float64{"Ga": 0.5, "As": 0.5}},
	}

	for _, mat := range materials {
		props, err := app.SimulateMaterialProperties(mat.name, mat.composition)
		if err != nil {
			fmt.Printf("Error simulating %s: %v\n", mat.name, err)
			continue
		}

		fmt.Printf("✓ %s properties calculated\n", props.Name)
		fmt.Printf("  Band Gap: %.2f eV\n", props.BandGap)
		fmt.Printf("  Conductivity: %.2e S/m\n", props.Conductivity)
		fmt.Printf("  Refractive Index: %.2f\n", props.RefractiveIndex)
		fmt.Printf("  Density: %.2f g/cm³\n", props.Density)
	}
}

func demonstrateUIEvents(controller *pt.UIController) {
	events := []pt.UIEvent{
		{
			EventType: "select_element",
			SourceID:  "ui_event_1",
			Data: map[string]interface{}{
				"symbol": "Au",
			},
		},
		{
			EventType: "run_simulation",
			SourceID:  "ui_event_2",
			Data: map[string]interface{}{
				"symbol": "Au",
			},
		},
		{
			EventType: "get_scene",
			SourceID:  "ui_event_3",
			Data: map[string]interface{}{
				"symbol": "Au",
			},
		},
	}

	for _, event := range events {
		response := controller.ProcessEvent(event)
		fmt.Printf("✓ Event: %s\n", event.EventType)
		fmt.Printf("  Success: %v\n", response.Success)
		fmt.Printf("  Message: %s\n", response.Message)
		fmt.Printf("  Response Time: %.3f ms\n", response.ResponseTime*1000)
	}
}

func demonstrateDashboard(app *pt.PeriodicTableApp) {
	dashboard := app.GetDashboardData()

	fmt.Println("✓ Dashboard data retrieved")

	// Pretty print dashboard as JSON
	jsonData, _ := json.MarshalIndent(dashboard, "  ", "  ")
	fmt.Println("  Dashboard Summary:")
	fmt.Printf("%s\n", string(jsonData))
}

func demonstrateQuantumIntegration(app *pt.PeriodicTableApp) {
	// Configure quantum provider
	fmt.Println("Configuring Quantum Provider...")
	app.ConfigureQuantumProvider("ionq", "workspace-123", "token-xyz")

	// Create quantum proxy
	proxy := pt.NewQuantumRDProxy(
		"workspace-123",
		"subscription-456",
		"eastus",
		"resource-group",
		"ionq",
		false, // hardware disabled for demo
	)

	fmt.Printf("✓ Quantum Proxy Created\n")
	fmt.Printf("  Provider: %s\n", proxy.TargetProvider)
	fmt.Printf("  Workspace: %s\n", proxy.WorkspaceID)

	// Run electron configuration simulation via proxy
	results, err := proxy.RunElectronConfigurationSimulation("C", 6, 6)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	fmt.Printf("✓ Electron Configuration Simulation via Q#\n")
	fmt.Printf("  Element: %s\n", results.ElementSymbol)
	fmt.Printf("  Simulation ID: %s\n", results.SimulationID)
	fmt.Printf("  Success: %v\n", results.Success)
	fmt.Printf("  Duration: %.3f seconds\n", results.Duration)

	// Run molecular simulation
	molStruct, _ := proxy.RunMolecularSimulation("H2O", []int{1, 8, 1})
	fmt.Printf("✓ Molecular Simulation via Q#\n")
	fmt.Printf("  Molecule: %s\n", molStruct.Molecule)
	fmt.Printf("  Atoms: %d\n", len(molStruct.Atoms))
	fmt.Printf("  Bonds: %d\n", len(molStruct.Bonds))

	// Run material properties simulation
	matProps, _ := proxy.RunMaterialPropertiesSimulation("Silicon", map[string]float64{"Si": 1.0})
	fmt.Printf("✓ Material Properties Simulation via Q#\n")
	fmt.Printf("  Material: %s\n", matProps.Name)
	fmt.Printf("  Band Gap: %.2f eV\n", matProps.BandGap)
	fmt.Printf("  Conductivity: %.2e S/m\n", matProps.Conductivity)

	// Demonstrate integration workflow
	fmt.Println("\n✓ R&D Integration Workflow:")
	workflow := pt.NewIntegrationWorkflow()

	workflow.AddStep("element_selection", "Select element", map[string]string{"element": "C"})
	workflow.CompleteStep(0, "Element selected", 0.05)

	workflow.AddStep("quantum_sim", "Run Q# simulation", nil)
	workflow.CompleteStep(1, results, 0.542)

	workflow.AddStep("model_gen", "Generate 3D model", nil)
	workflow.CompleteStep(2, "Model generated", 0.15)

	summary := workflow.GetWorkflowSummary()
	fmt.Printf("  Total Steps: %d\n", summary["total_steps"])
	fmt.Printf("  Completed: %d\n", summary["completed"])
	fmt.Printf("  Total Time: %.3f seconds\n", summary["total_time_sec"])
}

// Helper function for string repetition
func stringRepeat(s string, count int) string {
	result := ""
	for i := 0; i < count; i++ {
		result += s
	}
	return result
}
