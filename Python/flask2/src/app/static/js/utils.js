/* Utility Functions */

function formatNumber(value) {
    if (typeof value !== 'number') {
        value = parseFloat(value);
    }
    if (isNaN(value)) return 'N/A';
    return value.toFixed(2);
}

function formatPropertyName(key) {
    return key
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

function getContrastColor(hexColor) {
    // Convert hex to RGB and calculate brightness
    const hex = hexColor.replace('#', '');
    const r = parseInt(hex.substr(0, 2), 16);
    const g = parseInt(hex.substr(2, 2), 16);
    const b = parseInt(hex.substr(4, 2), 16);
    
    const brightness = (r * 299 + g * 587 + b * 114) / 1000;
    return brightness > 128 ? '#000000' : '#ffffff';
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        console.log('Copied to clipboard');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

function getElementColor(category) {
    const colorMap = {
        'nonmetal': '#1a5f1f',
        'alkali-metal': '#5f1f1f',
        'alkaline-earth-metal': '#5f4a1f',
        'transition-metal': '#1f3f5f',
        'lanthanide': '#4a3f5f',
        'actinide': '#5f3f4a',
        'halogen': '#5f5f1f',
        'noble-gas': '#3f4a5f',
        'metalloid': '#4a5f3f',
        'poor-metal': '#3f4a4a'
    };
    
    const key = category?.toLowerCase().replace(/\s+/g, '-') || 'default';
    return colorMap[key] || '#333';
}

// Fetch API with error handling
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        return null;
    }
}

// Format scientific notation
function formatScientific(value) {
    if (typeof value !== 'number') {
        value = parseFloat(value);
    }
    if (isNaN(value)) return 'N/A';
    
    if (Math.abs(value) >= 1000000 || Math.abs(value) < 0.0001) {
        return value.toExponential(2);
    }
    return value.toFixed(2);
}
