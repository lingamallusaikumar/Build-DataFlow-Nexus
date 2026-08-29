import pytest
from app.domain_services.qualityexecution_service import QualityExecutionService
from app.domain_models.qualityexecution import QualityExecution

def test_qualityexecution_service_get_all(mocker):
    mocker.patch('app.domain_models.qualityexecution.QualityExecution.query')
    result = QualityExecutionService.get_all()
    assert result is not None

def test_qualityexecution_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = QualityExecutionService.create(data)
    assert record.attribute_1 == 'val'

def test_qualityexecution_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.qualityexecution_service.QualityExecutionService.get_by_id')
    mock_instance = QualityExecution()
    mock_get.return_value = mock_instance
    
    updated = QualityExecutionService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
