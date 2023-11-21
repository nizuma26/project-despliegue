from django.urls import path
from core.ui_customizer.views import CustomizeBasicInterface

app_name = 'customize'

urlpatterns = [
    path('interface/', CustomizeBasicInterface.as_view(), name='customize'),
]