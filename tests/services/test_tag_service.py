import pytest
from app.domain_services.tag_service import TagService
from app.domain_models.tag import Tag

def test_tag_service_get_all(mocker):
    mocker.patch('app.domain_models.tag.Tag.query')
    result = TagService.get_all()
    assert result is not None

def test_tag_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = TagService.create(data)
    assert record.attribute_1 == 'val'

def test_tag_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.tag_service.TagService.get_by_id')
    mock_instance = Tag()
    mock_get.return_value = mock_instance
    
    updated = TagService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
