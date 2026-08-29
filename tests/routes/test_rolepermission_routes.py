import pytest

def test_rolepermission_route_list(client, mocker):
    mocker.patch('app.domain_services.rolepermission_service.RolePermissionService.get_all', return_value=[])
    response = client.get('/api/v2/rolepermissions/')
    assert response.status_code == 200

def test_rolepermission_route_get(client, mocker):
    mocker.patch('app.domain_services.rolepermission_service.RolePermissionService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/rolepermissions/123')
    assert response.status_code == 200

def test_rolepermission_route_create(client, mocker):
    mocker.patch('app.domain_services.rolepermission_service.RolePermissionService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/rolepermissions/', json={'attribute_1': 'test'})
    assert response.status_code == 201
