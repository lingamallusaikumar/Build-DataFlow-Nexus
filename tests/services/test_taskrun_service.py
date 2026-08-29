import pytest
from app.domain_services.taskrun_service import TaskRunService
from app.domain_models.taskrun import TaskRun

def test_taskrun_service_get_all(mocker):
    mocker.patch('app.domain_models.taskrun.TaskRun.query')
    result = TaskRunService.get_all()
    assert result is not None

def test_taskrun_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = TaskRunService.create(data)
    assert record.attribute_1 == 'val'

def test_taskrun_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.taskrun_service.TaskRunService.get_by_id')
    mock_instance = TaskRun()
    mock_get.return_value = mock_instance
    
    updated = TaskRunService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
