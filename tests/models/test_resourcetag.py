import pytest
from app.domain_models.resourcetag import ResourceTag

def test_resourcetag_creation():
    instance = ResourceTag()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_resourcetag_to_dict():
    instance = ResourceTag()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_resourcetag_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = ResourceTag()
    instance.soft_delete()
    assert instance.is_deleted is True
