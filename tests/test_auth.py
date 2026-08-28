def test_health_check(client):
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
