#pragma once

#include "ElementData.h"
#include <functional>
#include <memory>

namespace PeriodicTable {

/// <summary>
/// Display modes for element visualization
/// </summary>
enum class VisualizationMode {
    AtomicStructure,
    ElectronConfiguration,
    MolecularBond,
    CrystalStructure,
    QuantumProbabilityDensity
};

/// <summary>
/// Data structure for visual updates sent to the rendering system
/// </summary>
struct ElementVisualUpdateData {
    std::shared_ptr<ElementData> element;
    VisualizationMode display_mode;
    bool show_electron_orbitals;
    int orbitals_to_display;
    std::vector<Vector3D> electron_positions;
    std::vector<std::string> electron_colors;
};

/// <summary>
/// Handles visual representation and interactions for individual elements
/// Manages 3D model updates, electron orbital visualization,
/// and quantum property displays
/// </summary>
class ElementVisualizationController {
public:
    using ElementSelectedCallback = std::function<void(const std::shared_ptr<ElementData>&)>;
    using QuantumDataUpdatedCallback = std::function<void(const std::shared_ptr<QuantumMaterialProperties>&)>;
    using VisualUpdateCallback = std::function<void(const ElementVisualUpdateData&)>;

    ElementVisualizationController();
    ~ElementVisualizationController() = default;

    /// <summary>
    /// Register callback for element selection
    /// </summary>
    void on_element_selected(ElementSelectedCallback callback) {
        element_selected_callback_ = callback;
    }

    /// <summary>
    /// Register callback for quantum data updates
    /// </summary>
    void on_quantum_data_updated(QuantumDataUpdatedCallback callback) {
        quantum_data_updated_callback_ = callback;
    }

    /// <summary>
    /// Register callback for visual updates
    /// </summary>
    void on_visual_update_requested(VisualUpdateCallback callback) {
        visual_update_callback_ = callback;
    }

    /// <summary>
    /// Select an element and prepare its visualization
    /// </summary>
    void select_element(const std::shared_ptr<ElementData>& element);

    /// <summary>
    /// Update element with quantum-computed properties
    /// </summary>
    void update_with_quantum_properties(
        const std::shared_ptr<QuantumMaterialProperties>& properties);

    /// <summary>
    /// Get currently selected element
    /// </summary>
    std::shared_ptr<ElementData> get_current_element() const {
        return current_element_;
    }

    /// <summary>
    /// Get current quantum properties
    /// </summary>
    std::shared_ptr<QuantumMaterialProperties> get_current_quantum_properties() const {
        return current_quantum_properties_;
    }

    /// <summary>
    /// Clear selection and reset
    /// </summary>
    void clear_selection();

private:
    std::shared_ptr<ElementData> current_element_;
    std::shared_ptr<QuantumMaterialProperties> current_quantum_properties_;
    
    ElementSelectedCallback element_selected_callback_;
    QuantumDataUpdatedCallback quantum_data_updated_callback_;
    VisualUpdateCallback visual_update_callback_;

    /// <summary>
    /// Update the visual representation
    /// </summary>
    void update_element_visuals_();

    /// <summary>
    /// Generate 3D positions for electron spheres
    /// </summary>
    std::vector<Vector3D> generate_electron_positions_(
        const std::vector<ElectronOrbital>& orbitals);

    /// <summary>
    /// Generate colors for electron visualization
    /// </summary>
    std::vector<std::string> generate_electron_colors_(
        const std::vector<ElectronOrbital>& orbitals,
        const std::string& base_color);

    /// <summary>
    /// Adjust color brightness
    /// </summary>
    std::string adjust_color_brightness_(
        const std::string& hex_color, double factor);
};

}  // namespace PeriodicTable
