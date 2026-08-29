import pytest
from app.domain_models.alerthistory import AlertHistory

def test_alerthistory_creation():
    instance = AlertHistory()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_alerthistory_to_dict():
    instance = AlertHistory()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_alerthistory_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = AlertHistory()
    instance.soft_delete()
    assert instance.is_deleted is True
