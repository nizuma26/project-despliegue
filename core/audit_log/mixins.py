import json
from django.contrib.contenttypes.models import ContentType
from core.audit_log.models import UserActivity, DetUserActivity
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
log_id = {}
class AuditMixin(object):
    #PARA GUARDAR LOS REGISTROS DE AUDITORIA
    def save_log(self, user, message):
        log = UserActivity.objects.create(
            user_id=user,
            content_type_id=ContentType.objects.get_for_model(self).id,
            object_id=self.id,
            object_repr=str(self),
            action=message,
        )
        log_id['id'] = log.id
        #return log_id

    #PARA GUARDAR LOS CAMPOS QUE HAN SIDO MODIFICADOS
    def fields_save(changes, *args, **kwargs):
        for i in changes:
            DetUserActivity.objects.create(
            field = i['field'],
            previous_value = i['value_ant'],
            current_value = i['value_act'],
            user_activity_id = log_id['id'],
            )

    def save_addition(self, user):
        message = 'Creado'
        self.save_log(user, message)

    def save_edition(self, user):
        self.save_log(user, 'Modificado')

    def save_deletion(self, user):
        self.save_log(user, 'Eliminado')