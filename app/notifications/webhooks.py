import requests
import logging
from app.extensions import db
from app.models.base import BaseModel

logger = logging.getLogger(__name__)

class WebhookEndpoint(BaseModel):
    __tablename__ = 'webhook_endpoints'
    
    org_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    secret_token = db.Column(db.String(255), nullable=True) # Used for HMAC signatures
    is_active = db.Column(db.Boolean, default=True)

class WebhookService:
    @staticmethod
    def fire_webhook(url, payload, secret_token=None):
        """
        Fires an HTTP POST request to the target URL. 
        In production, this should be executed via a Celery background task to prevent blocking.
        """
        headers = {'Content-Type': 'application/json'}
        if secret_token:
            headers['X-Nexus-Signature'] = secret_token # Simplified signature for demonstration
            
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            response.raise_for_status()
            logger.info(f"Webhook delivered successfully to {url}")
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to deliver webhook to {url}: {e}")
            return False
