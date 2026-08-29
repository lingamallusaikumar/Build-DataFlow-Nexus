import pytest
from app.domain_models.qualityexecution import QualityExecution

def test_qualityexecution_creation():
    instance = QualityExecution()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_qualityexecution_to_dict():
    instance = QualityExecution()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_qualityexecution_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = QualityExecution()
    instance.soft_delete()
    assert instance.is_deleted is True
