package periodictable

import (
	"encoding/json"
	"fmt"
	"math"
	"time"
)

// DynamicModelGenerator creates and manages 3D models based on quantum results
type DynamicModelGenerator struct {
	ElementDatabase  *ElementDatabase
	GeneratedModels  map[string]*ElementVisual
	RenderingContext RenderingContext
	AnimationEnabled bool
	CurrentAnimFrame int
}

// RenderingContext holds rendering state
type RenderingContext struct {
	ViewMatrix    [16]float64 `json:"viewMatrix"`
	ProjectMatrix [16]float64 `json:"projectMatrix"`
	CameraPos     Vec3        `json:"cameraPos"`
	LightPos      Vec3        `json:"lightPos"`
	AmbientLight  float64     `json:"ambientLight"`
}

// SceneObject represents a renderable object
type SceneObject struct {
	ID         string                 `json:"id"`
	Type       string                 `json:"type"` // "nucleus", "electron", "orbital", "bond"
	Position   Vec3                   `json:"position"`
	Scale      Vec3                   `json:"scale"`
	Rotation   Vec3                   `json:"rotation"`
	Color      string                 `json:"color"`
	Material   MaterialDef            `json:"material"`
	Properties map[string]interface{} `json:"properties"`
	Visible    bool                   `json:"visible"`
}

// MaterialDef defines material properties for rendering
type MaterialDef struct {
	Diffuse           string  `json:"diffuse"`
	Specular          string  `json:"specular"`
	Roughness         float64 `json:"roughness"`
	Metallic          float64 `json:"metallic"`
	Transparency      float64 `json:"transparency"`
	EmissiveColor     string  `json:"emissiveColor"`
	EmissiveIntensity float64 `json:"emissiveIntensity"`
}

// Scene represents a complete 3D scene
type Scene struct {
	ID      string        `json:"id"`
	Objects []SceneObject `json:"objects"`
	Name    string        `json:"name"`
}

// NewDynamicModelGenerator creates a new model generator
func NewDynamicModelGenerator(db *ElementDatabase) *DynamicModelGenerator {
	return &DynamicModelGenerator{
		ElementDatabase:  db,
		GeneratedModels:  make(map[string]*ElementVisual),
		AnimationEnabled: true,
		CurrentAnimFrame: 0,
		RenderingContext: RenderingContext{
			CameraPos:    Vec3{X: 0, Y: 5, Z: 10},
			LightPos:     Vec3{X: 5, Y: 10, Z: 5},
			AmbientLight: 0.3,
		},
	}
}

// GenerateElementModel generates a visual model for an element
func (dmg *DynamicModelGenerator) GenerateElementModel(symbol string) (*ElementVisual, error) {
	if model, exists := dmg.GeneratedModels[symbol]; exists {
		return model, nil
	}

	elem := dmg.ElementDatabase.GetElement(symbol)
	if elem == nil {
		return nil, fmt.Errorf("element not found: %s", symbol)
	}

	visual := NewElementVisual(elem)
	dmg.GeneratedModels[symbol] = visual
	return visual, nil
}

