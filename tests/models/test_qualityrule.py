import pytest
from app.domain_models.qualityrule import QualityRule

def test_qualityrule_creation():
    instance = QualityRule()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_qualityrule_to_dict():
    instance = QualityRule()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_qualityrule_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = QualityRule()
    instance.soft_delete()
    assert instance.is_deleted is True
