from flask import Flask
from app.config.settings import config
from app.extensions import db, migrate, jwt, socketio, celery_app

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Configure celery
    celery_app.conf.update(app.config)

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    socketio.init_app(app)

    # Register Blueprints
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    
    from app.organizations.routes import org_bp
    app.register_blueprint(org_bp, url_prefix='/api/v1/organizations')

    from app.frontend_routes import frontend_bp
    app.register_blueprint(frontend_bp)

    from app.admin.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')

    from app.admin.health import health_bp
    app.register_blueprint(health_bp, url_prefix='/health')
    
    from app.common.error_handlers import register_error_handlers
    register_error_handlers(app)

    @app.route('/health_check')
    def health_check():
        return {'status': 'ok', 'message': 'DataFlow Nexus API is running'}

    # Import socket events
    #import app.monitoring.sockets

    
    # Dynamic Enterprise Blueprint Registrations
    from app.domain_routes.tenant_routes import tenant_bp
    app.register_blueprint(tenant_bp)
    from app.domain_routes.organization_routes import organization_bp
    app.register_blueprint(organization_bp)
    from app.domain_routes.user_routes import user_bp
    app.register_blueprint(user_bp)
    from app.domain_routes.role_routes import role_bp
    app.register_blueprint(role_bp)
    from app.domain_routes.permission_routes import permission_bp
    app.register_blueprint(permission_bp)
    from app.domain_routes.userrole_routes import userrole_bp
    app.register_blueprint(userrole_bp)
    from app.domain_routes.rolepermission_routes import rolepermission_bp
    app.register_blueprint(rolepermission_bp)
    from app.domain_routes.auditlog_routes import auditlog_bp
    app.register_blueprint(auditlog_bp)
    from app.domain_routes.session_routes import session_bp
    app.register_blueprint(session_bp)
    from app.domain_routes.apikey_routes import apikey_bp
    app.register_blueprint(apikey_bp)
    from app.domain_routes.billingplan_routes import billingplan_bp
    app.register_blueprint(billingplan_bp)
    from app.domain_routes.subscription_routes import subscription_bp
    app.register_blueprint(subscription_bp)
    from app.domain_routes.invoice_routes import invoice_bp
    app.register_blueprint(invoice_bp)
    from app.domain_routes.payment_routes import payment_bp
    app.register_blueprint(payment_bp)
    from app.domain_routes.pipeline_routes import pipeline_bp
    app.register_blueprint(pipeline_bp)
    from app.domain_routes.pipelineversion_routes import pipelineversion_bp
    app.register_blueprint(pipelineversion_bp)
    from app.domain_routes.dagnode_routes import dagnode_bp
    app.register_blueprint(dagnode_bp)
    from app.domain_routes.dagedge_routes import dagedge_bp
    app.register_blueprint(dagedge_bp)
    from app.domain_routes.pipelinerun_routes import pipelinerun_bp
    app.register_blueprint(pipelinerun_bp)
    from app.domain_routes.taskrun_routes import taskrun_bp
    app.register_blueprint(taskrun_bp)
    from app.domain_routes.tasklog_routes import tasklog_bp
    app.register_blueprint(tasklog_bp)
    from app.domain_routes.connector_routes import connector_bp
    app.register_blueprint(connector_bp)
    from app.domain_routes.connectioncredentials_routes import connectioncredentials_bp
    app.register_blueprint(connectioncredentials_bp)
    from app.domain_routes.dataset_routes import dataset_bp
    app.register_blueprint(dataset_bp)
    from app.domain_routes.dataschema_routes import dataschema_bp
    app.register_blueprint(dataschema_bp)
    from app.domain_routes.schemacolumn_routes import schemacolumn_bp
    app.register_blueprint(schemacolumn_bp)
    from app.domain_routes.qualityrule_routes import qualityrule_bp
    app.register_blueprint(qualityrule_bp)
    from app.domain_routes.qualityexecution_routes import qualityexecution_bp
    app.register_blueprint(qualityexecution_bp)
    from app.domain_routes.notificationconfig_routes import notificationconfig_bp
    app.register_blueprint(notificationconfig_bp)
    from app.domain_routes.webhook_routes import webhook_bp
    app.register_blueprint(webhook_bp)
    from app.domain_routes.webhookdelivery_routes import webhookdelivery_bp
    app.register_blueprint(webhookdelivery_bp)
    from app.domain_routes.deadletterqueue_routes import deadletterqueue_bp
    app.register_blueprint(deadletterqueue_bp)
    from app.domain_routes.datalineage_routes import datalineage_bp
    app.register_blueprint(datalineage_bp)
    from app.domain_routes.datacatalog_routes import datacatalog_bp
    app.register_blueprint(datacatalog_bp)
    from app.domain_routes.tag_routes import tag_bp
    app.register_blueprint(tag_bp)
    from app.domain_routes.resourcetag_routes import resourcetag_bp
    app.register_blueprint(resourcetag_bp)
    from app.domain_routes.setting_routes import setting_bp
    app.register_blueprint(setting_bp)
    from app.domain_routes.featureflag_routes import featureflag_bp
    app.register_blueprint(featureflag_bp)
    from app.domain_routes.quota_routes import quota_bp
    app.register_blueprint(quota_bp)
    from app.domain_routes.quotausage_routes import quotausage_bp
    app.register_blueprint(quotausage_bp)
    from app.domain_routes.metric_routes import metric_bp
    app.register_blueprint(metric_bp)
    from app.domain_routes.alert_routes import alert_bp
    app.register_blueprint(alert_bp)
    from app.domain_routes.alerthistory_routes import alerthistory_bp
    app.register_blueprint(alerthistory_bp)
    from app.domain_routes.savedquery_routes import savedquery_bp
    app.register_blueprint(savedquery_bp)

    return app
