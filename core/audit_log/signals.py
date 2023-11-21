from crum import get_current_request
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.erp.models import *

@receiver(post_save)
def audit_log(sender, instance, created, raw, update_fields, **kwargs):
  #Lista de los modelos que se requienran que escuche
    list_of_models = ['Categoria', 'Marca', 'Modelo', 'Unidad', 'Almacen', 'GrupoCtaBienes', 'SubGrupoCtaBienes', 'Moneda', 'Proveedor', 'Departamento', 'ConcepMovimiento',]
    if sender.__name__ not in list_of_models:
        return
    user = get_user()
    if created:
        instance.save_addition(user)
    elif not raw:
        instance.save_edition(user)

@receiver(post_delete)
def audit_delete_log(sender, instance, **kwargs):
  #Lista de los modelos que se requienran que escuche  
    list_of_models = ['Categoria', 'Marca', 'Modelo', 'AccessUsers', 'Producto', 'Unidad', 'Almacen', 'GrupoCtaBienes', 'SubGrupoCtaBienes', 'Moneda', 'Proveedor', 'CodBienes', 'Departamento', 'ConcepMovimiento', 'IngresoProduc']
    if sender.__name__ not in list_of_models:
        return
    user = get_user() 
    instance.save_deletion(user)

def get_user():
    request = get_current_request()
    user = request.user.id
    return user