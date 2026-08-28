import os

base_dir = r'c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus'

files = {
    'app/executor/state_manager.py': '''import redis
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
''',
    'app/executor/dlq_manager.py': '''from app.extensions import db
from app.models.base import BaseModel

class DeadLetterRecord(BaseModel):
    __tablename__ = 'dead_letter_records'
    
    execution_id = db.Column(db.String(36), nullable=False, index=True)
    pipeline_id = db.Column(db.String(36), nullable=False)
    node_id = db.Column(db.String(36), nullable=False)
    payload = db.Column(db.JSON, nullable=False)
    error_reason = db.Column(db.Text, nullable=False)

class DLQManager:
    """
    Handles capturing records that fail processing, preventing them from crashing the entire batch.
    """
    @staticmethod
    def push_to_dlq(execution_id, pipeline_id, node_id, payload, reason):
        dlq_record = DeadLetterRecord(
            execution_id=execution_id,
            pipeline_id=pipeline_id,
            node_id=node_id,
            payload=payload,
            error_reason=reason
        )
        db.session.add(dlq_record)
        db.session.commit()
''',
    'app/executor/dag_executor.py': '''import logging
from app.executor.state_manager import ExecutionStateManager
from app.executor.dlq_manager import DLQManager

logger = logging.getLogger(__name__)

class DAGExecutor:
    """
    Orchestrates the execution of a topological node array.
    """
    def __init__(self, execution_id, pipeline_id, nodes, topological_order):
        self.execution_id = execution_id
        self.pipeline_id = pipeline_id
        self.nodes = {n['id']: n for n in nodes}
        self.topological_order = topological_order
        self.state_manager = ExecutionStateManager()

    def execute(self):
        self.state_manager.set_execution_status(self.execution_id, 'running')
        
        # Memory buffer to hold intermediate dataframes/payloads between nodes
        data_buffer = {}
        
        try:
            for node_id in self.topological_order:
                node_config = self.nodes[node_id]
                self.state_manager.log_node_start(self.execution_id, node_id)
                
                logger.info(f"Executing node {node_id} (Type: {node_config.get('type')})")
                
                # Mock Processing Logic
                processed_count = 0
                error = None
                try:
                    if node_config.get('type') == 'Source':
                        data_buffer[node_id] = [{"mock_data": 1}, {"mock_data": 2}]
                        processed_count = 2
                    elif node_config.get('type') == 'Transform':
                        # Example of a record failing and going to DLQ
                        DLQManager.push_to_dlq(self.execution_id, self.pipeline_id, node_id, {"mock_data": -1}, "Negative value not allowed")
                        processed_count = 1
                    elif node_config.get('type') == 'Destination':
                        processed_count = len(data_buffer.get(node_id, []))
                except Exception as e:
                    error = e
                    logger.error(f"Node {node_id} failed: {e}")
                    raise
                    
                self.state_manager.log_node_complete(self.execution_id, node_id, processed_count, error)
                
            self.state_manager.set_execution_status(self.execution_id, 'success')
        except Exception as e:
            self.state_manager.set_execution_status(self.execution_id, 'failed')
            raise e
''',
    'tests/test_executor.py': '''import pytest
from app.executor.state_manager import ExecutionStateManager
from unittest.mock import patch, MagicMock

@patch('redis.from_url')
def test_state_manager_status(mock_redis):
    mock_client = MagicMock()
    mock_redis.return_value = mock_client
    
    manager = ExecutionStateManager()
    manager.set_execution_status('exec_123', 'running')
    
    mock_client.set.assert_called_with('execution:exec_123:status', 'running')

@patch('redis.from_url')
def test_state_manager_node_logging(mock_redis):
    mock_client = MagicMock()
    mock_redis.return_value = mock_client
    
    manager = ExecutionStateManager()
    manager.log_node_start('exec_123', 'node_A')
    
    assert mock_client.hset.called
'''
}

# Ensure the app/executor directory contains __init__.py
files['app/executor/__init__.py'] = ''

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Phase 5 Deep Dive components generated successfully.')
