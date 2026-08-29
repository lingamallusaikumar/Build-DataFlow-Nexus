import pytest

def test_savedquery_route_list(client, mocker):
    mocker.patch('app.domain_services.savedquery_service.SavedQueryService.get_all', return_value=[])
    response = client.get('/api/v2/savedquerys/')
    assert response.status_code == 200

def test_savedquery_route_get(client, mocker):
    mocker.patch('app.domain_services.savedquery_service.SavedQueryService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/savedquerys/123')
    assert response.status_code == 200

def test_savedquery_route_create(client, mocker):
    mocker.patch('app.domain_services.savedquery_service.SavedQueryService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/savedquerys/', json={'attribute_1': 'test'})
    assert response.status_code == 201
