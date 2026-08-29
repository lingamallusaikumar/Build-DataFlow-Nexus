import pytest
from app.domain_services.userrole_service import UserRoleService
from app.domain_models.userrole import UserRole

def test_userrole_service_get_all(mocker):
    mocker.patch('app.domain_models.userrole.UserRole.query')
    result = UserRoleService.get_all()
    assert result is not None

def test_userrole_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = UserRoleService.create(data)
    assert record.attribute_1 == 'val'

def test_userrole_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.userrole_service.UserRoleService.get_by_id')
    mock_instance = UserRole()
    mock_get.return_value = mock_instance
    
    updated = UserRoleService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
