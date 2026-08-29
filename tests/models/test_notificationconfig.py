import pytest
from app.domain_models.notificationconfig import NotificationConfig

def test_notificationconfig_creation():
    instance = NotificationConfig()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_notificationconfig_to_dict():
    instance = NotificationConfig()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_notificationconfig_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = NotificationConfig()
    instance.soft_delete()
    assert instance.is_deleted is True
