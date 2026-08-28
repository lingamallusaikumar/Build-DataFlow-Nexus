from flask import Flask
from app.config.settings import config
from app.extensions import db, migrate, jwt, socketio, celery_app

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Configure celery
    celery_app.conf.update(app.config)

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    socketio.init_app(app)

    # Register Blueprints
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    
    from app.organizations.routes import org_bp
    app.register_blueprint(org_bp, url_prefix='/api/v1/organizations')

    from app.frontend_routes import frontend_bp
    app.register_blueprint(frontend_bp)

    from app.admin.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')

    from app.admin.health import health_bp
    app.register_blueprint(health_bp, url_prefix='/health')
    
    from app.common.error_handlers import register_error_handlers
    register_error_handlers(app)

    @app.route('/health_check')
    def health_check():
        return {'status': 'ok', 'message': 'DataFlow Nexus API is running'}

    # Import socket events
    import app.monitoring.sockets

    return app
