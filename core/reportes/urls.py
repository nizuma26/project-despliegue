from django.urls import path

from core.reportes.views.ingresos.views import *
from core.reportes.views.salidas.views import *
from core.reportes.views.desinc_almac.views import *
from core.reportes.views.traslados.views import *
from core.reportes.views.desinc_unidad.views import *
from core.reportes.views.inventario.unidad_producto.views import *
from core.reportes.views.inventario.almacen_producto.views import *

app_name = 'report'

urlpatterns = [
    # reports ingreso
    path('ingreso/', ReportIngresoView.as_view(), name='ingreso_report'),

    # reports salidas
    path('salida/', ReportSalidasView.as_view(), name='salida_report'),

    # reports desinc_almacen
    path('desinc_almacen/', ReportDesincAlmView.as_view(), name='desinc_almacen_report'),

    # reports traslados
    path('traslado/', ReportTrasladoView.as_view(), name='traslado_report'),

    # reports traslados
    path('desinc_unidad/', ReportDesincUnidadView.as_view(), name='desinc_unidad_report'),
    
    # reports salida
    path('unidad_prod/', ReportUnidadProdView.as_view(), name='unidad_report'),
    path('almacen_prod/', ReportAlmacenProdView.as_view(), name='almacen_report'),
]