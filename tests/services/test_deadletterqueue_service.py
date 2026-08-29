import pytest
from app.domain_services.deadletterqueue_service import DeadLetterQueueService
from app.domain_models.deadletterqueue import DeadLetterQueue

def test_deadletterqueue_service_get_all(mocker):
    mocker.patch('app.domain_models.deadletterqueue.DeadLetterQueue.query')
    result = DeadLetterQueueService.get_all()
    assert result is not None

def test_deadletterqueue_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = DeadLetterQueueService.create(data)
    assert record.attribute_1 == 'val'

def test_deadletterqueue_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.deadletterqueue_service.DeadLetterQueueService.get_by_id')
    mock_instance = DeadLetterQueue()
    mock_get.return_value = mock_instance
    
    updated = DeadLetterQueueService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
