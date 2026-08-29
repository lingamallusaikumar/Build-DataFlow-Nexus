import pytest
from app.domain_services.apikey_service import ApiKeyService
from app.domain_models.apikey import ApiKey

def test_apikey_service_get_all(mocker):
    mocker.patch('app.domain_models.apikey.ApiKey.query')
    result = ApiKeyService.get_all()
    assert result is not None

def test_apikey_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = ApiKeyService.create(data)
    assert record.attribute_1 == 'val'

def test_apikey_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.apikey_service.ApiKeyService.get_by_id')
    mock_instance = ApiKey()
    mock_get.return_value = mock_instance
    
    updated = ApiKeyService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
