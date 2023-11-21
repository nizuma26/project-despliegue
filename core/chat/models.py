from django.db import models
from core.user.models import User
from datetime import datetime

# Create your models here.

tipo_sala_choices = [
        ("PRIVADA", 'Privada'),
        ("PÚBLICA", 'Pública'),
    ]

class Sala(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo_sala = models.CharField(max_length=14, choices=tipo_sala_choices, null=True, blank=True)

    def __str__(self):
        return f'{self.nombre} - {self.tipo_sala}'
    
    class Meta:
        ordering = ('fecha',)

class Usuario_sala(models.Model):
    usuario=models.ForeignKey(User, on_delete=models.CASCADE)
    sala=models.ForeignKey(Sala, on_delete=models.CASCADE)

class Mensaje(models.Model):
    contenido = models.TextField(null=True, blank=True)
    usuario=models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_user_set')
    sala=models.ForeignKey(Sala, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    editado = models.BooleanField(default=False)

    def __str__(self):
        return self.usuario.username

    class Meta:
        ordering = ('fecha',)