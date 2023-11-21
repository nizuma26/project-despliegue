import json
from core.erp.forms import FormCodbien
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.erp.mixins import Perms_Check
from core.erp.models import CodBienes, Unidad
from core.audit_log.mixins import AuditMixin

class CodBienListView(LoginRequiredMixin, Perms_Check, ListView):   
    model = CodBienes
    template_name = 'codbienes/list.html'
    permission_required = 'erp.view_codbienes'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in CodBienes.objects.all():
                    data.append(i.toJSON())

            elif action == 'add':
                perms = ('erp.add_codbienes',)
                if request.user.has_perms(perms):
                    code = CodBienes()                    
                    code.codbien = request.POST.get('codbien')
                    code.estado = request.POST.get('estado')
                    code.save()                    
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'                
            
            elif action == 'edit':
                perms = ('erp.change_codbienes',)
                if request.user.has_perms(perms):
                    code = CodBienes.objects.get(pk=request.POST['id'])                    
                    code.codbien = request.POST.get('codbien')
                    code.estado = request.POST.get('estado')
                    code.save()
                    fields = json.loads(request.POST['current_data'])
                    self.audit_fields(fields, code)
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'

            elif action == 'delete':
                perms = ('erp.delete_codbienes',)
                if request.user.has_perms(perms):
                    code = CodBienes.objects.get(pk=request.POST['id'])                   
                    code.delete()                   
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Codigos de Bien Nacional'
        context['entity'] = 'Codigos'
        context['btn_name'] = 'Nuevo Codigo'
        context['frmCodBien'] = FormCodbien()
        return context
    
    #PARA VERIFICAR SI LOS DATOS DEL REGISTRO SE HAN MODIFICADO O SIGUEN IGUAL
    def audit_fields(self, pre_value, post_value):
        changes = []
        fields = [
            {'field': 'Código de bien', 'value_ant': pre_value['codbien'], 'value_act': post_value.codbien},
            {'field': 'Estado', 'value_ant': pre_value['estado']['id'], 'value_act': post_value.estado},
        ]

        for i in fields:
            if i['value_ant'] != i['value_act']:
                changes.append(i)
        
        if len(changes) > 0:
            AuditMixin.fields_save(changes)