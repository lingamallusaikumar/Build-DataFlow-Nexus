import os

base_dir = r'c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus'
files = {
    'requirements.txt': '''Flask==3.0.0
SQLAlchemy==2.0.23
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
psycopg2-binary==2.9.9
redis==5.0.1
celery==5.3.6
Flask-SocketIO==5.3.6
Flask-JWT-Extended==4.5.3
bcrypt==4.1.2
pydantic==2.5.3
python-dotenv==1.0.0
gunicorn==21.2.0
pytest==7.4.3
''',
    '.env.example': '''# Flask Configuration
FLASK_APP=app:create_app
FLASK_ENV=development
SECRET_KEY=super-secret-key-change-in-production

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dataflow_nexus

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# JWT Configuration
JWT_SECRET_KEY=super-secret-jwt-key-change-in-production
''',
    'docker-compose.yml': '''version: '3.8'

services:
  web:
    build: .
    ports:
      - '5000:5000'
    environment:
      - FLASK_APP=app:create_app
      - FLASK_ENV=development
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/dataflow_nexus
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=dev-secret-key
      - JWT_SECRET_KEY=dev-jwt-secret
    depends_on:
      - db
      - redis
    volumes:
      - .:/app

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=dataflow_nexus
    ports:
      - '5432:5432'
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - '6379:6379'

  celery_worker:
    build: .
    command: celery -A app.extensions.celery_app worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/dataflow_nexus
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
      - web

volumes:
  postgres_data:
''',
    'Dockerfile': '''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]
''',
    'app/config/settings.py': '''import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis & Celery
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-default-secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
''',
    'app/extensions/__init__.py': '''from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from celery import Celery

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO(cors_allowed_origins="*")

def make_celery(app_name=__name__):
    celery = Celery(app_name)
    return celery

celery_app = make_celery()
''',
    'app/__init__.py': '''from flask import Flask
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

    @app.route('/health')
    def health_check():
        return {'status': 'ok', 'message': 'DataFlow Nexus API is running'}

    return app
'''
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('DevOps and Core Config files created.')
