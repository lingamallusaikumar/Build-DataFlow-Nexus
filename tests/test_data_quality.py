import pytest
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
