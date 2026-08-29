import pytest
from app.domain_services.schemacolumn_service import SchemaColumnService
from app.domain_models.schemacolumn import SchemaColumn

def test_schemacolumn_service_get_all(mocker):
    mocker.patch('app.domain_models.schemacolumn.SchemaColumn.query')
    result = SchemaColumnService.get_all()
    assert result is not None

def test_schemacolumn_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = SchemaColumnService.create(data)
    assert record.attribute_1 == 'val'

def test_schemacolumn_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.schemacolumn_service.SchemaColumnService.get_by_id')
    mock_instance = SchemaColumn()
    mock_get.return_value = mock_instance
    
    updated = SchemaColumnService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
