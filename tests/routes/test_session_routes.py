import pytest

def test_session_route_list(client, mocker):
    mocker.patch('app.domain_services.session_service.SessionService.get_all', return_value=[])
    response = client.get('/api/v2/sessions/')
    assert response.status_code == 200

def test_session_route_get(client, mocker):
    mocker.patch('app.domain_services.session_service.SessionService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/sessions/123')
    assert response.status_code == 200

def test_session_route_create(client, mocker):
    mocker.patch('app.domain_services.session_service.SessionService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/sessions/', json={'attribute_1': 'test'})
    assert response.status_code == 201
