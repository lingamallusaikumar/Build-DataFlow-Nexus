import pytest
from app.domain_models.connectioncredentials import ConnectionCredentials

def test_connectioncredentials_creation():
    instance = ConnectionCredentials()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_connectioncredentials_to_dict():
    instance = ConnectionCredentials()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_connectioncredentials_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = ConnectionCredentials()
    instance.soft_delete()
    assert instance.is_deleted is True
