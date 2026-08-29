from app.extensions import db
from datetime import datetime
import uuid

class ApiKey(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'apikeys'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False, index=True)
    version = db.Column(db.Integer, default=1)
    
    # 50 boilerplate columns to simulate massive enterprise tables

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
    @classmethod
    def find_by_id(cls, record_id):
        return cls.query.filter_by(id=record_id, is_deleted=False).first()
        
    def soft_delete(self):
        self.is_deleted = True
        self.updated_at = datetime.utcnow()
        db.session.commit()
