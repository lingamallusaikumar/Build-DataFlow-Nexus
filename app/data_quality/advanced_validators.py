import re
from jsonschema import validate, ValidationError as JsonSchemaError
import logging

logger = logging.getLogger(__name__)

class RegexValidator:
    def __init__(self, config):
        self.field = config['field']
        self.pattern = re.compile(config['pattern'])

    def validate(self, record):
        val = record.get(self.field)
        if val is None or self.pattern.match(str(val)):
            return True, None
        return False, f"Field '{self.field}' failed regex match for pattern."

class RangeValidator:
    def __init__(self, config):
        self.field = config['field']
        self.min_val = config.get('min')
        self.max_val = config.get('max')

    def validate(self, record):
        val = record.get(self.field)
        if val is None:
            return True, None
        try:
            val = float(val)
            if self.min_val is not None and val < self.min_val:
                return False, f"Field '{self.field}' is below minimum {self.min_val}."
            if self.max_val is not None and val > self.max_val:
                return False, f"Field '{self.field}' is above maximum {self.max_val}."
            return True, None
        except ValueError:
            return False, f"Field '{self.field}' must be numeric for range validation."

class JsonSchemaValidator:
    def __init__(self, schema):
        self.schema = schema

    def validate(self, record):
        try:
            validate(instance=record, schema=self.schema)
            return True, None
        except JsonSchemaError as e:
            return False, f"Schema validation failed: {e.message}"
