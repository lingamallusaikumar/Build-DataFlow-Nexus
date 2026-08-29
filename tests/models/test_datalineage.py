import pytest
from app.domain_models.datalineage import DataLineage

def test_datalineage_creation():
    instance = DataLineage()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_datalineage_to_dict():
    instance = DataLineage()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_datalineage_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = DataLineage()
    instance.soft_delete()
    assert instance.is_deleted is True
