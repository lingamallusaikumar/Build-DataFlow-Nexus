import os

base_dir = r'c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus'

files = {
    'app/pipelines/dag_parser.py': '''from collections import defaultdict, deque
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
''',
    'app/pipelines/validator.py': '''from app.pipelines.dag_parser import DAGParser

class PipelineValidator:
    """
    Validates a pipeline configuration before saving or executing.
    """
    @staticmethod
    def validate_config(config):
        errors = []
        
        if not config.get('nodes'):
            errors.append("Pipeline must contain at least one node.")
            return False, errors
            
        try:
            parser = DAGParser(config)
            order = parser.topological_sort()
            
            # Check for disconnected nodes (nodes with 0 in-degree and 0 out-degree, unless it's the only node)
            if len(parser.nodes) > 1:
                for node in parser.nodes:
                    nid = node['id']
                    if parser.in_degree[nid] == 0 and len(parser.adj_list[nid]) == 0:
                        errors.append(f"Node {nid} is disconnected from the pipeline.")
                        
        except ValueError as e:
            errors.append(str(e))
            
        return len(errors) == 0, errors
''',
    'app/pipelines/versioning.py': '''from app.extensions import db
from app.models.base import BaseModel

class PipelineVersion(BaseModel):
    __tablename__ = 'pipeline_versions'
    
    pipeline_id = db.Column(db.String(36), db.ForeignKey('pipelines.id'), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    configuration = db.Column(db.JSON, nullable=False)
    commit_message = db.Column(db.String(255), nullable=True)
    
    pipeline = db.relationship('Pipeline', backref=db.backref('versions', lazy='dynamic', cascade='all, delete-orphan'))
''',
    'tests/test_dag.py': '''import pytest
from app.pipelines.dag_parser import DAGParser
from app.pipelines.validator import PipelineValidator

def test_dag_topological_sort_success():
    config = {
        "nodes": [{"id": "A"}, {"id": "B"}, {"id": "C"}],
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "B", "target": "C"}
        ]
    }
    parser = DAGParser(config)
    order = parser.topological_sort()
    assert order == ["A", "B", "C"]

def test_dag_cycle_detection():
    config = {
        "nodes": [{"id": "A"}, {"id": "B"}, {"id": "C"}],
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "B", "target": "C"},
            {"source": "C", "target": "A"} # Cycle
        ]
    }
    parser = DAGParser(config)
    with pytest.raises(ValueError, match="contains a cycle"):
        parser.topological_sort()

def test_pipeline_validator_disconnected():
    config = {
        "nodes": [{"id": "A"}, {"id": "B"}, {"id": "C"}], # C is disconnected
        "edges": [
            {"source": "A", "target": "B"}
        ]
    }
    is_valid, errors = PipelineValidator.validate_config(config)
    assert not is_valid
    assert any("disconnected" in err for err in errors)
'''
}

# Update models/__init__.py or app/pipelines/models.py to import PipelineVersion so alembic sees it
models_path = os.path.join(base_dir, 'app/pipelines/models.py')
if os.path.exists(models_path):
    with open(models_path, 'a', encoding='utf-8') as f:
        f.write("\n# Import for alembic migrations\nfrom app.pipelines.versioning import PipelineVersion\n")

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Phase 4 Deep Dive components generated successfully.')
