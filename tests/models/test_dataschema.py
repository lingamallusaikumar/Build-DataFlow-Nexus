import pytest
from app.domain_models.dataschema import DataSchema

def test_dataschema_creation():
    instance = DataSchema()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_dataschema_to_dict():
    instance = DataSchema()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_dataschema_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = DataSchema()
    instance.soft_delete()
    assert instance.is_deleted is True
