import pytest
from app.domain_services.quotausage_service import QuotaUsageService
from app.domain_models.quotausage import QuotaUsage

def test_quotausage_service_get_all(mocker):
    mocker.patch('app.domain_models.quotausage.QuotaUsage.query')
    result = QuotaUsageService.get_all()
    assert result is not None

def test_quotausage_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = QuotaUsageService.create(data)
    assert record.attribute_1 == 'val'

def test_quotausage_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.quotausage_service.QuotaUsageService.get_by_id')
    mock_instance = QuotaUsage()
    mock_get.return_value = mock_instance
    
    updated = QuotaUsageService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
