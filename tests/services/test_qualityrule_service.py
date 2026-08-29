import pytest
from app.domain_services.qualityrule_service import QualityRuleService
from app.domain_models.qualityrule import QualityRule

def test_qualityrule_service_get_all(mocker):
    mocker.patch('app.domain_models.qualityrule.QualityRule.query')
    result = QualityRuleService.get_all()
    assert result is not None

def test_qualityrule_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = QualityRuleService.create(data)
    assert record.attribute_1 == 'val'

def test_qualityrule_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.qualityrule_service.QualityRuleService.get_by_id')
    mock_instance = QualityRule()
    mock_get.return_value = mock_instance
    
    updated = QualityRuleService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
