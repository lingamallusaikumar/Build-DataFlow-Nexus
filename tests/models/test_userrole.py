import pytest
from app.domain_models.userrole import UserRole

def test_userrole_creation():
    instance = UserRole()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_userrole_to_dict():
    instance = UserRole()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_userrole_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = UserRole()
    instance.soft_delete()
    assert instance.is_deleted is True
