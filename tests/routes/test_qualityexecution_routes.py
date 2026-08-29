import pytest

def test_qualityexecution_route_list(client, mocker):
    mocker.patch('app.domain_services.qualityexecution_service.QualityExecutionService.get_all', return_value=[])
    response = client.get('/api/v2/qualityexecutions/')
    assert response.status_code == 200

def test_qualityexecution_route_get(client, mocker):
    mocker.patch('app.domain_services.qualityexecution_service.QualityExecutionService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/qualityexecutions/123')
    assert response.status_code == 200

def test_qualityexecution_route_create(client, mocker):
    mocker.patch('app.domain_services.qualityexecution_service.QualityExecutionService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/qualityexecutions/', json={'attribute_1': 'test'})
    assert response.status_code == 201
