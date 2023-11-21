import json
from core.erp.forms import FormMarca
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.erp.mixins import Perms_Check
from core.erp.models import Marca
from core.audit_log.mixins import AuditMixin


class MarcaListView(LoginRequiredMixin, Perms_Check, ListView):   
    model = Marca
    template_name = 'marca/list.html'
    permission_required = 'erp.view_marca'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):        
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Marca.objects.all():
                    data.append(i.toJSON())

            elif action == 'add':
                perms = ('erp.add_marca',)
                if request.user.has_perms(perms):
                    marca = Marca()                    
                    marca.marca = request.POST.get('marca')
                    marca.save()
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'

            elif action == 'edit':
                perms = ('erp.change_marca',)
                if request.user.has_perms(perms):
                    marca = Marca.objects.get(pk=request.POST['id'])                    
                    marca.marca = request.POST.get('marca')
                    marca.save()
                    fields = json.loads(request.POST['current_data'])
                    self.audit_fields(fields['marca'], marca.marca)
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'

            elif action == 'delete':
                perms = ('erp.delete_marca',)
                if request.user.has_perms(perms):
                    marca = Marca.objects.get(pk=request.POST['id'])                    
                    marca.delete()
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción' 
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Marcas'
        context['entity'] = 'Marcas'
        context['btn_name'] = 'Nuevo Registro'
        context['frmMarca'] = FormMarca()
        return context
    
    def audit_fields(self, pre_value, post_value):
        changes = []

        if pre_value != post_value:
            changes.append({'field': 'Nombre', 'value_ant': pre_value, 'value_act': post_value})
        
        if len(changes) > 0:
            AuditMixin.fields_save(changes)