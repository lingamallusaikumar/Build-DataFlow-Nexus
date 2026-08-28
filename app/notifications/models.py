from app.extensions import db
from app.models.base import BaseModel

class Notification(BaseModel):
    __tablename__ = 'notifications'
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False) # e.g., 'pipeline_success', 'pipeline_failure', 'alert'
    is_read = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
