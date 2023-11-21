import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.timesince import timesince
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.erp.mixins import Perms_Check
from core.chat.models import *
from core.user.models import User
# Create your views here.

class SalaListView(ListView):   
    model = Sala

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create_private_room':
                message_list = []
                user = User.objects.values('username', 'id').get(id=request.POST['id'])
                username = user['username']
                name = f'{self.request.user}-{username}'
                usuario_actual = request.user
                sala_exist = Sala.objects.filter(usuario_sala__usuario=usuario_actual).filter(usuario_sala__usuario=user['id']).first()
                if sala_exist:
                    #print('SI EXISTE LA SALA')
                    message = Mensaje.objects.filter(sala_id=sala_exist.id)
                    for m in message[0:15]:
                        item = {
                            'body': m.contenido,
                            'date_joined': timesince(m.fecha),
                            'image': m.usuario.get_image(),
                            'first_user': m.usuario_id,
                            'second_user': usuario_actual.id,
                            'message_id': m.id,
                            'editado': m.editado
                        }
                        message_list.append(item)
                    return JsonResponse({'sala_id': sala_exist.id, 'message_list': message_list}, safe=False)
                    
                else:
                    #print('NO EXISTE')
                    sala = Sala.objects.create(
                        nombre=name,
                        tipo_sala='PRIVADA'
                    )
                    users = [{'user': usuario_actual.id}, {'user': user['id']}]
                    for i in users:
                        Usuario_sala.objects.create(
                            usuario_id=int(i['user']),
                            sala_id=int(sala.id)
                    )    
                    return JsonResponse({'sala_id': sala.id}, safe=False)               
                
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class ChatUserListView(ListView):   
    model = User
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'load_user':
                data = []
                users = User.objects.prefetch_related('groups', 'user_permissions').filter(is_active=1).exclude(id=self.request.user.id)
                for i in users[0:8]:
                    user = {
                        'id': i.id,
                        'full_name': i.get_full_name(),
                        'image': i.get_image(),
                    }
                    data.append(user)

            elif action == 'load_more_users':
                ids_exclude = json.loads(request.POST['ids'])
                lista_sin_repetidos = list(set(ids_exclude))
                data = []
                users = User.objects.prefetch_related('groups', 'user_permissions').filter(is_active=1).exclude(username=self.request.user).exclude(id__in=lista_sin_repetidos).distinct()
                for i in users[0:2]:
                    user = {
                        'id': i.id,
                        'full_name': i.get_full_name(),
                        'image': i.get_image(),
                    }
                    data.append(user)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
