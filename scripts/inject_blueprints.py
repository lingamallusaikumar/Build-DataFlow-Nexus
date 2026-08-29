import os

init_path = 'app/__init__.py'
with open(init_path, 'r') as f:
    content = f.read()

# Register the 44 new blueprints dynamically inside create_app
tables = [
    'Tenant', 'Organization', 'User', 'Role', 'Permission', 'UserRole', 'RolePermission',
    'AuditLog', 'Session', 'ApiKey', 'BillingPlan', 'Subscription', 'Invoice', 'Payment',
    'Pipeline', 'PipelineVersion', 'DagNode', 'DagEdge', 'PipelineRun', 'TaskRun', 
    'TaskLog', 'Connector', 'ConnectionCredentials', 'Dataset', 'DataSchema', 'SchemaColumn',
    'QualityRule', 'QualityExecution', 'NotificationConfig', 'Webhook', 'WebhookDelivery',
    'DeadLetterQueue', 'DataLineage', 'DataCatalog', 'Tag', 'ResourceTag', 'Setting',
    'FeatureFlag', 'Quota', 'QuotaUsage', 'Metric', 'Alert', 'AlertHistory', 'SavedQuery'
]

blueprint_registrations = "\n    # Dynamic Enterprise Blueprint Registrations\n"
for table in tables:
    blueprint_registrations += f"    from app.domain_routes.{table.lower()}_routes import {table.lower()}_bp\n"
    blueprint_registrations += f"    app.register_blueprint({table.lower()}_bp)\n"

# Inject before the return app statement
if '# Dynamic Enterprise Blueprint Registrations' not in content:
    content = content.replace('return app', blueprint_registrations + '\n    return app')
    with open(init_path, 'w') as f:
        f.write(content)
        print("Injected 44 blueprints into app/__init__.py")
else:
    print("Blueprints already injected.")
