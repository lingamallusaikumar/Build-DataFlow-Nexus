import pytest
from app.domain_services.dagnode_service import DagNodeService
from app.domain_models.dagnode import DagNode

def test_dagnode_service_get_all(mocker):
    mocker.patch('app.domain_models.dagnode.DagNode.query')
    result = DagNodeService.get_all()
    assert result is not None

def test_dagnode_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = DagNodeService.create(data)
    assert record.attribute_1 == 'val'

def test_dagnode_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.dagnode_service.DagNodeService.get_by_id')
    mock_instance = DagNode()
    mock_get.return_value = mock_instance
    
    updated = DagNodeService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
