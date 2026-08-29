import pytest
from app.domain_services.pipelineversion_service import PipelineVersionService
from app.domain_models.pipelineversion import PipelineVersion

def test_pipelineversion_service_get_all(mocker):
    mocker.patch('app.domain_models.pipelineversion.PipelineVersion.query')
    result = PipelineVersionService.get_all()
    assert result is not None

def test_pipelineversion_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = PipelineVersionService.create(data)
    assert record.attribute_1 == 'val'

def test_pipelineversion_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.pipelineversion_service.PipelineVersionService.get_by_id')
    mock_instance = PipelineVersion()
    mock_get.return_value = mock_instance
    
    updated = PipelineVersionService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
