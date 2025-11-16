"""
3D Model Generator Module
Generates 3D visual representations of molecular structures and quantum orbitals.
Uses VTK for 3D rendering integration.
"""

import math
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional, Any
from enum import Enum


class OrbitalType(Enum):
    """Types of electron orbitals."""
    S_ORBITAL = "s"
    P_ORBITAL = "p"
    D_ORBITAL = "d"
    F_ORBITAL = "f"


@dataclass
class Vector3D:
    """3D vector representation."""
    x: float
    y: float
    z: float
    
    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __mul__(self, scalar: float) -> 'Vector3D':
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)


@dataclass
class Atom:
    """Represents an atom in 3D space."""
    symbol: str
    position: Vector3D
    atomic_number: int
    radius: float = 1.0
    color: Tuple[float, float, float] = (0.5, 0.5, 0.5)


@dataclass
class Bond:
    """Represents a chemical bond between atoms."""
    atom_a_index: int
    atom_b_index: int
    bond_order: float = 1.0
    color: Tuple[float, float, float] = (0.8, 0.8, 0.8)


class MolecularGeometry:
    """Generates molecular geometry and 3D models."""
    
    @staticmethod
    def predict_geometry(central_atom_symbol: str, 
                        bonded_atoms: List[str],
                        lone_pairs: int = 0) -> str:
        """
        Predict molecular geometry using VSEPR theory.
        
        Args:
            central_atom_symbol: Central atom
            bonded_atoms: List of bonded atom symbols
            lone_pairs: Number of lone pairs
            
        Returns:
            Geometry name (tetrahedral, trigonal, linear, etc.)
        """
        steric_number = len(bonded_atoms) + lone_pairs
        
        if steric_number == 2:
            return "linear"
        elif steric_number == 3:
            return "trigonal_planar" if lone_pairs == 0 else "bent"
        elif steric_number == 4:
            if lone_pairs == 0:
                return "tetrahedral"
            elif lone_pairs == 1:
                return "trigonal_pyramidal"
            else:
                return "bent"
        elif steric_number == 5:
            return "trigonal_bipyramidal"
        elif steric_number == 6:
            return "octahedral"
        return "unknown"
    
    @staticmethod
    def generate_positions(geometry: str, 
                          num_atoms: int) -> List[Vector3D]:
        """
        Generate 3D positions for atoms based on geometry.
        
        Args:
            geometry: Molecular geometry
            num_atoms: Number of atoms to position
            
        Returns:
            List of Vector3D positions
        """
        positions = []
        center = Vector3D(0, 0, 0)
        distance = 1.5
        
        if geometry == "linear":
            positions = [
                Vector3D(-distance, 0, 0),
                Vector3D(distance, 0, 0)
            ]
        
        elif geometry == "trigonal_planar":
            angle_step = 2 * math.pi / 3
            for i in range(3):
                angle = i * angle_step
                x = distance * math.cos(angle)
                y = distance * math.sin(angle)
                positions.append(Vector3D(x, y, 0))
        
        elif geometry == "tetrahedral":
            # Tetrahedral coordinates
            coords = [
                (1, 1, 1),
                (1, -1, -1),
                (-1, 1, -1),
                (-1, -1, 1)
            ]
            norm = math.sqrt(3)
            for x, y, z in coords[:num_atoms]:
                positions.append(Vector3D(
                    x * distance / norm,
                    y * distance / norm,
                    z * distance / norm
                ))
        
        elif geometry == "trigonal_bipyramidal":
            # Equatorial atoms
            for i in range(3):
                angle = 2 * math.pi * i / 3
                positions.append(Vector3D(
                    distance * math.cos(angle),
                    distance * math.sin(angle),
                    0
                ))
            # Axial atoms
            if num_atoms > 3:
                positions.append(Vector3D(0, 0, distance))
            if num_atoms > 4:
                positions.append(Vector3D(0, 0, -distance))
        
        elif geometry == "octahedral":
            positions = [
                Vector3D(distance, 0, 0),
                Vector3D(-distance, 0, 0),
                Vector3D(0, distance, 0),
                Vector3D(0, -distance, 0),
                Vector3D(0, 0, distance),
                Vector3D(0, 0, -distance)
            ]
        
        return positions[:num_atoms]


