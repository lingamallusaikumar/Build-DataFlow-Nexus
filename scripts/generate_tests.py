import os

base_dir = r'c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus'
files = {
    'run.py': '''from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
''',
    'tests/conftest.py': '''import pytest
from app import create_app
from app.extensions import db

@pytest.fixture
def app():
    app = create_app('development')
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
''',
    'tests/test_auth.py': '''def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_registration(client):
    response = client.post('/api/v1/auth/register', json={
        "email": "test@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User"
    })
    assert response.status_code == 201
    assert "user_id" in response.json

def test_login(client):
    client.post('/api/v1/auth/register', json={
        "email": "test2@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User"
    })
    
    response = client.post('/api/v1/auth/login', json={
        "email": "test2@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json
'''
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Tests and entrypoint created.')
