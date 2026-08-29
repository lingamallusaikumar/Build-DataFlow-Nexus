import pytest

def test_setting_route_list(client, mocker):
    mocker.patch('app.domain_services.setting_service.SettingService.get_all', return_value=[])
    response = client.get('/api/v2/settings/')
    assert response.status_code == 200

def test_setting_route_get(client, mocker):
    mocker.patch('app.domain_services.setting_service.SettingService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/settings/123')
    assert response.status_code == 200

def test_setting_route_create(client, mocker):
    mocker.patch('app.domain_services.setting_service.SettingService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/settings/', json={'attribute_1': 'test'})
    assert response.status_code == 201
