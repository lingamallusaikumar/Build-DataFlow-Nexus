import pytest

def test_alert_route_list(client, mocker):
    mocker.patch('app.domain_services.alert_service.AlertService.get_all', return_value=[])
    response = client.get('/api/v2/alerts/')
    assert response.status_code == 200

def test_alert_route_get(client, mocker):
    mocker.patch('app.domain_services.alert_service.AlertService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/alerts/123')
    assert response.status_code == 200

def test_alert_route_create(client, mocker):
    mocker.patch('app.domain_services.alert_service.AlertService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/alerts/', json={'attribute_1': 'test'})
    assert response.status_code == 201
