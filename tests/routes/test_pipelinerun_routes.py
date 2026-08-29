import pytest

def test_pipelinerun_route_list(client, mocker):
    mocker.patch('app.domain_services.pipelinerun_service.PipelineRunService.get_all', return_value=[])
    response = client.get('/api/v2/pipelineruns/')
    assert response.status_code == 200

def test_pipelinerun_route_get(client, mocker):
    mocker.patch('app.domain_services.pipelinerun_service.PipelineRunService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/pipelineruns/123')
    assert response.status_code == 200

def test_pipelinerun_route_create(client, mocker):
    mocker.patch('app.domain_services.pipelinerun_service.PipelineRunService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/pipelineruns/', json={'attribute_1': 'test'})
    assert response.status_code == 201
