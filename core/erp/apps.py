from django.apps import AppConfig

class ErpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.erp'

    def ready(self):
        import core.audit_log.signals
        import core.erp.signals
