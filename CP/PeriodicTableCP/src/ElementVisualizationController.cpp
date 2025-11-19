#include "../include/ElementVisualizationController.h"
#include <cmath>
#include <algorithm>
#include <iostream>

namespace PeriodicTable {

    ElementVisualizationController::ElementVisualizationController()
        : current_element_(nullptr), current_quantum_properties_(nullptr) {
    }

    void ElementVisualizationController::select_element(const std::shared_ptr<ElementData>& element) {
        if (!element) {
            throw std::invalid_argument("Element cannot be null");
        }

        current_element_ = element;

        if (element_selected_callback_) {
            element_selected_callback_(element);
        }

        update_element_visuals_();
    }

    void ElementVisualizationController::update_with_quantum_properties(
        const std::shared_ptr<QuantumMaterialProperties>& properties) {
        if (!properties) {
            throw std::invalid_argument("Properties cannot be null");
        }

        current_quantum_properties_ = properties;

        if (quantum_data_updated_callback_) {
            quantum_data_updated_callback_(properties);
        }

        update_element_visuals_();
    }

    void ElementVisualizationController::update_element_visuals_() {
        if (!current_element_) {
            return;
        }

        try {
            ElementVisualUpdateData visual_data;
            visual_data.element = current_element_;
            visual_data.display_mode = VisualizationMode::AtomicStructure;
            visual_data.show_electron_orbitals = true;
            visual_data.orbitals_to_display = current_element_->quantum_orbital_data.size();

            if (!current_element_->quantum_orbital_data.empty()) {
                visual_data.electron_positions = generate_electron_positions_(
                    current_element_->quantum_orbital_data);
                visual_data.electron_colors = generate_electron_colors_(
                    current_element_->quantum_orbital_data,
                    current_element_->color_code);
            }

            if (visual_update_callback_) {
                visual_update_callback_(visual_data);
            }
        }
        catch (const std::exception& ex) {
            std::cerr << "Error updating visuals: " << ex.what() << std::endl;
        }
    }

    std::vector<Vector3D> ElementVisualizationController::generate_electron_positions_(
        const std::vector<ElectronOrbital>& orbitals) {
        std::vector<Vector3D> positions;

        for (const auto& orbital : orbitals) {
            if (orbital.probability_coordinates.empty()) {
                continue;
            }

            for (size_t i = 0; i < orbital.probability_coordinates.size(); ++i) {
                const auto& coords = orbital.probability_coordinates[i];
                double amplitude = (i < orbital.probability_amplitudes.size())
                    ? orbital.probability_amplitudes[i] : 0.5;

                // Only include high-probability positions
                if (amplitude > 0.1) {
                    positions.emplace_back(
                        coords[0] * amplitude,
                        coords[1] * amplitude,
                        coords[2] * amplitude
                    );
                }
            }
        }

        return positions;
    }

    std::vector<std::string> ElementVisualizationController::generate_electron_colors_(
        const std::vector<ElectronOrbital>& orbitals,
        const std::string& base_color) {
        std::vector<std::string> colors;

        for (const auto& orbital : orbitals) {
            std::string color_variant = adjust_color_brightness_(base_color, orbital.shell_level * 0.1);
            for (int i = 0; i < (orbital.electron_count > 0 ? orbital.electron_count : 1); ++i) {
                colors.push_back(color_variant);
            }
        }

        return colors;
    }

    std::string ElementVisualizationController::adjust_color_brightness_(
        const std::string& hex_color, double factor) {
        if (hex_color.empty() || hex_color[0] != '#' || hex_color.length() < 7) {
            return "#FFFFFF";
        }

        try {
            std::string hex = hex_color.substr(1);
            int r = std::stoi(hex.substr(0, 2), nullptr, 16);
            int g = std::stoi(hex.substr(2, 2), nullptr, 16);
            int b = std::stoi(hex.substr(4, 2), nullptr, 16);

            r = std::min(255, static_cast<int>(r * (1.0 + factor)));
            g = std::min(255, static_cast<int>(g * (1.0 + factor)));
            b = std::min(255, static_cast<int>(b * (1.0 + factor)));

            char buffer[8];
            std::snprintf(buffer, sizeof(buffer), "#%02X%02X%02X", r, g, b);
            return std::string(buffer);
        }
        catch (...) {
            return "#FFFFFF";
        }
    }

    void ElementVisualizationController::clear_selection() {
        current_element_ = nullptr;
        current_quantum_properties_ = nullptr;
    }

}  // namespace PeriodicTable
