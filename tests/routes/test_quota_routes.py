import pytest

def test_quota_route_list(client, mocker):
    mocker.patch('app.domain_services.quota_service.QuotaService.get_all', return_value=[])
    response = client.get('/api/v2/quotas/')
    assert response.status_code == 200

def test_quota_route_get(client, mocker):
    mocker.patch('app.domain_services.quota_service.QuotaService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/quotas/123')
    assert response.status_code == 200

def test_quota_route_create(client, mocker):
    mocker.patch('app.domain_services.quota_service.QuotaService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/quotas/', json={'attribute_1': 'test'})
    assert response.status_code == 201
