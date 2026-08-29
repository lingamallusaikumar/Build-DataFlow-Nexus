import pytest

def test_datacatalog_route_list(client, mocker):
    mocker.patch('app.domain_services.datacatalog_service.DataCatalogService.get_all', return_value=[])
    response = client.get('/api/v2/datacatalogs/')
    assert response.status_code == 200

def test_datacatalog_route_get(client, mocker):
    mocker.patch('app.domain_services.datacatalog_service.DataCatalogService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/datacatalogs/123')
    assert response.status_code == 200

def test_datacatalog_route_create(client, mocker):
    mocker.patch('app.domain_services.datacatalog_service.DataCatalogService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/datacatalogs/', json={'attribute_1': 'test'})
    assert response.status_code == 201
