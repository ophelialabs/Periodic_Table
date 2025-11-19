import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Flask-WTF
    WTF_CSRF_ENABLED = True
    
    # Flask-Caching - use simple cache for development
    CACHE_TYPE = 'simple'
    
    # Periodic table data
    PERIODIC_TABLE_JSON = os.path.join(
        os.path.dirname(__file__),
        'src/lib/Periodic-Table-JSON/PeriodicTableJSON.json'
    )

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    # In production, you might want to use Redis
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379'

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    CACHE_TYPE = 'simple'
