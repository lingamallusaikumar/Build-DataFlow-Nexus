import pytest

def test_payment_route_list(client, mocker):
    mocker.patch('app.domain_services.payment_service.PaymentService.get_all', return_value=[])
    response = client.get('/api/v2/payments/')
    assert response.status_code == 200

def test_payment_route_get(client, mocker):
    mocker.patch('app.domain_services.payment_service.PaymentService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/payments/123')
    assert response.status_code == 200

def test_payment_route_create(client, mocker):
    mocker.patch('app.domain_services.payment_service.PaymentService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/payments/', json={'attribute_1': 'test'})
    assert response.status_code == 201
