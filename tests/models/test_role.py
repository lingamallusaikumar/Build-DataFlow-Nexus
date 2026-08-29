import pytest
from app.domain_models.role import Role

def test_role_creation():
    instance = Role()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_role_to_dict():
    instance = Role()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_role_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = Role()
    instance.soft_delete()
    assert instance.is_deleted is True
