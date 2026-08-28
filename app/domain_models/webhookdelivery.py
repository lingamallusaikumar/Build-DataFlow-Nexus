from app.extensions import db
from datetime import datetime
import uuid

class WebhookDelivery(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'webhookdeliverys'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False, index=True)
    version = db.Column(db.Integer, default=1)
    
    # 50 boilerplate columns to simulate massive enterprise tables
    attribute_1 = db.Column(db.String(255), nullable=True)
    attribute_2 = db.Column(db.String(255), nullable=True)
    attribute_3 = db.Column(db.String(255), nullable=True)
    attribute_4 = db.Column(db.String(255), nullable=True)
    attribute_5 = db.Column(db.String(255), nullable=True)
    attribute_6 = db.Column(db.String(255), nullable=True)
    attribute_7 = db.Column(db.String(255), nullable=True)
    attribute_8 = db.Column(db.String(255), nullable=True)
    attribute_9 = db.Column(db.String(255), nullable=True)
    attribute_10 = db.Column(db.String(255), nullable=True)
    attribute_11 = db.Column(db.String(255), nullable=True)
    attribute_12 = db.Column(db.String(255), nullable=True)
    attribute_13 = db.Column(db.String(255), nullable=True)
    attribute_14 = db.Column(db.String(255), nullable=True)
    attribute_15 = db.Column(db.String(255), nullable=True)
    attribute_16 = db.Column(db.String(255), nullable=True)
    attribute_17 = db.Column(db.String(255), nullable=True)
    attribute_18 = db.Column(db.String(255), nullable=True)
    attribute_19 = db.Column(db.String(255), nullable=True)
    attribute_20 = db.Column(db.String(255), nullable=True)
    attribute_21 = db.Column(db.String(255), nullable=True)
    attribute_22 = db.Column(db.String(255), nullable=True)
    attribute_23 = db.Column(db.String(255), nullable=True)
    attribute_24 = db.Column(db.String(255), nullable=True)
    attribute_25 = db.Column(db.String(255), nullable=True)
    attribute_26 = db.Column(db.String(255), nullable=True)
    attribute_27 = db.Column(db.String(255), nullable=True)
    attribute_28 = db.Column(db.String(255), nullable=True)
    attribute_29 = db.Column(db.String(255), nullable=True)
    attribute_30 = db.Column(db.String(255), nullable=True)
    attribute_31 = db.Column(db.String(255), nullable=True)
    attribute_32 = db.Column(db.String(255), nullable=True)
    attribute_33 = db.Column(db.String(255), nullable=True)
    attribute_34 = db.Column(db.String(255), nullable=True)
    attribute_35 = db.Column(db.String(255), nullable=True)
    attribute_36 = db.Column(db.String(255), nullable=True)
    attribute_37 = db.Column(db.String(255), nullable=True)
    attribute_38 = db.Column(db.String(255), nullable=True)
    attribute_39 = db.Column(db.String(255), nullable=True)
    attribute_40 = db.Column(db.String(255), nullable=True)
    attribute_41 = db.Column(db.String(255), nullable=True)
    attribute_42 = db.Column(db.String(255), nullable=True)
    attribute_43 = db.Column(db.String(255), nullable=True)
    attribute_44 = db.Column(db.String(255), nullable=True)
    attribute_45 = db.Column(db.String(255), nullable=True)
    attribute_46 = db.Column(db.String(255), nullable=True)
    attribute_47 = db.Column(db.String(255), nullable=True)
    attribute_48 = db.Column(db.String(255), nullable=True)
    attribute_49 = db.Column(db.String(255), nullable=True)
    attribute_50 = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
    @classmethod
    def find_by_id(cls, record_id):
        return cls.query.filter_by(id=record_id, is_deleted=False).first()
        
    def soft_delete(self):
        self.is_deleted = True
        self.updated_at = datetime.utcnow()
        db.session.commit()
