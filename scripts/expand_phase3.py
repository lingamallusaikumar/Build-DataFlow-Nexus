import os

base_dir = r'c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus'

files = {
    'app/connectors/rest_connector.py': '''import requests
import time
import logging
from app.connectors.base.connector_interface import BaseConnector

logger = logging.getLogger(__name__)

class RestAPIConnector(BaseConnector):
    def connect(self):
        # REST APIs are stateless, so connect just returns the requests session
        session = requests.Session()
        if self.config.get('auth_type') == 'bearer':
            session.headers.update({'Authorization': f"Bearer {self.config.get('token')}"})
        elif self.config.get('auth_type') == 'basic':
            session.auth = (self.config.get('username'), self.config.get('password'))
        return session

    def test_connection(self):
        try:
            session = self.connect()
            test_url = self.config.get('test_url', self.config.get('base_url'))
            response = session.get(test_url, timeout=10)
            return response.status_code < 400
        except Exception as e:
            logger.error(f"REST API connection test failed: {e}")
            return False

    def fetch_data(self, endpoint, method='GET', params=None, max_retries=3):
        session = self.connect()
        url = f"{self.config.get('base_url')}/{endpoint.lstrip('/')}"
        
        for attempt in range(max_retries):
            try:
                if method == 'GET':
                    response = session.get(url, params=params, timeout=30)
                else:
                    response = session.post(url, json=params, timeout=30)
                    
                if response.status_code == 429: # Rate Limited
                    time.sleep(2 ** attempt) # Exponential backoff
                    continue
                    
                response.raise_for_status()
                return response.json()
                
            except requests.RequestException as e:
                logger.error(f"REST API fetch failed on attempt {attempt+1}: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)
                
    def push_data(self, endpoint, data):
        session = self.connect()
        url = f"{self.config.get('base_url')}/{endpoint.lstrip('/')}"
        response = session.post(url, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
''',
    'app/connectors/mongodb_connector.py': '''from app.connectors.base.connector_interface import BaseConnector
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging

logger = logging.getLogger(__name__)

class MongoDBConnector(BaseConnector):
    def connect(self):
        uri = self.config.get('uri')
        if not uri:
            # Build URI from parts
            user = self.config.get('user')
            password = self.config.get('password')
            host = self.config.get('host', 'localhost')
            port = self.config.get('port', 27017)
            uri = f"mongodb://{user}:{password}@{host}:{port}/"
            
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        return client

    def test_connection(self):
        try:
            client = self.connect()
            client.admin.command('ping')
            client.close()
            return True
        except ConnectionFailure as e:
            logger.error(f"MongoDB connection test failed: {e}")
            return False

    def fetch_data(self, database, collection, query=None, limit=1000):
        client = self.connect()
        try:
            db = client[database]
            col = db[collection]
            results = list(col.find(query or {}).limit(limit))
            # Convert ObjectId to string for JSON serialization
            for doc in results:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
            return results
        finally:
            client.close()

    def push_data(self, database, collection, data):
        client = self.connect()
        try:
            db = client[database]
            col = db[collection]
            if isinstance(data, list):
                result = col.insert_many(data)
                return [str(id) for id in result.inserted_ids]
            else:
                result = col.insert_one(data)
                return str(result.inserted_id)
        finally:
            client.close()
''',
    'app/connectors/file_connector.py': '''from app.connectors.base.connector_interface import BaseConnector
import pandas as pd
import io
import logging

logger = logging.getLogger(__name__)

class FileConnector(BaseConnector):
    """
    Handles CSV and Excel data streams.
    In a real environment, this might connect to AWS S3 or Google Cloud Storage to fetch the file bytes.
    """
    def connect(self):
        # Config would contain S3 buckets or local mount paths
        pass

    def test_connection(self):
        # Test bucket access
        return True

    def fetch_data(self, file_bytes, file_type='csv'):
        try:
            if file_type == 'csv':
                df = pd.read_csv(io.BytesIO(file_bytes))
            elif file_type == 'excel':
                df = pd.read_excel(io.BytesIO(file_bytes))
            else:
                raise ValueError("Unsupported file type")
                
            # Replace NaNs with None for JSON serialization
            df = df.where(pd.notnull(df), None)
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Failed to parse file: {e}")
            raise

    def push_data(self, file_path, data, file_type='csv'):
        df = pd.DataFrame(data)
        if file_type == 'csv':
            df.to_csv(file_path, index=False)
        elif file_type == 'excel':
            df.to_excel(file_path, index=False)
        return True
''',
    'app/connectors/registry.py': '''from app.connectors.base.postgres_connector import PostgresConnector
from app.connectors.rest_connector import RestAPIConnector
from app.connectors.mongodb_connector import MongoDBConnector
from app.connectors.file_connector import FileConnector

class ConnectorRegistry:
    """
    Factory class to dynamically instantiate the correct connector based on type.
    """
    _connectors = {
        'postgres': PostgresConnector,
        'rest_api': RestAPIConnector,
        'mongodb': MongoDBConnector,
        'file': FileConnector
    }

    @classmethod
    def get_connector(cls, connector_type, config):
        connector_class = cls._connectors.get(connector_type)
        if not connector_class:
            raise ValueError(f"Unsupported connector type: {connector_type}")
        return connector_class(config)
        
    @classmethod
    def register_connector(cls, connector_type, connector_class):
        cls._connectors[connector_type] = connector_class
''',
    'tests/test_connectors.py': '''import pytest
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
    csv_data = b"id,name,value\n1,Test,100\n2,Data,200"
    results = connector.fetch_data(csv_data, 'csv')
    
    assert len(results) == 2
    assert results[0]['name'] == 'Test'
    assert results[1]['value'] == 200
'''
}

# Update requirements.txt to include new dependencies
requirements_path = os.path.join(base_dir, 'requirements.txt')
if os.path.exists(requirements_path):
    with open(requirements_path, 'a', encoding='utf-8') as req_file:
        req_file.write("requests==2.31.0\npymongo==4.6.1\npandas==2.1.4\nopenpyxl==3.1.2\n")

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Phase 3 Deep Dive components generated successfully.')
