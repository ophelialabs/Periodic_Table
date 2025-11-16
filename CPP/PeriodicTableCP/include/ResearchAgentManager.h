#pragma once

#include "ElementData.h"
#include "QuantumProcessor.h"
#include <memory>
#include <functional>

namespace PeriodicTable {

/// <summary>
/// Orchestrates quantum research simulations for elements and materials
/// Manages the workflow of quantum computations and coordinates
/// with the visualization system
/// </summary>
class ResearchAgentManager {
public:
    using SimulationProgressCallback = std::function<void(const std::string&)>;
    using SimulationCompletedCallback = std::function<void(
        const std::shared_ptr<QuantumSimulationResult>&)>;

    ResearchAgentManager(
        std::shared_ptr<QuantumProcessor> quantum_processor,
        std::shared_ptr<class ModelGenerator> model_generator);
    ~ResearchAgentManager() = default;

    /// <summary>
    /// Register progress update callback
    /// </summary>
    void on_progress_updated(SimulationProgressCallback callback) {
        progress_updated_callback_ = callback;
    }

    /// <summary>
    /// Register simulation completed callback
    /// </summary>
    void on_simulation_completed(SimulationCompletedCallback callback) {
        simulation_completed_callback_ = callback;
    }

    /// <summary>
    /// Start quantum simulation for an element
    /// </summary>
    std::shared_ptr<QuantumSimulationResult> simulate_element(
        const std::shared_ptr<ElementData>& element);

    /// <summary>
    /// Simulate molecular interactions between two elements
    /// </summary>
    std::shared_ptr<QuantumSimulationResult> simulate_molecular_bond(
        const std::shared_ptr<ElementData>& element1,
        const std::shared_ptr<ElementData>& element2);

    /// <summary>
    /// Check if simulation is in progress
    /// </summary>
    bool is_simulating() const { return is_simulating_; }

    /// <summary>
    /// Cancel ongoing simulation
    /// </summary>
    void cancel_simulation();

private:
    std::shared_ptr<QuantumProcessor> quantum_processor_;
    std::shared_ptr<class ModelGenerator> model_generator_;
    bool is_simulating_;
    
    SimulationProgressCallback progress_updated_callback_;
    SimulationCompletedCallback simulation_completed_callback_;

    /// <summary>
    /// Prepare quantum input from element data
    /// </summary>
    QuantumInputData prepare_quantum_input_(const std::shared_ptr<ElementData>& element);

    /// <summary>
    /// Prepare molecular quantum input
    /// </summary>
    QuantumInputData prepare_molecular_quantum_input_(
        const std::shared_ptr<ElementData>& element1,
        const std::shared_ptr<ElementData>& element2);

    /// <summary>
    /// Process quantum results into material properties
    /// </summary>
    std::shared_ptr<QuantumMaterialProperties> process_quantum_results_(
        const std::shared_ptr<QuantumSimulationResult>& quantum_result,
        const std::shared_ptr<ElementData>& element);

    double extract_band_gap_energy_(const std::shared_ptr<QuantumSimulationResult>& result);
    double extract_magnetic_moment_(const std::shared_ptr<QuantumSimulationResult>& result);
    double extract_polarizability_(const std::shared_ptr<QuantumSimulationResult>& result);
    double extract_entanglement_index_(const std::shared_ptr<QuantumSimulationResult>& result);
    std::string classify_conductivity_(double band_gap_energy);
};

}  // namespace PeriodicTable
