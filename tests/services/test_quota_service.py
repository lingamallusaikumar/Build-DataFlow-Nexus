import pytest
from app.domain_services.quota_service import QuotaService
from app.domain_models.quota import Quota

def test_quota_service_get_all(mocker):
    mocker.patch('app.domain_models.quota.Quota.query')
    result = QuotaService.get_all()
    assert result is not None

def test_quota_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = QuotaService.create(data)
    assert record.attribute_1 == 'val'

def test_quota_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.quota_service.QuotaService.get_by_id')
    mock_instance = Quota()
    mock_get.return_value = mock_instance
    
    updated = QuotaService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
