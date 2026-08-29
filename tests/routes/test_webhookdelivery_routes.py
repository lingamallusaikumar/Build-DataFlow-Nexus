import pytest

def test_webhookdelivery_route_list(client, mocker):
    mocker.patch('app.domain_services.webhookdelivery_service.WebhookDeliveryService.get_all', return_value=[])
    response = client.get('/api/v2/webhookdeliverys/')
    assert response.status_code == 200

def test_webhookdelivery_route_get(client, mocker):
    mocker.patch('app.domain_services.webhookdelivery_service.WebhookDeliveryService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/webhookdeliverys/123')
    assert response.status_code == 200

def test_webhookdelivery_route_create(client, mocker):
    mocker.patch('app.domain_services.webhookdelivery_service.WebhookDeliveryService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/webhookdeliverys/', json={'attribute_1': 'test'})
    assert response.status_code == 201
