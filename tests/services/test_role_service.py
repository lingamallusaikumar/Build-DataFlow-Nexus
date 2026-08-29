import pytest
from app.domain_services.role_service import RoleService
from app.domain_models.role import Role

def test_role_service_get_all(mocker):
    mocker.patch('app.domain_models.role.Role.query')
    result = RoleService.get_all()
    assert result is not None

def test_role_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = RoleService.create(data)
    assert record.attribute_1 == 'val'

def test_role_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.role_service.RoleService.get_by_id')
    mock_instance = Role()
    mock_get.return_value = mock_instance
    
    updated = RoleService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
