import pytest
from app.domain_models.permission import Permission

def test_permission_creation():
    instance = Permission()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_permission_to_dict():
    instance = Permission()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_permission_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = Permission()
    instance.soft_delete()
    assert instance.is_deleted is True
