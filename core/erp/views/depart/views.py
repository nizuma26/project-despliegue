import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from core.erp.forms import FormDepart
from core.erp.models import Departamento
from core.erp.mixins import Perms_Check
from core.audit_log.mixins import AuditMixin

class DepartListView(LoginRequiredMixin, Perms_Check, ListView):   
    model = Departamento
    template_name = 'depart/list.html'
    permission_required = 'erp.view_departamento'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Departamento.objects.all():
                    data.append(i.toJSON())
            
            elif action == 'add':
                perms = ('erp.add_departamento',)
                if request.user.has_perms(perms):
                    depart = Departamento()                    
                    depart.nombre = request.POST.get('nombre')
                    depart.save()                    
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'                
            
            elif action == 'edit':
                perms = ('erp.change_departamento',)
                if request.user.has_perms(perms):
                    depart = Departamento.objects.get(pk=request.POST['id']) 
                    depart.nombre = request.POST.get('nombre')
                    depart.save()
                    pre_values = json.loads(request.POST['current_data'])
                    self.audit_fields(pre_values, depart)
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'

            elif action == 'delete':
                perms = ('erp.delete_departamento',)
                if request.user.has_perms(perms):
                    depart = Departamento.objects.get(pk=request.POST['id'])
                    depart.delete()
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Departamentos'
        context['create_url'] = ''#reverse_lazy('erp:category_create')
        context['list_url'] = ''#reverse_lazy('erp:category_list')
        context['entity'] = 'Departamentos'
        context['btn_name'] = 'Nuevo Departamento'
        context['frmDepart'] = FormDepart()
        return context

    def audit_fields(self, pre_value, post_value):
        changes = []
        fields = [{'field': 'Nombre', 'value_ant':pre_value['nombre'], 'value_act': post_value.nombre}]
        
        for i in fields:
            if i['value_ant'] != i['value_act']:
                changes.append(i)

        if len(changes) > 0:
            AuditMixin.fields_save(changes)