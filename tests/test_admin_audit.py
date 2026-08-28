from app.audit.diff_engine import AuditDiffEngine

def test_audit_diff_engine():
    old_state = {"name": "Test", "status": "active", "old_key": "exists"}
    new_state = {"name": "Test Modified", "status": "active", "new_key": "added"}
    
    diff = AuditDiffEngine.calculate_diff(old_state, new_state)
    
    assert "new_key" in diff['added']
    assert "old_key" in diff['removed']
    assert "name" in diff['modified']
    assert diff['modified']['name']['from'] == "Test"
    assert diff['modified']['name']['to'] == "Test Modified"
    
def test_liveness_probe(client):
    response = client.get('/health/liveness')
    assert response.status_code == 200
    assert response.json['status'] == 'alive'
