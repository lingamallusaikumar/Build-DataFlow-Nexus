import pytest
from app.domain_services.resourcetag_service import ResourceTagService
from app.domain_models.resourcetag import ResourceTag

def test_resourcetag_service_get_all(mocker):
    mocker.patch('app.domain_models.resourcetag.ResourceTag.query')
    result = ResourceTagService.get_all()
    assert result is not None

def test_resourcetag_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = ResourceTagService.create(data)
    assert record.attribute_1 == 'val'

def test_resourcetag_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.resourcetag_service.ResourceTagService.get_by_id')
    mock_instance = ResourceTag()
    mock_get.return_value = mock_instance
    
    updated = ResourceTagService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
