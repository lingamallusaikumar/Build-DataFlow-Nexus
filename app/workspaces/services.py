from app.extensions import db
from app.workspaces.models import Workspace

class WorkspaceService:
    @staticmethod
    def create_workspace(name, org_id):
        workspace = Workspace(name=name, org_id=org_id)
        db.session.add(workspace)
        db.session.commit()
        return workspace

    @staticmethod
    def get_workspaces_by_org(org_id):
        return Workspace.query.filter_by(org_id=org_id).all()
