import pytest
from app.domain_models.tasklog import TaskLog

def test_tasklog_creation():
    instance = TaskLog()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_tasklog_to_dict():
    instance = TaskLog()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_tasklog_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = TaskLog()
    instance.soft_delete()
    assert instance.is_deleted is True
