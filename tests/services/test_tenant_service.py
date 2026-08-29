import pytest
from app.domain_services.tenant_service import TenantService
from app.domain_models.tenant import Tenant

def test_tenant_service_get_all(mocker):
    mocker.patch('app.domain_models.tenant.Tenant.query')
    result = TenantService.get_all()
    assert result is not None

def test_tenant_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = TenantService.create(data)
    assert record.attribute_1 == 'val'

def test_tenant_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.tenant_service.TenantService.get_by_id')
    mock_instance = Tenant()
    mock_get.return_value = mock_instance
    
    updated = TenantService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
