from collections import defaultdict, deque
import logging

logger = logging.getLogger(__name__)

class DAGParser:
    """
    Parses visual pipeline configurations (nodes and edges) into an executable Directed Acyclic Graph.
    """
    def __init__(self, config):
        self.nodes = config.get('nodes', [])
        self.edges = config.get('edges', [])
        self.adj_list = defaultdict(list)
        self.in_degree = defaultdict(int)
        
        self._build_graph()

    def _build_graph(self):
        # Initialize in-degrees for all nodes
        for node in self.nodes:
            self.in_degree[node['id']] = 0
            
        # Build adjacency list and populate in-degrees
        for edge in self.edges:
            source = edge['source']
            target = edge['target']
            self.adj_list[source].append(target)
            self.in_degree[target] += 1

    def topological_sort(self):
        """
        Returns the nodes in execution order. Raises ValueError if a cycle is detected.
        """
        queue = deque([node_id for node_id, degree in self.in_degree.items() if degree == 0])
        execution_order = []
        
        while queue:
            current = queue.popleft()
            execution_order.append(current)
            
            for neighbor in self.adj_list[current]:
                self.in_degree[neighbor] -= 1
                if self.in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        if len(execution_order) != len(self.nodes):
            logger.error("Cycle detected in pipeline DAG.")
            raise ValueError("Pipeline contains a cycle and cannot be executed.")
            
        return execution_order
