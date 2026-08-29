import pytest
from app.domain_services.rolepermission_service import RolePermissionService
from app.domain_models.rolepermission import RolePermission

def test_rolepermission_service_get_all(mocker):
    mocker.patch('app.domain_models.rolepermission.RolePermission.query')
    result = RolePermissionService.get_all()
    assert result is not None

def test_rolepermission_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = RolePermissionService.create(data)
    assert record.attribute_1 == 'val'

def test_rolepermission_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.rolepermission_service.RolePermissionService.get_by_id')
    mock_instance = RolePermission()
    mock_get.return_value = mock_instance
    
    updated = RolePermissionService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
