from app.extensions import db
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
