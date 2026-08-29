import pytest
from app.domain_models.metric import Metric

def test_metric_creation():
    instance = Metric()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_metric_to_dict():
    instance = Metric()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_metric_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = Metric()
    instance.soft_delete()
    assert instance.is_deleted is True
