import pytest
from app.domain_services.webhookdelivery_service import WebhookDeliveryService
from app.domain_models.webhookdelivery import WebhookDelivery

def test_webhookdelivery_service_get_all(mocker):
    mocker.patch('app.domain_models.webhookdelivery.WebhookDelivery.query')
    result = WebhookDeliveryService.get_all()
    assert result is not None

def test_webhookdelivery_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = WebhookDeliveryService.create(data)
    assert record.attribute_1 == 'val'

def test_webhookdelivery_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.webhookdelivery_service.WebhookDeliveryService.get_by_id')
    mock_instance = WebhookDelivery()
    mock_get.return_value = mock_instance
    
    updated = WebhookDeliveryService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
