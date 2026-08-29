import pytest
from app.domain_services.auditlog_service import AuditLogService
from app.domain_models.auditlog import AuditLog

def test_auditlog_service_get_all(mocker):
    mocker.patch('app.domain_models.auditlog.AuditLog.query')
    result = AuditLogService.get_all()
    assert result is not None

def test_auditlog_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = AuditLogService.create(data)
    assert record.attribute_1 == 'val'

def test_auditlog_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.auditlog_service.AuditLogService.get_by_id')
    mock_instance = AuditLog()
    mock_get.return_value = mock_instance
    
    updated = AuditLogService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
