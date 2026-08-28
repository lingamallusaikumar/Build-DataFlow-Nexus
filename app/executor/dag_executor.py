import logging
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
