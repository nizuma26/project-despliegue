from datetime import datetime

from crum import get_current_request
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from core.audit_log.models import UserActivity, DetUserActivity
from django.urls import reverse_lazy


class IsSuperuserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('index_app:Index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_now'] = datetime.now()
        return context

class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        perms = []
        if isinstance(self.permission_required, str):
            perms.append(self.permission_required)
        else:
            perms = list(self.permission_required)
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('index_app:Index')
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        request = get_current_request()
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        if 'group' in request.session:
            group = request.session['group']
            perms = self.get_perms()
            for p in perms:
                if not group.permissions.filter(codename=p).exists():
                    messages.error(request, 'No tiene permiso para ingresar a este módulo')
                    print('aqui estoy', request)
                    return HttpResponseRedirect(self.get_url_redirect())
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No tiene permiso para ingresar a este módulo')
        return HttpResponseRedirect(self.get_url_redirect())


class Perms_Check(object):
    permission_required = ''
    url_redirect = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estado'] = 'error'
        return context
        
    def get_perms(self):
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms
    
    def get_url_rediret(self):
        if self.url_redirect is None:
            return reverse_lazy('index_app:Index')
        return self.url_redirect
    
    def dispatch(self, request,*args, **kwargs):
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No tiene permisos para realizar esta acción')
        return redirect(self.get_url_rediret())

log_id = {}
class AuditLog():
    def save_log(user, id, content, log, message):
        log = UserActivity.objects.create(
            user_id=int(user),
            content_type_id=int(content),
            object_id=int(id),
            object_repr=log,
            action=message,
        )
        log_id['id'] = log.id
    #PARA GUARDAR LOS CAMPOS QUE HAN SIDO MODIFICADOS
    def fields_save(changes, *args, **kwargs):
        for i in changes:
            DetUserActivity.objects.create(
            field = i['field'],
            previous_value = i['value_ant'],
            current_value = i['value_act'],
            user_activity_id = log_id['id'],
            )













    # permission_required = ''
    # url_redirect = None

    # def get_perms(self):
    #     perms = []
    #     if isinstance(self.permission_required, str):
    #         perms.append(self.permission_required)
    #     else:
    #         perms = list(self.permission_required)
    #     return perms

    # def get_url_redirect(self):
    #     if self.url_redirect is None:
    #         return reverse_lazy('index_app:Index')
    #     return self.url_redirect

    # def dispatch(self, request, *args, **kwargs):
    #     request = get_current_request()
    #     if request.user.is_superuser:
    #         return super().dispatch(request, *args, **kwargs)
    #     if 'group' in request.session:
    #         group = request.session['group']
    #         perms = self.get_perms()
    #         for p in perms:
    #             if not group.permissions.filter(codename=p).exists():
    #                 messages.error(request, 'No tiene permiso para ingresar a este módulo')
    #                 return HttpResponseRedirect(self.get_url_redirect())
    #         return super().dispatch(request, *args, **kwargs)
    #     messages.error(request, 'No tiene permiso para ingresar a este módulo')
    #     return HttpResponseRedirect(self.get_url_redirect())
    

