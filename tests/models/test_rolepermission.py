import pytest
from app.domain_models.rolepermission import RolePermission

def test_rolepermission_creation():
    instance = RolePermission()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_rolepermission_to_dict():
    instance = RolePermission()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_rolepermission_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = RolePermission()
    instance.soft_delete()
    assert instance.is_deleted is True
