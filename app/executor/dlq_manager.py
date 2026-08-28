from app.extensions import db
from app.models.base import BaseModel

class DeadLetterRecord(BaseModel):
    __tablename__ = 'dead_letter_records'
    
    execution_id = db.Column(db.String(36), nullable=False, index=True)
    pipeline_id = db.Column(db.String(36), nullable=False)
    node_id = db.Column(db.String(36), nullable=False)
    payload = db.Column(db.JSON, nullable=False)
    error_reason = db.Column(db.Text, nullable=False)

class DLQManager:
    """
    Handles capturing records that fail processing, preventing them from crashing the entire batch.
    """
    @staticmethod
    def push_to_dlq(execution_id, pipeline_id, node_id, payload, reason):
        dlq_record = DeadLetterRecord(
            execution_id=execution_id,
            pipeline_id=pipeline_id,
            node_id=node_id,
            payload=payload,
            error_reason=reason
        )
        db.session.add(dlq_record)
        db.session.commit()
