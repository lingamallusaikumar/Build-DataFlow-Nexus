import pytest

def test_taskrun_route_list(client, mocker):
    mocker.patch('app.domain_services.taskrun_service.TaskRunService.get_all', return_value=[])
    response = client.get('/api/v2/taskruns/')
    assert response.status_code == 200

def test_taskrun_route_get(client, mocker):
    mocker.patch('app.domain_services.taskrun_service.TaskRunService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/taskruns/123')
    assert response.status_code == 200

def test_taskrun_route_create(client, mocker):
    mocker.patch('app.domain_services.taskrun_service.TaskRunService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/taskruns/', json={'attribute_1': 'test'})
    assert response.status_code == 201
