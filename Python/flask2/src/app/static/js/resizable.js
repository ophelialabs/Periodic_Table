/* Resizable Panel Functionality */

let isResizing = false;
let startX = 0;
let startY = 0;
let leftPanelWidth = 700;

function initializeResizablePanel() {
    const divider = document.getElementById('panelDivider');
    const leftPanel = document.getElementById('leftPanel');
    const mainLayout = document.querySelector('.main-layout');
    
    if (!divider || !leftPanel || !mainLayout) return;
    
    // Check if we're in horizontal layout (width > 999px)
    const isHorizontalLayout = window.innerWidth > 999;
    
    if (isHorizontalLayout) {
        divider.addEventListener('mousedown', startHorizontalResize);
    } else {
        divider.addEventListener('mousedown', startVerticalResize);
    }
    
    // Handle window resize to switch between layouts
    window.addEventListener('resize', handleLayoutChange);
}

function startHorizontalResize(e) {
    isResizing = true;
    startX = e.clientX;
    const leftPanel = document.getElementById('leftPanel');
    leftPanelWidth = leftPanel.offsetWidth;
    
    const divider = document.getElementById('panelDivider');
    divider.classList.add('dragging');
    
    document.addEventListener('mousemove', doHorizontalResize);
    document.addEventListener('mouseup', stopResize);
}

function startVerticalResize(e) {
    isResizing = true;
    startY = e.clientY;
    const leftPanel = document.getElementById('leftPanel');
    
    document.addEventListener('mousemove', doVerticalResize);
    document.addEventListener('mouseup', stopResize);
}

function doHorizontalResize(e) {
    if (!isResizing) return;
    
    const leftPanel = document.getElementById('leftPanel');
    const mainLayout = document.querySelector('.main-layout');
    
    if (!leftPanel || !mainLayout) return;
    
    const deltaX = e.clientX - startX;
    const newWidth = leftPanelWidth + deltaX;
    
    // Enforce minimum widths
    const minLeftWidth = 400;
    const minRightWidth = 250;
    const maxLeftWidth = mainLayout.offsetWidth - minRightWidth;
    
    if (newWidth >= minLeftWidth && newWidth <= maxLeftWidth) {
        leftPanel.style.flex = `0 0 ${newWidth}px`;
    }
}

function doVerticalResize(e) {
    if (!isResizing) return;
    
    const leftPanel = document.getElementById('leftPanel');
    const container = document.querySelector('.container');
    
    if (!leftPanel || !container) return;
    
    const deltaY = e.clientY - startY;
    const currentHeight = leftPanel.offsetHeight;
    const newHeight = currentHeight + deltaY;
    
    // Enforce minimum heights
    const minLeftHeight = 200;
    const minRightHeight = 250;
    const maxLeftHeight = container.offsetHeight - minRightHeight;
    
    if (newHeight >= minLeftHeight && newHeight <= maxLeftHeight) {
        leftPanel.style.flex = `0 0 ${newHeight}px`;
        startY = e.clientY;
    }
}

function stopResize() {
    isResizing = false;
    document.removeEventListener('mousemove', doHorizontalResize);
    document.removeEventListener('mousemove', doVerticalResize);
    document.removeEventListener('mouseup', stopResize);
    
    const divider = document.getElementById('panelDivider');
    divider?.classList.remove('dragging');
}

function handleLayoutChange() {
    const isHorizontalLayout = window.innerWidth > 999;
    const divider = document.getElementById('panelDivider');
    const mainLayout = document.querySelector('.main-layout');
    
    if (!divider || !mainLayout) return;
    
    // Remove old listeners
    divider.removeEventListener('mousedown', startHorizontalResize);
    divider.removeEventListener('mousedown', startVerticalResize);
    
    // Add appropriate listener based on layout
    if (isHorizontalLayout) {
        mainLayout.style.flexDirection = 'row';
        divider.style.width = '4px';
        divider.style.height = 'auto';
        divider.addEventListener('mousedown', startHorizontalResize);
    } else {
        mainLayout.style.flexDirection = 'column';
        divider.style.width = '100%';
        divider.style.height = '4px';
        divider.addEventListener('mousedown', startVerticalResize);
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', initializeResizablePanel);
