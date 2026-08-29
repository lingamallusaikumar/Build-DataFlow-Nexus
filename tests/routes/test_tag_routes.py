import pytest

def test_tag_route_list(client, mocker):
    mocker.patch('app.domain_services.tag_service.TagService.get_all', return_value=[])
    response = client.get('/api/v2/tags/')
    assert response.status_code == 200

def test_tag_route_get(client, mocker):
    mocker.patch('app.domain_services.tag_service.TagService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/tags/123')
    assert response.status_code == 200

def test_tag_route_create(client, mocker):
    mocker.patch('app.domain_services.tag_service.TagService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/tags/', json={'attribute_1': 'test'})
    assert response.status_code == 201
