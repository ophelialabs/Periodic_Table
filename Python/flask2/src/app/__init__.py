"""
Periodic Table Flask Application
Interactive periodic table with visualizations and analysis tools.
"""

import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from src.element_database import ElementDatabase
from src.analysis_report import AnalysisReportGenerator


def create_app():
    """Create and configure the Flask application."""
    # Get absolute paths for templates and static files
    base_dir = Path(__file__).parent
    template_dir = str(base_dir / 'templates')
    static_dir = str(base_dir / 'static')
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    
    # Initialize database
    app.db = ElementDatabase()
    app.analysis = AnalysisReportGenerator(app.db)
    
    # Register blueprints and routes
    register_routes(app)
    
    return app


def register_routes(app):
    """Register application routes."""
    
    @app.route('/')
    def index():
        """Render main periodic table page."""
        elements = app.db.get_all_elements()
        categories = app.db.get_categories()
        return render_template('main/index.html', 
                             elements=elements,
                             categories=categories)
    
    @app.route('/api/element/<symbol>')
    def get_element(symbol):
        """Get element data by symbol."""
        element = app.db.get_element_by_symbol(symbol.title())
        if element:
            return jsonify(element)
        return jsonify({'error': 'Element not found'}), 404
    
    @app.route('/api/search')
    def search_elements():
        """Search elements by name, symbol, or category."""
        query = request.args.get('q', '').lower()
        category = request.args.get('category', '')
        
        results = app.db.search(query, category)
        return jsonify(results)
    
    @app.route('/api/categories')
    def get_categories():
        """Get all element categories."""
        return jsonify(app.db.get_categories())
    
    @app.route('/api/elements/all')
    def get_all_elements():
        """Get all elements with minimal data."""
        elements = app.db.get_all_elements()
        return jsonify(elements)
    
    @app.route('/api/analysis/summary')
    def analysis_summary():
        """Get statistical summary of elements."""
        summary = app.analysis.generate_summary_statistics()
        return jsonify({'summary': summary})
    
    @app.route('/api/analysis/heatmap')
    def get_heatmap_data():
        """Get heatmap data for property visualization."""
        property_name = request.args.get('property', 'atomic_mass')
        data = app.analysis.generate_heatmap_data(property_name)
        return jsonify(data)
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 errors."""
        return jsonify({'error': 'Server error'}), 500


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
