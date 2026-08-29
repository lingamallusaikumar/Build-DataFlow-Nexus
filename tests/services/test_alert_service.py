import pytest
from app.domain_services.alert_service import AlertService
from app.domain_models.alert import Alert

def test_alert_service_get_all(mocker):
    mocker.patch('app.domain_models.alert.Alert.query')
    result = AlertService.get_all()
    assert result is not None

def test_alert_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = AlertService.create(data)
    assert record.attribute_1 == 'val'

def test_alert_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.alert_service.AlertService.get_by_id')
    mock_instance = Alert()
    mock_get.return_value = mock_instance
    
    updated = AlertService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
