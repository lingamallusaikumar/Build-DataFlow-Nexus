import pytest
from app.domain_services.webhook_service import WebhookService
from app.domain_models.webhook import Webhook

def test_webhook_service_get_all(mocker):
    mocker.patch('app.domain_models.webhook.Webhook.query')
    result = WebhookService.get_all()
    assert result is not None

def test_webhook_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = WebhookService.create(data)
    assert record.attribute_1 == 'val'

def test_webhook_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.webhook_service.WebhookService.get_by_id')
    mock_instance = Webhook()
    mock_get.return_value = mock_instance
    
    updated = WebhookService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
