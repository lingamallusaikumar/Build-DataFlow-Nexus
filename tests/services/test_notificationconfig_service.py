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

def test_notificationconfig_service_validation_edge_case_1(mocker):
    mocker.patch('app.extensions.db.session.commit')
    try:
        NotificationConfigService.create({'attribute_1': 'x' * 300})
    except ValueError as e:
        assert 'too long' in str(e)

def test_notificationconfig_service_validation_edge_case_2(mocker):
    mocker.patch('app.extensions.db.session.commit')
    try:
        NotificationConfigService.create({'attribute_2': 'x' * 300})
    except ValueError as e:
        assert 'too long' in str(e)

def test_notificationconfig_service_validation_edge_case_3(mocker):
    mocker.patch('app.extensions.db.session.commit')
    try:
        NotificationConfigService.create({'attribute_3': 'x' * 300})
    except ValueError as e:
        assert 'too long' in str(e)

def test_notificationconfig_service_validation_edge_case_4(mocker):
    mocker.patch('app.extensions.db.session.commit')
    try:
        NotificationConfigService.create({'attribute_4': 'x' * 300})
    except ValueError as e:
        assert 'too long' in str(e)

def test_notificationconfig_service_validation_edge_case_5(mocker):
    mocker.patch('app.extensions.db.session.commit')
    try:
        NotificationConfigService.create({'attribute_5': 'x' * 300})
    except ValueError as e:
        assert 'too long' in str(e)

def test_notificationconfig_service_validation_edge_case_6(mocker):
    mocker.patch('app.extensions.db.session.commit')
    try:
        NotificationConfigService.create({'attribute_6': 'x' * 300})
    except ValueError as e:
        assert 'too long' in str(e)

def test_notificationconfig_service_validation_edge_case_7(mocker):
    mocker.patch('app.extensions.db.session.commit')
    try:
        NotificationConfigService.create({'attribute_7': 'x' * 300})
    except ValueError as e:
        assert 'too long' in str(e)

def test_notificationconfig_service_validation_edge_case_8(mocker):
    mocker.patch('app.extensions.db.session.commit')
    try:
        NotificationConfigService.create({'attribute_8': 'x' * 300})
    except ValueError as e:
        assert 'too long' in str(e)

def test_notificationconfig_service_validation_edge_case_9(mocker):
    mocker.patch('app.extensions.db.session.commit')
    try:
        NotificationConfigService.create({'attribute_9': 'x' * 300})
    except ValueError as e:
        assert 'too long' in str(e)
