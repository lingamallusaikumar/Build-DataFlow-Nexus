import pytest
from app.domain_services.tasklog_service import TaskLogService
from app.domain_models.tasklog import TaskLog

def test_tasklog_service_get_all(mocker):
    mocker.patch('app.domain_models.tasklog.TaskLog.query')
    result = TaskLogService.get_all()
    assert result is not None

def test_tasklog_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = TaskLogService.create(data)
    assert record.attribute_1 == 'val'

def test_tasklog_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.tasklog_service.TaskLogService.get_by_id')
    mock_instance = TaskLog()
    mock_get.return_value = mock_instance
    
    updated = TaskLogService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
