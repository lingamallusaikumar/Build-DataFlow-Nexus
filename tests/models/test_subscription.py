import pytest
from app.domain_models.subscription import Subscription

def test_subscription_creation():
    instance = Subscription()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_subscription_to_dict():
    instance = Subscription()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_subscription_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = Subscription()
    instance.soft_delete()
    assert instance.is_deleted is True