// ConvertVisualToScene converts an ElementVisual to a Scene for rendering
func (dmg *DynamicModelGenerator) ConvertVisualToScene(visual *ElementVisual) *Scene {
	scene := &Scene{
		ID:      fmt.Sprintf("scene_%s_%d", visual.Element.Symbol, time.Now().UnixNano()),
		Name:    fmt.Sprintf("%s Atom Model", visual.Element.Name),
		Objects: make([]SceneObject, 0),
	}

	// Add nucleus
	nucleusObj := SceneObject{
		ID:       fmt.Sprintf("nucleus_%s", visual.Element.Symbol),
		Type:     "nucleus",
		Position: visual.Position,
		Scale: Vec3{
			X: visual.NucleusRadius,
			Y: visual.NucleusRadius,
			Z: visual.NucleusRadius,
		},
		Rotation: visual.Rotation,
		Color:    visual.Element.Color,
		Material: MaterialDef{
			Diffuse:           visual.Element.Color,
			Specular:          "#FFFFFF",
			Roughness:         0.2,
			Metallic:          0.8,
			Transparency:      0.0,
			EmissiveColor:     visual.Element.Color,
			EmissiveIntensity: 0.3,
		},
		Properties: map[string]interface{}{
			"protons":  visual.Element.Protons,
			"neutrons": visual.Element.Neutrons,
		},
		Visible: true,
	}
	scene.Objects = append(scene.Objects, nucleusObj)

	// Add electron orbitals (as reference rings)
	for _, orbital := range visual.ElectronOrbitals {
		orbitalObj := SceneObject{
			ID:   fmt.Sprintf("orbital_%d", orbital.Number),
			Type: "orbital",
			Position: Vec3{
				X: visual.Position.X,
				Y: visual.Position.Y,
				Z: visual.Position.Z,
			},
			Scale: Vec3{
				X: orbital.Radius,
				Y: orbital.Radius,
				Z: orbital.Radius,
			},
			Rotation: visual.Rotation,
			Color:    orbital.Color,
			Material: MaterialDef{
				Diffuse:           orbital.Color,
				Specular:          "#FFFFFF",
				Roughness:         0.5,
				Metallic:          0.0,
				Transparency:      0.3,
				EmissiveColor:     orbital.Color,
				EmissiveIntensity: 0.2,
			},
			Properties: map[string]interface{}{
				"electrons":  orbital.Electrons,
				"orbitalNum": orbital.Number,
			},
			Visible: true,
		}
		scene.Objects = append(scene.Objects, orbitalObj)
	}

	// Add electron spheres
	for i, electron := range visual.ElectronSpheres {
		electronObj := SceneObject{
			ID:       fmt.Sprintf("electron_%d", i),
			Type:     "electron",
			Position: electron.Position,
			Scale: Vec3{
				X: electron.Radius,
				Y: electron.Radius,
				Z: electron.Radius,
			},
			Rotation: visual.Rotation,
			Color:    electron.Color,
			Material: MaterialDef{
				Diffuse:           electron.Color,
				Specular:          "#FFFFFF",
				Roughness:         0.1,
				Metallic:          1.0,
				Transparency:      0.1,
				EmissiveColor:     electron.Color,
				EmissiveIntensity: 0.5,
			},
			Properties: map[string]interface{}{
				"energy":     electron.Energy,
				"orbitalNum": electron.OrbitalNum,
			},
			Visible: true,
		}
		scene.Objects = append(scene.Objects, electronObj)
	}

	return scene
}

// UpdateSceneWithQuantumResults updates a scene based on quantum simulation results
func (dmg *DynamicModelGenerator) UpdateSceneWithQuantumResults(scene *Scene, visual *ElementVisual, results *QuantumResults) {
	// Update electron positions based on probabilities
	electronIdx := 0
	for i, obj := range scene.Objects {
		if obj.Type == "electron" && electronIdx < len(results.ElectronProbabilities) {
			// Update color intensity based on probability
			intensity := results.ElectronProbabilities[electronIdx]
			scene.Objects[i].Material.EmissiveIntensity = intensity

			// Update scale based on energy
			if electronIdx < len(results.EnergyLevels) {
				scale := 0.1 + (results.EnergyLevels[electronIdx]/5.0)*0.2
				scene.Objects[i].Scale = Vec3{X: scale, Y: scale, Z: scale}
			}

			electronIdx++
		}
	}
}

