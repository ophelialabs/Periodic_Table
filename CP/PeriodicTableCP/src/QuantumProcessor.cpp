#include "../include/QuantumProcessor.h"
#include <algorithm>
#include <cmath>
#include <numeric>
#include <iostream>
#include <sstream>

namespace PeriodicTable {

    QuantumProcessor::QuantumProcessor(std::shared_ptr<IQuantumTarget> quantum_target)
        : quantum_target_(quantum_target) {
        if (!quantum_target_) {
            throw std::invalid_argument("Quantum target cannot be null");
        }
    }

    std::shared_ptr<QuantumSimulationResult> QuantumProcessor::run_quantum_simulation(
        const QuantumInputData& input,
        const std::shared_ptr<ElementData>& element) {

        try {
            auto quantum_params = prepare_quantum_parameters_(input, element);
            auto raw_result = quantum_target_->execute_atomic_simulation(quantum_params);

            last_job_id_ = raw_result.job_id;

            auto result = process_quantum_results_(raw_result, element);

            if (job_completed_callback_) {
                job_completed_callback_(result->job_id, true, result);
            }

            return result;
        }
        catch (const std::exception& ex) {
            if (job_completed_callback_) {
                job_completed_callback_(last_job_id_, false, nullptr);
            }
            throw;
        }
    }

    std::shared_ptr<QuantumSimulationResult> QuantumProcessor::run_molecular_simulation(
        const QuantumInputData& input) {

        try {
            auto quantum_params = prepare_molecular_parameters_(input);
            auto raw_result = quantum_target_->execute_molecular_simulation(quantum_params);

            last_job_id_ = raw_result.job_id;

            auto result = process_molecular_results_(raw_result);

            if (job_completed_callback_) {
                job_completed_callback_(result->job_id, true, result);
            }

            return result;
        }
        catch (const std::exception& ex) {
            if (job_completed_callback_) {
                job_completed_callback_(last_job_id_, false, nullptr);
            }
            throw;
        }
    }

    QuantumParameters QuantumProcessor::prepare_quantum_parameters_(
        const QuantumInputData& input,
        const std::shared_ptr<ElementData>& element) {

        QuantumParameters params;
        params.atomic_number = input.atomic_number;
        params.num_electrons = input.electron_count;
        params.nuclear_charge = input.nuclear_charge;
        params.desired_precision = input.desired_precision;
        params.max_iterations = input.max_iterations;
        params.element_symbol = element->symbol;
        params.element_name = element->name;
        params.extra_properties = input.element_properties;

        return params;
    }

    QuantumParameters QuantumProcessor::prepare_molecular_parameters_(const QuantumInputData& input) {
        QuantumParameters params;
        params.atomic_number = input.atomic_number;
        params.secondary_atomic_number = input.secondary_atomic_number;
        params.num_electrons = input.electron_count;
        params.nuclear_charge = input.nuclear_charge;
        params.desired_precision = input.desired_precision;
        params.max_iterations = input.max_iterations;
        params.is_molecular = true;
        params.extra_properties = input.element_properties;

        return params;
    }

    std::shared_ptr<QuantumSimulationResult> QuantumProcessor::process_quantum_results_(
        const RawQuantumResult& raw_result,
        const std::shared_ptr<ElementData>& element) {

        auto result = std::make_shared<QuantumSimulationResult>();
        result->job_id = raw_result.job_id;
        result->timestamp = std::chrono::system_clock::now();
        result->element_atomic_number = element->atomic_number;
        result->energy_levels = parse_energy_levels_(raw_result.counts);
        result->probability_amplitudes = extract_probabilities_(raw_result.counts);
        result->spatial_coordinates = extract_spatial_data_(raw_result.metadata);
        result->convergence_metric = raw_result.convergence_metric;
        result->iterations_performed = raw_result.iterations_performed;

        return result;
    }

    std::shared_ptr<QuantumSimulationResult> QuantumProcessor::process_molecular_results_(
        const RawQuantumResult& raw_result) {

        auto result = std::make_shared<QuantumSimulationResult>();
        result->job_id = raw_result.job_id;
        result->timestamp = std::chrono::system_clock::now();
        result->energy_levels = parse_energy_levels_(raw_result.counts);
        result->probability_amplitudes = extract_probabilities_(raw_result.counts);
        result->convergence_metric = raw_result.convergence_metric;
        result->iterations_performed = raw_result.iterations_performed;
        result->is_molecular_bond = true;

        return result;
    }

    std::vector<double> QuantumProcessor::parse_energy_levels_(
        const std::map<std::string, int>& counts) {

        std::vector<double> energies;

        for (const auto& kvp : counts) {
            double energy = calculate_energy_from_bitstring_(kvp.first);
            energies.push_back(energy);
        }

        std::sort(energies.begin(), energies.end());
        return energies;
    }

    double QuantumProcessor::calculate_energy_from_bitstring_(const std::string& bitstring) {
        // Rydberg energy scale
        const double RYDBERG = 13.6;

        int num_ones = 0;
        for (char bit : bitstring) {
            if (bit == '1') {
                num_ones++;
            }
        }

        double energy = -RYDBERG / std::pow(num_ones + 1.0, 2.0);
        return energy;
    }

    std::vector<double> QuantumProcessor::extract_probabilities_(
        const std::map<std::string, int>& counts) {

        if (counts.empty()) {
            return {};
        }

        int total_shots = 0;
        for (const auto& kvp : counts) {
            total_shots += kvp.second;
        }

        std::vector<double> probabilities;
        for (const auto& kvp : counts) {
            probabilities.push_back(static_cast<double>(kvp.second) / total_shots);
        }

        return probabilities;
    }

    std::vector<std::array<double, 3>> QuantumProcessor::extract_spatial_data_(
        const std::map<std::string, std::string>& metadata) {

        std::vector<std::array<double, 3>> coordinates;

        auto it = metadata.find("spatial_data");
        if (it != metadata.end()) {
            std::istringstream iss(it->second);
            std::string value;
            std::vector<double> values;

            while (std::getline(iss, value, ',')) {
                try {
                    values.push_back(std::stod(value));
                }
                catch (...) {
                    continue;
                }
            }

            for (size_t i = 0; i + 2 < values.size(); i += 3) {
                coordinates.push_back({ values[i], values[i + 1], values[i + 2] });
            }
        }

        return coordinates;
    }

    void QuantumProcessor::cancel_simulation() {
        // TODO: Implement cancellation mechanism if needed
    }

}  // namespace PeriodicTable
