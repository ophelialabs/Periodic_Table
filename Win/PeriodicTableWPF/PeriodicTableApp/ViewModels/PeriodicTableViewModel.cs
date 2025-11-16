using System;
using System.Collections.ObjectModel;
using System.Windows.Input;
using System.Windows.Media.Media3D;
using PeriodicTableApp.Models;
using PeriodicTableApp.Services;

namespace PeriodicTableApp.ViewModels
{
    /// <summary>
    /// ViewModel for managing the periodic table and element interactions
    /// </summary>
    public class PeriodicTableViewModel : ViewModelBase
    {
        private readonly ResearchAgentManager _researchAgent;
        private readonly PeriodicTableDataService _dataService;
        private Element _selectedElement;
        private Element _selectedElement2;
        private Model3D _current3DModel;
        private string _statusMessage;
        private int _progressValue;
        private bool _isLoading;

        public ObservableCollection<Element> AllElements { get; }
        public RelayCommand<Element> SelectElementCommand { get; }
        public RelayCommand SimulateElementCommand { get; }
        public RelayCommand SimulateBondCommand { get; }
        public RelayCommand ClearSelectionCommand { get; }

        public PeriodicTableViewModel()
        {
            _researchAgent = new ResearchAgentManager();
            _dataService = new PeriodicTableDataService();
            
            AllElements = new ObservableCollection<Element>();
            
            SelectElementCommand = new RelayCommand<Element>(SelectElement);
            SimulateElementCommand = new RelayCommand(SimulateElement, CanSimulate);
            SimulateBondCommand = new RelayCommand(SimulateBond, CanSimulateBond);
            ClearSelectionCommand = new RelayCommand(ClearSelection);

            InitializeElements();
            SubscribeToResearchAgent();
            
            StatusMessage = "Ready";
        }

        // Properties

        public Element SelectedElement
        {
            get => _selectedElement;
            set
            {
                if (SetProperty(ref _selectedElement, value))
                {
                    OnPropertyChanged(nameof(CanSimulateBond));
                }
            }
        }

        public Element SelectedElement2
        {
            get => _selectedElement2;
            set
            {
                if (SetProperty(ref _selectedElement2, value))
                {
                    OnPropertyChanged(nameof(CanSimulateBond));
                }
            }
        }

        public Model3D Current3DModel
        {
            get => _current3DModel;
            set => SetProperty(ref _current3DModel, value);
        }

        public string StatusMessage
        {
            get => _statusMessage;
            set => SetProperty(ref _statusMessage, value);
        }

        public int ProgressValue
        {
            get => _progressValue;
            set => SetProperty(ref _progressValue, value);
        }

        public bool IsLoading
        {
            get => _isLoading;
            set => SetProperty(ref _isLoading, value);
        }

        public bool CanSimulate => _selectedElement != null && !IsLoading;
        public bool CanSimulateBond => _selectedElement != null && _selectedElement2 != null && !IsLoading;

        // Commands

        private void SelectElement(Element element)
        {
            SelectedElement = element;
            StatusMessage = $"Selected: {element.Name}";
        }

        private async void SimulateElement()
        {
            if (!CanSimulate || _selectedElement == null)
                return;

            IsLoading = true;
            ProgressValue = 0;

            try
            {
                await _researchAgent.SimulateElementAsync(_selectedElement);
                Current3DModel = new Model3DGroup();
            }
            catch (Exception ex)
            {
                StatusMessage = $"Error: {ex.Message}";
            }
            finally
            {
                IsLoading = false;
            }
        }

        private async void SimulateBond()
        {
            if (!CanSimulateBond)
                return;

            IsLoading = true;
            ProgressValue = 0;

            try
            {
                var result = await _researchAgent.SimulateMolecularBondAsync(
                    _selectedElement, 
                    _selectedElement2);

                if (result != null)
                {
                    Current3DModel = result.Model3D;
                    StatusMessage = $"Bond simulation complete - Strength: {result.BondStrength:F2}";
                }
            }
            catch (Exception ex)
            {
                StatusMessage = $"Error: {ex.Message}";
            }
            finally
            {
                IsLoading = false;
            }
        }

        private void ClearSelection()
        {
            SelectedElement = null;
            SelectedElement2 = null;
            Current3DModel = null;
            StatusMessage = "Selection cleared";
        }

        // Private methods

        private void InitializeElements()
        {
            var elements = _dataService.GetAllElements();
            foreach (var element in elements)
            {
                AllElements.Add(element);
            }
        }

        private void SubscribeToResearchAgent()
        {
            _researchAgent.ProgressUpdated += (s, e) =>
            {
                StatusMessage = e.Status;
                ProgressValue = e.Progress;
            };

            _researchAgent.ResearchCompleted += (s, e) =>
            {
                Current3DModel = e.Model3D;
                StatusMessage = $"Simulation complete: {e.Element.Symbol}";
                ProgressValue = 100;
            };

            _researchAgent.ErrorOccurred += (s, e) =>
            {
                StatusMessage = e.Message;
                IsLoading = false;
            };
        }
    }

    /// <summary>
    /// Base view model class with property change notification
    /// </summary>
    public abstract class ViewModelBase : System.ComponentModel.INotifyPropertyChanged
    {
        public event System.ComponentModel.PropertyChangedEventHandler PropertyChanged;

        protected void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new System.ComponentModel.PropertyChangedEventArgs(propertyName));
        }

        protected bool SetProperty<T>(ref T storage, T value, [System.Runtime.CompilerServices.CallerMemberName] string propertyName = null)
        {
            if (Equals(storage, value))
                return false;

            storage = value;
            OnPropertyChanged(propertyName);
            return true;
        }
    }

    /// <summary>
    /// Relay command for MVVM
    /// </summary>
    public class RelayCommand : ICommand
    {
        private readonly Action _execute;
        private readonly Func<bool> _canExecute;

        public RelayCommand(Action execute, Func<bool> canExecute = null)
        {
            _execute = execute ?? throw new ArgumentNullException(nameof(execute));
            _canExecute = canExecute;
        }

        public event EventHandler CanExecuteChanged
        {
            add => CommandManager.RequerySuggested += value;
            remove => CommandManager.RequerySuggested -= value;
        }

        public bool CanExecute(object parameter) => _canExecute?.Invoke() ?? true;
        public void Execute(object parameter) => _execute();
    }

    /// <summary>
    /// Generic relay command for parameters
    /// </summary>
    public class RelayCommand<T> : ICommand
    {
        private readonly Action<T> _execute;
        private readonly Predicate<T> _canExecute;

        public RelayCommand(Action<T> execute, Predicate<T> canExecute = null)
        {
            _execute = execute ?? throw new ArgumentNullException(nameof(execute));
            _canExecute = canExecute;
        }

        public event EventHandler CanExecuteChanged
        {
            add => CommandManager.RequerySuggested += value;
            remove => CommandManager.RequerySuggested -= value;
        }

        public bool CanExecute(object parameter) => _canExecute?.Invoke((T)parameter) ?? true;
        public void Execute(object parameter) => _execute((T)parameter);
    }
}
