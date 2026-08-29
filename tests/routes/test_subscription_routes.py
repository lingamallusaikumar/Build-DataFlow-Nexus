import pytest

def test_subscription_route_list(client, mocker):
    mocker.patch('app.domain_services.subscription_service.SubscriptionService.get_all', return_value=[])
    response = client.get('/api/v2/subscriptions/')
    assert response.status_code == 200

def test_subscription_route_get(client, mocker):
    mocker.patch('app.domain_services.subscription_service.SubscriptionService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/subscriptions/123')
    assert response.status_code == 200

def test_subscription_route_create(client, mocker):
    mocker.patch('app.domain_services.subscription_service.SubscriptionService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/subscriptions/', json={'attribute_1': 'test'})
    assert response.status_code == 201
