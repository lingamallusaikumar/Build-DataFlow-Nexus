import pytest

def test_billingplan_route_list(client, mocker):
    mocker.patch('app.domain_services.billingplan_service.BillingPlanService.get_all', return_value=[])
    response = client.get('/api/v2/billingplans/')
    assert response.status_code == 200

def test_billingplan_route_get(client, mocker):
    mocker.patch('app.domain_services.billingplan_service.BillingPlanService.get_by_id', return_value=mocker.MagicMock())
    response = client.get('/api/v2/billingplans/123')
    assert response.status_code == 200

def test_billingplan_route_create(client, mocker):
    mocker.patch('app.domain_services.billingplan_service.BillingPlanService.create', return_value=mocker.MagicMock())
    response = client.post('/api/v2/billingplans/', json={'attribute_1': 'test'})
    assert response.status_code == 201
