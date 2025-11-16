using System;
using System.Windows.Media.Media3D;
using System.Collections.Generic;
using System.Linq;

namespace PeriodicTableApp.Services
{
    /// <summary>
    /// Handles visual representation and 3D modeling of individual elements
    /// </summary>
    public class ElementVisualizer
    {
        /// <summary>
        /// Generates a 3D electron cloud representation based on orbital probabilities
        /// </summary>
        public static Model3D GenerateElectronCloud(Models.Element element, double[] orbitalProbabilities)
        {
            var modelGroup = new Model3DGroup();

            if (element?.OrbitalProbabilities == null || element.OrbitalProbabilities.Length == 0)
                return modelGroup;

            // Create nucleus representation
            var nucleusMesh = new MeshGeometry3D();
            AddSphereMesh(nucleusMesh, new Point3D(0, 0, 0), 0.15);
            
            var nucleusMaterial = new DiffuseMaterial(
                new System.Windows.Media.SolidColorBrush(System.Windows.Media.Colors.Red));
            var nucleusModel = new GeometryModel3D(nucleusMesh, nucleusMaterial);
            modelGroup.Children.Add(nucleusModel);

            // Generate electron probability shells
            int shellCount = Math.Min(element.AtomicNumber / 2 + 1, 5);
            
            for (int shell = 0; shell < shellCount; shell++)
            {
                double shellRadius = (shell + 1) * 0.4;
                double probability = shell < orbitalProbabilities.Length 
                    ? orbitalProbabilities[shell] 
                    : 0.5;

                // Create electron probability sphere
                var shellMesh = new MeshGeometry3D();
                AddSphereMesh(shellMesh, new Point3D(0, 0, 0), shellRadius, 
                    (int)(16 + shell * 8), (int)(8 + shell * 4));

                // Color based on probability
                System.Windows.Media.Color shellColor = InterpolateColor(
                    System.Windows.Media.Colors.Blue,
                    System.Windows.Media.Colors.Green,
                    probability);

                var shellMaterial = new DiffuseMaterial(
                    new System.Windows.Media.SolidColorBrush(shellColor))
                {
                    AmbientColor = shellColor
                };

                var shellModel = new GeometryModel3D(shellMesh, shellMaterial);
                modelGroup.Children.Add(shellModel);

                // Add electron position indicators
                int electronCount = (int)Math.Round(probability * 8);
                AddElectronIndicators(modelGroup, shellRadius, electronCount, shell);
            }

            return modelGroup;
        }

        /// <summary>
        /// Generates a 3D molecular bonding visualization between two elements
        /// </summary>
        public static Model3D GenerateMolecularBond(
            Models.Element element1, 
            Models.Element element2,
            double[] bondMetrics)
        {
            var modelGroup = new Model3DGroup();

            if (bondMetrics == null || bondMetrics.Length < 3)
                return modelGroup;

            double bondDistance = 1.5;
            double bondStrength = bondMetrics[1];
            double energy = bondMetrics[2];

            // Create atom 1
            var atom1Mesh = new MeshGeometry3D();
            var atom1Pos = new Point3D(-bondDistance / 2, 0, 0);
            AddSphereMesh(atom1Mesh, atom1Pos, 0.3);
            
            var atom1Material = new DiffuseMaterial(
                new System.Windows.Media.SolidColorBrush(HexToColor(element1.Color)));
            var atom1Model = new GeometryModel3D(atom1Mesh, atom1Material);
            modelGroup.Children.Add(atom1Model);

            // Create atom 2
            var atom2Mesh = new MeshGeometry3D();
            var atom2Pos = new Point3D(bondDistance / 2, 0, 0);
            AddSphereMesh(atom2Mesh, atom2Pos, 0.3);
            
            var atom2Material = new DiffuseMaterial(
                new System.Windows.Media.SolidColorBrush(HexToColor(element2.Color)));
            var atom2Model = new GeometryModel3D(atom2Mesh, atom2Material);
            modelGroup.Children.Add(atom2Model);

            // Create bond visualization
            double bondThickness = 0.08 + (bondStrength * 0.12);
            var bondMesh = new MeshGeometry3D();
            AddCylinderMesh(bondMesh, atom1Pos, atom2Pos, bondThickness);

            System.Windows.Media.Color bondColor = InterpolateColor(
                System.Windows.Media.Colors.Orange,
                System.Windows.Media.Colors.Yellow,
                bondStrength);

            var bondMaterial = new DiffuseMaterial(
                new System.Windows.Media.SolidColorBrush(bondColor));
            var bondModel = new GeometryModel3D(bondMesh, bondMaterial);
            modelGroup.Children.Add(bondModel);

            return modelGroup;
        }

        /// <summary>
        /// Generates a material structure visualization based on quantum properties
        /// </summary>
        public static Model3D GenerateMaterialStructure(
            Models.MaterialProperties properties,
            int crystalSize = 3)
        {
            var modelGroup = new Model3DGroup();

            // Create lattice structure based on properties
            double density = 0.5 + properties.Density * 0.5;
            double hardness = properties.Hardness;

            for (int x = 0; x < crystalSize; x++)
            {
                for (int y = 0; y < crystalSize; y++)
                {
                    for (int z = 0; z < crystalSize; z++)
                    {
                        double spacing = 0.5 / density;
                        var position = new Point3D(
                            x * spacing - (crystalSize - 1) * spacing / 2,
                            y * spacing - (crystalSize - 1) * spacing / 2,
                            z * spacing - (crystalSize - 1) * spacing / 2);

                        var atomMesh = new MeshGeometry3D();
                        double atomRadius = 0.1 + hardness * 0.1;
                        AddSphereMesh(atomMesh, position, atomRadius, 8, 6);

                        System.Windows.Media.Color atomColor = InterpolateColor(
                            System.Windows.Media.Colors.Cyan,
                            System.Windows.Media.Colors.Red,
                            properties.Conductivity);

                        var atomMaterial = new DiffuseMaterial(
                            new System.Windows.Media.SolidColorBrush(atomColor));
                        var atomModel = new GeometryModel3D(atomMesh, atomMaterial);
                        modelGroup.Children.Add(atomModel);
                    }
                }
            }

            return modelGroup;
        }

