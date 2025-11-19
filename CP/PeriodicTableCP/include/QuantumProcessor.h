#pragma once

#include "ElementData.h"
#include <memory>
#include <vector>
#include <functional>

namespace PeriodicTable {

    /// <summary>
    /// Result from quantum simulation execution
    /// </summary>
    struct QuantumSimulationResult {
        std::string job_id;
        std::chrono::system_clock::time_point timestamp;
        int element_atomic_number;
        std::vector<double> energy_levels;
        std::vector<double> probability_amplitudes;
        std::vector<std::array<double, 3>> spatial_coordinates;
        double convergence_metric;
        int iterations_performed;
        bool is_molecular_bond = false;
    };

    /// <summary>
    /// Raw quantum execution results from Q# operations
    /// </summary>
    struct RawQuantumResult {
        std::string job_id;
        std::map<std::string, int> counts;                    // Bitstring -> frequency
        std::map<std::string, std::string> metadata;
        double convergence_metric;
        int iterations_performed;
    };

    /// <summary>
    /// Quantum parameters passed to Q# operations
    /// </summary>
    struct QuantumParameters {
        int atomic_number;
        int secondary_atomic_number;
        int num_electrons;
        int nuclear_charge;
        double desired_precision;
        int max_iterations;
        bool is_molecular;
        std::map<std::string, double> extra_properties;
        std::string element_symbol;
        std::string element_name;
    };

    /// <summary>
    /// Interface for quantum execution targets
    /// Implementations can target Azure Quantum, local simulator, or other backends
    /// </summary>
    class IQuantumTarget {
    public:
        virtual ~IQuantumTarget() = default;

        /// <summary>
        /// Execute atomic structure simulation
        /// </summary>
        virtual RawQuantumResult execute_atomic_simulation(
            const QuantumParameters& parameters) = 0;

        /// <summary>
        /// Execute molecular bonding simulation
        /// </summary>
        virtual RawQuantumResult execute_molecular_simulation(
            const QuantumParameters& parameters) = 0;
    };

    /// <summary>
    /// Manages quantum simulation execution and result processing
    /// Integration layer between C++ and Q# quantum operations
    /// </summary>
    class QuantumProcessor {
    public:
        using JobCompletedCallback = std::function<void(
            const std::string& job_id, bool is_successful,
            const std::shared_ptr<QuantumSimulationResult>& result)>;

        explicit QuantumProcessor(std::shared_ptr<IQuantumTarget> quantum_target);
        ~QuantumProcessor() = default;

        /// <summary>
        /// Register callback for job completion
        /// </summary>
        void on_job_completed(JobCompletedCallback callback) {
            job_completed_callback_ = callback;
        }

        /// <summary>
        /// Execute quantum simulation for atomic properties
        /// </summary>
        std::shared_ptr<QuantumSimulationResult> run_quantum_simulation(
            const QuantumInputData& input,
            const std::shared_ptr<ElementData>& element);

        /// <summary>
        /// Execute quantum simulation for molecular bonding
        /// </summary>
        std::shared_ptr<QuantumSimulationResult> run_molecular_simulation(
            const QuantumInputData& input);

        /// <summary>
        /// Cancel ongoing simulation
        /// </summary>
        void cancel_simulation();

        /// <summary>
        /// Get last job ID
        /// </summary>
        std::string get_last_job_id() const { return last_job_id_; }

    private:
        std::shared_ptr<IQuantumTarget> quantum_target_;
        std::string last_job_id_;
        JobCompletedCallback job_completed_callback_;

        /// <summary>
        /// Prepare quantum parameters from input data
        /// </summary>
        QuantumParameters prepare_quantum_parameters_(
            const QuantumInputData& input,
            const std::shared_ptr<ElementData>& element);

        /// <summary>
        /// Prepare molecular quantum parameters
        /// </summary>
        QuantumParameters prepare_molecular_parameters_(const QuantumInputData& input);

        /// <summary>
        /// Process raw quantum results
        /// </summary>
        std::shared_ptr<QuantumSimulationResult> process_quantum_results_(
            const RawQuantumResult& raw_result,
            const std::shared_ptr<ElementData>& element);

        /// <summary>
        /// Process molecular simulation results
        /// </summary>
        std::shared_ptr<QuantumSimulationResult> process_molecular_results_(
            const RawQuantumResult& raw_result);

        /// <summary>
        /// Extract energy levels from measurement counts
        /// </summary>
        std::vector<double> parse_energy_levels_(
            const std::map<std::string, int>& counts);

        /// <summary>
        /// Calculate energy from bitstring
        /// </summary>
        double calculate_energy_from_bitstring_(const std::string& bitstring);

        /// <summary>
        /// Extract probability amplitudes
        /// </summary>
        std::vector<double> extract_probabilities_(
            const std::map<std::string, int>& counts);

        /// <summary>
        /// Extract spatial coordinate data
        /// </summary>
        std::vector<std::array<double, 3>> extract_spatial_data_(
            const std::map<std::string, std::string>& metadata);
    };

}  // namespace PeriodicTable
