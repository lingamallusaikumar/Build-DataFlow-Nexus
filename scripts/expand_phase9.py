import os

base_dir = r'c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus'

files = {
    'app/ai/data_classifier.py': '''import re
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
''',
    'app/ai/predictive_maintenance.py': '''import logging

logger = logging.getLogger(__name__)

class PredictiveFailureModel:
    """
    Simulated Machine Learning model to predict pipeline failure probabilities.
    In production, this would load an ONNX/Pickle model trained via Scikit-Learn or TensorFlow.
    """
    def __init__(self, recent_error_rate, cpu_spike_count, memory_saturation, latency_trend):
        self.features = {
            'recent_error_rate': recent_error_rate,   # e.g., 0.05 (5% of records failed recently)
            'cpu_spike_count': cpu_spike_count,       # e.g., 3 spikes above 90% in last hour
            'memory_saturation': memory_saturation,   # e.g., 0.85 (85% memory used)
            'latency_trend': latency_trend            # e.g., 1.5 (execution taking 1.5x longer than baseline)
        }

    def predict_failure_probability(self):
        """
        Calculates a heuristic-based probability of failure in the next 1 hour.
        Returns a float between 0.0 and 1.0.
        """
        risk_score = 0.0
        
        # Heuristic weights (acting as linear regression coefficients)
        risk_score += self.features['recent_error_rate'] * 5.0
        risk_score += (self.features['cpu_spike_count'] / 10.0)
        
        if self.features['memory_saturation'] > 0.8:
            risk_score += (self.features['memory_saturation'] - 0.8) * 2.0
            
        if self.features['latency_trend'] > 1.2:
            risk_score += (self.features['latency_trend'] - 1.2) * 0.5
            
        # Sigmoid activation to squash between 0 and 1
        probability = min(max(risk_score, 0.0), 1.0)
        
        if probability > 0.7:
            logger.warning(f"HIGH PIPELINE FAILURE RISK DETECTED: {probability*100:.1f}%")
            
        return probability
''',
    'tests/test_ai_ml.py': '''import pytest
from app.ai.data_classifier import PIIClassifier
from app.ai.predictive_maintenance import PredictiveFailureModel

def test_pii_email_classifier():
    data = ["user@example.com", "admin@test.org", "not_an_email", "another@domain.com"]
    tags = PIIClassifier.classify_column(data)
    assert "PII_EMAIL" in tags
    assert "PII_SSN" not in tags

def test_pii_credit_card_classifier():
    data = ["4111111111111111", "5123456789012345", "not_a_cc"]
    tags = PIIClassifier.classify_column(data)
    assert "PII_CREDIT_CARD" in tags

def test_predictive_failure_low_risk():
    model = PredictiveFailureModel(
        recent_error_rate=0.01,
        cpu_spike_count=0,
        memory_saturation=0.5,
        latency_trend=1.0
    )
    prob = model.predict_failure_probability()
    assert prob < 0.3 # Low risk

def test_predictive_failure_high_risk():
    model = PredictiveFailureModel(
        recent_error_rate=0.10, # 10% errors
        cpu_spike_count=5,      # 5 CPU spikes
        memory_saturation=0.9,  # 90% memory
        latency_trend=2.0       # 2x slower
    )
    prob = model.predict_failure_probability()
    assert prob > 0.7 # High risk
'''
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Phase 9 Deep Dive components generated successfully.')
