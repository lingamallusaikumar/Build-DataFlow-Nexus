import pytest
from app.domain_services.session_service import SessionService
from app.domain_models.session import Session

def test_session_service_get_all(mocker):
    mocker.patch('app.domain_models.session.Session.query')
    result = SessionService.get_all()
    assert result is not None

def test_session_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = SessionService.create(data)
    assert record.attribute_1 == 'val'

def test_session_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.session_service.SessionService.get_by_id')
    mock_instance = Session()
    mock_get.return_value = mock_instance
    
    updated = SessionService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
