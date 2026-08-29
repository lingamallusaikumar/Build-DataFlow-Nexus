import pytest

def test_webhook_route_list(client, mocker):
    mocker.patch('app.domain_services.webhook_service.WebhookService.get_all', return_value=[])
    response = client.get('/api/v2/webhooks/')
    assert response.status_code == 200

def test_webhook_route_get(client, mocker):
    mocker.patch('app.domain_services.webhook_service.WebhookService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/webhooks/123')
    assert response.status_code == 200

def test_webhook_route_create(client, mocker):
    mocker.patch('app.domain_services.webhook_service.WebhookService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/webhooks/', json={'attribute_1': 'test'})
    assert response.status_code == 201
