import pytest

def test_pipelineversion_route_list(client, mocker):
    mocker.patch('app.domain_services.pipelineversion_service.PipelineVersionService.get_all', return_value=[])
    response = client.get('/api/v2/pipelineversions/')
    assert response.status_code == 200

def test_pipelineversion_route_get(client, mocker):
    mocker.patch('app.domain_services.pipelineversion_service.PipelineVersionService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/pipelineversions/123')
    assert response.status_code == 200

def test_pipelineversion_route_create(client, mocker):
    mocker.patch('app.domain_services.pipelineversion_service.PipelineVersionService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/pipelineversions/', json={'attribute_1': 'test'})
    assert response.status_code == 201
