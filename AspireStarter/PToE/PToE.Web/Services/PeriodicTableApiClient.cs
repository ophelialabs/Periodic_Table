using System.Text.Json;
using PToE.Web.Models;

namespace PToE.Web.Services;

public class PeriodicTableApiClient
{
    private readonly HttpClient _client;
    private static readonly JsonSerializerOptions JsonOptions = new() { PropertyNameCaseInsensitive = true };

    public PeriodicTableApiClient(HttpClient client)
    {
        _client = client;
    }

    public async Task<List<Element>?> GetAllElementsAsync()
    {
        try
        {
            var response = await _client.GetAsync("/api/elements");
            response.EnsureSuccessStatusCode();
            var json = await response.Content.ReadAsStringAsync();
            return JsonSerializer.Deserialize<List<Element>>(json, JsonOptions);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error fetching elements: {ex.Message}");
            return null;
        }
    }

    public async Task<Element?> GetElementByNumberAsync(int atomicNumber)
    {
        try
        {
            var response = await _client.GetAsync($"/api/elements/number/{atomicNumber}");
            if (!response.IsSuccessStatusCode)
                return null;
            var json = await response.Content.ReadAsStringAsync();
            return JsonSerializer.Deserialize<Element>(json, JsonOptions);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error fetching element: {ex.Message}");
            return null;
        }
    }

    public async Task<Element?> GetElementBySymbolAsync(string symbol)
    {
        try
        {
            var response = await _client.GetAsync($"/api/elements/symbol/{symbol}");
            if (!response.IsSuccessStatusCode)
                return null;
            var json = await response.Content.ReadAsStringAsync();
            return JsonSerializer.Deserialize<Element>(json, JsonOptions);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error fetching element: {ex.Message}");
            return null;
        }
    }

    public async Task<List<Element>?> SearchElementsAsync(string query)
    {
        try
        {
            var response = await _client.GetAsync($"/api/elements/search?q={Uri.EscapeDataString(query)}");
            if (!response.IsSuccessStatusCode)
                return null;
            var json = await response.Content.ReadAsStringAsync();
            return JsonSerializer.Deserialize<List<Element>>(json, JsonOptions);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error searching elements: {ex.Message}");
            return null;
        }
    }

    public async Task<List<Element>?> GetElementsByCategoryAsync(string category)
    {
        try
        {
            var response = await _client.GetAsync($"/api/elements/category/{Uri.EscapeDataString(category)}");
            if (!response.IsSuccessStatusCode)
                return null;
            var json = await response.Content.ReadAsStringAsync();
            return JsonSerializer.Deserialize<List<Element>>(json, JsonOptions);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error fetching category: {ex.Message}");
            return null;
        }
    }
}
