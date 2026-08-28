import os

base_dir = r'c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus'

files = {
    'app/data_quality/advanced_validators.py': '''import re
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
''',
    'app/transformations/advanced_engine.py': '''from app.transformations.engine import BaseTransformation
from datetime import datetime

class StringTransformation(BaseTransformation):
    """
    Applies string operations like upper, lower, or trim to a field.
    """
    def apply(self, data):
        field = self.config.get('field')
        operation = self.config.get('operation', 'trim') # upper, lower, trim
        
        if field in data and isinstance(data[field], str):
            if operation == 'upper':
                data[field] = data[field].upper()
            elif operation == 'lower':
                data[field] = data[field].lower()
            elif operation == 'trim':
                data[field] = data[field].strip()
        return data

class DateTransformation(BaseTransformation):
    """
    Converts date strings from one format to another.
    """
    def apply(self, data):
        field = self.config.get('field')
        input_format = self.config.get('input_format', '%Y-%m-%d')
        output_format = self.config.get('output_format', '%Y-%m-%dT%H:%M:%SZ')
        
        if field in data and isinstance(data[field], str):
            try:
                parsed_date = datetime.strptime(data[field], input_format)
                data[field] = parsed_date.strftime(output_format)
            except ValueError:
                pass # Fail silently or push to DLQ in a real pipeline
        return data

class MathTransformation(BaseTransformation):
    """
    Applies basic math operations to a numeric field.
    """
    def apply(self, data):
        field = self.config.get('field')
        operation = self.config.get('operation', 'multiply')
        operand = self.config.get('operand', 1)
        
        if field in data and isinstance(data[field], (int, float)):
            if operation == 'multiply':
                data[field] = data[field] * operand
            elif operation == 'add':
                data[field] = data[field] + operand
            elif operation == 'round':
                data[field] = round(data[field], int(operand))
        return data
''',
    'tests/test_data_quality.py': '''import pytest
from app.data_quality.advanced_validators import RegexValidator, RangeValidator

def test_regex_validator():
    validator = RegexValidator({'field': 'email', 'pattern': r'^[\w\.-]+@[\w\.-]+\.\w+$'})
    
    # Valid
    is_valid, err = validator.validate({'email': 'test@example.com'})
    assert is_valid
    
    # Invalid
    is_valid, err = validator.validate({'email': 'invalid-email'})
    assert not is_valid
    assert "failed regex match" in err

def test_range_validator():
    validator = RangeValidator({'field': 'age', 'min': 18, 'max': 65})
    
    # Valid
    assert validator.validate({'age': 30})[0] == True
    
    # Too young
    assert validator.validate({'age': 16})[0] == False
    
    # Too old
    assert validator.validate({'age': 70})[0] == False
    
    # Invalid type
    assert validator.validate({'age': 'thirty'})[0] == False
''',
    'tests/test_transformations.py': '''from app.transformations.advanced_engine import StringTransformation, DateTransformation, MathTransformation

def test_string_transformation():
    transformer = StringTransformation({'field': 'name', 'operation': 'upper'})
    result = transformer.apply({'name': 'john doe', 'age': 30})
    assert result['name'] == 'JOHN DOE'

def test_date_transformation():
    transformer = DateTransformation({
        'field': 'created_at',
        'input_format': '%Y-%m-%d',
        'output_format': '%d/%m/%Y'
    })
    result = transformer.apply({'created_at': '2026-08-28'})
    assert result['created_at'] == '28/08/2026'

def test_math_transformation():
    transformer = MathTransformation({'field': 'price', 'operation': 'multiply', 'operand': 1.2})
    result = transformer.apply({'price': 100})
    assert result['price'] == 120.0
'''
}

# Add jsonschema to requirements
requirements_path = os.path.join(base_dir, 'requirements.txt')
if os.path.exists(requirements_path):
    with open(requirements_path, 'a', encoding='utf-8') as req_file:
        req_file.write("jsonschema==4.20.0\n")

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Phase 6 Deep Dive components generated successfully.')
