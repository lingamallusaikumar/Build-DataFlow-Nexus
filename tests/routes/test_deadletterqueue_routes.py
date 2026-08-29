import pytest

def test_deadletterqueue_route_list(client, mocker):
    mocker.patch('app.domain_services.deadletterqueue_service.DeadLetterQueueService.get_all', return_value=[])
    response = client.get('/api/v2/deadletterqueues/')
    assert response.status_code == 200

def test_deadletterqueue_route_get(client, mocker):
    mocker.patch('app.domain_services.deadletterqueue_service.DeadLetterQueueService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/deadletterqueues/123')
    assert response.status_code == 200

def test_deadletterqueue_route_create(client, mocker):
    mocker.patch('app.domain_services.deadletterqueue_service.DeadLetterQueueService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/deadletterqueues/', json={'attribute_1': 'test'})
    assert response.status_code == 201
