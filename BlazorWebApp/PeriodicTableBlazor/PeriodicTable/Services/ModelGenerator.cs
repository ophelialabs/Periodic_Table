using PeriodicTable.Models;

namespace PeriodicTable.Services;

/// <summary>
/// Generates 3D visual models and data visualizations from quantum simulation results.
/// </summary>
public class ModelGenerator
{
    private readonly ILogger<ModelGenerator> _logger;

    public ModelGenerator(ILogger<ModelGenerator> logger)
    {
        _logger = logger;
    }

    /// <summary>
    /// Generates a complete 3D visual representation of an element.
    /// </summary>
    public ElementVisual GenerateVisual(Element element, QuantumElementData quantumData)
    {
        _logger.LogInformation($"Generating 3D visual for {element.Symbol}");

        var visual = new ElementVisual
        {
            ElementSymbol = element.Symbol,
            MaterialColor = element.HexColor,
            NucleusPosition = new Vector3D(0, 0, 0),
            ElectronSpheres = GenerateElectronSpheres(quantumData),
            OrbitalRings = GenerateOrbitalRings(quantumData)
        };

        return visual;
    }

    /// <summary>
    /// Generates electron cloud spheres based on probability distribution.
    /// </summary>
    private List<Sphere> GenerateElectronSpheres(QuantumElementData quantumData)
    {
        var spheres = new List<Sphere>();

        if (quantumData.ElectronCloudPoints == null || quantumData.ElectronCloudPoints.Length == 0)
        {
            return spheres;
        }

        // Group points by distance from nucleus to create orbital layers
        var groupedPoints = GroupPointsByDistance(quantumData.ElectronCloudPoints);

        int sphereCount = 0;
        foreach (var group in groupedPoints)
        {
            if (sphereCount >= 20) break; // Limit for performance

            var center = CalculateCentroid(group.Value);
            var radius = CalculateRadius(group.Value);
            var probability = quantumData.ElectronProbabilities.Length > sphereCount 
                ? quantumData.ElectronProbabilities[sphereCount] 
                : 0.5;

            spheres.Add(new Sphere
            {
                Position = center,
                Radius = Math.Max(0.05, radius),
                Opacity = Math.Min(1.0, probability * 1.5), // Scale for visibility
                Color = InterpolateColor(probability)
            });

            sphereCount++;
        }

        return spheres;
    }

    /// <summary>
    /// Generates orbital rings based on calculated orbital radii.
    /// </summary>
    private List<Ring> GenerateOrbitalRings(QuantumElementData quantumData)
    {
        var rings = new List<Ring>();
        var axes = new[] { "X", "Y", "Z" };

        for (int i = 0; i < quantumData.OrbitalRadii.Length; i++)
        {
            var radius = quantumData.OrbitalRadii[i];
            
            // Create one ring per orbital, rotating on different axes
            var ring = new Ring
            {
                Center = new Vector3D(0, 0, 0),
                Radius = radius,
                Axis = axes[i % 3],
                Color = GetOrbitalColor(i, quantumData.OrbitalRadii.Length)
            };

            rings.Add(ring);
        }

        return rings;
    }

    /// <summary>
    /// Groups 3D points by their distance from the origin.
    /// </summary>
    private Dictionary<int, List<Vector3D>> GroupPointsByDistance(Vector3D[] points)
    {
        var groups = new Dictionary<int, List<Vector3D>>();
        const int binCount = 10;

        foreach (var point in points)
        {
            double distance = Math.Sqrt(point.X * point.X + point.Y * point.Y + point.Z * point.Z);
            int bin = Math.Min((int)(distance * binCount), binCount - 1);

            if (!groups.ContainsKey(bin))
            {
                groups[bin] = new List<Vector3D>();
            }

            groups[bin].Add(point);
        }

        return groups.OrderBy(x => x.Key).ToDictionary(x => x.Key, x => x.Value);
    }

    /// <summary>
    /// Calculates the centroid (center) of a set of points.
    /// </summary>
    private Vector3D CalculateCentroid(List<Vector3D> points)
    {
        if (points.Count == 0)
            return new Vector3D(0, 0, 0);

        double avgX = points.Average(p => p.X);
        double avgY = points.Average(p => p.Y);
        double avgZ = points.Average(p => p.Z);

        return new Vector3D(avgX, avgY, avgZ);
    }

    /// <summary>
    /// Calculates the radius (spread) of a set of points.
    /// </summary>
    private double CalculateRadius(List<Vector3D> points)
    {
        if (points.Count == 0)
            return 0.1;

        var centroid = CalculateCentroid(points);
        double maxDistance = points.Max(p =>
        {
            double dx = p.X - centroid.X;
            double dy = p.Y - centroid.Y;
            double dz = p.Z - centroid.Z;
            return Math.Sqrt(dx * dx + dy * dy + dz * dz);
        });

        return maxDistance * 0.5; // Use 50% of max distance as radius
    }

