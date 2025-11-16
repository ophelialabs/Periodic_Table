#include "../include/ResearchAgentManager.h"
#include "../include/ModelGenerator.h"
#include <iostream>

namespace PeriodicTable {

ResearchAgentManager::ResearchAgentManager(
    std::shared_ptr<QuantumProcessor> quantum_processor,
    std::shared_ptr<ModelGenerator> model_generator)
    : quantum_processor_(quantum_processor),
      model_generator_(model_generator),
      is_simulating_(false) {
    
    if (!quantum_processor_) {
        throw std::invalid_argument("Quantum processor cannot be null");
    }
    if (!model_generator_) {
        throw std::invalid_argument("Model generator cannot be null");
    }
}

std::shared_ptr<QuantumSimulationResult> ResearchAgentManager::simulate_element(
    const std::shared_ptr<ElementData>& element) {
    
    if (!element) {
        throw std::invalid_argument("Element cannot be null");
    }
    
    if (is_simulating_) {
        throw std::runtime_error("Simulation already in progress");
    }
    
    is_simulating_ = true;
    try {
        std::string msg = "Starting quantum simulation for " + element->name + "...";
        if (progress_updated_callback_) {
            progress_updated_callback_(msg);
        }
        
        // Step 1: Prepare quantum input
        if (progress_updated_callback_) {
            progress_updated_callback_("Preparing quantum parameters...");
        }
        auto quantum_input = prepare_quantum_input_(element);
        
        // Step 2: Execute quantum simulation
        if (progress_updated_callback_) {
            progress_updated_callback_("Running quantum processor...");
        }
        auto quantum_result = quantum_processor_->run_quantum_simulation(quantum_input, element);
        
        if (!quantum_result) {
            throw std::runtime_error("Quantum simulation returned null result");
        }
        
        if (progress_updated_callback_) {
            progress_updated_callback_("Processing quantum results...");
        }
        
        // Step 3: Process results and generate material properties
        auto material_properties = process_quantum_results_(quantum_result, element);
        
        // Step 4: Generate 3D model data
        if (progress_updated_callback_) {
            progress_updated_callback_("Generating 3D model...");
        }
        auto model_data = model_generator_->generate_orbital_model(element, material_properties);
        element->quantum_orbital_data = model_data;
        element->quantum_properties = material_properties;
        
        if (progress_updated_callback_) {
            progress_updated_callback_("Simulation complete for " + element->name);
        }
        
        if (simulation_completed_callback_) {
            simulation_completed_callback_(quantum_result);
        }
        
        is_simulating_ = false;
        return quantum_result;
    } catch (const std::exception& ex) {
        if (progress_updated_callback_) {
            progress_updated_callback_("Simulation error: " + std::string(ex.what()));
        }
        is_simulating_ = false;
        throw;
    }
}

std::shared_ptr<QuantumSimulationResult> ResearchAgentManager::simulate_molecular_bond(
    const std::shared_ptr<ElementData>& element1,
    const std::shared_ptr<ElementData>& element2) {
    
    if (!element1 || !element2) {
        throw std::invalid_argument("Elements cannot be null");
    }
    
    if (is_simulating_) {
        throw std::runtime_error("Simulation already in progress");
    }
    
    is_simulating_ = true;
    try {
        std::string msg = "Simulating molecular bond: " + element1->symbol + "-" + element2->symbol + "...";
        if (progress_updated_callback_) {
            progress_updated_callback_(msg);
        }
        
        auto quantum_input = prepare_molecular_quantum_input_(element1, element2);
        auto quantum_result = quantum_processor_->run_molecular_simulation(quantum_input);
        
        if (progress_updated_callback_) {
            progress_updated_callback_("Processing molecular simulation results...");
        }
        
        auto material_properties = process_quantum_results_(quantum_result, element1);
        
        if (simulation_completed_callback_) {
            simulation_completed_callback_(quantum_result);
        }
        
        is_simulating_ = false;
        return quantum_result;
    } catch (const std::exception& ex) {
        if (progress_updated_callback_) {
            progress_updated_callback_("Simulation error: " + std::string(ex.what()));
        }
        is_simulating_ = false;
        throw;
    }
}

QuantumInputData ResearchAgentManager::prepare_quantum_input_(
    const std::shared_ptr<ElementData>& element) {
    
    QuantumInputData input;
    input.atomic_number = element->atomic_number;
    input.electron_count = element->valence_electrons;
    input.nuclear_charge = element->atomic_number;
    input.desired_precision = 0.001;
    input.max_iterations = 1000;
    
    input.element_properties["mass"] = element->atomic_mass;
    input.element_properties["radius"] = element->atomic_radius;
    input.element_properties["ionization_energy"] = element->ionization_energy;
    input.element_properties["electronegativity"] = element->electronegativity;
    
    return input;
}

QuantumInputData ResearchAgentManager::prepare_molecular_quantum_input_(
    const std::shared_ptr<ElementData>& element1,
    const std::shared_ptr<ElementData>& element2) {
    
    QuantumInputData input;
    input.atomic_number = element1->atomic_number;
    input.secondary_atomic_number = element2->atomic_number;
    input.electron_count = element1->valence_electrons + element2->valence_electrons;
    input.nuclear_charge = element1->atomic_number + element2->atomic_number;
    input.desired_precision = 0.001;
    input.max_iterations = 2000;
    input.is_molecular = true;
    
    input.element_properties["bond_distance"] = 1.0;
    input.element_properties["mass1"] = element1->atomic_mass;
    input.element_properties["mass2"] = element2->atomic_mass;
    
    return input;
}

std::shared_ptr<QuantumMaterialProperties> ResearchAgentManager::process_quantum_results_(
    const std::shared_ptr<QuantumSimulationResult>& quantum_result,
    const std::shared_ptr<ElementData>& element) {
    
    if (!quantum_result) {
        throw std::invalid_argument("Quantum result cannot be null");
    }
    
    auto properties = std::make_shared<QuantumMaterialProperties>();
    properties->element_symbol = element->symbol;
    properties->simulation_timestamp = std::chrono::system_clock::now();
    properties->quantum_job_id = quantum_result->job_id;
    properties->band_gap_energy = extract_band_gap_energy_(quantum_result);
    properties->magnetic_moment = extract_magnetic_moment_(quantum_result);
    properties->polarizability = extract_polarizability_(quantum_result);
    properties->quantum_entanglement_index = extract_entanglement_index_(quantum_result);
    properties->conductivity_class = classify_conductivity_(properties->band_gap_energy);
    
    return properties;
}

double ResearchAgentManager::extract_band_gap_energy_(
    const std::shared_ptr<QuantumSimulationResult>& result) {
    
    if (!result || result->energy_levels.size() < 2) {
        return 0.0;
    }
    
    return result->energy_levels[1] - result->energy_levels[0];
}

double ResearchAgentManager::extract_magnetic_moment_(
    const std::shared_ptr<QuantumSimulationResult>& result) {
    
    if (!result || result->probability_amplitudes.empty()) {
        return 0.0;
    }
    
    double sum_squares = 0.0;
    for (double amplitude : result->probability_amplitudes) {
        sum_squares += amplitude * amplitude;
    }
    
    return std::sqrt(sum_squares / result->probability_amplitudes.size());
}

double ResearchAgentManager::extract_polarizability_(
    const std::shared_ptr<QuantumSimulationResult>& result) {
    
    if (!result || result->energy_levels.empty()) {
        return 0.0;
    }
    
    return 1.0 / (std::abs(result->energy_levels[0]) + 0.1);
}

double ResearchAgentManager::extract_entanglement_index_(
    const std::shared_ptr<QuantumSimulationResult>& result) {
    
    if (!result || result->probability_amplitudes.empty()) {
        return 0.0;
    }
    
    double entropy = 0.0;
    for (double p : result->probability_amplitudes) {
        if (p > 0) {
            entropy -= p * std::log(p);
        }
    }
    
    return std::min(entropy, 1.0);
}

std::string ResearchAgentManager::classify_conductivity_(double band_gap_energy) {
    if (band_gap_energy < 0.1) {
        return "Conductor";
    } else if (band_gap_energy < 3.0) {
        return "Semiconductor";
    } else {
        return "Insulator";
    }
}

void ResearchAgentManager::cancel_simulation() {
    quantum_processor_->cancel_simulation();
    is_simulating_ = false;
}

}  // namespace PeriodicTable
