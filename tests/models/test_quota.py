import pytest
from app.domain_models.quota import Quota

def test_quota_creation():
    instance = Quota()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_quota_to_dict():
    instance = Quota()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_quota_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = Quota()
    instance.soft_delete()
    assert instance.is_deleted is True
