import pytest
from app.domain_services.connectioncredentials_service import ConnectionCredentialsService
from app.domain_models.connectioncredentials import ConnectionCredentials

def test_connectioncredentials_service_get_all(mocker):
    mocker.patch('app.domain_models.connectioncredentials.ConnectionCredentials.query')
    result = ConnectionCredentialsService.get_all()
    assert result is not None

def test_connectioncredentials_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = ConnectionCredentialsService.create(data)
    assert record.attribute_1 == 'val'

def test_connectioncredentials_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.connectioncredentials_service.ConnectionCredentialsService.get_by_id')
    mock_instance = ConnectionCredentials()
    mock_get.return_value = mock_instance
    
    updated = ConnectionCredentialsService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
