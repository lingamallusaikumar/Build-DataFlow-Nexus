import pytest
from app.domain_models.connector import Connector

def test_connector_creation():
    instance = Connector()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_connector_to_dict():
    instance = Connector()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_connector_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = Connector()
    instance.soft_delete()
    assert instance.is_deleted is True
