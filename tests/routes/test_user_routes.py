import pytest

def test_user_route_list(client, mocker):
    mocker.patch('app.domain_services.user_service.UserService.get_all', return_value=[])
    response = client.get('/api/v2/users/')
    assert response.status_code == 200

def test_user_route_get(client, mocker):
    mocker.patch('app.domain_services.user_service.UserService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/users/123')
    assert response.status_code == 200

def test_user_route_create(client, mocker):
    mocker.patch('app.domain_services.user_service.UserService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/users/', json={'attribute_1': 'test'})
    assert response.status_code == 201
