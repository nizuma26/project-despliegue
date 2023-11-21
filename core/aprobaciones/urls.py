from django.urls import path
from core.aprobaciones.view.distribuciones.views import AprobacionDistFormView
from core.aprobaciones.view.incorporaciones.views import AprobIncorpFormView
from core.aprobaciones.view.traslados.views import AprobacionTrasFormView
from core.aprobaciones.view.desincorporaciones.bienes_en_deposito.views import AprobacionDesincAlmacenFormView
from core.aprobaciones.view.desincorporaciones.bienes_en_uso.views import AprobacionDesincorpFormView
from core.aprobaciones.view.solicitudes.views import ManageRequest

app_name = 'aprobaciones'

urlpatterns = [
    path('distribucion/list/', AprobacionDistFormView.as_view(), name='aprob_distribucion_list'),
    path('incorporacion/list/', AprobIncorpFormView.as_view(), name='aprob_incorporacion_list'),
    path('traslado/list/', AprobacionTrasFormView.as_view(), name='aprob_traslado_list'),
    path('descincorp_almacen/list/', AprobacionDesincAlmacenFormView.as_view(), name='aprob_desincorp_almacen_list'),
    path('descincorp/list/', AprobacionDesincorpFormView.as_view(), name='aprob_desincorp_list'),
    path('solicitud/movimiento/', ManageRequest.as_view(), name='solicitud_movimiento'),
]