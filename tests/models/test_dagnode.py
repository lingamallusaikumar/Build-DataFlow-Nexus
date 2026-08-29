import pytest
from app.domain_models.dagnode import DagNode

def test_dagnode_creation():
    instance = DagNode()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_dagnode_to_dict():
    instance = DagNode()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_dagnode_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = DagNode()
    instance.soft_delete()
    assert instance.is_deleted is True
