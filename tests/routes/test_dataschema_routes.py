import pytest

def test_dataschema_route_list(client, mocker):
    mocker.patch('app.domain_services.dataschema_service.DataSchemaService.get_all', return_value=[])
    response = client.get('/api/v2/dataschemas/')
    assert response.status_code == 200

def test_dataschema_route_get(client, mocker):
    mocker.patch('app.domain_services.dataschema_service.DataSchemaService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/dataschemas/123')
    assert response.status_code == 200

def test_dataschema_route_create(client, mocker):
    mocker.patch('app.domain_services.dataschema_service.DataSchemaService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/dataschemas/', json={'attribute_1': 'test'})
    assert response.status_code == 201
