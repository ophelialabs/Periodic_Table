#pragma once

#include <string>
#include <vector>
#include <map>
#include <memory>
#include <cmath>
#include <chrono>

namespace PeriodicTable {

    /// <summary>
    /// Represents electron orbital data from quantum simulations
    /// Used for 3D visualization of electron probability densities
    /// </summary>
    struct ElectronOrbital {
        int shell_level;                              // Orbital shell (1, 2, 3, etc.)
        std::string sub_shell;                        // Subshell (s, p, d, f)
        int electron_count;                           // Electrons in this orbital
        std::vector<std::array<double, 3>> probability_coordinates;  // 3D coordinates
        std::vector<double> probability_amplitudes;   // Probability values [0,1]
        double average_radius;                        // Average orbital radius (Ångströms)
        std::string visualization_color;              // Hex color for rendering
    };

    /// <summary>
    /// Quantum-derived material properties for research visualization
    /// </summary>
    struct QuantumMaterialProperties {
        std::string element_symbol;
        double band_gap_energy;                       // eV
        std::string conductivity_class;               // Conductor/Semiconductor/Insulator
        double magnetic_moment;                       // Bohr magnetons
        double polarizability;                        // Quantum derived
        double quantum_entanglement_index;            // [0, 1]
        std::chrono::system_clock::time_point simulation_timestamp;
        std::string quantum_job_id;
    };

    /// <summary>
    /// Core data structure holding all element properties
    /// Foundation for all UI interactions and quantum simulations
    /// </summary>
    class ElementData {
    public:
        // Basic properties
        int atomic_number;
        std::string symbol;
        std::string name;
        double atomic_mass;
        std::string electron_configuration;
        int valence_electrons;
        double electronegativity;
        double ionization_energy;
        double atomic_radius;

        // Classification
        std::string category;
        int period;
        int group;
        std::string color_code;

        // Physical state
        std::string physical_state;                   // Solid, Liquid, Gas
        double density;                               // g/cm³
        double melting_point;                         // °C
        double boiling_point;                         // °C
        std::vector<int> oxidation_states;

        // Discovery info
        int discovery_year;
        std::string discoverer;
        std::string description;

        // Quantum simulation data
        std::vector<ElectronOrbital> quantum_orbital_data;
        std::shared_ptr<QuantumMaterialProperties> quantum_properties;

        ElementData();
        ElementData(int atomic_number, const std::string& symbol, const std::string& name);

        std::string to_string() const;
        void clear_quantum_data();
    };

    /// <summary>
    /// Represents 3D spatial data for visualization
    /// </summary>
    struct Vector3D {
        double x, y, z;

        Vector3D() : x(0), y(0), z(0) {}
        Vector3D(double x, double y, double z) : x(x), y(y), z(z) {}

        double magnitude() const {
            return std::sqrt(x * x + y * y + z * z);
        }
    };

    /// <summary>
    /// Parameters for quantum simulation execution
    /// </summary>
    struct QuantumInputData {
        int atomic_number;
        int secondary_atomic_number;                  // For molecular simulations
        int electron_count;
        int nuclear_charge;
        double desired_precision;
        int max_iterations;
        bool is_molecular;
        std::map<std::string, double> element_properties;

        QuantumInputData() : atomic_number(0), secondary_atomic_number(0),
            electron_count(0), nuclear_charge(0),
            desired_precision(0.001), max_iterations(1000),
            is_molecular(false) {
        }
    };

}  // namespace PeriodicTable
