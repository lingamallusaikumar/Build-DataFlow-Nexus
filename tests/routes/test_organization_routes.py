import pytest

def test_organization_route_list(client, mocker):
    mocker.patch('app.domain_services.organization_service.OrganizationService.get_all', return_value=[])
    response = client.get('/api/v2/organizations/')
    assert response.status_code == 200

def test_organization_route_get(client, mocker):
    mocker.patch('app.domain_services.organization_service.OrganizationService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/organizations/123')
    assert response.status_code == 200

def test_organization_route_create(client, mocker):
    mocker.patch('app.domain_services.organization_service.OrganizationService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/organizations/', json={'attribute_1': 'test'})
    assert response.status_code == 201
