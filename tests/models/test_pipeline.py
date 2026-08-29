import pytest
from app.domain_models.pipeline import Pipeline

def test_pipeline_creation():
    instance = Pipeline()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_pipeline_to_dict():
    instance = Pipeline()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_pipeline_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = Pipeline()
    instance.soft_delete()
    assert instance.is_deleted is True
