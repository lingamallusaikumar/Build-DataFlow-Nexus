from typing import Dict, Any, List

class SchemaChecker:
    def __init__(self, expected_schema: Dict[str, type]):
        self.expected_schema = expected_schema

    def validate_record(self, record: Dict[str, Any]) -> List[str]:
        """Validates a single record against the expected schema, returning error messages if any."""
        errors = []
        for field, expected_type in self.expected_schema.items():
            if field not in record:
                errors.append(f"Missing required field: '{field}'")
            elif not isinstance(record[field], expected_type):
                errors.append(f"Invalid type for '{field}': expected {expected_type.__name__}, got {type(record[field]).__name__}")
        return errors

    def is_valid(self, record: Dict[str, Any]) -> bool:
        return len(self.validate_record(record)) == 0
