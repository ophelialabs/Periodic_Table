/* Visualization Framework */

let currentVisualization = null;

function initializeVisualizations() {
    // Visualization initialization
}

function showVisualization(vizType) {
    console.log(`Showing visualization: ${vizType}`);
    
    // Get selected element
    const selectedElement = document.querySelector('.element.selected');
    if (!selectedElement) {
        alert('Please select an element first');
        return;
    }
    
    const symbol = selectedElement.dataset.symbol;
    const element = elementsData.find(e => e.symbol === symbol);
    
    if (!element) return;
    
    // Create visualization container
    const vizContainer = createVisualizationWindow(element, vizType);
    document.body.appendChild(vizContainer);
    
    currentVisualization = vizType;
}

function createVisualizationWindow(element, vizType) {
    const container = document.createElement('div');
    container.className = 'viz-window';
    container.id = `viz-${vizType}`;
    
    let content = `
        <div class="viz-header">
            <h3>${element.symbol} - ${getVisualizationTitle(vizType)}</h3>
            <button class="viz-close" onclick="this.parentElement.parentElement.remove()">✕</button>
        </div>
        <div class="viz-content">
    `;
    
    switch(vizType) {
        case '3d-atomic':
            content += generate3DAtomicViz(element);
            break;
        case '3d-ionization':
            content += generate3DIonizationViz(element);
            break;
        case '3d-electron':
            content += generate3DElectronViz(element);
            break;
        case '3d-thermal':
            content += generate3DThermalViz(element);
            break;
        case 'spectral-signature':
            content += generateSpectralViz(element);
            break;
        case 'band-ratio':
            content += generateBandRatioViz(element);
            break;
        case 'wavelength-map':
            content += generateWavelengthViz(element);
            break;
        case 'mineral-detection':
            content += generateMineralViz(element);
            break;
        case 'property-heatmap':
            content += generateHeatmapViz(element);
            break;
        case 'distribution-chart':
            content += generateDistributionViz(element);
            break;
        default:
            content += '<p>Visualization not yet implemented</p>';
    }
    
    content += `</div>`;
    container.innerHTML = content;
    
    // Add styles
    container.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 90%;
        max-width: 1200px;
        height: 600px;
        background: #1a1a1a;
        border: 2px solid #667eea;
        border-radius: 8px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        z-index: 1000;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    `;
    
    const header = container.querySelector('.viz-header');
    header.style.cssText = `
        padding: 1rem;
        border-bottom: 1px solid #333;
        display: flex;
        justify-content: space-between;
        align-items: center;
    `;
    
    const content_div = container.querySelector('.viz-content');
    content_div.style.cssText = `
        flex: 1;
        padding: 1rem;
        overflow: auto;
        display: flex;
        align-items: center;
        justify-content: center;
    `;
    
    const closeBtn = container.querySelector('.viz-close');
    closeBtn.style.cssText = `
        background: none;
        border: none;
        color: #e0e0e0;
        font-size: 1.5rem;
        cursor: pointer;
        padding: 0;
        width: 30px;
        height: 30px;
    `;
    
    return container;
}

function getVisualizationTitle(vizType) {
    const titles = {
        '3d-atomic': '3D Atomic Structure',
        '3d-ionization': 'Ionization Energy Levels',
        '3d-electron': 'Electron Shell Structure',
        '3d-thermal': 'Thermal Properties',
        'spectral-signature': 'Spectral Signature',
        'band-ratio': 'Band Ratio Analysis',
        'wavelength-map': 'Wavelength Mapping',
        'mineral-detection': 'Lithium-bearing Mineral Detection',
        'property-heatmap': 'Property Heatmap',
        'distribution-chart': 'Property Distribution'
    };
    return titles[vizType] || 'Visualization';
}

// Visualization generators
function generate3DAtomicViz(element) {
    return `
        <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
            <p style="text-align: center; color: #aaa;">
                3D Atomic Structure for ${element.symbol}<br>
                <small>Bohr model visualization would be rendered here</small>
            </p>
        </div>
    `;
}

function generate3DIonizationViz(element) {
    return `
        <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
            <p style="text-align: center; color: #aaa;">
                Ionization Energy Visualization for ${element.symbol}<br>
                <small>Energy level transitions would be shown here</small>
            </p>
        </div>
    `;
}

function generate3DElectronViz(element) {
    return `
        <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
            <p style="text-align: center; color: #aaa;">
                Electron Shell Structure for ${element.symbol}<br>
                <small>Electron configuration: ${element.electron_configuration || 'N/A'}</small>
            </p>
        </div>
    `;
}

function generate3DThermalViz(element) {
    return `
        <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
            <p style="text-align: center; color: #aaa;">
                Thermal Properties for ${element.symbol}<br>
                <small>Melting: ${element.melting_point || 'N/A'} K | Boiling: ${element.boiling_point || 'N/A'} K</small>
            </p>
        </div>
    `;
}

function generateSpectralViz(element) {
    return `
        <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
            <p style="text-align: center; color: #aaa;">
                Spectral Signature (200-2500nm)<br>
                <small>Hyperspectral analysis for ${element.symbol} would be displayed here</small>
            </p>
        </div>
    `;
}

function generateBandRatioViz(element) {
    return `
        <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
            <p style="text-align: center; color: #aaa;">
                Band Ratio Analysis<br>
                <small>IR and visible wavelength ratios for ${element.symbol}</small>
            </p>
        </div>
    `;
}

function generateWavelengthViz(element) {
    return `
        <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
            <p style="text-align: center; color: #aaa;">
                Minimum Wavelength Mapping<br>
                <small>Element identification data for ${element.symbol}</small>
            </p>
        </div>
    `;
}

function generateMineralViz(element) {
    return `
        <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
            <p style="text-align: center; color: #aaa;">
                Lithium-bearing Mineral Detection<br>
                <small>4-panel analysis for ${element.symbol}</small>
            </p>
        </div>
    `;
}

function generateHeatmapViz(element) {
    return `
        <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
            <p style="text-align: center; color: #aaa;">
                Property Heatmap Across Periodic Table<br>
                <small>Shows distribution of properties like atomic mass, density, etc.</small>
            </p>
        </div>
    `;
}

function generateDistributionViz(element) {
    return `
        <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
            <p style="text-align: center; color: #aaa;">
                Property Distribution Charts<br>
                <small>Histograms and statistical summaries</small>
            </p>
        </div>
    `;
}

// Initialize visualizations on DOM ready
document.addEventListener('DOMContentLoaded', initializeVisualizations);
