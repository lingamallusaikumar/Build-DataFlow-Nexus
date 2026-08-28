class DataValidator:
    def __init__(self, rules):
        self.rules = rules

    def validate_record(self, record):
        errors = []
        for field, rule in self.rules.items():
            value = record.get(field)
            if rule.get('required') and value is None:
                errors.append(f"{field} is required.")
            if rule.get('type') and value is not None:
                if type(value).__name__ != rule['type']:
                    errors.append(f"{field} must be of type {rule['type']}.")
        
        return len(errors) == 0, errors
