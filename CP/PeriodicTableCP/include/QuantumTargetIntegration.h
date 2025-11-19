#pragma once

#include "QuantumProcessor.h"
#include <memory>
#include <map>
#include <string>

namespace PeriodicTable {

    /// <summary>
    /// Azure Quantum target for IonQ and other providers
    /// Integration layer for calling Q# operations on Azure Quantum
    /// </summary>
    class AzureQuantumTarget : public IQuantumTarget {
    public:
        AzureQuantumTarget(
            const std::string& subscription_id,
            const std::string& resource_group,
            const std::string& workspace,
            const std::string& target_id,
            const std::string& storage_connection_string);

        /// <summary>
        /// Execute atomic structure simulation on Azure Quantum
        /// </summary>
        RawQuantumResult execute_atomic_simulation(
            const QuantumParameters& parameters) override;

        /// <summary>
        /// Execute molecular bonding simulation on Azure Quantum
        /// </summary>
        RawQuantumResult execute_molecular_simulation(
            const QuantumParameters& parameters) override;

    private:
        std::string subscription_id_;
        std::string resource_group_;
        std::string workspace_;
        std::string target_id_;
        std::string storage_connection_string_;

        /// <summary>
        /// Compile atomic simulation to QIR
        /// </summary>
        std::string compile_atomic_simulation_to_qir_(const QuantumParameters& parameters);

        /// <summary>
        /// Compile molecular simulation to QIR
        /// </summary>
        std::string compile_molecular_simulation_to_qir_(const QuantumParameters& parameters);

        /// <summary>
        /// Submit QIR program to Azure Quantum
        /// </summary>
        std::string submit_to_azure_quantum_(
            const std::string& qir_program,
            const std::string& operation_name,
            const QuantumParameters& parameters);

        /// <summary>
        /// Wait for job completion
        /// </summary>
        RawQuantumResult wait_for_job_completion_(const std::string& job_id);

        /// <summary>
        /// Generate mock quantum results for demonstration
        /// </summary>
        RawQuantumResult generate_mock_quantum_result_(const std::string& job_id);
    };

    /// <summary>
    /// Local quantum simulator for development and testing
    /// Executes quantum simulations without requiring Azure connection
    /// </summary>
    class LocalQuantumSimulator : public IQuantumTarget {
    public:
        LocalQuantumSimulator() = default;

        /// <summary>
        /// Execute atomic simulation locally
        /// </summary>
        RawQuantumResult execute_atomic_simulation(
            const QuantumParameters& parameters) override;

        /// <summary>
        /// Execute molecular simulation locally
        /// </summary>
        RawQuantumResult execute_molecular_simulation(
            const QuantumParameters& parameters) override;

    private:
        /// <summary>
        /// Simulate quantum computation locally
        /// </summary>
        RawQuantumResult simulate_quantum_computation_(
            const QuantumParameters& parameters,
            const std::string& operation_name);
    };

}  // namespace PeriodicTable
