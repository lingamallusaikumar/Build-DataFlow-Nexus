import pytest
from app.domain_models.setting import Setting

def test_setting_creation():
    instance = Setting()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_setting_to_dict():
    instance = Setting()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_setting_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = Setting()
    instance.soft_delete()
    assert instance.is_deleted is True
