from dataclasses import field
from django.db import models
from crum import get_current_request
from django.contrib.auth.models import ContentType
#from configuracion.settings import AUTH_USER_MODEL
from core.user.models import User
from datetime import datetime
from django.forms import model_to_dict
from django.http import JsonResponse
from django.db import models
from user_agents import parse

class UserActivity(models.Model):
    action_date = models.DateField(default=datetime.now)
    action_time = models.TimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    object_repr = models.CharField(max_length=255)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    device = models.CharField(max_length=90, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def toJSON(self):
        item = model_to_dict(self)
        item['content_type'] = [{'id': c.id, 'name': c.name} for c in self.content_type.all()]
        item['user'] = self.user.toJSON()
        item['action_date'] = self.action_date.strftime('%Y-%m-%d')
        item['action_time'] = self.action_time.strftime('%H:%M:%S')
        return item
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:            
            request = get_current_request()
            user_agent = request.META.get('HTTP_USER_AGENT')
            if user_agent:                
                parsed_user_agent = parse(user_agent)                
                #Capturar el dispositivo y sistema operativo
                if parsed_user_agent.is_mobile:
                    self.device = f"Teléfono Móvil / {parsed_user_agent.os.family} {parsed_user_agent.os.version_string}"
                elif parsed_user_agent.is_tablet:
                    self.device = f"Tablet / {parsed_user_agent.os.family} {parsed_user_agent.os.version_string}"
                else:
                    self.device = f"PC / {parsed_user_agent.os.family} {parsed_user_agent.os.version_string}"
        except:
            pass
        super(UserActivity, self).save()


    class Meta:
        verbose_name = 'Actividad de Usuario'
        verbose_name_plural = 'Actividades de Usuarios'
        default_permissions = ()
        permissions = (
            ('view_activity_users', 'Can view Actividades de Usuarios'),
            ('delete_activity_users', 'Can delete Actividades de Usuarios'),
        )
        ordering = ['id']

class DetUserActivity(models.Model):
    user_activity = models.ForeignKey(UserActivity, on_delete=models.CASCADE, blank=True, null=True, related_name='det_user_activity_set', verbose_name='Actividad de Usuario')
    field = models.CharField(max_length=255, null=True, blank=True, verbose_name='Campo Modificado')
    previous_value = models.CharField(max_length=255, null=True, blank=True, verbose_name='Valor Anterior')
    current_value = models.CharField(max_length=255, null=True, blank=True, verbose_name='Valor Actual')

    def __str__(self):
        return self.user_activity.object_repr

    class Meta:
        verbose_name = 'Actividad de Usuario'
        verbose_name_plural = 'Actividades de Usuarios'
        default_permissions = ()
        permissions = (
            ('view_det_activity_users', 'Can view Detalle Actividades de Usuarios'),
            ('delete_det_activity_users', 'Can delete Detalle Actividades de Usuarios'),
        )
        ordering = ['id']