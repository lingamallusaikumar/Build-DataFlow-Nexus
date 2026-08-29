import pytest
from app.domain_models.apikey import ApiKey

def test_apikey_creation():
    instance = ApiKey()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_apikey_to_dict():
    instance = ApiKey()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_apikey_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = ApiKey()
    instance.soft_delete()
    assert instance.is_deleted is True
