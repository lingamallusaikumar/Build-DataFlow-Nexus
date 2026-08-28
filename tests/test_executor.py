import pytest
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
