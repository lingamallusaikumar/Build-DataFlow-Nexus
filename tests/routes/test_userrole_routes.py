import pytest

def test_userrole_route_list(client, mocker):
    mocker.patch('app.domain_services.userrole_service.UserRoleService.get_all', return_value=[])
    response = client.get('/api/v2/userroles/')
    assert response.status_code == 200

def test_userrole_route_get(client, mocker):
    mocker.patch('app.domain_services.userrole_service.UserRoleService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/userroles/123')
    assert response.status_code == 200

def test_userrole_route_create(client, mocker):
    mocker.patch('app.domain_services.userrole_service.UserRoleService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/userroles/', json={'attribute_1': 'test'})
    assert response.status_code == 201
