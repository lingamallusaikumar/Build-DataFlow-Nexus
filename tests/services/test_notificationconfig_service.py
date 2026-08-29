import pytest
from app.domain_services.notificationconfig_service import NotificationConfigService
from app.domain_models.notificationconfig import NotificationConfig

def test_notificationconfig_service_get_all(mocker):
    mocker.patch('app.domain_models.notificationconfig.NotificationConfig.query')
    result = NotificationConfigService.get_all()
    assert result is not None

def test_notificationconfig_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = NotificationConfigService.create(data)
    assert record.attribute_1 == 'val'

def test_notificationconfig_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.notificationconfig_service.NotificationConfigService.get_by_id')
    mock_instance = NotificationConfig()
    mock_get.return_value = mock_instance
    
    updated = NotificationConfigService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
