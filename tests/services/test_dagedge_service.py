import pytest
from app.domain_services.dagedge_service import DagEdgeService
from app.domain_models.dagedge import DagEdge

def test_dagedge_service_get_all(mocker):
    mocker.patch('app.domain_models.dagedge.DagEdge.query')
    result = DagEdgeService.get_all()
    assert result is not None

def test_dagedge_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = DagEdgeService.create(data)
    assert record.attribute_1 == 'val'

def test_dagedge_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.dagedge_service.DagEdgeService.get_by_id')
    mock_instance = DagEdge()
    mock_get.return_value = mock_instance
    
    updated = DagEdgeService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
