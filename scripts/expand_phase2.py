import os

base_dir = r'c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus'

files = {
    'app/organizations/invitation_models.py': '''from app.extensions import db
from app.models.base import BaseModel
from datetime import datetime, timedelta

class OrganizationInvitation(BaseModel):
    __tablename__ = 'organization_invitations'
    
    org_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    token = db.Column(db.String(64), unique=True, nullable=False, index=True)
    role = db.Column(db.String(50), nullable=False, default='developer')
    expires_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=7))
    is_accepted = db.Column(db.Boolean, default=False)
    
    organization = db.relationship('Organization')
''',
    'app/organizations/tenant_utils.py': '''from flask import abort
import logging

logger = logging.getLogger(__name__)

def get_tenant_resource_or_404(model, org_id, resource_id):
    """
    Enforces strict tenant isolation at the query level.
    Ensures that a requested resource explicitly belongs to the requesting organization.
    """
    resource = model.query.filter_by(id=resource_id, org_id=org_id).first()
    if not resource:
        logger.warning(f"Tenant isolation breach attempt or resource missing: org_id={org_id}, resource={model.__name__}, id={resource_id}")
        abort(404, description="Resource not found or access denied.")
    return resource
''',
    'app/organizations/invitation_services.py': '''from app.extensions import db
from app.organizations.invitation_models import OrganizationInvitation
from app.organizations.models import OrganizationMember
from app.auth.models import User
from app.auth.utils import generate_secure_token
from datetime import datetime

class InvitationService:
    @staticmethod
    def invite_user(org_id, email, role='developer'):
        # Check if already a member
        user = User.query.filter_by(email=email).first()
        if user:
            existing_member = OrganizationMember.query.filter_by(org_id=org_id, user_id=user.id).first()
            if existing_member:
                return None, "User is already a member of this organization."
                
        token = generate_secure_token(64)
        invitation = OrganizationInvitation(
            org_id=org_id,
            email=email,
            token=token,
            role=role
        )
        
        db.session.add(invitation)
        db.session.commit()
        
        # In a real app, integrate Celery task here to send the email:
        # send_invitation_email.delay(email, token)
        
        return invitation, None

    @staticmethod
    def accept_invitation(token, user_id):
        invitation = OrganizationInvitation.query.filter_by(token=token, is_accepted=False).first()
        
        if not invitation:
            return False, "Invalid or already accepted invitation token."
            
        if invitation.expires_at < datetime.utcnow():
            return False, "Invitation has expired."
            
        # Add user to organization
        member = OrganizationMember(
            org_id=invitation.org_id,
            user_id=user_id,
            role=invitation.role
        )
        
        invitation.is_accepted = True
        
        db.session.add(member)
        db.session.commit()
        return True, "Successfully joined the organization."
''',
    'tests/test_multi_tenancy.py': '''import pytest
from app.organizations.tenant_utils import get_tenant_resource_or_404
from werkzeug.exceptions import NotFound

# Mock models for testing
class MockResource:
    def __init__(self, id, org_id):
        self.id = id
        self.org_id = org_id
        
class MockQuery:
    def __init__(self, items):
        self.items = items
    def filter_by(self, id, org_id):
        result = [item for item in self.items if item.id == id and item.org_id == org_id]
        class ResultProxy:
            def first(self):
                return result[0] if result else None
        return ResultProxy()

class MockModel:
    __name__ = 'MockModel'
    query = MockQuery([MockResource("res_1", "org_1"), MockResource("res_2", "org_2")])

def test_tenant_isolation_success():
    resource = get_tenant_resource_or_404(MockModel, "org_1", "res_1")
    assert resource.id == "res_1"

def test_tenant_isolation_failure_wrong_org():
    with pytest.raises(NotFound):
        get_tenant_resource_or_404(MockModel, "org_1", "res_2") # res_2 belongs to org_2

def test_tenant_isolation_failure_missing_resource():
    with pytest.raises(NotFound):
        get_tenant_resource_or_404(MockModel, "org_1", "res_99")
'''
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Phase 2 Deep Dive components generated successfully.')
