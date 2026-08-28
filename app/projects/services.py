from app.extensions import db
from app.projects.models import Project

class ProjectService:
    @staticmethod
    def create_project(name, description, workspace_id):
        project = Project(name=name, description=description, workspace_id=workspace_id)
        db.session.add(project)
        db.session.commit()
        return project
