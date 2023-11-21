from django.contrib import admin
from core.erp.models import *
# Register your models here.
# Modelos

admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(Modelo)
admin.site.register(Moneda)
admin.site.register(Almacen)
admin.site.register(Producto)
admin.site.register(ConcepMovimiento)
admin.site.register(CodBienes)

# admin.site.register(Client)