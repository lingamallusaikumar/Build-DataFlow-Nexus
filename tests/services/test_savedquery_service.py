import pytest
from app.domain_services.savedquery_service import SavedQueryService
from app.domain_models.savedquery import SavedQuery

def test_savedquery_service_get_all(mocker):
    mocker.patch('app.domain_models.savedquery.SavedQuery.query')
    result = SavedQueryService.get_all()
    assert result is not None

def test_savedquery_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = SavedQueryService.create(data)
    assert record.attribute_1 == 'val'

def test_savedquery_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.savedquery_service.SavedQueryService.get_by_id')
    mock_instance = SavedQuery()
    mock_get.return_value = mock_instance
    
    updated = SavedQueryService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
