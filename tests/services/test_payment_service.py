import pytest
from app.domain_services.payment_service import PaymentService
from app.domain_models.payment import Payment

def test_payment_service_get_all(mocker):
    mocker.patch('app.domain_models.payment.Payment.query')
    result = PaymentService.get_all()
    assert result is not None

def test_payment_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = PaymentService.create(data)
    assert record.attribute_1 == 'val'

def test_payment_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.payment_service.PaymentService.get_by_id')
    mock_instance = Payment()
    mock_get.return_value = mock_instance
    
    updated = PaymentService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
