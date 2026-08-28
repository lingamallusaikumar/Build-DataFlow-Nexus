import redis
import json
import logging
from app.config.settings import config

logger = logging.getLogger(__name__)

class ExecutionStateManager:
    """
    Manages the real-time state of pipeline executions in Redis.
    Allows for high-throughput tracking without hammering the PostgreSQL DB.
    """
    def __init__(self, redis_url=None):
        url = redis_url or config['default'].REDIS_URL
        self.redis_client = redis.from_url(url)

    def set_execution_status(self, execution_id, status):
        key = f"execution:{execution_id}:status"
        self.redis_client.set(key, status)
        
    def get_execution_status(self, execution_id):
        key = f"execution:{execution_id}:status"
        status = self.redis_client.get(key)
        return status.decode('utf-8') if status else 'unknown'

    def log_node_start(self, execution_id, node_id):
        key = f"execution:{execution_id}:nodes"
        self.redis_client.hset(key, node_id, json.dumps({'status': 'running', 'records_processed': 0}))

    def log_node_complete(self, execution_id, node_id, records_processed, error=None):
        key = f"execution:{execution_id}:nodes"
        state = {
            'status': 'failed' if error else 'success',
            'records_processed': records_processed,
            'error': str(error) if error else None
        }
        self.redis_client.hset(key, node_id, json.dumps(state))
