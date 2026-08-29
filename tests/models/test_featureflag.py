import pytest
from app.domain_models.featureflag import FeatureFlag

def test_featureflag_creation():
    instance = FeatureFlag()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_featureflag_to_dict():
    instance = FeatureFlag()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_featureflag_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = FeatureFlag()
    instance.soft_delete()
    assert instance.is_deleted is True
