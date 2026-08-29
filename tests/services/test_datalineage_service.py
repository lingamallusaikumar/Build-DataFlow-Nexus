import pytest
from app.domain_services.datalineage_service import DataLineageService
from app.domain_models.datalineage import DataLineage

def test_datalineage_service_get_all(mocker):
    mocker.patch('app.domain_models.datalineage.DataLineage.query')
    result = DataLineageService.get_all()
    assert result is not None

def test_datalineage_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = DataLineageService.create(data)
    assert record.attribute_1 == 'val'

def test_datalineage_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.datalineage_service.DataLineageService.get_by_id')
    mock_instance = DataLineage()
    mock_get.return_value = mock_instance
    
    updated = DataLineageService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
