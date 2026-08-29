import pytest
from app.domain_services.dataschema_service import DataSchemaService
from app.domain_models.dataschema import DataSchema

def test_dataschema_service_get_all(mocker):
    mocker.patch('app.domain_models.dataschema.DataSchema.query')
    result = DataSchemaService.get_all()
    assert result is not None

def test_dataschema_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = DataSchemaService.create(data)
    assert record.attribute_1 == 'val'

def test_dataschema_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.dataschema_service.DataSchemaService.get_by_id')
    mock_instance = DataSchema()
    mock_get.return_value = mock_instance
    
    updated = DataSchemaService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
