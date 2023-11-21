import json
from core.erp.forms import FormGrupo
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.erp.mixins import Perms_Check
from core.erp.models import GrupoCtaBienes
from core.audit_log.mixins import AuditMixin

class GrupoListView(LoginRequiredMixin, Perms_Check, ListView):   
    model = GrupoCtaBienes
    template_name = 'grupo/list.html'
    permission_required = 'erp.view_grupoctabienes'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in GrupoCtaBienes.objects.all():
                    data.append(i.toJSON())

            elif action == 'add':
                perms = ('erp.add_grupoctabienes',)
                if request.user.has_perms(perms):                 
                    grupo = GrupoCtaBienes()                    
                    grupo.cod_grupo = request.POST['cod_grupo']
                    grupo.nombre = request.POST['nombre']  
                    grupo.save()                    
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'

            elif action == 'edit':
                perms = ('erp.change_grupoctabienes',)
                if request.user.has_perms(perms):                 
                    grupo = GrupoCtaBienes.objects.get(pk=request.POST['id'])                    
                    grupo.cod_grupo = request.POST['cod_grupo']
                    grupo.nombre = request.POST['nombre']  
                    grupo.save()
                    pre_values = json.loads(request.POST['current_data'])
                    self.audit_fields(pre_values, grupo)
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'

            elif action == 'delete':
                perms = ('erp.add_grupoctabienes',)
                if request.user.has_perms(perms):                 
                    grupo = GrupoCtaBienes.objects.get(pk=request.POST['id'])
                    grupo.delete()                    
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Grupos de Productos'
        context['btn_name'] = 'Nuevo Registro'
        context['frmGrupo'] = FormGrupo()
        return context
    
    #PARA VERIFICAR SI LOS DATOS DEL REGISTRO SE HAN MODIFICADO O SIGUEN IGUAL
    def audit_fields(self, pre_value, post_value):
        changes = []
        fields = [
            {'field': 'Código', 'value_ant': pre_value['cod_grupo'], 'value_act': post_value.cod_grupo},
            {'field': 'Nombre', 'value_ant': pre_value['nombre'], 'value_act': post_value.nombre},
        ]

        for i in fields:
            if i['value_ant'] != i['value_act']:
                changes.append(i)

        if len(changes) > 0:
            AuditMixin.fields_save(changes)