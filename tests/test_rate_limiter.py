import pytest
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
