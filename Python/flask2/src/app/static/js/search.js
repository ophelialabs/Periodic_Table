/* Search functionality */

function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    
    if (searchInput) {
        searchInput.addEventListener('input', performSearch);
    }
    
    if (categoryFilter) {
        categoryFilter.addEventListener('change', performSearch);
    }
}

function performSearch() {
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    
    const query = (searchInput?.value || '').toLowerCase();
    const category = categoryFilter?.value || '';
    
    // Filter local elements data
    const filteredElements = elementsData.filter(element => {
        const matchesQuery = !query || 
            element.name.toLowerCase().includes(query) ||
            element.symbol.toLowerCase().includes(query);
        
        const matchesCategory = !category || 
            (element.category || '').toLowerCase() === category.toLowerCase();
        
        return matchesQuery && matchesCategory;
    });
    
    // Update periodic table display
    updatePeriodicTableDisplay(filteredElements);
}

function updatePeriodicTableDisplay(filteredElements) {
    const filteredSet = new Set(filteredElements.map(e => e.symbol));
    
    document.querySelectorAll('.element').forEach(el => {
        const symbol = el.dataset.symbol;
        if (filteredSet.has(symbol)) {
            el.style.display = '';
            el.style.opacity = '1';
        } else {
            el.style.opacity = '0.2';
            el.pointerEvents = 'none';
        }
    });
}

function resetSearch() {
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    
    if (searchInput) searchInput.value = '';
    if (categoryFilter) categoryFilter.value = '';
    
    performSearch();
}

// Initialize search on DOM ready
document.addEventListener('DOMContentLoaded', initializeSearch);
