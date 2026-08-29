import pytest
from app.domain_services.setting_service import SettingService
from app.domain_models.setting import Setting

def test_setting_service_get_all(mocker):
    mocker.patch('app.domain_models.setting.Setting.query')
    result = SettingService.get_all()
    assert result is not None

def test_setting_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = SettingService.create(data)
    assert record.attribute_1 == 'val'

def test_setting_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.setting_service.SettingService.get_by_id')
    mock_instance = Setting()
    mock_get.return_value = mock_instance
    
    updated = SettingService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
