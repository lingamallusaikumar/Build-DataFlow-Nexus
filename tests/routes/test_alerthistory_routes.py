import pytest

def test_alerthistory_route_list(client, mocker):
    mocker.patch('app.domain_services.alerthistory_service.AlertHistoryService.get_all', return_value=[])
    response = client.get('/api/v2/alerthistorys/')
    assert response.status_code == 200

def test_alerthistory_route_get(client, mocker):
    mocker.patch('app.domain_services.alerthistory_service.AlertHistoryService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/alerthistorys/123')
    assert response.status_code == 200

def test_alerthistory_route_create(client, mocker):
    mocker.patch('app.domain_services.alerthistory_service.AlertHistoryService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/alerthistorys/', json={'attribute_1': 'test'})
    assert response.status_code == 201
