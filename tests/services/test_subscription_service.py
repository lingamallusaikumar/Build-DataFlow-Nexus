import pytest
from app.domain_services.subscription_service import SubscriptionService
from app.domain_models.subscription import Subscription

def test_subscription_service_get_all(mocker):
    mocker.patch('app.domain_models.subscription.Subscription.query')
    result = SubscriptionService.get_all()
    assert result is not None

def test_subscription_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = SubscriptionService.create(data)
    assert record.attribute_1 == 'val'

def test_subscription_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.subscription_service.SubscriptionService.get_by_id')
    mock_instance = Subscription()
    mock_get.return_value = mock_instance
    
    updated = SubscriptionService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
