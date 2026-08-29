import pytest

def test_schemacolumn_route_list(client, mocker):
    mocker.patch('app.domain_services.schemacolumn_service.SchemaColumnService.get_all', return_value=[])
    response = client.get('/api/v2/schemacolumns/')
    assert response.status_code == 200

def test_schemacolumn_route_get(client, mocker):
    mocker.patch('app.domain_services.schemacolumn_service.SchemaColumnService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/schemacolumns/123')
    assert response.status_code == 200

def test_schemacolumn_route_create(client, mocker):
    mocker.patch('app.domain_services.schemacolumn_service.SchemaColumnService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/schemacolumns/', json={'attribute_1': 'test'})
    assert response.status_code == 201
