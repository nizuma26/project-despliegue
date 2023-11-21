from django.urls import path
from core.notificaciones.views import *

app_name = 'notificacion'

urlpatterns = [
    path('list/', NotificacionListView.as_view(), name='sala'),
]