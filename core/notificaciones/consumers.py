import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timesince import timesince
from django.db.models import Q
from .models import *
from core.user.models import User

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):        
        self.my_id = self.scope['user'].id
        self.room_group_name = 'notificacion'
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()        

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        title = text_data_json["title"]
        message = text_data_json["message"]
        url = text_data_json["url"]
        image = text_data_json["image"]
        user_id = text_data_json["user_id"]
        permissions = text_data_json["permissions"]

        print('RECEIVE: ',type)

        if type == 'create_operation_notification':

            new_notification_request = await self.create_operation_notification(title, message, url, image, permissions)

            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'new_notification',
                    'user_receptor': new_notification_request['user_id'],
                    'title': new_notification_request['titulo'],
                    'image': new_notification_request['image'],
                    'message': new_notification_request['mensaje'],
                    'url': url,
                    'id': new_notification_request['id'],
                    'created_at': timesince(new_notification_request['fecha']),
                }
            )

        if type == 'status_request_notification':

            new_notification_approve = await self.status_request_notification(title, message, url, image, user_id)

            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'new_notification',
                    'user_receptor': new_notification_approve['user_id'],
                    'title': new_notification_approve['titulo'],
                    'image': new_notification_approve['image'],
                    'message': new_notification_approve['mensaje'],
                    'url': url,
                    'id': new_notification_approve['id'],
                    'created_at': timesince(new_notification_approve['fecha']),
                }
            )

    async def new_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'user_receptor': event['user_receptor'],
            'title': event['title'],
            'image': event['image'],
            'message': event['message'],
            'url': event['url'],
            'id': event['id'],
            'created_at': event['created_at'],
        }))

    # @sync_to_async
    # def get_notification(self):        
    #     self.notification = Notificacion.objects.filter(usuario=self.my_id)

    @sync_to_async
    def create_operation_notification(self, title, message, url, image, permissions):

        users = User.objects.filter(Q(groups__permissions__codename=permissions) | Q(user_permissions__codename=permissions)).distinct()

        notifications = []
        notification = Notificacion.objects.create(
            titulo=title,
            mensaje=message,
            url=url,
            imagen=image
        )
        for user in users:
            noti = NotificacionUsuario.objects.create(
                notificacion_id = notification.id,
                usuario_id = user.id
            )
            notifications.append({'id': user.id})

        notify = {'id': notification.id, 'titulo': notification.titulo, 'mensaje': notification.mensaje, 'fecha': notification.fecha, 'image': notification.imagen.url, 'url': notification.url, 'user_id': notifications}
        return notify
    
    @sync_to_async
    def status_request_notification(self, title, message, url, image, user_id):   

        notifications = []
        notification = Notificacion.objects.create(
            titulo=title,
            mensaje=message,
            url=url,
            imagen=image
        )        
        noti = NotificacionUsuario.objects.create(
            notificacion_id = notification.id,
            usuario_id = int(user_id)
        )
        notifications.append({'id': noti.usuario.id})

        notify = {'id': notification.id, 'titulo': notification.titulo, 
                  'mensaje': notification.mensaje, 'fecha': notification.fecha,
                  'image': notification.imagen.url, 'url': notification.url, 
                  'user_id': notifications
                  }

        return notify
            