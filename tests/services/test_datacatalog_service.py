import pytest
from app.domain_services.datacatalog_service import DataCatalogService
from app.domain_models.datacatalog import DataCatalog

def test_datacatalog_service_get_all(mocker):
    mocker.patch('app.domain_models.datacatalog.DataCatalog.query')
    result = DataCatalogService.get_all()
    assert result is not None

def test_datacatalog_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = DataCatalogService.create(data)
    assert record.attribute_1 == 'val'

def test_datacatalog_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.datacatalog_service.DataCatalogService.get_by_id')
    mock_instance = DataCatalog()
    mock_get.return_value = mock_instance
    
    updated = DataCatalogService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
