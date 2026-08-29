import pytest
from app.domain_services.connector_service import ConnectorService
from app.domain_models.connector import Connector

def test_connector_service_get_all(mocker):
    mocker.patch('app.domain_models.connector.Connector.query')
    result = ConnectorService.get_all()
    assert result is not None

def test_connector_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = ConnectorService.create(data)
    assert record.attribute_1 == 'val'

def test_connector_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.connector_service.ConnectorService.get_by_id')
    mock_instance = Connector()
    mock_get.return_value = mock_instance
    
    updated = ConnectorService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
