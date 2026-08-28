import pytest
from app.organizations.tenant_utils import get_tenant_resource_or_404
from werkzeug.exceptions import NotFound

# Mock models for testing
class MockResource:
    def __init__(self, id, org_id):
        self.id = id
        self.org_id = org_id
        
class MockQuery:
    def __init__(self, items):
        self.items = items
    def filter_by(self, id, org_id):
        result = [item for item in self.items if item.id == id and item.org_id == org_id]
        class ResultProxy:
            def first(self):
                return result[0] if result else None
        return ResultProxy()

class MockModel:
    __name__ = 'MockModel'
    query = MockQuery([MockResource("res_1", "org_1"), MockResource("res_2", "org_2")])

def test_tenant_isolation_success():
    resource = get_tenant_resource_or_404(MockModel, "org_1", "res_1")
    assert resource.id == "res_1"

def test_tenant_isolation_failure_wrong_org():
    with pytest.raises(NotFound):
        get_tenant_resource_or_404(MockModel, "org_1", "res_2") # res_2 belongs to org_2

def test_tenant_isolation_failure_missing_resource():
    with pytest.raises(NotFound):
        get_tenant_resource_or_404(MockModel, "org_1", "res_99")
