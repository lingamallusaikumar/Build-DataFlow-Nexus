import pytest

def test_resourcetag_route_list(client, mocker):
    mocker.patch('app.domain_services.resourcetag_service.ResourceTagService.get_all', return_value=[])
    response = client.get('/api/v2/resourcetags/')
    assert response.status_code == 200

def test_resourcetag_route_get(client, mocker):
    mocker.patch('app.domain_services.resourcetag_service.ResourceTagService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/resourcetags/123')
    assert response.status_code == 200

def test_resourcetag_route_create(client, mocker):
    mocker.patch('app.domain_services.resourcetag_service.ResourceTagService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/resourcetags/', json={'attribute_1': 'test'})
    assert response.status_code == 201
