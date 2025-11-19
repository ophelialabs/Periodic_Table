#include "../include/ElementData.h"
#include <sstream>
#include <iomanip>

namespace PeriodicTable {

    ElementData::ElementData()
        : atomic_number(0), atomic_mass(0.0), valence_electrons(0),
        electronegativity(0.0), ionization_energy(0.0), atomic_radius(0.0),
        period(0), group(0), density(0.0), melting_point(0.0),
        boiling_point(0.0), discovery_year(0) {
    }

    ElementData::ElementData(int atomic_number, const std::string& symbol, const std::string& name)
        : atomic_number(atomic_number), symbol(symbol), name(name),
        atomic_mass(0.0), valence_electrons(0), electronegativity(0.0),
        ionization_energy(0.0), atomic_radius(0.0), period(0), group(0),
        density(0.0), melting_point(0.0), boiling_point(0.0), discovery_year(0) {
    }

    std::string ElementData::to_string() const {
        std::ostringstream oss;
        oss << atomic_number << " - " << symbol << " (" << name << ")";
        return oss.str();
    }

    void ElementData::clear_quantum_data() {
        quantum_orbital_data.clear();
        quantum_properties = nullptr;
    }

}  // namespace PeriodicTable
