import pytest

def test_quotausage_route_list(client, mocker):
    mocker.patch('app.domain_services.quotausage_service.QuotaUsageService.get_all', return_value=[])
    response = client.get('/api/v2/quotausages/')
    assert response.status_code == 200

def test_quotausage_route_get(client, mocker):
    mocker.patch('app.domain_services.quotausage_service.QuotaUsageService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/quotausages/123')
    assert response.status_code == 200

def test_quotausage_route_create(client, mocker):
    mocker.patch('app.domain_services.quotausage_service.QuotaUsageService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/quotausages/', json={'attribute_1': 'test'})
    assert response.status_code == 201
