from django.apps import AppConfig


class AuditLogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.audit_log'
