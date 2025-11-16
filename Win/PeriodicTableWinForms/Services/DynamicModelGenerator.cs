namespace PeriodicTableWinForms.Services;

using PeriodicTableWinForms.Models;

/// <summary>
/// Generates 3D models and visual representations from quantum simulation results.
/// Converts probability amplitudes into spatial coordinates for electron visualization.
/// </summary>
public class DynamicModelGenerator
{
    private readonly ILogger<DynamicModelGenerator> _logger;

    public DynamicModelGenerator()
    {
        _logger = LoggerFactory.Create(builder => builder.AddConsole())
            .CreateLogger<DynamicModelGenerator>();
    }

    /// <summary>
    /// Generates 3D electron positions based on quantum state amplitudes.
    /// Uses probability amplitudes to determine electron cloud density.
    /// </summary>
    public (double x, double y, double z)[] GenerateElectronPositions(Element element, double[] amplitudes)
    {
        _logger.LogInformation($"Generating electron positions for {element.Symbol}");

        var positions = new List<(double, double, double)>();
        var random = new Random(element.AtomicNumber);

        // Number of electron particles to visualize
        int particleCount = Math.Min(element.ElectronConfiguration * 50, amplitudes.Length * 2);

        for (int i = 0; i < particleCount; i++)
        {
            // Use amplitude as probability weight for position generation
            double amplitude = amplitudes[i % amplitudes.Length];

            // Generate random position weighted by amplitude
            var (x, y, z) = GenerateWeightedPosition(amplitude, element.AtomicRadius, random);
            positions.Add((x, y, z));
        }

        _logger.LogInformation($"Generated {positions.Count} electron positions");
        return positions.ToArray();
    }

    /// <summary>
    /// Generates a single 3D position weighted by quantum amplitude.
    /// </summary>
    private (double x, double y, double z) GenerateWeightedPosition(double amplitude, double radius, Random random)
    {
        // Use spherical coordinates with radius weighted by amplitude
        double theta = random.NextDouble() * 2 * Math.PI;
        double phi = Math.Acos(2 * random.NextDouble() - 1);
        double r = radius * amplitude * random.NextDouble();

        // Convert to Cartesian
        double x = r * Math.Sin(phi) * Math.Cos(theta);
        double y = r * Math.Sin(phi) * Math.Sin(theta);
        double z = r * Math.Cos(phi);

        return (x, y, z);
    }

    /// <summary>
    /// Generates visual data for rendering electron cloud.
    /// </summary>
    public ElectronCloudVisual GenerateElectronCloudVisual(Element element)
    {
        if (element.ElectronPositions.Length == 0)
        {
            return new ElectronCloudVisual { Particles = Array.Empty<ElectronParticle>() };
        }

        var particles = new List<ElectronParticle>();

        for (int i = 0; i < element.ElectronPositions.Length; i++)
        {
            var pos = element.ElectronPositions[i];
            var amplitude = i < element.QuantumStateAmplitudes.Length 
                ? element.QuantumStateAmplitudes[i] 
                : 0.5;

            particles.Add(new ElectronParticle
            {
                Position = (pos.x, pos.y, pos.z),
                Radius = 2 + (amplitude * 5),
                Opacity = 0.5 + (amplitude * 0.5),
                Color = AdjustColorByAmplitude(element.DisplayColor, amplitude)
            });
        }

        return new ElectronCloudVisual
        {
            ElementSymbol = element.Symbol,
            NucleusRadius = Math.Max(5, element.AtomicNumber / 5.0),
            Particles = particles.ToArray(),
            BoundingRadius = element.AtomicRadius * 1.5
        };
    }

    /// <summary>
    /// Adjusts color brightness based on quantum amplitude.
    /// </summary>
    private (int R, int G, int B) AdjustColorByAmplitude((int R, int G, int B) baseColor, double amplitude)
    {
        var factor = 0.5 + (amplitude * 0.5); // Range from 0.5 to 1.0
        return (
            (int)(baseColor.R * factor),
            (int)(baseColor.G * factor),
            (int)(baseColor.B * factor)
        );
    }

    /// <summary>
    /// Generates animated frame data for visualization over time.
    /// </summary>
    public AnimationFrame[] GenerateAnimationFrames(Element element, int frameCount = 30)
    {
        var frames = new List<AnimationFrame>();
        var random = new Random(element.AtomicNumber);

        for (int frame = 0; frame < frameCount; frame++)
        {
            var positions = new List<(double, double, double)>();
            double timeProgress = frame / (double)frameCount;

            for (int i = 0; i < element.ElectronPositions.Length; i++)
            {
                var basePos = element.ElectronPositions[i];
                var amplitude = element.QuantumStateAmplitudes[i % element.QuantumStateAmplitudes.Length];

                // Apply oscillation based on time
                double oscillation = Math.Sin(timeProgress * Math.PI * 2 + i);
                double scale = 1.0 + (oscillation * amplitude * 0.3);

                positions.Add((
                    basePos.x * scale,
                    basePos.y * scale,
                    basePos.z * scale
                ));
            }

            frames.Add(new AnimationFrame
            {
                FrameNumber = frame,
                TimeProgress = timeProgress,
                Positions = positions.ToArray()
            });
        }

        return frames.ToArray();
    }
}

public class ElectronCloudVisual
{
    public string ElementSymbol { get; set; }
    public double NucleusRadius { get; set; }
    public ElectronParticle[] Particles { get; set; }
    public double BoundingRadius { get; set; }
}

public class ElectronParticle
{
    public (double x, double y, double z) Position { get; set; }
    public double Radius { get; set; }
    public double Opacity { get; set; }
    public (int R, int G, int B) Color { get; set; }
}

public class AnimationFrame
{
    public int FrameNumber { get; set; }
    public double TimeProgress { get; set; }
    public (double x, double y, double z)[] Positions { get; set; }
}
