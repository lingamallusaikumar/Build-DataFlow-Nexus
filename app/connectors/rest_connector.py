import requests
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
