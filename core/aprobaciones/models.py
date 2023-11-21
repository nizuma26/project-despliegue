from django.db import models
from datetime import datetime
# Django
from core.erp.models import *
from core.user.models import User
from core.solicitudes.choices import *
from django.forms import model_to_dict

# Create your models here.
class Aprobaciones(models.Model):

    class Action(models.TextChoices):
        returned = 'RETORNADA', 'Retornar',
        approved = 'APROBADA', 'Aprobar',
        declined = 'RECHAZADA', 'Rechazar'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aprobacion_user_set')    
    accion = models.CharField(max_length=25, choices=Action.choices, default=Action.approved)
    motivo = models.TextField(null=True, blank=True)
    operacion = models.CharField(max_length=255, blank=True, null=True)
    codigo= models.CharField(max_length=120, blank=True, null=True)
    fecha = models.DateField(default=datetime.now)

    def __str__(self):
        return f'{self.codigo} - {self.accion}'

    class Meta:
        verbose_name = 'Gestion de Aprobacion'
        verbose_name_plural = 'Gestion de Aprovaciones'
        default_permissions = ()
        permissions = (
            ('approve_movimientos', 'Can approve movimientos'),
            ('approve_solicitudes', 'Can approve solicitudes'),
        )
        ordering = ['-fecha']