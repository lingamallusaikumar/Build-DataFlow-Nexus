import pytest

def test_tasklog_route_list(client, mocker):
    mocker.patch('app.domain_services.tasklog_service.TaskLogService.get_all', return_value=[])
    response = client.get('/api/v2/tasklogs/')
    assert response.status_code == 200

def test_tasklog_route_get(client, mocker):
    mocker.patch('app.domain_services.tasklog_service.TaskLogService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/tasklogs/123')
    assert response.status_code == 200

def test_tasklog_route_create(client, mocker):
    mocker.patch('app.domain_services.tasklog_service.TaskLogService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/tasklogs/', json={'attribute_1': 'test'})
    assert response.status_code == 201
