import json
from django.http import JsonResponse
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import FormView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from core.erp.mixins import Perms_Check
from core.reportes.forms import ReportForm
from core.security.models import AccessUsers
from core.audit_log.models import UserActivity, DetUserActivity
from django.contrib.auth.models import ContentType


class AccessUsersListView(Perms_Check, FormView):
    form_class = ReportForm
    template_name = 'access_users/list.html'
    permission_required = 'security.view_access_users'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):  
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_data_access':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = AccessUsers.objects.prefetch_related('user').all()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    item = {}                  
                    item['id'] = i.id                  
                    item['user'] = i.user.username
                    item['date_joined'] = i.date_joined.strftime('%Y-%m-%d')
                    item['time_joined'] = i.time_joined.strftime('%H:%M:%S')
                    item['ip_address'] = i.ip_address
                    item['browser'] = i.browser
                    item['device'] = i.device                        
                    item['type'] = i.type                      
                    data.append(item)                    

            elif action == 'search_data_activity':
                data = []
                start_date_act = request.POST['start_date_act']
                end_date_act = request.POST['end_date_act']
                queryset = UserActivity.objects.prefetch_related('user', 'content_type').all()
                if len(start_date_act) and len(end_date_act):
                    queryset = queryset.filter(action_date__range=[start_date_act, end_date_act])
                for i in queryset:
                    item = {}
                    item['id'] = i.id
                    item['user'] = i.user.username
                    item['date_joined'] = i.action_date.strftime('%Y-%m-%d') + ' / ' + i.action_time.strftime('%H:%M:%S')
                    item['action'] = i.action
                    item['modules'] = i.content_type.name
                    item['object_id'] = i.object_id
                    item['object_repr'] = i.object_repr  
                    #item['device'] = i.device                     
                    data.append(item)

            elif action == 'detail':
                data = []
                queryset = DetUserActivity.objects.prefetch_related('user_activity').all()
                for i in queryset.filter(user_activity_id=request.POST['id']):
                    item ={}
                    item['field'] = i.field
                    item['previous_value'] = i.previous_value
                    item['current_value'] = i.current_value
                    data.append(item)
            
            elif action == 'delete_log_audit':
                queryset = UserActivity.objects.prefetch_related('user', 'content_type').get(pk=request.POST['id_log'])
                queryset.delete()
            
            elif action == 'delete_multiple_access':
                with transaction.atomic():
                    perms = ('security.delete_access_users',)
                    if request.user.has_perms(perms):
                        ids = json.loads(request.POST['id'])
                        queryset = AccessUsers.objects.prefetch_related('user').filter(id__in=ids)
                        queryset.delete()
                    else:
                        data['error'] = 'No tiene permisos para realizar esta acción'
            
            elif action == 'delete_multiple_historical':
                with transaction.atomic():
                    perms = ('audit_log.delete_activity_users',)
                    if request.user.has_perms(perms):
                        ids = json.loads(request.POST['id'])
                        queryset = UserActivity.objects.prefetch_related('user', 'content_type').filter(id__in=ids)
                        queryset.delete()
                    else:
                        data['error'] = 'No tiene permisos para realizar esta acción'
                                     
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Bitácora de Usuarios'
        context['list_url'] = reverse_lazy('security:access_users_list')
        context['entity'] = 'Bitacora'
        return context

class AccessUsersDeleteView(Perms_Check, DeleteView):
    model = AccessUsers
    permission_required = 'security.delete_access_users'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            perms = ('security.delete_access_users',)
            if request.user.has_perms(perms):
                self.object.delete()
            else:
                data['error'] = 'No tiene permisos para realizar esta acción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context