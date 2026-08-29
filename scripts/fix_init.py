import os

tables = [
    'Tenant', 'Organization', 'User', 'Role', 'Permission', 'UserRole', 'RolePermission',
    'AuditLog', 'Session', 'ApiKey', 'BillingPlan', 'Subscription', 'Invoice', 'Payment',
    'Pipeline', 'PipelineVersion', 'DagNode', 'DagEdge', 'PipelineRun', 'TaskRun', 
    'TaskLog', 'Connector', 'ConnectionCredentials', 'Dataset', 'DataSchema', 'SchemaColumn',
    'QualityRule', 'QualityExecution', 'NotificationConfig', 'Webhook', 'WebhookDelivery',
    'DeadLetterQueue', 'DataLineage', 'DataCatalog', 'Tag', 'ResourceTag', 'Setting',
    'FeatureFlag', 'Quota', 'QuotaUsage', 'Metric', 'Alert', 'AlertHistory', 'SavedQuery'
]

with open('app/domain_models/__init__.py', 'w') as f:
    for table in tables:
        f.write(f'from .{table.lower()} import {table}\n')
