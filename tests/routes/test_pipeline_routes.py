import pytest

def test_pipeline_route_list(client, mocker):
    mocker.patch('app.domain_services.pipeline_service.PipelineService.get_all', return_value=[])
    response = client.get('/api/v2/pipelines/')
    assert response.status_code == 200

def test_pipeline_route_get(client, mocker):
    mocker.patch('app.domain_services.pipeline_service.PipelineService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/pipelines/123')
    assert response.status_code == 200

def test_pipeline_route_create(client, mocker):
    mocker.patch('app.domain_services.pipeline_service.PipelineService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/pipelines/', json={'attribute_1': 'test'})
    assert response.status_code == 201
