import pytest
from app.domain_models.webhook import Webhook

def test_webhook_creation():
    instance = Webhook()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_webhook_to_dict():
    instance = Webhook()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_webhook_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = Webhook()
    instance.soft_delete()
    assert instance.is_deleted is True
