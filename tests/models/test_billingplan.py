import pytest
from app.domain_models.billingplan import BillingPlan

def test_billingplan_creation():
    instance = BillingPlan()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_billingplan_to_dict():
    instance = BillingPlan()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_billingplan_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = BillingPlan()
    instance.soft_delete()
    assert instance.is_deleted is True
