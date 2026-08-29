import pytest

def test_qualityrule_route_list(client, mocker):
    mocker.patch('app.domain_services.qualityrule_service.QualityRuleService.get_all', return_value=[])
    response = client.get('/api/v2/qualityrules/')
    assert response.status_code == 200

def test_qualityrule_route_get(client, mocker):
    mocker.patch('app.domain_services.qualityrule_service.QualityRuleService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/qualityrules/123')
    assert response.status_code == 200

def test_qualityrule_route_create(client, mocker):
    mocker.patch('app.domain_services.qualityrule_service.QualityRuleService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/qualityrules/', json={'attribute_1': 'test'})
    assert response.status_code == 201
