import json
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.contrib.auth.models import Permission
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView, FormView

from core.erp.mixins import Perms_Check
from core.user.forms import *
from core.reportes.forms import FormAction
from core.user.models import User
from core.security.models import AccessUsers


class UserListView(LoginRequiredMixin, Perms_Check, FormView):   
    form_class = FormAction
    template_name = 'user/list.html'
    permission_required = 'user.view_user'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in User.objects.prefetch_related('user_permissions', 'groups').all():
                    data.append(i.toJSON())

            elif action == 'search_access':
                data = []
                queryset = AccessUsers.objects.all().prefetch_related('user')
                for i in queryset.filter(user_id=request.POST['id']):
                    item = {}                  
                    item['user'] = i.user.username
                    item['date_joined'] = i.date_joined.strftime('%Y-%m-%d')
                    item['time_joined'] = i.time_joined.strftime('%H:%M:%S')
                    item['ip_address'] = i.ip_address
                    item['browser'] = i.browser
                    item['device'] = i.device                        
                    item['type'] = i.type                        
                    data.append(item)

            elif action == 'search_detail':
                data = []
                usuario = User.objects.all()
                position = 1
                for i in usuario.filter(id=request.POST['id']):
                    user_permissions = i.get_user_permissions()
                    group_permissions = i.get_group_permissions()
                    all_permissions = user_permissions.union(group_permissions)

                    for p in all_permissions:
                        item = {}
                        perm_object = Permission.objects.get(codename=p.split('.')[-1])
                        item['id'] = position
                        item['name'] = perm_object.name
                        data.append(item)
                        position += 1

            elif action == 'activar':
                with transaction.atomic():
                    perms = ('user.change_user',)
                    if request.user.has_perms(perms):
                        status = User.objects.get(id=request.POST['id'])
                        status.is_active = True
                        status.save()
                    else:
                        data['error'] = 'No tiene permisos para realizar esta acción'

            elif action == 'inactivar':
                with transaction.atomic():
                    perms = ('user.change_user',)
                    if request.user.has_perms(perms):
                        status = User.objects.get(id=request.POST['id'])
                        user = self.request.user
                        if status.username == str(user):
                            data['error'] = 'No puede inactivar su usuario mientras se encuentre en sesión'
                        else:
                            status.is_active = False
                            status.save()
                                                  
                    else:
                        data['error'] = 'No tiene permisos para realizar esta acción'
            
            elif action == 'inactive_multiple':
                with transaction.atomic():
                    perms = ('user.change_user',)
                    if request.user.has_perms(perms):
                        ids = json.loads(request.POST['id'])                        
                        users = User.objects.filter(id__in=ids)                        
                        for status in users.exclude(username=self.request.user):
                            status.is_active = False
                            status.save()
                    else:
                        data['error'] = 'No tiene permisos para realizar esta acción'
            
            elif action == 'active_multiple':
                with transaction.atomic():
                    perms = ('user.change_user',)
                    if request.user.has_perms(perms):
                        ids = json.loads(request.POST['id'])
                        users = User.objects.filter(id__in=ids)
                        for status in users:
                            status.is_active = True
                            status.save()                            
                    else:
                        data['error'] = 'No tiene permisos para realizar esta acción'
            
            elif action == 'delete_multiple':
                with transaction.atomic():
                    perms = ('user.delete_user',)
                    if request.user.has_perms(perms):
                        ids = json.loads(request.POST['id'])
                        users = User.objects.filter(id__in=ids)
                        users.delete()
                    else:
                        data['error'] = 'No tiene permisos para realizar esta acción'

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Usuarios'
        context['create_url'] = reverse_lazy('user:user_create')
        context['list_url'] = reverse_lazy('user:user_list')
        context['btn_name'] = 'Nuevo Usuario'
        return context

