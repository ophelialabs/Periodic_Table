namespace PeriodicTableWinForms.UI;

using PeriodicTableWinForms.Models;
using PeriodicTableWinForms.Services;
using System.Windows.Forms;

/// <summary>
/// Main form for the interactive periodic table application.
/// </summary>
public partial class PeriodicTableForm : Form
{
    private ResearchAgentManager _agentManager;
    private ThreeDRenderer _renderer;
    private Element _selectedElement;
    private Dictionary<int, ElementButton> _elementButtons;
    private int _animationFrame = 0;
    private Timer _animationTimer;
    private AnimationFrame[] _currentAnimationFrames;

    public PeriodicTableForm()
    {
        InitializeComponent();
        InitializeServices();
        InitializePeriodicTable();
        SetupEventHandlers();
    }

    private void InitializeComponent()
    {
        this.Text = "Interactive Periodic Table - Quantum Research";
        this.Size = new Size(1600, 1000);
        this.StartPosition = FormStartPosition.CenterScreen;
        this.BackColor = Color.Black;

        // Main layout
        var mainLayout = new TableLayoutPanel
        {
            Dock = DockStyle.Fill,
            ColumnCount = 2,
            RowCount = 1,
            Padding = new Padding(10)
        };

        mainLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 60f));
        mainLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 40f));

        // Periodic table panel
        _tablePanel = new Panel { Dock = DockStyle.Fill, BackColor = Color.Black };

        // Right panel
        var rightPanel = new Panel { Dock = DockStyle.Fill, BackColor = Color.DarkGray };
        var rightLayout = new TableLayoutPanel
        {
            Dock = DockStyle.Fill,
            ColumnCount = 1,
            RowCount = 4,
            Padding = new Padding(5)
        };

        // 3D visualization
        _renderPanel = new Panel { Dock = DockStyle.Fill, BackColor = Color.Black };
        _renderPanel.Paint += RenderPanel_Paint;

        // Element info
        _infoLabel = new Label
        {
            Dock = DockStyle.Fill,
            ForeColor = Color.White,
            BackColor = Color.DarkSlateGray,
            AutoSize = false,
            Text = "Select an element..."
        };

        // Quantum state chart
        _stateChartPanel = new Panel { Dock = DockStyle.Fill, BackColor = Color.Black };
        _stateChartPanel.Paint += StateChartPanel_Paint;

        // Controls
        var controlsPanel = new FlowLayoutPanel
        {
            Dock = DockStyle.Fill,
            FlowDirection = FlowDirection.TopDown,
            BackColor = Color.DarkGray,
            AutoScroll = true
        };

        var analyzeButton = new Button
        {
            Text = "Analyze Element",
            Width = 150,
            Height = 30
        };
        analyzeButton.Click += (s, e) => AnalyzeSelectedElement();

        var rotateLeftBtn = new Button { Text = "Rotate Left", Width = 150, Height = 30 };
        rotateLeftBtn.Click += (s, e) => { _renderer.SetRotation(_rotation.x, _rotation.y + 0.1f, _rotation.z); _renderPanel.Invalidate(); };

        var rotateRightBtn = new Button { Text = "Rotate Right", Width = 150, Height = 30 };
        rotateRightBtn.Click += (s, e) => { _renderer.SetRotation(_rotation.x, _rotation.y - 0.1f, _rotation.z); _renderPanel.Invalidate(); };

        var rotateUpBtn = new Button { Text = "Rotate Up", Width = 150, Height = 30 };
        rotateUpBtn.Click += (s, e) => { _renderer.SetRotation(_rotation.x - 0.1f, _rotation.y, _rotation.z); _renderPanel.Invalidate(); };

        var rotateDownBtn = new Button { Text = "Rotate Down", Width = 150, Height = 30 };
        rotateDownBtn.Click += (s, e) => { _renderer.SetRotation(_rotation.x + 0.1f, _rotation.y, _rotation.z); _renderPanel.Invalidate(); };

        var resetViewBtn = new Button { Text = "Reset View", Width = 150, Height = 30 };
        resetViewBtn.Click += (s, e) => { _rotation = (0, 0, 0); _renderer.SetRotation(0, 0, 0); _renderPanel.Invalidate(); };

        var generateReportBtn = new Button { Text = "Generate Report", Width = 150, Height = 30 };
        generateReportBtn.Click += (s, e) => GenerateReport();

        controlsPanel.Controls.AddRange(new Control[] { analyzeButton, rotateLeftBtn, rotateRightBtn, rotateUpBtn, rotateDownBtn, resetViewBtn, generateReportBtn });

        rightLayout.Controls.Add(_renderPanel, 0, 0);
        rightLayout.Controls.Add(_infoLabel, 0, 1);
        rightLayout.Controls.Add(_stateChartPanel, 0, 2);
        rightLayout.Controls.Add(controlsPanel, 0, 3);

        rightLayout.RowStyles.Add(new RowStyle(SizeType.Percent, 50f));
        rightLayout.RowStyles.Add(new RowStyle(SizeType.Percent, 20f));
        rightLayout.RowStyles.Add(new RowStyle(SizeType.Percent, 15f));
        rightLayout.RowStyles.Add(new RowStyle(SizeType.Percent, 15f));

        mainLayout.Controls.Add(_tablePanel, 0, 0);
        mainLayout.Controls.Add(rightPanel, 1, 0);

        rightPanel.Controls.Add(rightLayout);
        this.Controls.Add(mainLayout);
    }

    private void InitializeServices()
    {
        var logger = LoggerFactory.Create(builder => builder.AddConsole())
            .CreateLogger<ResearchAgentManager>();
        _agentManager = new ResearchAgentManager(logger);
        _renderer = new ThreeDRenderer();
        _elementButtons = new Dictionary<int, ElementButton>();
        _rotation = (0, 0, 0);

        _animationTimer = new Timer();
        _animationTimer.Interval = 50;
        _animationTimer.Tick += AnimationTimer_Tick;
    }

    private void InitializePeriodicTable()
    {
        _tablePanel.Controls.Clear();

        // Layout periodic table with proper positioning
        var elements = ElementDatabase.Elements.Values.OrderBy(e => e.AtomicNumber);

        foreach (var element in elements)
        {
            var button = new Button
            {
                Text = $"{element.Symbol}\n{element.AtomicNumber}",
                Width = 50,
                Height = 50,
                ForeColor = Color.White,
                BackColor = GetCategoryColor(element.Category),
                Font = new Font("Arial", 8, FontStyle.Bold)
            };

            int x = (element.Group - 1) * 55 + 10;
            int y = (element.Period - 1) * 55 + 10;

            button.Location = new Point(x, y);
            button.Click += (s, e) => SelectElement(element);

            _tablePanel.Controls.Add(button);
            _elementButtons[element.AtomicNumber] = new ElementButton { Button = button, Element = element };
        }
    }

    private Color GetCategoryColor(string category)
    {
        return category switch
        {
            "Alkali Metal" => Color.FromArgb(204, 51, 51),
            "Alkaline Earth Metal" => Color.FromArgb(0, 128, 0),
            "Transition Metal" => Color.FromArgb(200, 100, 50),
            "Nonmetal" => Color.FromArgb(128, 128, 128),
            "Noble Gas" => Color.FromArgb(255, 192, 203),
            "Metalloid" => Color.FromArgb(255, 165, 0),
            _ => Color.FromArgb(100, 100, 100)
        };
    }

    private void SelectElement(Element element)
    {
        _selectedElement = element;
        _infoLabel.Text = element.ToString() + Environment.NewLine +
            $"Atomic Mass: {element.AtomicMass:F3}" + Environment.NewLine +
            $"Electronegativity: {element.ElectronegativeityPauling:F2}" + Environment.NewLine +
            $"Category: {element.Category}";

        if (element.ElectronPositions.Length > 0)
        {
            _renderPanel.Invalidate();
        }

        _stateChartPanel.Invalidate();
    }

    private async void AnalyzeSelectedElement()
    {
        if (_selectedElement == null)
        {
            MessageBox.Show("Please select an element first.");
            return;
        }

        try
        {
            this.Cursor = Cursors.WaitCursor;
            _infoLabel.Text = "Analyzing...";

            var result = await _agentManager.AnalyzeElementAsync(_selectedElement);

            _selectedElement = result;
            SelectElement(result);

            _infoLabel.Text += Environment.NewLine + Environment.NewLine + "Analysis Complete!";
        }
        catch (Exception ex)
        {
            MessageBox.Show($"Analysis failed: {ex.Message}");
        }
        finally
        {
            this.Cursor = Cursors.Default;
        }
    }

    private void GenerateReport()
    {
        if (_selectedElement == null)
        {
            MessageBox.Show("Please select an element first.");
            return;
        }

        var report = _agentManager.GenerateResearchReport(_selectedElement);
        var reportForm = new Form
        {
            Text = $"Research Report: {_selectedElement.Name}",
            Size = new Size(600, 500),
            StartPosition = FormStartPosition.CenterParent
        };

        var textBox = new TextBox
        {
            Dock = DockStyle.Fill,
            Multiline = true,
            ReadOnly = true,
            Text = report,
            Font = new Font("Courier New", 10)
        };

        reportForm.Controls.Add(textBox);
        reportForm.ShowDialog(this);
    }

    private void SetupEventHandlers()
    {
        _agentManager.OnAnalysisStarted += (s, e) =>
        {
            _infoLabel.Text = $"Analyzing {e.Element.Name}...";
        };

        _agentManager.OnAnalysisCompleted += (s, e) =>
        {
            _renderPanel.Invalidate();
            _stateChartPanel.Invalidate();
        };
    }

    private void RenderPanel_Paint(object sender, PaintEventArgs e)
    {
        if (_selectedElement?.ElectronPositions.Length > 0)
        {
            var visual = new DynamicModelGenerator().GenerateElectronCloudVisual(_selectedElement);
            var bitmap = _renderer.RenderElectronCloud(visual, _renderPanel.Width, _renderPanel.Height);
            e.Graphics.DrawImageUnscaled(bitmap, 0, 0);
        }
    }

    private void StateChartPanel_Paint(object sender, PaintEventArgs e)
    {
        if (_selectedElement?.QuantumStateAmplitudes.Length > 0)
        {
            var bitmap = _renderer.RenderStateTimeline(_selectedElement.QuantumStateAmplitudes, 
                _stateChartPanel.Width, _stateChartPanel.Height);
            e.Graphics.DrawImageUnscaled(bitmap, 0, 0);
        }
    }

    private void AnimationTimer_Tick(object sender, EventArgs e)
    {
        if (_currentAnimationFrames != null && _currentAnimationFrames.Length > 0)
        {
            _animationFrame = (_animationFrame + 1) % _currentAnimationFrames.Length;
            _renderPanel.Invalidate();
        }
    }

    // Fields
    private Panel _tablePanel;
    private Panel _renderPanel;
    private Label _infoLabel;
    private Panel _stateChartPanel;
    private (float x, float y, float z) _rotation;

    private class ElementButton
    {
        public Button Button { get; set; }
        public Element Element { get; set; }
    }
}
