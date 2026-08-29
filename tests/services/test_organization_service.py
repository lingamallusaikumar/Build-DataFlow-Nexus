import pytest
from app.domain_services.organization_service import OrganizationService
from app.domain_models.organization import Organization

def test_organization_service_get_all(mocker):
    mocker.patch('app.domain_models.organization.Organization.query')
    result = OrganizationService.get_all()
    assert result is not None

def test_organization_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = OrganizationService.create(data)
    assert record.attribute_1 == 'val'

def test_organization_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.organization_service.OrganizationService.get_by_id')
    mock_instance = Organization()
    mock_get.return_value = mock_instance
    
    updated = OrganizationService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
