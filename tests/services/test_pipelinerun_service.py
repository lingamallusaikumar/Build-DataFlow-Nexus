import pytest
from app.domain_services.pipelinerun_service import PipelineRunService
from app.domain_models.pipelinerun import PipelineRun

def test_pipelinerun_service_get_all(mocker):
    mocker.patch('app.domain_models.pipelinerun.PipelineRun.query')
    result = PipelineRunService.get_all()
    assert result is not None

def test_pipelinerun_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = PipelineRunService.create(data)
    assert record.attribute_1 == 'val'

def test_pipelinerun_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.pipelinerun_service.PipelineRunService.get_by_id')
    mock_instance = PipelineRun()
    mock_get.return_value = mock_instance
    
    updated = PipelineRunService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
