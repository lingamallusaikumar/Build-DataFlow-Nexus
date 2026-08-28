import pytest
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
