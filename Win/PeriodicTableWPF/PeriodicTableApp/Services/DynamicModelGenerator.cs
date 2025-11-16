using System;
using System.Windows.Media.Media3D;
using PeriodicTableApp.Models;

namespace PeriodicTableApp.Services
{
    /// <summary>
    /// Dynamically generates 3D models based on quantum simulation results
    /// </summary>
    public class DynamicModelGenerator
    {
        /// <summary>
        /// Generates a complete 3D model for an element based on quantum simulation
        /// </summary>
        public Model3D GenerateElementModel(Element element)
        {
            var modelGroup = new Model3DGroup();

            if (element.OrbitalProbabilities == null || element.OrbitalProbabilities.Length == 0)
            {
                return CreateDefaultElementModel(element);
            }

            // Generate electron cloud
            var electronCloud = ElementVisualizer.GenerateElectronCloud(
                element, 
                element.OrbitalProbabilities);
            modelGroup.Children.Add(electronCloud);

            // Add information label as light
            var light = new DirectionalLight(
                System.Windows.Media.Colors.White,
                new Vector3D(-0.5, -0.5, -1));
            modelGroup.Children.Add(light);

            return modelGroup;
        }

        /// <summary>
        /// Generates a 3D model for a molecular bond between two elements
        /// </summary>
        public Model3D GenerateMolecularBondModel(
            Element element1,
            Element element2,
            double[] bondMetrics)
        {
            var modelGroup = new Model3DGroup();

            var bondModel = ElementVisualizer.GenerateMolecularBond(
                element1, 
                element2, 
                bondMetrics);
            modelGroup.Children.Add(bondModel);

            // Add lighting
            var light = new DirectionalLight(
                System.Windows.Media.Colors.White,
                new Vector3D(-0.3, -0.5, -1));
            modelGroup.Children.Add(light);

            return modelGroup;
        }

        /// <summary>
        /// Generates a 3D material structure based on quantum properties
        /// </summary>
        public Model3D GenerateMaterialStructureModel(MaterialProperties properties)
        {
            var modelGroup = new Model3DGroup();

            int crystalSize = (int)(2 + properties.Density * 4);
            var structure = ElementVisualizer.GenerateMaterialStructure(
                properties,
                crystalSize);
            modelGroup.Children.Add(structure);

            // Add dynamic lighting based on conductivity
            var lightColor = InterpolateColor(
                System.Windows.Media.Colors.DarkBlue,
                System.Windows.Media.Colors.Yellow,
                properties.Conductivity);

            var light = new DirectionalLight(
                lightColor,
                new Vector3D(-0.4, -0.4, -1));
            modelGroup.Children.Add(light);

            // Add ambient light
            var ambientLight = new AmbientLight(
                System.Windows.Media.Color.FromArgb(100, 100, 100, 100));
            modelGroup.Children.Add(ambientLight);

            return modelGroup;
        }

        /// <summary>
        /// Creates an animated electron cloud that updates based on simulation progress
        /// </summary>
        public Model3D GenerateAnimatedElectronCloud(
            Element element,
            double[] orbitalProbabilities,
            int animationFrames = 60)
        {
            var modelGroup = new Model3DGroup();

            // Create multi-layer representation
            for (int layer = 0; layer < orbitalProbabilities.Length; layer++)
            {
                double probability = orbitalProbabilities[layer];
                double radius = (layer + 1) * 0.5;
                double opacity = probability;

                var layerMesh = new MeshGeometry3D();
                CreateSphereMesh(layerMesh, new Point3D(0, 0, 0), radius, 32, 16);

                System.Windows.Media.Color layerColor = InterpolateColor(
                    System.Windows.Media.Colors.Blue,
                    System.Windows.Media.Colors.Cyan,
                    probability);

                var material = new DiffuseMaterial(
                    new System.Windows.Media.SolidColorBrush(layerColor));

                var model = new GeometryModel3D(layerMesh, material);
                modelGroup.Children.Add(model);
            }

            return modelGroup;
        }

