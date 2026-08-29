import pytest
from app.domain_models.alert import Alert

def test_alert_creation():
    instance = Alert()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_alert_to_dict():
    instance = Alert()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_alert_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = Alert()
    instance.soft_delete()
    assert instance.is_deleted is True