// GenerateMolecularScene creates a scene from molecular structure
func (dmg *DynamicModelGenerator) GenerateMolecularScene(molecule *MolecularStructure) *Scene {
	scene := &Scene{
		ID:      fmt.Sprintf("molecule_%d", time.Now().UnixNano()),
		Name:    fmt.Sprintf("%s Molecule Model", molecule.Molecule),
		Objects: make([]SceneObject, 0),
	}

	// Add atoms
	for i, atom := range molecule.Atoms {
		atomObj := SceneObject{
			ID:   fmt.Sprintf("atom_%d", i),
			Type: "nucleus",
			Position: Vec3{
				X: atom.X,
				Y: atom.Y,
				Z: atom.Z,
			},
			Scale: Vec3{X: 0.3, Y: 0.3, Z: 0.3},
			Color: "#FFA500",
			Material: MaterialDef{
				Diffuse:           "#FFA500",
				Specular:          "#FFFFFF",
				Roughness:         0.3,
				Metallic:          0.7,
				Transparency:      0.0,
				EmissiveColor:     "#FFA500",
				EmissiveIntensity: 0.2,
			},
			Properties: map[string]interface{}{
				"element":       atom.Element,
				"partialCharge": atom.PartialCharge,
			},
			Visible: true,
		}
		scene.Objects = append(scene.Objects, atomObj)
	}

	// Add bonds
	for _, bond := range molecule.Bonds {
		bondObj := SceneObject{
			ID:   fmt.Sprintf("bond_%d_%d", bond.AtomA, bond.AtomB),
			Type: "bond",
			Position: Vec3{
				X: (molecule.Atoms[bond.AtomA].X + molecule.Atoms[bond.AtomB].X) / 2,
				Y: (molecule.Atoms[bond.AtomA].Y + molecule.Atoms[bond.AtomB].Y) / 2,
				Z: (molecule.Atoms[bond.AtomA].Z + molecule.Atoms[bond.AtomB].Z) / 2,
			},
			Scale: Vec3{X: 0.1, Y: bond.Length, Z: 0.1},
			Color: "#CCCCCC",
			Material: MaterialDef{
				Diffuse:           "#CCCCCC",
				Specular:          "#FFFFFF",
				Roughness:         0.4,
				Metallic:          0.5,
				Transparency:      0.0,
				EmissiveColor:     "#CCCCCC",
				EmissiveIntensity: 0.1,
			},
			Properties: map[string]interface{}{
				"bondOrder": bond.BondOrder,
				"length":    bond.Length,
			},
			Visible: true,
		}
		scene.Objects = append(scene.Objects, bondObj)
	}

	return scene
}

// SetCameraPosition sets the camera position
func (dmg *DynamicModelGenerator) SetCameraPosition(x, y, z float64) {
	dmg.RenderingContext.CameraPos = Vec3{X: x, Y: y, Z: z}
}

// SetLightPosition sets the light position
func (dmg *DynamicModelGenerator) SetLightPosition(x, y, z float64) {
	dmg.RenderingContext.LightPos = Vec3{X: x, Y: y, Z: z}
}

// AnimateElectrons updates electron positions for animation
func (dmg *DynamicModelGenerator) AnimateElectrons(visual *ElementVisual, frameNum int) {
	angle := float64(frameNum) * 0.1
	for i, electron := range visual.ElectronSpheres {
		orbital := visual.ElectronOrbitals[electron.OrbitalNum-1]
		baseAngle := (2 * 3.14159 * float64(i)) / float64(len(visual.ElectronSpheres))
		currentAngle := baseAngle + angle

		electron.Position = Vec3{
			X: orbital.Radius * math.Cos(currentAngle),
			Y: 0.1 * math.Sin(float64(i)*0.5+angle),
			Z: orbital.Radius * math.Sin(currentAngle),
		}
	}
}

// ExportSceneToJSON exports a scene as JSON
func (dmg *DynamicModelGenerator) ExportSceneToJSON(scene *Scene) (string, error) {
	data, err := json.MarshalIndent(scene, "", "  ")
	if err != nil {
		return "", err
	}
	return string(data), nil
}

// GetModelStatistics returns statistics about generated models
func (dmg *DynamicModelGenerator) GetModelStatistics() map[string]interface{} {
	totalElectrons := 0
	totalOrbitals := 0

	for _, visual := range dmg.GeneratedModels {
		totalElectrons += len(visual.ElectronSpheres)
		totalOrbitals += len(visual.ElectronOrbitals)
	}

	return map[string]interface{}{
		"generated_models":  len(dmg.GeneratedModels),
		"total_electrons":   totalElectrons,
		"total_orbitals":    totalOrbitals,
		"animation_frame":   dmg.CurrentAnimFrame,
		"animation_enabled": dmg.AnimationEnabled,
		"camera_position":   dmg.RenderingContext.CameraPos,
	}
}
