import pytest
from app.domain_services.billingplan_service import BillingPlanService
from app.domain_models.billingplan import BillingPlan

def test_billingplan_service_get_all(mocker):
    mocker.patch('app.domain_models.billingplan.BillingPlan.query')
    result = BillingPlanService.get_all()
    assert result is not None

def test_billingplan_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = BillingPlanService.create(data)
    assert record.attribute_1 == 'val'

def test_billingplan_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.billingplan_service.BillingPlanService.get_by_id')
    mock_instance = BillingPlan()
    mock_get.return_value = mock_instance
    
    updated = BillingPlanService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
