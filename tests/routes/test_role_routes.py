import pytest

def test_role_route_list(client, mocker):
    mocker.patch('app.domain_services.role_service.RoleService.get_all', return_value=[])
    response = client.get('/api/v2/roles/')
    assert response.status_code == 200

def test_role_route_get(client, mocker):
    mocker.patch('app.domain_services.role_service.RoleService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/roles/123')
    assert response.status_code == 200

def test_role_route_create(client, mocker):
    mocker.patch('app.domain_services.role_service.RoleService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/roles/', json={'attribute_1': 'test'})
    assert response.status_code == 201
