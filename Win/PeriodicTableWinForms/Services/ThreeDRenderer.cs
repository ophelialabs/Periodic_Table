namespace PeriodicTableWinForms.Services;

using PeriodicTableWinForms.Models;
using System.Drawing;

/// <summary>
/// Renders 3D visualizations of electron clouds in 2D (GDI+).
/// Projects 3D coordinates to 2D for display in Windows Forms.
/// </summary>
public class ThreeDRenderer
{
    private const float CameraDistance = 400f;
    private float _rotationX = 0f;
    private float _rotationY = 0f;
    private float _rotationZ = 0f;

    public void SetRotation(float x, float y, float z)
    {
        _rotationX = x;
        _rotationY = y;
        _rotationZ = z;
    }

    /// <summary>
    /// Renders electron cloud visualization to a bitmap.
    /// </summary>
    public Bitmap RenderElectronCloud(ElectronCloudVisual cloud, int width, int height)
    {
        var bitmap = new Bitmap(width, height);
        using (var graphics = Graphics.FromImage(bitmap))
        {
            graphics.Clear(Color.Black);
            graphics.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;

            var centerX = width / 2f;
            var centerY = height / 2f;

            // Draw nucleus
            var nucleusRadius = (float)cloud.NucleusRadius;
            var nucleusBrush = new SolidBrush(Color.White);
            graphics.FillEllipse(nucleusBrush, centerX - nucleusRadius, centerY - nucleusRadius, 
                nucleusRadius * 2, nucleusRadius * 2);

            // Draw electrons
            var zSorted = cloud.Particles
                .Select((p, i) => new { Particle = p, Index = i, Z = RotateAndProject(p.Position).z })
                .OrderBy(x => x.Z)
                .ToList();

            foreach (var item in zSorted)
            {
                var particle = item.Particle;
                var projected = RotateAndProject(particle.Position);

                // Project 3D to 2D
                float screenX = centerX + (projected.x / (CameraDistance + projected.z)) * 200f;
                float screenY = centerY - (projected.y / (CameraDistance + projected.z)) * 200f;

                if (screenX >= 0 && screenX < width && screenY >= 0 && screenY < height)
                {
                    float radius = (float)particle.Radius;
                    var color = Color.FromArgb(
                        (int)(particle.Opacity * 255),
                        particle.Color.R,
                        particle.Color.G,
                        particle.Color.B
                    );
                    var brush = new SolidBrush(color);
                    graphics.FillEllipse(brush, screenX - radius, screenY - radius, radius * 2, radius * 2);
                }
            }

            // Draw label
            var font = new Font("Arial", 12);
            var textBrush = new SolidBrush(Color.White);
            graphics.DrawString(cloud.ElementSymbol, font, textBrush, centerX + 20, centerY + 20);
        }

        return bitmap;
    }

    /// <summary>
    /// Rotates a 3D point and projects it to 2D screen space.
    /// </summary>
    private (double x, double y, double z) RotateAndProject((double x, double y, double z) point)
    {
        // Apply rotation matrices
        double x = point.x;
        double y = point.y;
        double z = point.z;

        // Rotate around X axis
        double cosX = Math.Cos(_rotationX);
        double sinX = Math.Sin(_rotationX);
        double y1 = y * cosX - z * sinX;
        double z1 = y * sinX + z * cosX;

        // Rotate around Y axis
        double cosY = Math.Cos(_rotationY);
        double sinY = Math.Sin(_rotationY);
        double x2 = x * cosY + z1 * sinY;
        double z2 = -x * sinY + z1 * cosY;

        // Rotate around Z axis
        double cosZ = Math.Cos(_rotationZ);
        double sinZ = Math.Sin(_rotationZ);
        double x3 = x2 * cosZ - y1 * sinZ;
        double y3 = x2 * sinZ + y1 * cosZ;

        return (x3, y3, z2);
    }

    /// <summary>
    /// Renders a timeline of quantum state evolution.
    /// </summary>
    public Bitmap RenderStateTimeline(double[] amplitudes, int width, int height)
    {
        var bitmap = new Bitmap(width, height);
        using (var graphics = Graphics.FromImage(bitmap))
        {
            graphics.Clear(Color.DarkGray);

            float xScale = width / (float)amplitudes.Length;
            float yScale = height / amplitudes.Max();

            using (var pen = new Pen(Color.Cyan, 2f))
            {
                for (int i = 1; i < amplitudes.Length; i++)
                {
                    float x1 = (i - 1) * xScale;
                    float y1 = height - (float)amplitudes[i - 1] * yScale;
                    float x2 = i * xScale;
                    float y2 = height - (float)amplitudes[i] * yScale;

                    graphics.DrawLine(pen, x1, y1, x2, y2);
                }
            }
        }

        return bitmap;
    }
}
