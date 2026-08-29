import pytest

def test_metric_route_list(client, mocker):
    mocker.patch('app.domain_services.metric_service.MetricService.get_all', return_value=[])
    response = client.get('/api/v2/metrics/')
    assert response.status_code == 200

def test_metric_route_get(client, mocker):
    mocker.patch('app.domain_services.metric_service.MetricService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/metrics/123')
    assert response.status_code == 200

def test_metric_route_create(client, mocker):
    mocker.patch('app.domain_services.metric_service.MetricService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/metrics/', json={'attribute_1': 'test'})
    assert response.status_code == 201
