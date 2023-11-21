from django.utils.timesince import timesince
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from core.notificaciones.models import *

class NotificacionListView(ListView):   
    model = Notificacion

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_notification':
                notifications = []
                notify = NotificacionUsuario.objects.prefetch_related('notificacion', 'usuario').filter(usuario=request.POST['id']).order_by('-id')
                #notify = notify.filter(usuario=self-request.user)
                notify_unread = len(notify.filter(leida=False))
                for i in notify:
                    item = {
                        'read': i.leida,
                        'title': i.notificacion.titulo,
                        'image': i.notificacion.imagen.url,
                        'message': i.notificacion.mensaje,
                        'url': i.notificacion.url,
                        'created_at': timesince(i.notificacion.fecha),
                        'id': i.notificacion.id,
                    }
                    notifications.append(item)
                return JsonResponse({'notify': notifications, 'unread': notify_unread}, safe=False)
            
            elif action == 'read':

                notification_id = request.POST['notification_id']
                user_id = request.POST['user_id']

                notification = NotificacionUsuario.objects.prefetch_related('notificacion', 'usuario').filter(notificacion_id=notification_id, usuario_id=user_id)
                notification.update(leida=True)
                url = notification.values('notificacion__url').first()
                print('URLLLL: ', url['notificacion__url'])

                return JsonResponse({'notify': False, 'url': url['notificacion__url']}, safe=False)
            
            elif action == 'delete':

                notification_id = request.POST['notification_id']
                user_id = request.POST['user_id']

                notification = NotificacionUsuario.objects.prefetch_related('notificacion', 'usuario').filter(notificacion_id=notification_id, usuario_id=user_id)
                yes = notification.values('leida')
                noti = yes[0]['leida']
                notification.delete()
                print('ES LEIDA? ', noti)
                return JsonResponse({'notify': noti}, safe=False)
                
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

