import pytest
from app.domain_models.datacatalog import DataCatalog

def test_datacatalog_creation():
    instance = DataCatalog()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_datacatalog_to_dict():
    instance = DataCatalog()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_datacatalog_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = DataCatalog()
    instance.soft_delete()
    assert instance.is_deleted is True
