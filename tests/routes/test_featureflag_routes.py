import pytest

def test_featureflag_route_list(client, mocker):
    mocker.patch('app.domain_services.featureflag_service.FeatureFlagService.get_all', return_value=[])
    response = client.get('/api/v2/featureflags/')
    assert response.status_code == 200

def test_featureflag_route_get(client, mocker):
    mocker.patch('app.domain_services.featureflag_service.FeatureFlagService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/featureflags/123')
    assert response.status_code == 200

def test_featureflag_route_create(client, mocker):
    mocker.patch('app.domain_services.featureflag_service.FeatureFlagService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/featureflags/', json={'attribute_1': 'test'})
    assert response.status_code == 201
