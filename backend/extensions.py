from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from celery import Celery
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
cache = Cache()
mail = Mail()
jwt = JWTManager()
csrf = CSRFProtect()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="redis://localhost:6379/0" # overriden in app init
)

# Initialize Celery explicitly
celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

def init_extensions(app):
    """Initialize all Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'
    
    cache.init_app(app)
    
    # Re-configure Limiter storage with app config if available
    if app.config.get("RATELIMIT_STORAGE_URI"):
        limiter._storage_uri = app.config.get("RATELIMIT_STORAGE_URI")
    limiter.init_app(app)
    
    mail.init_app(app)
    jwt.init_app(app)
    csrf.init_app(app)
