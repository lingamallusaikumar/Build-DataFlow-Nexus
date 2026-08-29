import pytest
from app.domain_models.pipelineversion import PipelineVersion

def test_pipelineversion_creation():
    instance = PipelineVersion()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_pipelineversion_to_dict():
    instance = PipelineVersion()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_pipelineversion_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = PipelineVersion()
    instance.soft_delete()
    assert instance.is_deleted is True
