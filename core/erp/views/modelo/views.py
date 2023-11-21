import json
from core.erp.forms import FormModelo
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.erp.mixins import Perms_Check
from core.erp.models import Modelo, Marca
from core.audit_log.mixins import AuditMixin

class ModeloListView(LoginRequiredMixin, Perms_Check, ListView):   
    model = Modelo
    template_name = 'modelo/list.html'
    permission_required = 'erp.view_modelo'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Modelo.objects.all().select_related('marcas'):
                    data.append(i.toJSON())
            
            elif action == 'add':
                perms = ('erp.add_modelo',)
                if request.user.has_perms(perms):                 
                    modelo = Modelo()
                    modelo.modelo = request.POST['modelo']
                    modelo.marcas_id = request.POST['marcas']  
                    modelo.save()                    
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'
            
            elif action == 'edit':
                perms = ('erp.change_modelo',)
                if request.user.has_perms(perms):
                    modelo = Modelo.objects.get(pk=request.POST['id'])                    
                    modelo.modelo = request.POST['modelo']
                    modelo.marcas_id = request.POST['marca_id']
                    modelo.save()
                    pre_values = json.loads(request.POST['current_data'])
                    self.audit_fields(pre_values, modelo)
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'   
            
            elif action == 'delete':
                perms = ('erp.delete_modelo',)
                if request.user.has_perms(perms):          
                    modelo =  Modelo.objects.get(pk=request.POST['id'])
                    modelo.delete()                    
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción' 

            elif action == 'search_marcas':
                data = []
                term = request.POST['term']
                marca = Marca.objects.filter(marca__icontains=term)                   
                for i in marca:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Modelos'
        context['entity'] = 'Modelos'
        context['btn_name'] = 'Nuevo Modelo'
        context['frmModelos'] = FormModelo()
        return context

    def audit_fields(self, pre_value, post_value):
        changes = []
        fields = [
            {'field': 'Nombre', 'value_ant': pre_value['modelo'], 'value_act': post_value.modelo},
            {'field': 'Marca', 'value_ant': pre_value['marcas']['marca'], 'value_act': post_value.marcas.marca},
        ]

        for i in fields:
            if i['value_ant'] != i['value_act']:
                changes.append(i)

        if len(changes) > 0:
            AuditMixin.fields_save(changes)