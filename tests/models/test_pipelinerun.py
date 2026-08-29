import pytest
from app.domain_models.pipelinerun import PipelineRun

def test_pipelinerun_creation():
    instance = PipelineRun()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_pipelinerun_to_dict():
    instance = PipelineRun()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_pipelinerun_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = PipelineRun()
    instance.soft_delete()
    assert instance.is_deleted is True
