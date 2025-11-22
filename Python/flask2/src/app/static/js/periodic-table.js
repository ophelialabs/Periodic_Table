/* Periodic Table JavaScript */

let periodicTable = null;

function initializePeriodicTable() {
    periodicTable = document.getElementById('periodicTable');
    renderPeriodicTable();
}

function renderPeriodicTable() {
    if (!periodicTable || !elementsData) return;
    
    periodicTable.innerHTML = '';
    
    // Get unique positions to create proper grid layout
    const maxRow = Math.max(...elementsData.map(e => e.period || 1));
    const maxCol = Math.max(...elementsData.map(e => e.group || 1));
    
    // Create grid layout
    periodicTable.style.gridTemplateColumns = `repeat(${maxCol}, 1fr)`;
    
    // Create a map for quick lookup
    const elementMap = {};
    elementsData.forEach(element => {
        const key = `${element.period}-${element.group}`;
        elementMap[key] = element;
    });
    
    // Render all positions
    for (let row = 1; row <= maxRow; row++) {
        for (let col = 1; col <= maxCol; col++) {
            const key = `${row}-${col}`;
            const element = elementMap[key];
            
            if (element) {
                const elementDiv = createElementButton(element);
                periodicTable.appendChild(elementDiv);
            } else {
                // Add empty cell to maintain grid
                const emptyDiv = document.createElement('div');
                emptyDiv.className = 'empty-cell';
                periodicTable.appendChild(emptyDiv);
            }
        }
    }
}

function createElementButton(element) {
    const div = document.createElement('div');
    div.className = `element ${getCategoryClass(element.category || '')}`;
    div.dataset.symbol = element.symbol;
    div.dataset.number = element.number;
    div.title = element.name;
    
    div.innerHTML = `
        <span class="element-number">${element.number}</span>
        <span class="element-symbol">${element.symbol}</span>
        <span class="element-name">${element.name}</span>
        <span class="element-mass">${(parseFloat(element.atomic_mass) || 0).toFixed(2)}</span>
    `;
    
    div.addEventListener('click', () => selectElement(element));
    
    return div;
}

function getCategoryClass(category) {
    if (!category) return 'default';
    
    // Convert category to CSS class format
    return category.toLowerCase().replace(/\s+/g, '-').replace(/[()]/g, '');
}

function selectElement(element) {
    // Update visual selection
    document.querySelectorAll('.element').forEach(el => {
        el.classList.remove('selected');
    });
    
    document.querySelector(`[data-symbol="${element.symbol}"]`)?.classList.add('selected');
    
    // Show element details
    displayElementDetails(element);
}

function displayElementDetails(element) {
    const detailsDiv = document.getElementById('elementDetails');
    if (!detailsDiv) return;
    
    let html = `
        <div class="element-header">
            <h2>${element.symbol}</h2>
            <p>${element.name}</p>
        </div>
        <div class="element-info">
    `;
    
    // Define property order and display names
    const properties = [
        { key: 'atomic_mass', name: 'Atomic Mass' },
        { key: 'number', name: 'Atomic Number' },
        { key: 'density', name: 'Density (g/cm³)' },
        { key: 'melting_point', name: 'Melting Point (K)' },
        { key: 'boiling_point', name: 'Boiling Point (K)' },
        { key: 'electron_configuration', name: 'Electron Configuration' },
        { key: 'category', name: 'Category' },
        { key: 'period', name: 'Period' },
        { key: 'group', name: 'Group' }
    ];
    
    properties.forEach(prop => {
        const value = element[prop.key];
        if (value !== undefined && value !== null && value !== '') {
            html += `
                <div class="element-property">
                    <div class="element-property-name">${prop.name}</div>
                    <div class="element-property-value">${formatPropertyValue(value)}</div>
                </div>
            `;
        }
    });
    
    html += `</div>`;
    
    detailsDiv.innerHTML = html;
}

function formatPropertyValue(value) {
    if (typeof value === 'number') {
        return value.toFixed(2);
    }
    return String(value);
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initializePeriodicTable);
