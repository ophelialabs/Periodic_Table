using PToE.ApiService.Services;

var builder = WebApplication.CreateBuilder(args);

// Add service defaults & Aspire client integrations.
builder.AddServiceDefaults();

// Add services
builder.Services.AddScoped<IPeriodicTableService, PeriodicTableService>();
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.WithOrigins("https+http://webfrontend", "http://localhost:3000", "https://localhost:3001")
            .AllowAnyMethod()
            .AllowAnyHeader();
    });
});

var app = builder.Build();

app.UseCors();

// Map health check endpoint
app.MapDefaultEndpoints();

// Periodic Table API Endpoints
var group = app.MapGroup("/api/elements").WithName("Periodic Table");

group.MapGet("/", GetAllElements)
    .WithName("GetAllElements")
    .WithSummary("Get all elements from the periodic table");

group.MapGet("/search", SearchElements)
    .WithName("SearchElements")
    .WithSummary("Search elements by name, symbol, or category");

group.MapGet("/category/{category}", GetElementsByCategory)
    .WithName("GetElementsByCategory")
    .WithSummary("Get elements by category");

group.MapGet("/number/{number}", GetElementByNumber)
    .WithName("GetElementByNumber")
    .WithSummary("Get element by atomic number");

group.MapGet("/symbol/{symbol}", GetElementBySymbol)
    .WithName("GetElementBySymbol")
    .WithSummary("Get element by chemical symbol");

group.MapGet("/name/{name}", GetElementByName)
    .WithName("GetElementByName")
    .WithSummary("Get element by name");

app.Run();

// Endpoint implementations
async Task<IResult> GetAllElements(IPeriodicTableService service)
{
    var elements = await service.GetAllElementsAsync();
    return Results.Ok(elements);
}

async Task<IResult> SearchElements(IPeriodicTableService service, string? q)
{
    if (string.IsNullOrWhiteSpace(q))
        return Results.BadRequest("Search query is required");

    var results = await service.SearchElementsAsync(q);
    return Results.Ok(results);
}

async Task<IResult> GetElementsByCategory(IPeriodicTableService service, string category)
{
    var elements = await service.GetElementsByCategoryAsync(category);
    if (!elements.Any())
        return Results.NotFound($"No elements found in category: {category}");

    return Results.Ok(elements);
}

async Task<IResult> GetElementByNumber(IPeriodicTableService service, int number)
{
    var element = await service.GetElementByNumberAsync(number);
    return element == null ? Results.NotFound($"Element with atomic number {number} not found") : Results.Ok(element);
}

async Task<IResult> GetElementBySymbol(IPeriodicTableService service, string symbol)
{
    var element = await service.GetElementBySymbolAsync(symbol);
    return element == null ? Results.NotFound($"Element with symbol {symbol} not found") : Results.Ok(element);
}

async Task<IResult> GetElementByName(IPeriodicTableService service, string name)
{
    var element = await service.GetElementByNameAsync(name);
    return element == null ? Results.NotFound($"Element with name {name} not found") : Results.Ok(element);
}
