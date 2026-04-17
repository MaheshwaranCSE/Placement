import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
from backend.config import config_by_name
from backend.extensions import init_extensions

def create_app(config_name='development'):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config_by_name[config_name])

    # Initialize Extensions
    init_extensions(app)

    # Register Blueprints
    from backend.routes import auth_bp, dashboard_bp, students_bp, placement_bp, predict_bp, reports_bp, api_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(placement_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(api_bp)

    # Configure Logging
    if not app.debug and not app.testing:
        import os
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240000, backupCount=5)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Campus Placement Portal startup')

    # Security Headers Hook
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        # Basic CSP, can be extended
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data:;"
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response

    # Global Error Handlers
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    # User Loader for Flask-Login
    from backend.models import User
    from backend.extensions import login_manager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Initialize celery app instance context
    from backend.extensions import celery
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return app
