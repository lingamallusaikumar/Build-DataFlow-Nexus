import pytest
from app.connectors.registry import ConnectorRegistry
from app.connectors.rest_connector import RestAPIConnector
from app.connectors.mongodb_connector import MongoDBConnector
import pandas as pd
import io

def test_registry_resolution():
    connector = ConnectorRegistry.get_connector('rest_api', {'base_url': 'http://test.com'})
    assert isinstance(connector, RestAPIConnector)
    
def test_registry_unsupported():
    with pytest.raises(ValueError):
        ConnectorRegistry.get_connector('unsupported_type', {})

def test_file_connector_csv():
    connector = ConnectorRegistry.get_connector('file', {})
    # Create mock CSV bytes
    csv_data = b"id,name,value
1,Test,100
2,Data,200"
    results = connector.fetch_data(csv_data, 'csv')
    
    assert len(results) == 2
    assert results[0]['name'] == 'Test'
    assert results[1]['value'] == 200
