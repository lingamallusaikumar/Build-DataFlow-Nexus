import pytest
from app.domain_models.invoice import Invoice

def test_invoice_creation():
    instance = Invoice()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_invoice_to_dict():
    instance = Invoice()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_invoice_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = Invoice()
    instance.soft_delete()
    assert instance.is_deleted is True
