from app.transformations.advanced_engine import StringTransformation, DateTransformation, MathTransformation

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
