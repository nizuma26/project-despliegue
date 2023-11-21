from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Producto, IngresoProduc, SalidaProduc, TrasladoProduc, DesincAlmacen, DesincProduc

@receiver(post_save, sender=Producto)
def product_code(sender, instance, created, **kwargs):
    if created and not instance.codigo:
        id = instance.id
        instance.codigo = 'P' + str(id).zfill(8)
        instance.save(update_fields=['codigo'])
    
@receiver(post_save, sender=IngresoProduc)
def incorp_code(sender, instance, created, **kwargs):
    if created and not instance.cod_ingreso:
        id = instance.id
        instance.cod_ingreso = 'IN' + str(id).zfill(9)
        instance.save(update_fields=['cod_ingreso'])

@receiver(post_save, sender=SalidaProduc)
def distrib_code(sender, instance, created, **kwargs):
    if created and not instance.cod_salida:
        id = instance.id
        instance.cod_salida = 'DIS' + str(id).zfill(10)
        instance.save(update_fields=['cod_salida'])

@receiver(post_save, sender=TrasladoProduc)
def traslado_code(sender, instance, created, **kwargs):
    if created and not instance.cod_traslado:
        id = instance.id
        instance.cod_traslado = 'TR' + str(id).zfill(10)
        instance.save(update_fields=['cod_traslado'])

@receiver(post_save, sender=DesincProduc)
def desinc_code(sender, instance, created, **kwargs):
    if created and not instance.cod_desinc:
        id = instance.id
        instance.cod_desinc = 'DSU' + str(id).zfill(10)
        instance.save(update_fields=['cod_desinc'])

@receiver(post_save, sender=DesincAlmacen)
def desinc_almacen_code(sender, instance, created, **kwargs):
    if created and not instance.cod_desinc:
        id = instance.id
        instance.cod_desinc = 'DSA' + str(id).zfill(10)
        instance.save(update_fields=['cod_desinc'])