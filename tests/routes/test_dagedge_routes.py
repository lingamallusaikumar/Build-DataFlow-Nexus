import pytest

def test_dagedge_route_list(client, mocker):
    mocker.patch('app.domain_services.dagedge_service.DagEdgeService.get_all', return_value=[])
    response = client.get('/api/v2/dagedges/')
    assert response.status_code == 200

def test_dagedge_route_get(client, mocker):
    mocker.patch('app.domain_services.dagedge_service.DagEdgeService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/dagedges/123')
    assert response.status_code == 200

def test_dagedge_route_create(client, mocker):
    mocker.patch('app.domain_services.dagedge_service.DagEdgeService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/dagedges/', json={'attribute_1': 'test'})
    assert response.status_code == 201
