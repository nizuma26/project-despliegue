from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=Solicitudes)
def generar_codigo(sender, instance, created, **kwargs):
    if created and not instance.codigo:
        print(instance)
        print('ID: ', instance.id)
        id = instance.id
        # last_id = Solicitudes.objects.order_by('-id').first().id
        # next_id = last_id + 1 if last_id else 1
        instance.codigo = 'SM' + str(id).zfill(8)
        instance.save(update_fields=['codigo'])