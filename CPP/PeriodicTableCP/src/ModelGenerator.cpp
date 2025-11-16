#include "../include/ModelGenerator.h"
#include "../include/ElementData.h"
#include <cmath>
#include <algorithm>
#include <random>
#include <sstream>

namespace PeriodicTable {

std::vector<ElectronOrbital> ModelGenerator::generate_orbital_model(
    const std::shared_ptr<ElementData>& element,
    const std::shared_ptr<QuantumMaterialProperties>& quantum_properties) {
    
    if (!element) {
        throw std::invalid_argument("Element cannot be null");
    }
    
    std::vector<ElectronOrbital> orbitals;
    
    // Parse electron configuration and create orbitals
    auto orbital_config = parse_electron_configuration_(element->electron_configuration);
    
    int shell_level = 0;
    for (const auto& config : orbital_config) {
        shell_level++;
        ElectronOrbital orbital;
        orbital.shell_level = shell_level;
        orbital.sub_shell = config.sub_shell;
        orbital.electron_count = config.electron_count;
        orbital.average_radius = calculate_orbital_radius_(shell_level, config.sub_shell);
        orbital.visualization_color = element->color_code;
        
        // Generate probability density coordinates
        generate_probability_density_(orbital, quantum_properties);
        
        orbitals.push_back(orbital);
    }
    
    return orbitals;
}

std::vector<ModelGenerator::OrbitalConfig> ModelGenerator::parse_electron_configuration_(
    const std::string& configuration) {
    
    std::vector<OrbitalConfig> orbitals;
    
    if (configuration.empty()) {
        return orbitals;
    }
    
    // Simple parser for electron configuration
    std::istringstream iss(configuration);
    std::string part;
    
    while (iss >> part) {
        auto config = parse_orbital_notation_(part);
        if (config.shell_number > 0) {
            orbitals.push_back(config);
        }
    }
    
    return orbitals;
}

ModelGenerator::OrbitalConfig ModelGenerator::parse_orbital_notation_(const std::string& notation) {
    OrbitalConfig config{0, "", 0};
    
    if (notation.empty() || notation.length() < 2) {
        return config;
    }
    
    try {
        config.shell_number = std::stoi(std::string(1, notation[0]));
        config.sub_shell = std::string(1, notation[1]);
        
        // Extract electron count (handle superscript)
        if (notation.length() > 2) {
            std::string superscript = notation.substr(2);
            // Replace superscript characters
            if (superscript == "²" || superscript == "2") {
                config.electron_count = 2;
            } else if (superscript == "¹⁰" || superscript == "10") {
                config.electron_count = 10;
            } else if (superscript == "⁶" || superscript == "6") {
                config.electron_count = 6;
            } else if (superscript == "¹⁴" || superscript == "14") {
                config.electron_count = 14;
            } else {
                config.electron_count = std::stoi(superscript);
            }
        } else {
            config.electron_count = 2;  // Default
        }
    } catch (...) {
        return OrbitalConfig{0, "", 0};
    }
    
    return config;
}

double ModelGenerator::calculate_orbital_radius_(int shell_level, const std::string& sub_shell) {
    double n = static_cast<double>(shell_level);
    double l = get_angular_momentum_(sub_shell);
    
    // Apply screening effect
    double screening_constant = 0.3 * (n - 1.0);
    double effective_z = 1.0 - screening_constant;
    
    // Bohr model: radius = n² / Z_eff * a₀
    return (n * n / effective_z) * BOHR_RADIUS;
}

double ModelGenerator::get_angular_momentum_(const std::string& sub_shell) {
    if (sub_shell.empty()) {
        return 0.0;
    }
    
    switch (sub_shell[0]) {
        case 's': return 0.0;
        case 'p': return 1.0;
        case 'd': return 2.0;
        case 'f': return 3.0;
        default: return 0.0;
    }
}

void ModelGenerator::generate_probability_density_(
    ElectronOrbital& orbital,
    const std::shared_ptr<QuantumMaterialProperties>& quantum_properties) {
    
    int num_points = calculate_point_density_(orbital.electron_count);
    double radius = orbital.average_radius * SCALE_FACTOR;
    
    // Use spherical coordinates
    for (int i = 0; i < num_points; ++i) {
        double theta = 2.0 * M_PI * (i % 10) / 10.0;        // Azimuthal
        double phi = M_PI * ((i / 10) % 5) / 5.0;            // Polar
        
        // Spherical to Cartesian
        double x = radius * std::sin(phi) * std::cos(theta);
        double y = radius * std::sin(phi) * std::sin(theta);
        double z = radius * std::cos(phi);
        
        // Add Gaussian spread
        double spread = generate_gaussian_spread_();
        orbital.probability_coordinates.push_back({
            x + spread,
            y + spread,
            z + spread
        });
        
        // Probability amplitude decreases with distance
        double distance = std::sqrt(x * x + y * y + z * z);
        double amplitude = std::exp(-distance / radius);
        orbital.probability_amplitudes.push_back(amplitude);
    }
    
    // Normalize amplitudes
    normalize_amplitudes_(orbital.probability_amplitudes);
}

int ModelGenerator::calculate_point_density_(int electron_count) {
    return std::max(10, std::min(100, electron_count * 20));
}

double ModelGenerator::generate_gaussian_spread_() {
    static std::random_device rd;
    static std::mt19937 gen(rd());
    std::normal_distribution<> dis(0.0, 0.1);
    return dis(gen);
}

void ModelGenerator::normalize_amplitudes_(std::vector<double>& amplitudes) {
    if (amplitudes.empty()) {
        return;
    }
    
    double sum = 0.0;
    for (double amp : amplitudes) {
        sum += amp;
    }
    
    if (sum > 0) {
        for (auto& amp : amplitudes) {
            amp /= sum;
        }
    }
}

std::vector<MolecularOrbitalModel> ModelGenerator::generate_molecular_orbital(
    const std::shared_ptr<ElementData>& element1,
    const std::shared_ptr<ElementData>& element2,
    double bond_distance) {
    
    std::vector<MolecularOrbitalModel> orbitals;
    
    // Bonding orbital (lower energy)
    MolecularOrbitalModel bonding;
    bonding.orbital_type = "Bonding";
    bonding.energy = -2.0;
    bonding.center1 = Vector3D(-bond_distance / 2.0, 0.0, 0.0);
    bonding.center2 = Vector3D(bond_distance / 2.0, 0.0, 0.0);
    bonding.amplitude1 = 1.0;
    bonding.amplitude2 = 1.0;
    bonding.element1 = element1;
    bonding.element2 = element2;
    orbitals.push_back(bonding);
    
    // Anti-bonding orbital (higher energy)
    MolecularOrbitalModel antibonding;
    antibonding.orbital_type = "Anti-bonding";
    antibonding.energy = 2.0;
    antibonding.center1 = Vector3D(-bond_distance / 2.0, 0.0, 0.0);
    antibonding.center2 = Vector3D(bond_distance / 2.0, 0.0, 0.0);
    antibonding.amplitude1 = 1.0;
    antibonding.amplitude2 = -1.0;  // Out of phase
    antibonding.element1 = element1;
    antibonding.element2 = element2;
    orbitals.push_back(antibonding);
    
    return orbitals;
}

CrystalStructureModel ModelGenerator::generate_crystal_structure(
    const std::shared_ptr<ElementData>& element,
    const std::string& crystal_system) {
    
    CrystalStructureModel structure;
    structure.element = element;
    structure.crystal_system = crystal_system;
    structure.lattice_parameter = element->atomic_radius * 2.8;
    
    if (crystal_system == "Hexagonal") {
        generate_hexagonal_unit_cell_(structure);
    } else {
        generate_cubic_unit_cell_(structure);
    }
    
    return structure;
}

void ModelGenerator::generate_cubic_unit_cell_(CrystalStructureModel& structure) {
    double a = structure.lattice_parameter;
    
    // Corner atoms
    for (int i = 0; i <= 1; ++i) {
        for (int j = 0; j <= 1; ++j) {
            for (int k = 0; k <= 1; ++k) {
                structure.atom_positions.emplace_back(i * a, j * a, k * a);
            }
        }
    }
}

void ModelGenerator::generate_hexagonal_unit_cell_(CrystalStructureModel& structure) {
    double a = structure.lattice_parameter;
    double c = a * 1.633;  // c/a ratio for hexagonal
    
    structure.atom_positions.emplace_back(0.0, 0.0, 0.0);
    structure.atom_positions.emplace_back(a / 2.0, a * std::sqrt(3.0) / 2.0, 0.0);
    structure.atom_positions.emplace_back(0.0, 0.0, c / 2.0);
    structure.atom_positions.emplace_back(a / 2.0, a * std::sqrt(3.0) / 2.0, c / 2.0);
}

}  // namespace PeriodicTable
