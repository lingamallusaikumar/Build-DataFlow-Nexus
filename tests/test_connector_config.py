import pytest
from app.data_quality.schema_checker import SchemaChecker

def test_schema_checker_valid_record():
    schema = {"id": int, "name": str, "active": bool}
    checker = SchemaChecker(schema)
    valid_record = {"id": 101, "name": "ETL Pipeline A", "active": True}
    assert checker.is_valid(valid_record) is True
    assert len(checker.validate_record(valid_record)) == 0

def test_schema_checker_missing_field():
    schema = {"id": int, "name": str}
    checker = SchemaChecker(schema)
    invalid_record = {"id": 102}
    assert checker.is_valid(invalid_record) is False
    errors = checker.validate_record(invalid_record)
    assert "Missing required field: 'name'" in errors[0]
