using System.Text.Json.Serialization;

namespace PToE.Web.Models;

public class Element
{
    [JsonPropertyName("name")]
    public string Name { get; set; } = string.Empty;

    [JsonPropertyName("symbol")]
    public string Symbol { get; set; } = string.Empty;

    [JsonPropertyName("number")]
    public int AtomicNumber { get; set; }

    [JsonPropertyName("atomic_mass")]
    public double AtomicMass { get; set; }

    [JsonPropertyName("category")]
    public string Category { get; set; } = string.Empty;

    [JsonPropertyName("appearance")]
    public string? Appearance { get; set; }

    [JsonPropertyName("boil")]
    public double? BoilingPoint { get; set; }

    [JsonPropertyName("melt")]
    public double? MeltingPoint { get; set; }

    [JsonPropertyName("density")]
    public double? Density { get; set; }

    [JsonPropertyName("discovered_by")]
    public string? DiscoveredBy { get; set; }

    [JsonPropertyName("named_by")]
    public string? NamedBy { get; set; }

    [JsonPropertyName("period")]
    public int Period { get; set; }

    [JsonPropertyName("group")]
    public int Group { get; set; }

    [JsonPropertyName("phase")]
    public string Phase { get; set; } = string.Empty;

    [JsonPropertyName("source")]
    public string? WikipediaSource { get; set; }

    [JsonPropertyName("summary")]
    public string? Summary { get; set; }

    [JsonPropertyName("xpos")]
    public int XPosition { get; set; }

    [JsonPropertyName("ypos")]
    public int YPosition { get; set; }

    [JsonPropertyName("wxpos")]
    public int WidthXPosition { get; set; }

    [JsonPropertyName("wypos")]
    public int WidthYPosition { get; set; }

    [JsonPropertyName("shells")]
    public List<int>? Shells { get; set; }

    [JsonPropertyName("electron_configuration")]
    public string? ElectronConfiguration { get; set; }

    [JsonPropertyName("electron_configuration_semantic")]
    public string? ElectronConfigurationSemantic { get; set; }

    [JsonPropertyName("electron_affinity")]
    public double? ElectronAffinity { get; set; }

    [JsonPropertyName("electronegativity_pauling")]
    public double? Electronegativity { get; set; }

    [JsonPropertyName("ionization_energies")]
    public List<double>? IonizationEnergies { get; set; }

    [JsonPropertyName("cpk-hex")]
    public string? CpkHex { get; set; }

    [JsonPropertyName("block")]
    public string? Block { get; set; }

    [JsonPropertyName("bohr_model_3d")]
    public string? BohrModel3D { get; set; }

    [JsonPropertyName("bohr_model_image")]
    public string? BohrModelImage { get; set; }

    [JsonPropertyName("spectral_img")]
    public string? SpectralImage { get; set; }

    [JsonPropertyName("image")]
    public ElementImage? Image { get; set; }

    [JsonPropertyName("molar_heat")]
    public double? MolarHeat { get; set; }
}

public class ElementImage
{
    [JsonPropertyName("title")]
    public string Title { get; set; } = string.Empty;

    [JsonPropertyName("url")]
    public string Url { get; set; } = string.Empty;

    [JsonPropertyName("attribution")]
    public string Attribution { get; set; } = string.Empty;
}
