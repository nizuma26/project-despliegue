from django.db import models
from core.user.models import User
from datetime import datetime
from configuracion.settings import MEDIA_URL, STATIC_URL

# Create your models here.
class Notificacion(models.Model):
    titulo = models.CharField(max_length=255, null=True, blank=True)
    mensaje = models.CharField(max_length=255, null=True, blank=True)
    imagen=models.ImageField(upload_to='notificaciones/%Y/%m/%d', default='notificaciones/info.png', null=True, blank=True)
    url= models.TextField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mensaje
    
    def get_image(self):
        if self.imagen:
            return f'{MEDIA_URL}{self.imagen}'
        return f'{MEDIA_URL}notificaciones/info.png'

    class Meta:
        default_permissions = ()
        permissions = (
            ('view_notificacion', 'Can view notificaciones'),
        )
        ordering = ('fecha',)

class NotificacionUsuario(models.Model):
    notificacion=models.ForeignKey(Notificacion, on_delete=models.CASCADE, related_name='notification_set')
    usuario=models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_user_set')
    leida = models.BooleanField(default=False)
    
# class UsuarioNotificacion(models.Model):
#     usuario=models.ForeignKey(User, on_delete=models.CASCADE)
#     notificacion=models.ForeignKey(Notificacion, on_delete=models.CASCADE)