from functools import wraps
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
