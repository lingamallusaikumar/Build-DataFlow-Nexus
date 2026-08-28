from app.extensions import db
from app.models.base import BaseModel

class Connector(BaseModel):
    __tablename__ = 'connectors'
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False) # e.g., postgres, rest_api, mongodb
    org_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=False)
    config = db.Column(db.JSON, nullable=False) # Credentials/Host configs (encrypted in real scenario)
    is_active = db.Column(db.Boolean, default=True)
