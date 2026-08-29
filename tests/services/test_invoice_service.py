import pytest
from app.domain_services.invoice_service import InvoiceService
from app.domain_models.invoice import Invoice

def test_invoice_service_get_all(mocker):
    mocker.patch('app.domain_models.invoice.Invoice.query')
    result = InvoiceService.get_all()
    assert result is not None

def test_invoice_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = InvoiceService.create(data)
    assert record.attribute_1 == 'val'

def test_invoice_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.invoice_service.InvoiceService.get_by_id')
    mock_instance = Invoice()
    mock_get.return_value = mock_instance
    
    updated = InvoiceService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
