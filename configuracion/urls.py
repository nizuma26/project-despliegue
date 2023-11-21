from django.contrib import admin
from django.conf import settings   
from django.conf.urls.static import static 
from django.urls import path, include
from django.conf.urls import handler404
from core.inicio.views import page_not_found404
# handler404 = page_not_found404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.inicio.urls')),
    path('login/', include('core.login.urls')),
    path('erp/', include('core.erp.urls')),
    path('user/', include('core.user.urls')),
    path('solicitudes/', include('core.solicitudes.urls')),
    path('security/', include('core.security.urls')),
    path('group/', include('core.group.urls')),
    path('chat/', include('core.chat.urls')),
    path('notificacion/', include('core.notificaciones.urls')),
    path('reportes/', include('core.reportes.urls')),
    path('aprobaciones/', include('core.aprobaciones.urls')),
    path('customize/', include('core.ui_customizer.urls'))
]
#agregaros al  urlpatterns la url de las imagenes
#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)