    /// <summary>
    /// Interpolates color based on probability (blue for high, red for low).
    /// </summary>
    private string InterpolateColor(double probability)
    {
        // Clamp to 0-1 range
        probability = Math.Max(0, Math.Min(1, probability));

        // Blue (high probability) to Red (low probability)
        int r = (int)(255 * probability);
        int g = 0;
        int b = (int)(255 * (1 - probability));

        return $"#{r:X2}{g:X2}{b:X2}";
    }

    /// <summary>
    /// Gets color for orbital ring based on shell index.
    /// </summary>
    private string GetOrbitalColor(int shellIndex, int totalShells)
    {
        string[] colors = new[]
        {
            "#00FF00", // Green - 1st shell
            "#00FFFF", // Cyan - 2nd shell
            "#FFFF00", // Yellow - 3rd shell
            "#FF00FF", // Magenta - 4th shell
            "#FF6600"  // Orange - 5th shell
        };

        return colors[shellIndex % colors.Length];
    }

    /// <summary>
    /// Generates JSON representation suitable for Three.js visualization.
    /// </summary>
    public string GenerateThreeJsJson(ElementVisual visual)
    {
        var json = new
        {
            visual.ElementSymbol,
            nucleus = new
            {
                position = new
                {
                    visual.NucleusPosition.X,
                    visual.NucleusPosition.Y,
                    visual.NucleusPosition.Z
                },
                radius = 0.2,
                color = "#FF0000"
            },
            electrons = visual.ElectronSpheres.Select(s => new
            {
                position = new { s.Position.X, s.Position.Y, s.Position.Z },
                s.Radius,
                s.Opacity,
                s.Color
            }),
            orbitals = visual.OrbitalRings.Select(r => new
            {
                center = new { r.Center.X, r.Center.Y, r.Center.Z },
                r.Radius,
                r.Axis,
                r.Color
            })
        };

        return System.Text.Json.JsonSerializer.Serialize(json, new System.Text.Json.JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = false,
            PropertyNamingPolicy = System.Text.Json.JsonNamingPolicy.CamelCase
        });
    }

    /// <summary>
    /// Generates SVG visualization for 2D display.
    /// </summary>
    public string GenerateSvgVisualization(ElementVisual visual, int width = 400, int height = 400)
    {
        var svg = new System.Text.StringBuilder();
        svg.AppendLine($"<svg width=\"{width}\" height=\"{height}\" xmlns=\"http://www.w3.org/2000/svg\">");
        
        // Background
        svg.AppendLine($"<rect width=\"{width}\" height=\"{height}\" fill=\"#1a1a1a\"/>");

        int centerX = width / 2;
        int centerY = height / 2;
        double scale = (width - 40) / 10.0; // Scale factor for display

        // Draw orbital rings
        foreach (var ring in visual.OrbitalRings)
        {
            int radius = (int)(ring.Radius * scale);
            svg.AppendLine($"<circle cx=\"{centerX}\" cy=\"{centerY}\" r=\"{radius}\" " +
                          $"fill=\"none\" stroke=\"{ring.Color}\" stroke-width=\"2\" opacity=\"0.7\"/>");
        }

        // Draw electron spheres
        foreach (var sphere in visual.ElectronSpheres)
        {
            int x = centerX + (int)(sphere.Position.X * scale);
            int y = centerY + (int)(sphere.Position.Y * scale);
            int radius = Math.Max(2, (int)(sphere.Radius * scale * 5));

            svg.AppendLine($"<circle cx=\"{x}\" cy=\"{y}\" r=\"{radius}\" " +
                          $"fill=\"{sphere.Color}\" opacity=\"{sphere.Opacity}\"/>");
        }

        // Draw nucleus
        int nucleusX = centerX + (int)(visual.NucleusPosition.X * scale);
        int nucleusY = centerY + (int)(visual.NucleusPosition.Y * scale);
        svg.AppendLine($"<circle cx=\"{nucleusX}\" cy=\"{nucleusY}\" r=\"6\" fill=\"#FF0000\"/>");

        // Add label
        svg.AppendLine($"<text x=\"{width - 50}\" y=\"30\" font-size=\"20\" fill=\"#FFFFFF\" " +
                      $"font-weight=\"bold\">{visual.ElementSymbol}</text>");

        svg.AppendLine("</svg>");

        return svg.ToString();
    }
}
