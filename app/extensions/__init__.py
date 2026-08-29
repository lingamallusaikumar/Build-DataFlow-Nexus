from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

class DummyCelery:
    class Conf:
        def update(self, *args, **kwargs):
            pass
    conf = Conf()
    def task(self, *args, **kwargs):
        def decorator(f):
            return f
        return decorator

class DummySocketIO:
    def init_app(self, *args, **kwargs):
        pass
    def on(self, *args, **kwargs):
        def decorator(f):
            return f
        return decorator
    def emit(self, *args, **kwargs):
        pass
    def start_background_task(self, *args, **kwargs):
        pass
    def sleep(self, *args, **kwargs):
        pass

celery_app = DummyCelery()
socketio = DummySocketIO()
