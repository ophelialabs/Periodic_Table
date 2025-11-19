from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """Render the periodic table home page."""
    return render_template('index.html')
