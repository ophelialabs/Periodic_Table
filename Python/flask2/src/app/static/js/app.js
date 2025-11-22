/* Main Application Initialization */

function initializeApp() {
    console.log('Initializing Periodic Table Explorer');
    
    // Check if elements data is loaded
    if (!elementsData || elementsData.length === 0) {
        console.error('Elements data not loaded');
        return;
    }
    
    console.log(`Loaded ${elementsData.length} elements`);
    
    // Initialize all components
    // (Other initializations are handled by individual modules)
    
    console.log('App initialization complete');
}

// Run initialization when DOM is ready
document.addEventListener('DOMContentLoaded', initializeApp);

// Handle global errors
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

// Handle unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});
