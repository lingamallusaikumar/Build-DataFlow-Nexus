import pytest
from app.domain_services.metric_service import MetricService
from app.domain_models.metric import Metric

def test_metric_service_get_all(mocker):
    mocker.patch('app.domain_models.metric.Metric.query')
    result = MetricService.get_all()
    assert result is not None

def test_metric_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = MetricService.create(data)
    assert record.attribute_1 == 'val'

def test_metric_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.metric_service.MetricService.get_by_id')
    mock_instance = Metric()
    mock_get.return_value = mock_instance
    
    updated = MetricService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
