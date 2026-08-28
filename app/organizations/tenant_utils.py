from flask import abort
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
