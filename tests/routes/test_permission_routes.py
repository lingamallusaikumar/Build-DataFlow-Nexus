import pytest

def test_permission_route_list(client, mocker):
    mocker.patch('app.domain_services.permission_service.PermissionService.get_all', return_value=[])
    response = client.get('/api/v2/permissions/')
    assert response.status_code == 200

def test_permission_route_get(client, mocker):
    mocker.patch('app.domain_services.permission_service.PermissionService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/permissions/123')
    assert response.status_code == 200

def test_permission_route_create(client, mocker):
    mocker.patch('app.domain_services.permission_service.PermissionService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/permissions/', json={'attribute_1': 'test'})
    assert response.status_code == 201
