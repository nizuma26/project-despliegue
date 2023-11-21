from datetime import datetime
# Django
from django.db import models
from core.erp.models import Unidad, Departamento, Producto, InventarioBienes, ConcepMovimiento
from core.user.models import User
from core.erp.models import InventarioBienes, ConcepMovimiento
from core.solicitudes.choices import *
from django.forms import model_to_dict

# Create your models here.
class SolicSoporte(models.Model):
    codigo= models.CharField(max_length=14, unique=True, blank=True, null=True, verbose_name='Código')
    usuario=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='solicitud_soporte_user', verbose_name='Usuario')
    estado= models.CharField(max_length=3, choices=status_choices, default='ECR', null=True, blank=True, verbose_name='Estado de la Solicitud')    
    prioridad = models.CharField(max_length=2, choices=prioridad_choices, null=True, blank=True)
    tipo_solic=models.CharField(max_length=3, choices=tipo_solic_soporte_choices, default='AST', null=True, blank=True)
    tipo_prod = models.CharField(max_length=3, choices=prod_solicitud_choices, null=True, blank=True)
    fecha = models.DateField(default=datetime.now, verbose_name='Fecha de Solicitud')
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, blank=True, null=True, related_name='solicitud_soporte_unidad', verbose_name='Unidad Solicitante')
    descrip=models.TextField(max_length=200, null=True, blank=True, verbose_name='Descripción')
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} - {}'.format(self.codigo, self.usuario.get_full_name())
    
    def toJSON(self):
        item = model_to_dict(self)
        item['unidad'] = self.unidad.toJSON()      
        item['fecha_solicitud'] = self.fecha.strftime('%Y-%m-%d')
        item['usuario'] = self.usuario.toJSON()
        item['estado'] = {'id': self.estado, 'name': self.get_estado_display()}
        item['prioridad'] = {'id': self.prioridad, 'name': self.get_prioridad_display()}
        item['tipo_solic'] = {'id': self.tipo_solic, 'name': self.get_tipo_solic_display()}
        item['tipo_prod'] = {'id': self.tipo_prod, 'name': self.get_tipo_prod_display()}
        item['det'] = [i.toJSON() for i in self.solic_soport_set.all()]
        return item

    class Meta:
        verbose_name = 'Solicitud de Servicio Técnico'
        verbose_name_plural = 'Solicitudes de Servicio Técnico'
        ordering = ['codigo']

class DetSolicSoporte(models.Model):
    solic_soport = models.ForeignKey(SolicSoporte, on_delete=models.CASCADE, blank=True, null=True, related_name='solic_soport_set', verbose_name='Código de Solicitud')
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True, null=True, related_name='prodsolic_soport_set', verbose_name='Producto')
    diagnostico = models.CharField(max_length=200, null=True, blank=True, verbose_name="Diagnóstico")

    def __str__(self):
        return self.solic_soport.codigo

    def toJSON(self):
        item = model_to_dict(self, exclude=['solic_soport'])
        item['prod'] = self.prod.toJSON()
        return item

    class Meta:
        verbose_name = 'Detalle Solicitud de Servicio Técnico'
        verbose_name_plural = 'Detalle Solicitudes de Servicio Técnico'       
        ordering = ['id']

class Solicitudes(models.Model):
    class Status(models.TextChoices):
        in_creation = 'EN CREACIÓN', 'En creación',
        waiting = 'EN ESPERA', 'En espera',

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitud_user_set')
    unidad_origen = models.ForeignKey(Unidad, on_delete=models.CASCADE, related_name='solicitud_unidad_origen_set', null=True, blank=True)
    unidad_destino = models.ForeignKey(Unidad, on_delete=models.CASCADE, related_name='solicitud_unidad_destino_set', null=True, blank=True)
    codigo= models.CharField(max_length=14, unique=True, blank=True, null=True)
    tipo_solicitud = models.CharField(max_length=25, choices=tipo_solic_choices)
    concepto = models.ForeignKey(ConcepMovimiento, on_delete=models.CASCADE, related_name='solicitud_concept_set', null=True, blank=True)
    prioridad = models.CharField(max_length=25, choices=prioridad_choices, default='NM', null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=25, choices=Status.choices, default=Status.waiting)
    fecha = models.DateField(default=datetime.now)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} - {}'.format(self.codigo, self.unidad_origen.nombre)
    
    # def toJSON(self):
    #     item = model_to_dict(self)
    #     item['unidad'] = self.unidad.toJSON()
    #     item['fecha'] = self.fecha.strftime('%Y-%m-%d')
    #     item['usuario'] = self.user.toJSON()
    #     item['estado'] = {'id': self.estado, 'name': self.get_estado_display()}
    #     item['prioridad'] = {'id': self.prioridad, 'name': self.get_prioridad_display()}
    #     item['tipo_solicitud'] = {'id': self.tipo_solicitud, 'name': self.get_tipo_solicitud_display()}
    #     item['det'] = [i.toJSON() for i in self.solicitud_set.all()]
    #     return item

    class Meta:
        verbose_name = 'Solicitud de movimiento'
        verbose_name_plural = 'Solicitudes de Movimientos'
        ordering = ['codigo']

class DetSolicitud(models.Model):
    solicitud = models.ForeignKey(Solicitudes, on_delete=models.CASCADE, blank=True, null=True, related_name='solicitud_set')
    productos = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='solicitud_productos_set')
    inventario = models.ForeignKey(InventarioBienes, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.IntegerField(default=0)
    cantidad_aprobada = models.IntegerField(default=0)
    aprobado = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return self.solicitud.codigo

    def toJSON(self):
        item = model_to_dict(self, exclude=['solicitud'])
        item['productos'] = self.productos.toJSON()
        item['inventario'] = self.inventario.toJSON()
        return item

    class Meta:
        verbose_name = 'Detalle Solicitud de Movimiento'
        verbose_name_plural = 'Detalle Solicitudes de Movimientos'       
        ordering = ['id']