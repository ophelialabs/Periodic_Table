from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_caching import Cache
import os
import sys

# Add parent directory to path to access config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import Config

# Initialize Flask extensions
bootstrap = Bootstrap()
moment = Moment()
cache = Cache()

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_class)

    # Initialize extensions with app
    bootstrap.init_app(app)
    moment.init_app(app)
    cache.init_app(app)

    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app