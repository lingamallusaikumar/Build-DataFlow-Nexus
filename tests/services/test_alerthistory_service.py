import pytest
from app.domain_services.alerthistory_service import AlertHistoryService
from app.domain_models.alerthistory import AlertHistory

def test_alerthistory_service_get_all(mocker):
    mocker.patch('app.domain_models.alerthistory.AlertHistory.query')
    result = AlertHistoryService.get_all()
    assert result is not None

def test_alerthistory_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = AlertHistoryService.create(data)
    assert record.attribute_1 == 'val'

def test_alerthistory_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.alerthistory_service.AlertHistoryService.get_by_id')
    mock_instance = AlertHistory()
    mock_get.return_value = mock_instance
    
    updated = AlertHistoryService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
