from app.extensions import db
from app.organizations.models import Organization, OrganizationMember
from sqlalchemy.exc import IntegrityError

class OrganizationService:
    @staticmethod
    def create_organization(name, slug, user_id):
        try:
            org = Organization(name=name, slug=slug)
            db.session.add(org)
            db.session.flush() # Get ID without committing

            member = OrganizationMember(org_id=org.id, user_id=user_id, role='owner')
            db.session.add(member)
            db.session.commit()
            return org, None
        except IntegrityError:
            db.session.rollback()
            return None, "Organization slug already exists."

    @staticmethod
    def get_user_organizations(user_id):
        memberships = OrganizationMember.query.filter_by(user_id=user_id).all()
        return [Organization.query.get(m.org_id) for m in memberships]
