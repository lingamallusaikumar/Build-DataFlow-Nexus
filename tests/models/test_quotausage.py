import pytest
from app.domain_models.quotausage import QuotaUsage

def test_quotausage_creation():
    instance = QuotaUsage()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_quotausage_to_dict():
    instance = QuotaUsage()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_quotausage_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = QuotaUsage()
    instance.soft_delete()
    assert instance.is_deleted is True
