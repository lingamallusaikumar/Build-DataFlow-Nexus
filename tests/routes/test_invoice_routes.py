import pytest

def test_invoice_route_list(client, mocker):
    mocker.patch('app.domain_services.invoice_service.InvoiceService.get_all', return_value=[])
    response = client.get('/api/v2/invoices/')
    assert response.status_code == 200

def test_invoice_route_get(client, mocker):
    mocker.patch('app.domain_services.invoice_service.InvoiceService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/invoices/123')
    assert response.status_code == 200

def test_invoice_route_create(client, mocker):
    mocker.patch('app.domain_services.invoice_service.InvoiceService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/invoices/', json={'attribute_1': 'test'})
    assert response.status_code == 201
