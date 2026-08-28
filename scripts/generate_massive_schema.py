import os

models_dir = 'app/domain_models'
os.makedirs(models_dir, exist_ok=True)

# Generate a massive schema
tables = [
    'Tenant', 'Organization', 'User', 'Role', 'Permission', 'UserRole', 'RolePermission',
    'AuditLog', 'Session', 'ApiKey', 'BillingPlan', 'Subscription', 'Invoice', 'Payment',
    'Pipeline', 'PipelineVersion', 'DagNode', 'DagEdge', 'PipelineRun', 'TaskRun', 
    'TaskLog', 'Connector', 'ConnectionCredentials', 'Dataset', 'DataSchema', 'SchemaColumn',
    'QualityRule', 'QualityExecution', 'NotificationConfig', 'Webhook', 'WebhookDelivery',
    'DeadLetterQueue', 'DataLineage', 'DataCatalog', 'Tag', 'ResourceTag', 'Setting',
    'FeatureFlag', 'Quota', 'QuotaUsage', 'Metric', 'Alert', 'AlertHistory', 'SavedQuery'
]

base_template = '''from app.extensions import db
from datetime import datetime
import uuid

class {name}(db.Model):
    __tablename__ = '{table_name}'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False, index=True)
    version = db.Column(db.Integer, default=1)
    
    # 50 boilerplate columns to simulate massive enterprise tables
'''

for table in tables:
    content = base_template.format(name=table, table_name=table.lower() + 's')
    
    # Add massive amounts of columns to simulate real enterprise schemas
    for i in range(1, 51):
        content += f"    attribute_{i} = db.Column(db.String(255), nullable=True)\n"
    
    # Add boilerplate methods
    content += '''
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
    @classmethod
    def find_by_id(cls, record_id):
        return cls.query.filter_by(id=record_id, is_deleted=False).first()
        
    def soft_delete(self):
        self.is_deleted = True
        self.updated_at = datetime.utcnow()
        db.session.commit()
'''
    with open(f'{models_dir}/{table.lower()}.py', 'w') as f:
        f.write(content)

with open(f'{models_dir}/__init__.py', 'w') as f:
    for table in tables:
        f.write(f'from .{table.lower()} import {table}\\n')

print(f"Generated {len(tables)} massive enterprise domain models.")