        // Helper Methods

        private static void AddSphereMesh(MeshGeometry3D mesh, Point3D center, double radius,
            int longitudeDivisions = 16, int latitudeDivisions = 8)
        {
            double pi = Math.PI;
            int vertexCount = 0;

            for (int lat = 0; lat <= latitudeDivisions; lat++)
            {
                double phi = pi * lat / latitudeDivisions;
                double sinPhi = Math.Sin(phi);
                double cosPhi = Math.Cos(phi);

                for (int lon = 0; lon <= longitudeDivisions; lon++)
                {
                    double theta = 2 * pi * lon / longitudeDivisions;
                    double sinTheta = Math.Sin(theta);
                    double cosTheta = Math.Cos(theta);

                    double x = radius * sinPhi * cosTheta;
                    double y = radius * cosPhi;
                    double z = radius * sinPhi * sinTheta;

                    mesh.Positions.Add(new Point3D(center.X + x, center.Y + y, center.Z + z));
                }
            }

            // Add triangles
            for (int lat = 0; lat < latitudeDivisions; lat++)
            {
                for (int lon = 0; lon < longitudeDivisions; lon++)
                {
                    int first = lat * (longitudeDivisions + 1) + lon;
                    int second = first + longitudeDivisions + 1;

                    mesh.TriangleIndices.Add(first);
                    mesh.TriangleIndices.Add(second);
                    mesh.TriangleIndices.Add(first + 1);

                    mesh.TriangleIndices.Add(first + 1);
                    mesh.TriangleIndices.Add(second);
                    mesh.TriangleIndices.Add(second + 1);
                }
            }
        }

        private static void AddCylinderMesh(MeshGeometry3D mesh, Point3D start, Point3D end, double radius)
        {
            Vector3D direction = end - start;
            double length = direction.Length;
            direction.Normalize();

            Vector3D perpendicular = Math.Abs(direction.X) < 0.9
                ? new Vector3D(0, 1, 0)
                : new Vector3D(1, 0, 0);

            Vector3D right = Vector3D.CrossProduct(direction, perpendicular);
            right.Normalize();
            Vector3D up = Vector3D.CrossProduct(right, direction);
            up.Normalize();

            int segments = 12;
            for (int i = 0; i <= 1; i++)
            {
                Point3D basePoint = i == 0 ? start : end;
                for (int j = 0; j < segments; j++)
                {
                    double angle = 2 * Math.PI * j / segments;
                    double x = Math.Cos(angle) * radius;
                    double y = Math.Sin(angle) * radius;

                    Point3D point = basePoint + x * right + y * up;
                    mesh.Positions.Add(point);
                }
            }

            // Add side triangles
            for (int j = 0; j < segments; j++)
            {
                int current = j;
                int next = (j + 1) % segments;
                int currentTop = current + segments;
                int nextTop = next + segments;

                mesh.TriangleIndices.Add(current);
                mesh.TriangleIndices.Add(currentTop);
                mesh.TriangleIndices.Add(next);

                mesh.TriangleIndices.Add(next);
                mesh.TriangleIndices.Add(currentTop);
                mesh.TriangleIndices.Add(nextTop);
            }
        }

        private static void AddElectronIndicators(Model3DGroup group, double radius, int count, int shell)
        {
            for (int i = 0; i < count; i++)
            {
                double angle = 2 * Math.PI * i / count;
                double x = radius * Math.Cos(angle);
                double z = radius * Math.Sin(angle);

                var electronMesh = new MeshGeometry3D();
                AddSphereMesh(electronMesh, new Point3D(x, 0, z), 0.08, 6, 4);

                var electronMaterial = new DiffuseMaterial(
                    new System.Windows.Media.SolidColorBrush(System.Windows.Media.Colors.Yellow));
                var electronModel = new GeometryModel3D(electronMesh, electronMaterial);
                group.Children.Add(electronModel);
            }
        }

        private static System.Windows.Media.Color InterpolateColor(
            System.Windows.Media.Color color1,
            System.Windows.Media.Color color2,
            double factor)
        {
            factor = Math.Clamp(factor, 0, 1);
            return System.Windows.Media.Color.FromArgb(
                (byte)(color1.A * (1 - factor) + color2.A * factor),
                (byte)(color1.R * (1 - factor) + color2.R * factor),
                (byte)(color1.G * (1 - factor) + color2.G * factor),
                (byte)(color1.B * (1 - factor) + color2.B * factor));
        }

        private static System.Windows.Media.Color HexToColor(string hex)
        {
            try
            {
                hex = hex.TrimStart('#');
                if (hex.Length == 6)
                {
                    return (System.Windows.Media.Color)System.Windows.Media.ColorConverter.ConvertFromString("#" + hex);
                }
            }
            catch { }
            return System.Windows.Media.Colors.Gray;
        }
    }
}
