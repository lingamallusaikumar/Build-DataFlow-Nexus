import pytest

def test_tenant_route_list(client, mocker):
    mocker.patch('app.domain_services.tenant_service.TenantService.get_all', return_value=[])
    response = client.get('/api/v2/tenants/')
    assert response.status_code == 200

def test_tenant_route_get(client, mocker):
    mocker.patch('app.domain_services.tenant_service.TenantService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/tenants/123')
    assert response.status_code == 200

def test_tenant_route_create(client, mocker):
    mocker.patch('app.domain_services.tenant_service.TenantService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/tenants/', json={'attribute_1': 'test'})
    assert response.status_code == 201
