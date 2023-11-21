from django.urls import path
from core.solicitudes.views.servicio_tecnico.views import *
from core.solicitudes.views.movimientos.views import *

app_name = 'solicitudes'


urlpatterns = [
    # movimientos
    path('solicitud/list/', SolicitudListView.as_view(), name='solicitud_list'),
    path('solicitud/add/', SolicitudCreateView.as_view(), name='solicitud_create'),
    path('solicitud/update/<int:pk>/', SolicitudUpdateView.as_view(), name='solicitud_update'),
    path('solicitud/detail/<int:pk>/', SolicitudDetailView.as_view(), name='solicitud_detail'),
    # servicio técnico
    path('soporte/list/', SolicSoporteListView.as_view(), name='soporte_list'),
    path('soporte/add/', SolicSoporteCreateView.as_view(), name='soporte_create'),
    path('soporte/update/<int:pk>/', SolicSoporteUpdateView.as_view(), name='soporte_update'),

]