class OrbitalVisualizer:
    """Generates visual representations of electron orbitals."""
    
    @staticmethod
    def generate_orbital_surface(orbital_type: OrbitalType,
                                 n: int,
                                 l: int,
                                 resolution: int = 20) -> Dict[str, Any]:
        """
        Generate orbital surface mesh data.
        
        Args:
            orbital_type: Type of orbital (s, p, d, f)
            n: Principal quantum number
            l: Angular momentum quantum number
            resolution: Mesh resolution
            
        Returns:
            Dictionary with vertices and faces
        """
        vertices = []
        faces = []
        
        if orbital_type == OrbitalType.S_ORBITAL:
            # Generate sphere (s-orbital)
            vertices, faces = OrbitalVisualizer._generate_sphere(
                radius=n, resolution=resolution
            )
        
        elif orbital_type == OrbitalType.P_ORBITAL:
            # Generate dumbbell shape (p-orbital)
            vertices, faces = OrbitalVisualizer._generate_dumbbell(
                length=n * 2, radius=0.5, resolution=resolution
            )
        
        elif orbital_type == OrbitalType.D_ORBITAL:
            # Generate cloverleaf shape (d-orbital)
            vertices, faces = OrbitalVisualizer._generate_cloverleaf(
                size=n, resolution=resolution
            )
        
        elif orbital_type == OrbitalType.F_ORBITAL:
            # Generate complex f-orbital shape
            vertices, faces = OrbitalVisualizer._generate_f_orbital(
                size=n, resolution=resolution
            )
        
        return {
            'vertices': vertices,
            'faces': faces,
            'orbital_type': orbital_type.value,
            'n': n,
            'l': l
        }
    
    @staticmethod
    def _generate_sphere(radius: float, resolution: int) -> Tuple[List, List]:
        """Generate spherical mesh."""
        vertices = []
        faces = []
        
        for i in range(resolution):
            theta = 2 * math.pi * i / resolution
            for j in range(resolution):
                phi = math.pi * j / resolution
                
                x = radius * math.sin(phi) * math.cos(theta)
                y = radius * math.sin(phi) * math.sin(theta)
                z = radius * math.cos(phi)
                vertices.append((x, y, z))
        
        # Generate faces (simplified)
        for i in range(resolution - 1):
            for j in range(resolution - 1):
                v1 = i * resolution + j
                v2 = i * resolution + j + 1
                v3 = (i + 1) * resolution + j
                v4 = (i + 1) * resolution + j + 1
                
                faces.append((v1, v2, v3))
                faces.append((v2, v4, v3))
        
        return vertices, faces
    
    @staticmethod
    def _generate_dumbbell(length: float, radius: float, 
                          resolution: int) -> Tuple[List, List]:
        """Generate dumbbell-shaped mesh."""
        vertices = []
        faces = []
        
        # Top sphere
        for i in range(resolution):
            theta = 2 * math.pi * i / resolution
            for j in range(resolution // 2):
                phi = math.pi * j / (resolution // 2)
                
                x = radius * math.sin(phi) * math.cos(theta)
                y = radius * math.sin(phi) * math.sin(theta)
                z = length / 2 + radius * math.cos(phi)
                vertices.append((x, y, z))
        
        # Bottom sphere
        for i in range(resolution):
            theta = 2 * math.pi * i / resolution
            for j in range(resolution // 2):
                phi = math.pi * j / (resolution // 2)
                
                x = radius * math.sin(phi) * math.cos(theta)
                y = radius * math.sin(phi) * math.sin(theta)
                z = -length / 2 - radius * math.cos(phi)
                vertices.append((x, y, z))
        
        # Create faces (simplified)
        for i in range(len(vertices) - 2):
            faces.append((i, i + 1, i + 2))
        
        return vertices, faces
    
    @staticmethod
    def _generate_cloverleaf(size: float, resolution: int) -> Tuple[List, List]:
        """Generate cloverleaf (d-orbital) shape."""
        vertices = []
        faces = []
        
        # Generate 4 lobes in xy-plane
        for lobe in range(4):
            lobe_angle = lobe * math.pi / 2
            for i in range(resolution):
                theta = 2 * math.pi * i / resolution
                for j in range(resolution // 2):
                    r = size * (0.3 + 0.7 * math.sin(theta))
                    phi = math.pi * j / (resolution // 2)
                    
                    x = r * math.cos(lobe_angle) * math.cos(phi)
                    y = r * math.sin(lobe_angle) * math.cos(phi)
                    z = r * math.sin(phi) * 0.3
                    vertices.append((x, y, z))
        
        for i in range(len(vertices) - 2):
            faces.append((i, i + 1, i + 2))
        
        return vertices, faces
    
    @staticmethod
    def _generate_f_orbital(size: float, resolution: int) -> Tuple[List, List]:
        """Generate complex f-orbital shape."""
        vertices = []
        faces = []
        
        # Simplified f-orbital with multiple lobes
        for lobe in range(8):
            lobe_angle = lobe * math.pi / 4
            for i in range(resolution):
                theta = 2 * math.pi * i / resolution
                r = size * (0.4 + 0.6 * math.sin(theta * 2))
                
                x = r * math.cos(lobe_angle) * math.sin(theta)
                y = r * math.sin(lobe_angle) * math.sin(theta)
                z = r * math.cos(theta) * 0.5
                vertices.append((x, y, z))
        
        for i in range(len(vertices) - 2):
            faces.append((i, i + 1, i + 2))
        
        return vertices, faces
    
    @staticmethod
    def get_orbital_color(orbital_type: OrbitalType) -> Tuple[float, float, float]:
        """Get RGB color for orbital type."""
        colors = {
            OrbitalType.S_ORBITAL: (1.0, 0.0, 0.0),      # Red
            OrbitalType.P_ORBITAL: (0.0, 1.0, 0.0),      # Green
            OrbitalType.D_ORBITAL: (0.0, 0.0, 1.0),      # Blue
            OrbitalType.F_ORBITAL: (1.0, 1.0, 0.0),      # Yellow
        }
        return colors.get(orbital_type, (0.5, 0.5, 0.5))


class MolecularModel:
    """Complete 3D molecular model representation."""
    
    def __init__(self, name: str):
        """
        Initialize molecular model.
        
        Args:
            name: Name of the molecule
        """
        self.name = name
        self.atoms: List[Atom] = []
        self.bonds: List[Bond] = []
        self.metadata: Dict[str, Any] = {}
    
    def add_atom(self, symbol: str, position: Vector3D, 
                 atomic_number: int, radius: float = 1.0,
                 color: Tuple[float, float, float] = None):
        """Add atom to model."""
        if color is None:
            # Default colors for common atoms
            color_map = {
                'H': (1.0, 1.0, 1.0),      # White
                'C': (0.2, 0.2, 0.2),      # Gray
                'N': (0.0, 0.0, 1.0),      # Blue
                'O': (1.0, 0.0, 0.0),      # Red
                'S': (1.0, 1.0, 0.0),      # Yellow
                'P': (1.0, 0.5, 0.0),      # Orange
            }
            color = color_map.get(symbol, (0.5, 0.5, 0.5))
        
        atom = Atom(symbol, position, atomic_number, radius, color)
        self.atoms.append(atom)
    
    def add_bond(self, atom_a_index: int, atom_b_index: int, 
                 bond_order: float = 1.0):
        """Add bond between atoms."""
        bond = Bond(atom_a_index, atom_b_index, bond_order)
        self.bonds.append(bond)
    
    def get_mesh_data(self) -> Dict[str, Any]:
        """
        Get mesh data for 3D rendering.
        
        Returns:
            Dictionary with vertices, faces, and colors
        """
        vertices = []
        colors = []
        bonds_data = []
        
        # Add atom vertices
        for atom in self.atoms:
            vertices.append(atom.position.to_tuple())
            colors.append(atom.color)
        
        # Add bond data
        for bond in self.bonds:
            atom_a = self.atoms[bond.atom_a_index]
            atom_b = self.atoms[bond.atom_b_index]
            
            bonds_data.append({
                'from': atom_a.position.to_tuple(),
                'to': atom_b.position.to_tuple(),
                'order': bond.bond_order,
                'color': bond.color
            })
        
        return {
            'vertices': vertices,
            'colors': colors,
            'bonds': bonds_data,
            'num_atoms': len(self.atoms),
            'num_bonds': len(self.bonds)
        }
    
    def calculate_properties(self) -> Dict[str, Any]:
        """Calculate molecular properties."""
        # Calculate molecular mass
        mass = 0
        atomic_masses = {
            'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999,
            'S': 32.06, 'P': 30.974, 'Cl': 35.45, 'Br': 79.904
        }
        for atom in self.atoms:
            mass += atomic_masses.get(atom.symbol, atom.atomic_number)
        
        # Calculate center of mass
        com = Vector3D(0, 0, 0)
        for atom in self.atoms:
            com = com + atom.position * atomic_masses.get(atom.symbol, 1)
        if mass > 0:
            com = com * (1 / mass)
        
        # Calculate molecular size
        max_distance = 0
        for atom in self.atoms:
            dist = atom.position.magnitude()
            if dist > max_distance:
                max_distance = dist
        
        return {
            'molecular_mass': mass,
            'center_of_mass': com.to_tuple(),
            'molecular_size': max_distance * 2,
            'num_atoms': len(self.atoms),
            'num_bonds': len(self.bonds)
        }
