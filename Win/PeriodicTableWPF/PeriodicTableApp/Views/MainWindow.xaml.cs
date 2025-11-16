using System;
using System.Windows;
using System.Windows.Media.Media3D;
using PeriodicTableApp.ViewModels;

namespace PeriodicTableApp
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            DataContext = new PeriodicTableViewModel();
            Loaded += MainWindow_Loaded;
        }

        private void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {
            // Set up viewport camera
            var camera = viewport3D.Camera as PerspectiveCamera;
            if (camera != null)
            {
                camera.Position = new Point3D(0, 0, 4);
                camera.LookDirection = new Vector3D(0, 0, -4);
                camera.UpDirection = new Vector3D(0, 1, 0);
                camera.FieldOfView = 60;
            }

            // Add default lighting
            var modelGroup = new Model3DGroup();

            // Directional light
            var directionalLight = new DirectionalLight(
                System.Windows.Media.Colors.White,
                new Vector3D(-0.5, -0.5, -1));
            modelGroup.Children.Add(directionalLight);

            // Ambient light
            var ambientLight = new AmbientLight(
                System.Windows.Media.Color.FromArgb(150, 150, 150, 150));
            modelGroup.Children.Add(ambientLight);

            viewport3D.Children.Add(new ModelVisual3D { Content = modelGroup });
        }
    }

    /// <summary>
    /// Converter for boolean to visibility
    /// </summary>
    public class BoolToVisibilityConverter : System.Windows.Data.IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, 
            System.Globalization.CultureInfo culture)
        {
            if (value is bool b)
                return b ? Visibility.Visible : Visibility.Collapsed;
            return Visibility.Collapsed;
        }

        public object ConvertBack(object value, Type targetType, object parameter,
            System.Globalization.CultureInfo culture)
        {
            if (value is Visibility v)
                return v == Visibility.Visible;
            return false;
        }
    }
}
