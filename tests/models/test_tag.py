import pytest
from app.domain_models.tag import Tag

def test_tag_creation():
    instance = Tag()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_tag_to_dict():
    instance = Tag()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_tag_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = Tag()
    instance.soft_delete()
    assert instance.is_deleted is True
