import re
import logging

logger = logging.getLogger(__name__)

class PIIClassifier:
    """
    Scans data payloads and classifies columns containing sensitive information (PII).
    In a massive enterprise setting, this could wrap a HuggingFace transformers pipeline (e.g., Presidio).
    """
    RULES = {
        'PII_EMAIL': re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$'),
        'PII_SSN': re.compile(r'^\d{3}-\d{2}-\d{4}$'),
        'PII_CREDIT_CARD': re.compile(r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})$'),
        'PII_PHONE': re.compile(r'^\+?1?\d{9,15}$')
    }

    @classmethod
    def classify_column(cls, column_data):
        """
        Analyzes a sample of column data and returns a confidence score for PII types.
        """
        scores = {key: 0 for key in cls.RULES.keys()}
        total_samples = len(column_data)
        
        if total_samples == 0:
            return None
            
        for value in column_data:
            str_val = str(value)
            for pii_type, regex in cls.RULES.items():
                if regex.match(str_val):
                    scores[pii_type] += 1
                    
        # Calculate percentages
        confidence = {k: (v / total_samples) for k, v in scores.items() if v > 0}
        
        # If > 50% of the data matches a PII rule, classify the entire column as that PII type
        detected_tags = [k for k, v in confidence.items() if v > 0.5]
        return detected_tags
