package periodictable

import (
	"fmt"
	"math"
)

// ElementVisual handles the 3D visual representation of an element
type ElementVisual struct {
	Element          *Element
	Position         Vec3
	Scale            Vec3
	Rotation         Vec3
	ElectronSpheres  []ElectronSphere
	NucleusRadius    float64
	ElectronOrbitals []Orbital
}

// Vec3 represents a 3D vector
type Vec3 struct {
	X, Y, Z float64
}

// ElectronSphere represents a single electron visualization
type ElectronSphere struct {
	Position   Vec3
	Radius     float64
	Energy     float64
	OrbitalNum int
	Color      string
}

// Orbital represents an electron orbital
type Orbital struct {
	Number    int
	Electrons int
	Radius    float64
	Color     string
}

// NewElementVisual creates a new visual representation of an element
func NewElementVisual(elem *Element) *ElementVisual {
	ev := &ElementVisual{
		Element:       elem,
		Position:      Vec3{X: 0, Y: 0, Z: 0},
		Scale:         Vec3{X: 1, Y: 1, Z: 1},
		Rotation:      Vec3{X: 0, Y: 0, Z: 0},
		NucleusRadius: float64(elem.Protons) * 0.5,
	}
	ev.generateElectronConfiguration()
	return ev
}

// generateElectronConfiguration creates electrons based on the element's configuration
func (ev *ElementVisual) generateElectronConfiguration() {
	orbitalRadii := []float64{1.0, 2.0, 3.0, 4.0, 5.0}
	electronConfig := make([]int, 5)

	// Parse electron configuration (simplified)
	// For a more complete implementation, parse ElectronConfig string
	switch ev.Element.Electrons {
	case 1:
		electronConfig = []int{1, 0, 0, 0, 0}
	case 2:
		electronConfig = []int{2, 0, 0, 0, 0}
	case 6:
		electronConfig = []int{2, 4, 0, 0, 0}
	case 8:
		electronConfig = []int{2, 6, 0, 0, 0}
	case 26:
		electronConfig = []int{2, 8, 14, 2, 0}
	case 79:
		electronConfig = []int{2, 8, 18, 32, 1}
	default:
		// Default: fill shells sequentially
		remaining := ev.Element.Electrons
		for i := 0; i < len(electronConfig) && remaining > 0; i++ {
			maxElectrons := 2 * (i + 1) * (i + 1)
			if remaining >= maxElectrons {
				electronConfig[i] = maxElectrons
				remaining -= maxElectrons
			} else {
				electronConfig[i] = remaining
				remaining = 0
			}
		}
	}

	// Generate electron spheres
	sphereID := 0
	for orbitalNum, numElectrons := range electronConfig {
		if numElectrons == 0 {
			continue
		}

		orbital := Orbital{
			Number:    orbitalNum + 1,
			Electrons: numElectrons,
			Radius:    orbitalRadii[orbitalNum],
			Color:     ev.generateOrbitalColor(orbitalNum),
		}
		ev.ElectronOrbitals = append(ev.ElectronOrbitals, orbital)

		// Generate electron positions around the orbital
		for i := 0; i < numElectrons; i++ {
			angle := (2 * math.Pi * float64(i)) / float64(numElectrons)
			x := orbital.Radius * math.Cos(angle)
			z := orbital.Radius * math.Sin(angle)
			y := 0.1 * math.Sin(float64(sphereID)*0.5)

			sphere := ElectronSphere{
				Position:   Vec3{X: x, Y: y, Z: z},
				Radius:     0.15,
				Energy:     float64(orbitalNum) * 0.5,
				OrbitalNum: orbitalNum + 1,
				Color:      orbital.Color,
			}
			ev.ElectronSpheres = append(ev.ElectronSpheres, sphere)
			sphereID++
		}
	}
}

// generateOrbitalColor generates a color based on orbital number
func (ev *ElementVisual) generateOrbitalColor(orbitalNum int) string {
	colors := []string{
		"#FF6B6B", // Red
		"#4ECDC4", // Teal
		"#45B7D1", // Blue
		"#FFA07A", // Light salmon
		"#98D8C8", // Mint
	}
	if orbitalNum < len(colors) {
		return colors[orbitalNum]
	}
	return "#CCCCCC"
}

// UpdatePosition updates the visual position
func (ev *ElementVisual) UpdatePosition(x, y, z float64) {
	ev.Position = Vec3{X: x, Y: y, Z: z}
}

// Rotate rotates the visual representation
func (ev *ElementVisual) Rotate(rx, ry, rz float64) {
	ev.Rotation = Vec3{X: rx, Y: ry, Z: rz}
}

// GetVisualizationData returns the current state as a map for rendering
func (ev *ElementVisual) GetVisualizationData() map[string]interface{} {
	return map[string]interface{}{
		"element":           ev.Element.Symbol,
		"elementName":       ev.Element.Name,
		"position":          ev.Position,
		"scale":             ev.Scale,
		"rotation":          ev.Rotation,
		"nucleusRadius":     ev.NucleusRadius,
		"nucleusColor":      ev.Element.Color,
		"electronSpheres":   ev.ElectronSpheres,
		"electronOrbitals":  ev.ElectronOrbitals,
		"totalElectrons":    ev.Element.Electrons,
		"atomicNumber":      ev.Element.AtomicNumber,
		"atomicMass":        ev.Element.AtomicMass,
		"electronConfig":    ev.Element.ElectronConfig,
		"electronegativity": ev.Element.Electronegativity,
	}
}

// UpdateFromQuantumResults updates the visual based on quantum simulation results
func (ev *ElementVisual) UpdateFromQuantumResults(results QuantumResults) {
	// Update electron positions based on probability distribution
	for i, prob := range results.ElectronProbabilities {
		if i < len(ev.ElectronSpheres) {
			// Scale position based on probability
			scale := math.Sqrt(prob)
			orbital := ev.ElectronOrbitals[ev.ElectronSpheres[i].OrbitalNum-1]
			angle := (2 * math.Pi * float64(i)) / float64(len(ev.ElectronSpheres))

			ev.ElectronSpheres[i].Position = Vec3{
				X: orbital.Radius * scale * math.Cos(angle),
				Y: scale * 0.5 * math.Sin(float64(i)*0.3),
				Z: orbital.Radius * scale * math.Sin(angle),
			}
			ev.ElectronSpheres[i].Energy = prob
		}
	}

	// Update nucleus based on spatial distribution
	if len(results.SpatialData) > 0 {
		ev.NucleusRadius = float64(ev.Element.Protons)*0.5 + results.SpatialData[0]*0.2
	}
}

// DebugInfo returns debug information about the visual
func (ev *ElementVisual) DebugInfo() string {
	return fmt.Sprintf(
		"Element: %s (%s), Electrons: %d, Orbitals: %d, Position: (%.2f, %.2f, %.2f)",
		ev.Element.Symbol,
		ev.Element.Name,
		ev.Element.Electrons,
		len(ev.ElectronOrbitals),
		ev.Position.X, ev.Position.Y, ev.Position.Z,
	)
}
