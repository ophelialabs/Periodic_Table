/* Element Details Panel Management */

function initializeElementDetails() {
    // Details panel initialization
    const detailsPanel = document.getElementById('elementDetails');
    if (detailsPanel) {
        // Default message already in HTML
    }
}

function displayElementComparison(symbols) {
    const detailsDiv = document.getElementById('elementDetails');
    if (!detailsDiv) return;
    
    const elements = symbols
        .map(s => elementsData.find(e => e.symbol === s))
        .filter(e => e);
    
    if (elements.length === 0) return;
    
    let html = '<div class="comparison-container">';
    html += `<h3>Comparing ${elements.length} Elements</h3>`;
    
    elements.forEach(element => {
        html += `
            <div class="comparison-element">
                <div class="element-header">
                    <h3>${element.symbol}</h3>
                    <p>${element.name}</p>
                </div>
                <div class="element-info">
                    <div class="element-property">
                        <div class="element-property-name">Atomic Mass</div>
                        <div class="element-property-value">${(parseFloat(element.atomic_mass) || 0).toFixed(2)}</div>
                    </div>
                    <div class="element-property">
                        <div class="element-property-name">Category</div>
                        <div class="element-property-value">${element.category || 'Unknown'}</div>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    detailsDiv.innerHTML = html;
}

function getElementInfo(symbol) {
    return elementsData.find(e => e.symbol === symbol.toUpperCase());
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', initializeElementDetails);