class UserCreateView(LoginRequiredMixin, Perms_Check, CreateView):
    model = User
    form_class = UserForm
    template_name = 'user/create_user.html'
    success_url = reverse_lazy('user:user_list')
    permission_required = 'user.add_user'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_perms':               
                data = []
                ids_exclude = ['logentry', 'contenttype', 'session', 'dettrasladoprod', 'detsalidainsumos', 'detingresoproduc', 'detdesincprod', 'detdesincalmacen', 'permission', 'detsalidaprod', 'detsolicsoporte', 'inventariobienes', 'seriales', 'lotes']
                for i in Permission.objects.exclude(content_type__model__in=ids_exclude):
                    item = {}
                    item['id'] = i.id
                    item['perms'] = i.name
                    data.append(item)

            elif action == 'add':
                with transaction.atomic():                   
                    user_data = json.loads(request.POST['data'])
                    dni = User.objects.filter(dni = user_data['dni'])
                    if dni:
                        data['error'] = "Ya existe un usuario con este número de cedúla"
                    else:
                        user = User()
                        user.first_name = user_data['first_name']
                        user.last_name = user_data['last_name']
                        user.dni = user_data['dni']
                        user.email = user_data['email']
                        user.image = user_data['image']
                        user.username = user_data['username']                    
                        user.set_password(user_data['password'])                    
                        user.is_active = user_data['is_active']                                    
                        user.save()
                        
                        user.groups.clear()
                        for g in user_data['groups']:
                            user.groups.add(g)
                        
                        user.user_permissions.clear()
                        for p in user_data['user_permissions']:
                            user.user_permissions.add(p)
                        
                        #global_data(request)
                    
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'      
        return context

class UserUpdateView(LoginRequiredMixin, Perms_Check, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/create_user.html'
    success_url = reverse_lazy('user:user_list')
    permission_required = 'user.change_user'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()        
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_perms':               
                data = []
                ids_exclude = ['logentry', 'contenttype', 'session', 'dettrasladoprod', 'detsalidainsumos', 'detingresoproduc', 'detdesincprod', 'detdesincalmacen', 'permission', 'detsalidaprod', 'detsolicsoporte', 'inventariobienes', 'seriales', 'lotes']
                for i in Permission.objects.exclude(content_type__model__in=ids_exclude):
                    item = {}
                    item['id'] = i.id
                    item['perms'] = i.name
                    data.append(item)

            elif action == 'edit':                
                #changes = []
                with transaction.atomic():
                    user_data = json.loads(request.POST['data'])
                    user = self.get_object()
                    dni = User.objects.exclude(id=user.id).values('dni')
                    dni = dni.filter(dni=user_data['dni'])
                    if dni:
                        data['error'] = "Ya existe un usuario con este número de cedúla"
                    else:
                        user.first_name = user_data['first_name']
                        user.last_name = user_data['last_name']
                        user.dni = user_data['dni']
                        user.email = user_data['email']
                        user.image = user_data['image']
                        user.username = user_data['username']                    
                        user.is_active = user_data['is_active']  
                        password = user_data['password']   
                        if self.get_object().password != password:
                            user.set_password(password)  
                        else:
                            user.password = self.get_object().password
                        user.save()
                        print('LOS VALORES SON: ',data)
                        user.groups.clear()
                        for g in user_data['groups']:
                            user.groups.add(g)

                        user.user_permissions.clear()
                        for p in user_data['user_permissions']:
                            user.user_permissions.add(p)
                        
                        # user_edit = {}
                        # if user.first_name != user_data['first_name']:
                        #     user_edit['first_name_ant'] = user.first_name
                        #     user_edit['first_name_act'] = user_data['first_name']
                        #     changes.append(user_edit)                       
                        #     print('LOS VALORES SON: ',changes)

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_perms_user(self):
        data = []
        try:            
            for i in User.objects.filter(id=self.get_object().id):                
                for p in i.user_permissions.all():
                    data.append(p.id)
        except:
            pass
        return data
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['perms'] = json.dumps(self.get_perms_user())
        context['action'] = 'edit'
        context['id'] = self.object.id
        return context

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    form_class = UserForm
    template_name = 'user/list.html' 
    permission_required = 'user.delete_user'   
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            perms = ('user.delete_user',)
            if request.user.has_perms(perms):
                user = self.request.user
                if self.object.username == str(user):
                    data['error'] = 'No puede eliminar su usuario mientras se encuentre en sesión'
                else:
                    self.object.delete()
            else:
                data['error'] = 'No tiene permisos para realizar esta acción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'user/profile2.html'
    success_url = reverse_lazy('index_app:Index')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Perfil'
        context['entity'] = 'Perfil'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class UserChangePasswordView(LoginRequiredMixin, FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'user/change_password.html'
    success_url = reverse_lazy('usuarios_app:login')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['placeholder'] = 'Ingrese su contraseña actual'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Ingrese su nueva contraseña'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Repita su contraseña'
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Password'
        context['entity'] = 'Password'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
