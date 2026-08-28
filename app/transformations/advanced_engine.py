from app.transformations.engine import BaseTransformation
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
