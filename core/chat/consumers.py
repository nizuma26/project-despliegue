import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timesince import timesince
from .models import *

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):        
        self.room_name = self.scope['url_route']['kwargs']['id']
        self.my_id = self.scope['user'].id
        self.room_group_name = f'chat_{self.room_name}'

        await self.get_sala()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json["message"]
        message_id = text_data_json["message_id"]
        message_position = text_data_json["message_position"]
        sala = text_data_json["sala"]
        id = self.my_id
        writing = text_data_json["writing"]

        self.id_msg = message_id

        print('MENSAJE: ',message)
        print('RECEIVE: ',type)

        if type == 'message':

            new_message = await self.create_message(message, sala)

            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'chat_message',
                    'id': self.my_id,
                    'message': message,
                    'message_id': new_message.id,
                    'sala': sala,
                    'created_at': timesince(new_message.fecha),
                }
            )

        elif type == 'update_message':
            print('MODIFICAR')
            updated_message = await self.update_message(message)
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'updated_msg',
                    'id': self.my_id,
                    'message': updated_message.contenido,
                    'message_id': updated_message.id,
                    'message_position': message_position,
                    #'sala': sala,
                }
            )
        elif type == 'writing':
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'writing_active',
                    'id': self.my_id,
                    'message': message,
                    'sala': sala,
                    'writing': writing,
                }
            )
        elif type == 'delete_message':
            delete_message = await self.delete_message(self.id_msg)
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'delete_msg',
                    'id': self.my_id,
                    'message': message,
                    'sala': sala,
                    # 'message_id': delete_message.id,
                    'message_position': message_position,
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'id': event['id'],
            'message': event['message'],
            'message_id': event['message_id'],
            'sala': event['sala'],
            'created_at': event['created_at'],
        }))
    
    async def updated_msg(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'id': event['id'],
            'message': event['message'],
            'message_id': event['message_id'],
            'message_position': event['message_position'],
        }))
    
    async def writing_active(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'id': event['id'],
            'message': event['message'],
            'sala': event['sala'],
            'writing': event['writing'],
        }))

    async def delete_msg(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            # 'message_id': event['message_id'],
            'message_position': event['message_position'],
        }))

    @sync_to_async
    def get_sala(self):        
        self.room = Sala.objects.get(id=self.room_name)

    @sync_to_async
    def create_message(self, message, sala):
        message = Mensaje.objects.create(
            contenido=message, 
            sala_id=int(sala), 
            usuario_id=self.my_id
        )
        return message

    @sync_to_async
    def delete_message(self, message_id):
        msg = Mensaje.objects.prefetch_related('sala', 'usuario').get(id=self.id_msg)
        msg.delete()
        return msg
    
    @sync_to_async
    def update_message(self, message):
        msg = Mensaje.objects.prefetch_related('sala', 'usuario').get(id=self.id_msg)
        msg.contenido = message
        msg.editado = True
        msg.save()
        return msg

    
# class PrivateChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         my_id = self.scope['user'].id
#         other_user_id = self.scope['url_route']['kwargs']['id']
#         #print('MI ID: ', my_id, other_user_id)
#         if int(my_id) > int(other_user_id):
#             self.room_name = f'{my_id}-{other_user_id}'
#         else:
#             self.room_name = f'{other_user_id}-{my_id}'
        
#         self.room_group_name = 'chat_%s' % self.room_name

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()
    
#     async def disconnect(self, close_code):
#         self.channel_layer.group_discard(
#             self.room_group_name, 
#             self.channel_name
#         )
    
