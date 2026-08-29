import pytest
from app.domain_models.dagedge import DagEdge

def test_dagedge_creation():
    instance = DagEdge()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_dagedge_to_dict():
    instance = DagEdge()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_dagedge_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = DagEdge()
    instance.soft_delete()
    assert instance.is_deleted is True
