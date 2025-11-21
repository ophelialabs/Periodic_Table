using System.Text.Json;
using PToE.ApiService.Models;

namespace PToE.ApiService.Services;

public interface IPeriodicTableService
{
    Task<List<Element>> GetAllElementsAsync();
    Task<Element?> GetElementByNumberAsync(int atomicNumber);
    Task<Element?> GetElementBySymbolAsync(string symbol);
    Task<Element?> GetElementByNameAsync(string name);
    Task<List<Element>> SearchElementsAsync(string query);
    Task<List<Element>> GetElementsByCategoryAsync(string category);
}

public class PeriodicTableService : IPeriodicTableService
{
    private List<Element>? _elements;
    private readonly ILogger<PeriodicTableService> _logger;
    private readonly string _dataFilePath;

    public PeriodicTableService(ILogger<PeriodicTableService> logger, IWebHostEnvironment env)
    {
        _logger = logger;
        // Data file is stored in lib/Periodic-Table-JSON/
        _dataFilePath = Path.Combine(env.ContentRootPath, "lib", "Periodic-Table-JSON", "periodic-table-lookup.json");
    }

    private async Task EnsureDataLoadedAsync()
    {
        if (_elements != null)
            return;

        try
        {
            var json = await File.ReadAllTextAsync(_dataFilePath);
            var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
            var data = JsonSerializer.Deserialize<PeriodicTableData>(json, options);

            if (data == null || data.Elements == null)
            {
                _logger.LogError("Failed to deserialize periodic table data");
                _elements = new();
                return;
            }

            _elements = new();

            // Convert each element from the JSON data
            foreach (var elementName in data.Order)
            {
                if (data.Elements.TryGetValue(elementName, out var elementObj))
                {
                    try
                    {
                        var json_str = JsonSerializer.Serialize(elementObj);
                        var element = JsonSerializer.Deserialize<Element>(json_str, options);
                        if (element != null)
                        {
                            _elements.Add(element);
                        }
                    }
                    catch (Exception ex)
                    {
                        _logger.LogWarning("Failed to deserialize element {ElementName}: {Message}", elementName, ex.Message);
                    }
                }
            }

            _logger.LogInformation("Loaded {ElementCount} elements from periodic table", _elements.Count);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to load periodic table data");
            _elements = new();
        }
    }

    public async Task<List<Element>> GetAllElementsAsync()
    {
        await EnsureDataLoadedAsync();
        return _elements ?? new();
    }

    public async Task<Element?> GetElementByNumberAsync(int atomicNumber)
    {
        await EnsureDataLoadedAsync();
        return _elements?.FirstOrDefault(e => e.AtomicNumber == atomicNumber);
    }

    public async Task<Element?> GetElementBySymbolAsync(string symbol)
    {
        await EnsureDataLoadedAsync();
        return _elements?.FirstOrDefault(e => e.Symbol.Equals(symbol, StringComparison.OrdinalIgnoreCase));
    }

    public async Task<Element?> GetElementByNameAsync(string name)
    {
        await EnsureDataLoadedAsync();
        return _elements?.FirstOrDefault(e => e.Name.Equals(name, StringComparison.OrdinalIgnoreCase));
    }

    public async Task<List<Element>> SearchElementsAsync(string query)
    {
        await EnsureDataLoadedAsync();
        if (string.IsNullOrWhiteSpace(query))
            return _elements ?? new();

        var lowerQuery = query.ToLower();
        return _elements?.Where(e =>
            e.Name.ToLower().Contains(lowerQuery) ||
            e.Symbol.ToLower().Contains(lowerQuery) ||
            (e.Category?.ToLower().Contains(lowerQuery) ?? false)).ToList() ?? new();
    }

    public async Task<List<Element>> GetElementsByCategoryAsync(string category)
    {
        await EnsureDataLoadedAsync();
        return _elements?.Where(e => e.Category.Equals(category, StringComparison.OrdinalIgnoreCase)).ToList() ?? new();
    }
}
