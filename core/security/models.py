from django.db import models
from crum import get_current_request
from datetime import datetime
from django.forms import model_to_dict
from core.user.models import User
from core.security.choices import LOGIN_TYPE, FREQUENCIES
from user_agents import parse
from core.audit_log.mixins import AuditMixin


class AccessUsers(AuditMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    time_joined = models.TimeField(default=datetime.now)
    ip_address = models.CharField(max_length=50)
    browser = models.CharField(max_length=60, null=True, blank=True)
    device = models.CharField(max_length=90, null=True, blank=True)
    type = models.CharField(max_length=15, choices=LOGIN_TYPE, default=LOGIN_TYPE[0][0])

    def __str__(self):
        return self.ip_address

    def toJSON(self):
        item = model_to_dict(self)
        item['type'] = {'id': self.type, 'name': self.get_type_display()}
        item['user'] = self.user.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['time_joined'] = self.time_joined.strftime('%H:%M:%S')
        return item
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:            
            request = get_current_request()
            print(request)
            self.ip_address = request.META['REMOTE_ADDR']
            
            #el User-Agent HTTP del navegador en la solicitud
            user_agent = request.META.get('HTTP_USER_AGENT')

            if user_agent:                
                parsed_user_agent = parse(user_agent)
                #Capturar el nombre del navegador y su versión
                self.browser = f"{parsed_user_agent.browser.family} {parsed_user_agent.browser.version_string}"
                #Capturar el dispositivo y sistema operativo
                if parsed_user_agent.is_mobile:
                    self.device = f"Teléfono Móvil / {parsed_user_agent.os.family} {parsed_user_agent.os.version_string}"
                elif parsed_user_agent.is_tablet:
                    self.device = f"Tablet / {parsed_user_agent.os.family} {parsed_user_agent.os.version_string}"
                else:
                    self.device = f"PC / {parsed_user_agent.os.family} {parsed_user_agent.os.version_string}"
        except:
            pass
        super(AccessUsers, self).save()

    class Meta:
        verbose_name = 'Acceso de Usuario'
        verbose_name_plural = 'Accesos de Usuarios'
        default_permissions = ()
        permissions = (
            ('view_access_users', 'Can view Accesos de Usuarios'),
            ('delete_access_users', 'Can delete Accesos de Usuarios'),
        )
        ordering = ['id']

