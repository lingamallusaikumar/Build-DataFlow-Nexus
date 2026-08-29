import pytest
from app.domain_services.permission_service import PermissionService
from app.domain_models.permission import Permission

def test_permission_service_get_all(mocker):
    mocker.patch('app.domain_models.permission.Permission.query')
    result = PermissionService.get_all()
    assert result is not None

def test_permission_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = PermissionService.create(data)
    assert record.attribute_1 == 'val'

def test_permission_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.permission_service.PermissionService.get_by_id')
    mock_instance = Permission()
    mock_get.return_value = mock_instance
    
    updated = PermissionService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
