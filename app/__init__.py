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

    @app.route('/health')
    def health_check():
        return {'status': 'ok', 'message': 'DataFlow Nexus API is running'}

    return app
