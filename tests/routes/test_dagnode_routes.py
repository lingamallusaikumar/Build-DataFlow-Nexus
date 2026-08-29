import pytest

def test_dagnode_route_list(client, mocker):
    mocker.patch('app.domain_services.dagnode_service.DagNodeService.get_all', return_value=[])
    response = client.get('/api/v2/dagnodes/')
    assert response.status_code == 200

def test_dagnode_route_get(client, mocker):
    mocker.patch('app.domain_services.dagnode_service.DagNodeService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/dagnodes/123')
    assert response.status_code == 200

def test_dagnode_route_create(client, mocker):
    mocker.patch('app.domain_services.dagnode_service.DagNodeService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/dagnodes/', json={'attribute_1': 'test'})
    assert response.status_code == 201
