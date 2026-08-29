import pytest
from app.domain_models.webhookdelivery import WebhookDelivery

def test_webhookdelivery_creation():
    instance = WebhookDelivery()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_webhookdelivery_to_dict():
    instance = WebhookDelivery()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_webhookdelivery_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = WebhookDelivery()
    instance.soft_delete()
    assert instance.is_deleted is True