        /// <summary>
        /// Generates a reaction pathway visualization showing molecular interactions
        /// </summary>
        public Model3D GenerateReactionPathway(
            Element reactant1,
            Element reactant2,
            Element product,
            double[] reactionMetrics)
        {
            var modelGroup = new Model3DGroup();

            // Position reactants on left, product on right
            double spacing = 2.0;

            // Reactant 1
            var r1Mesh = new MeshGeometry3D();
            var r1Pos = new Point3D(-spacing, spacing / 2, 0);
            CreateSphereMesh(r1Mesh, r1Pos, 0.4, 12, 8);
            var r1Material = new DiffuseMaterial(
                new System.Windows.Media.SolidColorBrush(
                    System.Windows.Media.Color.FromArgb(255, 100, 150, 255)));
            var r1Model = new GeometryModel3D(r1Mesh, r1Material);
            modelGroup.Children.Add(r1Model);

            // Reactant 2
            var r2Mesh = new MeshGeometry3D();
            var r2Pos = new Point3D(-spacing, -spacing / 2, 0);
            CreateSphereMesh(r2Mesh, r2Pos, 0.4, 12, 8);
            var r2Material = new DiffuseMaterial(
                new System.Windows.Media.SolidColorBrush(
                    System.Windows.Media.Color.FromArgb(255, 150, 100, 255)));
            var r2Model = new GeometryModel3D(r2Mesh, r2Material);
            modelGroup.Children.Add(r2Model);

            // Product
            var pMesh = new MeshGeometry3D();
            var pPos = new Point3D(spacing, 0, 0);
            CreateSphereMesh(pMesh, pPos, 0.5, 12, 8);
            var pMaterial = new DiffuseMaterial(
                new System.Windows.Media.SolidColorBrush(
                    System.Windows.Media.Color.FromArgb(255, 100, 255, 100)));
            var pModel = new GeometryModel3D(pMesh, pMaterial);
            modelGroup.Children.Add(pModel);

            // Connection arrows (simplified as lines)
            var connectionMesh = new MeshGeometry3D();
            CreateCylinderMesh(connectionMesh, r1Pos, pPos, 0.08);
            CreateCylinderMesh(connectionMesh, r2Pos, pPos, 0.08);

            var connectionMaterial = new DiffuseMaterial(
                new System.Windows.Media.SolidColorBrush(
                    System.Windows.Media.Colors.Orange));
            var connectionModel = new GeometryModel3D(connectionMesh, connectionMaterial);
            modelGroup.Children.Add(connectionModel);

            return modelGroup;
        }

        // Helper methods

        private Model3D CreateDefaultElementModel(Element element)
        {
            var modelGroup = new Model3DGroup();

            var mesh = new MeshGeometry3D();
            CreateSphereMesh(mesh, new Point3D(0, 0, 0), 0.5, 16, 8);

            System.Windows.Media.Color elementColor = HexToColor(element.Color);
            var material = new DiffuseMaterial(
                new System.Windows.Media.SolidColorBrush(elementColor));

            var model = new GeometryModel3D(mesh, material);
            modelGroup.Children.Add(model);

            return modelGroup;
        }

        private void CreateSphereMesh(MeshGeometry3D mesh, Point3D center, double radius,
            int longitudeDivisions = 16, int latitudeDivisions = 8)
        {
            double pi = Math.PI;

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

        private void CreateCylinderMesh(MeshGeometry3D mesh, Point3D start, Point3D end, double radius)
        {
            Vector3D direction = end - start;
            double length = direction.Length;
            if (length < 0.001) return;

            direction.Normalize();

            Vector3D perpendicular = Math.Abs(direction.X) < 0.9
                ? new Vector3D(0, 1, 0)
                : new Vector3D(1, 0, 0);

            Vector3D right = Vector3D.CrossProduct(direction, perpendicular);
            right.Normalize();
            Vector3D up = Vector3D.CrossProduct(right, direction);
            up.Normalize();

            int segments = 8;
            int startIndex = mesh.Positions.Count;

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

            for (int j = 0; j < segments; j++)
            {
                int current = startIndex + j;
                int next = startIndex + (j + 1) % segments;
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

        private System.Windows.Media.Color InterpolateColor(
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

        private System.Windows.Media.Color HexToColor(string hex)
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
