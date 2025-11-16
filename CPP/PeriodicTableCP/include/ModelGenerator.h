#pragma once

#include "ElementData.h"
#include <memory>
#include <vector>

namespace PeriodicTable {

// Forward declaration
class QuantumMaterialProperties;

/// <summary>
/// Molecular orbital model for bond visualization
/// </summary>
struct MolecularOrbitalModel {
    std::string orbital_type;                     // Bonding, Anti-bonding
    double energy;
    Vector3D center1, center2;
    double amplitude1, amplitude2;
    std::shared_ptr<ElementData> element1;
    std::shared_ptr<ElementData> element2;
};

/// <summary>
/// Crystal structure model
/// </summary>
struct CrystalStructureModel {
    std::shared_ptr<ElementData> element;
    std::string crystal_system;                   // Cubic, Hexagonal, etc.
    double lattice_parameter;
    std::vector<Vector3D> atom_positions;
};

/// <summary>
/// Generates dynamic 3D models from quantum simulation results
/// Converts quantum probability data into visualizable structures
/// </summary>
class ModelGenerator {
public:
    ModelGenerator() = default;
    ~ModelGenerator() = default;

    /// <summary>
    /// Generate orbital model from quantum simulation data
    /// </summary>
    std::vector<ElectronOrbital> generate_orbital_model(
        const std::shared_ptr<ElementData>& element,
        const std::shared_ptr<QuantumMaterialProperties>& quantum_properties);

    /// <summary>
    /// Generate molecular orbital model for bonding
    /// </summary>
    std::vector<MolecularOrbitalModel> generate_molecular_orbital(
        const std::shared_ptr<ElementData>& element1,
        const std::shared_ptr<ElementData>& element2,
        double bond_distance = 1.5);

    /// <summary>
    /// Generate crystal structure visualization
    /// </summary>
    CrystalStructureModel generate_crystal_structure(
        const std::shared_ptr<ElementData>& element,
        const std::string& crystal_system = "Cubic");

private:
    static constexpr double BOHR_RADIUS = 0.53;      // Ångströms
    static constexpr double SCALE_FACTOR = 2.0;

    /// <summary>
    /// Parse electron configuration string
    /// </summary>
    struct OrbitalConfig {
        int shell_number;
        std::string sub_shell;
        int electron_count;
    };

    std::vector<OrbitalConfig> parse_electron_configuration_(
        const std::string& configuration);

    /// <summary>
    /// Parse individual orbital notation
    /// </summary>
    OrbitalConfig parse_orbital_notation_(const std::string& notation);

    /// <summary>
    /// Calculate orbital radius
    /// </summary>
    double calculate_orbital_radius_(int shell_level, const std::string& sub_shell);

    /// <summary>
    /// Get angular momentum quantum number
    /// </summary>
    double get_angular_momentum_(const std::string& sub_shell);

    /// <summary>
    /// Generate 3D probability density coordinates
    /// </summary>
    void generate_probability_density_(
        ElectronOrbital& orbital,
        const std::shared_ptr<QuantumMaterialProperties>& quantum_properties);

    /// <summary>
    /// Calculate point density
    /// </summary>
    int calculate_point_density_(int electron_count);

    /// <summary>
    /// Generate Gaussian-distributed value
    /// </summary>
    double generate_gaussian_spread_();

    /// <summary>
    /// Normalize probability amplitudes
    /// </summary>
    void normalize_amplitudes_(std::vector<double>& amplitudes);

    /// <summary>
    /// Generate cubic unit cell
    /// </summary>
    void generate_cubic_unit_cell_(CrystalStructureModel& structure);

    /// <summary>
    /// Generate hexagonal unit cell
    /// </summary>
    void generate_hexagonal_unit_cell_(CrystalStructureModel& structure);
};

}  // namespace PeriodicTable
