from flask import Blueprint, jsonify
import json
import os
import sys

bp = Blueprint('api', __name__)

def load_periodic_table():
    """Load periodic table data from JSON file."""
    try:
        # Construct path to periodic table JSON
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        data_path = os.path.join(
            base_dir,
            'src/lib/Periodic-Table-JSON/PeriodicTableJSON.json'
        )
        with open(data_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"elements": []}

@bp.route('/elements', methods=['GET'])
def get_elements():
    """Get all elements from the periodic table."""
    data = load_periodic_table()
    return jsonify(data)

@bp.route('/element/<int:atomic_number>', methods=['GET'])
def get_element(atomic_number):
    """Get a specific element by atomic number."""
    data = load_periodic_table()
    elements = data.get('elements', [])
    
    for element in elements:
        if element.get('number') == atomic_number:
            return jsonify(element)
    
    return jsonify({'error': 'Element not found'}), 404

@bp.route('/element/<symbol>', methods=['GET'])
def get_element_by_symbol(symbol):
    """Get a specific element by symbol."""
    data = load_periodic_table()
    elements = data.get('elements', [])
    
    for element in elements:
        if element.get('symbol').lower() == symbol.lower():
            return jsonify(element)
    
    return jsonify({'error': 'Element not found'}), 404
