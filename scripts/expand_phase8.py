import os

base_dir = r'c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus'

files = {
    'app/notifications/webhooks.py': '''import requests
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
''',
    'app/notifications/email.py': '''import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_alert_email(to_email, subject, html_content):
        """
        Sends an HTML email via SMTP.
        Configuration should be loaded from environment variables in production.
        """
        smtp_host = os.environ.get('SMTP_HOST', 'smtp.mailtrap.io')
        smtp_port = int(os.environ.get('SMTP_PORT', 2525))
        smtp_user = os.environ.get('SMTP_USER', 'mock_user')
        smtp_pass = os.environ.get('SMTP_PASS', 'mock_pass')
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = "alerts@dataflownexus.com"
        msg['To'] = to_email
        
        part = MIMEText(html_content, 'html')
        msg.attach(part)
        
        try:
            # Using a context manager for the SMTP connection
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                if smtp_user and smtp_pass:
                    server.login(smtp_user, smtp_pass)
                server.sendmail(msg['From'], [msg['To']], msg.as_string())
                
            logger.info(f"Alert email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
''',
    'app/api_management/rate_limiter.py': '''from functools import wraps
from flask import request, jsonify
import redis
import logging
from app.config.settings import config

logger = logging.getLogger(__name__)
redis_client = redis.from_url(config['default'].REDIS_URL)

def rate_limit(limit=100, window=60):
    """
    Redis-based Fixed-Window Rate Limiter Decorator.
    limit: Maximum number of requests allowed.
    window: Timeframe in seconds.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Identify the client by API Key or IP address
            api_key = request.headers.get('X-API-Key')
            identifier = api_key if api_key else request.remote_addr
            
            redis_key = f"rate_limit:{identifier}"
            
            try:
                # Atomically increment the request count
                current = redis_client.incr(redis_key)
                
                # If this is the first request in the window, set the expiration
                if current == 1:
                    redis_client.expire(redis_key, window)
                    
                if current > limit:
                    logger.warning(f"Rate limit exceeded for {identifier}")
                    return jsonify({
                        "error": "Too Many Requests",
                        "message": f"Rate limit of {limit} requests per {window}s exceeded."
                    }), 429
                    
            except redis.RedisError as e:
                # Fail open if Redis is down to prevent blocking valid traffic
                logger.error(f"Redis error in rate limiter: {e}")
                
            return fn(*args, **kwargs)
        return wrapper
    return decorator
''',
    'tests/test_rate_limiter.py': '''import pytest
from app.api_management.rate_limiter import rate_limit
from flask import Flask
from unittest.mock import patch, MagicMock

app = Flask(__name__)

@app.route('/test')
@rate_limit(limit=2, window=60)
def dummy_route():
    return "OK", 200

@patch('app.api_management.rate_limiter.redis_client')
def test_rate_limiter_allows_under_limit(mock_redis, client):
    # Mock redis returning 1 (first request)
    mock_redis.incr.return_value = 1
    
    response = client.get('/test', headers={'X-API-Key': 'valid_key'})
    assert response.status_code == 200
    mock_redis.expire.assert_called_with('rate_limit:valid_key', 60)

@patch('app.api_management.rate_limiter.redis_client')
def test_rate_limiter_blocks_over_limit(mock_redis, client):
    # Mock redis returning 3 (over the limit of 2)
    mock_redis.incr.return_value = 3
    
    response = client.get('/test', headers={'X-API-Key': 'spam_key'})
    assert response.status_code == 429
    assert b"Too Many Requests" in response.data
'''
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Phase 8 Deep Dive components generated successfully.')
