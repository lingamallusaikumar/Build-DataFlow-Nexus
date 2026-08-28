import pytest
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
