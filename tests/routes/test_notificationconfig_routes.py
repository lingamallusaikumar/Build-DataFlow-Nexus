import pytest

def test_notificationconfig_route_list(client, mocker):
    mocker.patch('app.domain_services.notificationconfig_service.NotificationConfigService.get_all', return_value=[])
    response = client.get('/api/v2/notificationconfigs/')
    assert response.status_code == 200

def test_notificationconfig_route_get(client, mocker):
    mocker.patch('app.domain_services.notificationconfig_service.NotificationConfigService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/notificationconfigs/123')
    assert response.status_code == 200

def test_notificationconfig_route_create(client, mocker):
    mocker.patch('app.domain_services.notificationconfig_service.NotificationConfigService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/notificationconfigs/', json={'attribute_1': 'test'})
    assert response.status_code == 201
