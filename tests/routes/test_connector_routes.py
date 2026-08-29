import pytest

def test_connector_route_list(client, mocker):
    mocker.patch('app.domain_services.connector_service.ConnectorService.get_all', return_value=[])
    response = client.get('/api/v2/connectors/')
    assert response.status_code == 200

def test_connector_route_get(client, mocker):
    mocker.patch('app.domain_services.connector_service.ConnectorService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/connectors/123')
    assert response.status_code == 200

def test_connector_route_create(client, mocker):
    mocker.patch('app.domain_services.connector_service.ConnectorService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/connectors/', json={'attribute_1': 'test'})
    assert response.status_code == 201
