import pytest
from app.domain_models.tenant import Tenant

def test_tenant_creation():
    instance = Tenant()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_tenant_to_dict():
    instance = Tenant()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_tenant_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = Tenant()
    instance.soft_delete()
    assert instance.is_deleted is True
