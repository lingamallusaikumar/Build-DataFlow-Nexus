import pytest
from app.domain_models.taskrun import TaskRun

def test_taskrun_creation():
    instance = TaskRun()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_taskrun_to_dict():
    instance = TaskRun()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_taskrun_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = TaskRun()
    instance.soft_delete()
    assert instance.is_deleted is True
