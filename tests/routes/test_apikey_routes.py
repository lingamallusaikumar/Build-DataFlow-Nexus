import pytest

def test_apikey_route_list(client, mocker):
    mocker.patch('app.domain_services.apikey_service.ApiKeyService.get_all', return_value=[])
    response = client.get('/api/v2/apikeys/')
    assert response.status_code == 200

def test_apikey_route_get(client, mocker):
    mocker.patch('app.domain_services.apikey_service.ApiKeyService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/apikeys/123')
    assert response.status_code == 200

def test_apikey_route_create(client, mocker):
    mocker.patch('app.domain_services.apikey_service.ApiKeyService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/apikeys/', json={'attribute_1': 'test'})
    assert response.status_code == 201
