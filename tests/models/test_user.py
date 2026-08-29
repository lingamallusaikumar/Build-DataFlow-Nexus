import pytest
from app.domain_models.user import User

def test_user_creation():
    instance = User()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_user_to_dict():
    instance = User()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_user_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = User()
    instance.soft_delete()
    assert instance.is_deleted is True
