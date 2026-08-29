import pytest
from app.domain_services.pipeline_service import PipelineService
from app.domain_models.pipeline import Pipeline

def test_pipeline_service_get_all(mocker):
    mocker.patch('app.domain_models.pipeline.Pipeline.query')
    result = PipelineService.get_all()
    assert result is not None

def test_pipeline_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = PipelineService.create(data)
    assert record.attribute_1 == 'val'

def test_pipeline_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.pipeline_service.PipelineService.get_by_id')
    mock_instance = Pipeline()
    mock_get.return_value = mock_instance
    
    updated = PipelineService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
