import pytest

def test_dataset_route_list(client, mocker):
    mocker.patch('app.domain_services.dataset_service.DatasetService.get_all', return_value=[])
    response = client.get('/api/v2/datasets/')
    assert response.status_code == 200

def test_dataset_route_get(client, mocker):
    mocker.patch('app.domain_services.dataset_service.DatasetService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/datasets/123')
    assert response.status_code == 200

def test_dataset_route_create(client, mocker):
    mocker.patch('app.domain_services.dataset_service.DatasetService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/datasets/', json={'attribute_1': 'test'})
    assert response.status_code == 201
