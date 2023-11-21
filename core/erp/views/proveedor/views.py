import json
from core.erp.forms import ProveedorForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.erp.mixins import Perms_Check
from core.erp.models import Proveedor
from core.audit_log.mixins import AuditMixin

class ProveedorListView(LoginRequiredMixin, Perms_Check, ListView):   
    model = Proveedor
    template_name = 'proveedor/list.html'
    permission_required = 'erp.view_proveedor'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Proveedor.objects.all():
                    data.append(i.toJSON())

            elif action == 'add':
                perms = ('erp.add_proveedor',)
                if request.user.has_perms(perms):
                    proveedor = Proveedor()
                    proveedor.empresa = request.POST['empresa']
                    proveedor.documento = request.POST['documento']
                    proveedor.ramo = request.POST['ramo']
                    proveedor.tipo_docu = request.POST['tipo_docu']
                    proveedor.represen = request.POST['represen']
                    proveedor.ced_repre = request.POST['ced_repre']
                    proveedor.tlf = request.POST['tlf']
                    proveedor.email = request.POST['email']
                    proveedor.direccion = request.POST['direccion']
                    proveedor.save()                    
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'
            
            elif action == 'edit':
                perms = ('erp.change_proveedor',)
                if request.user.has_perms(perms):
                    proveedor = Proveedor.objects.get(pk=request.POST['id'])
                    proveedor.empresa = request.POST['empresa']
                    proveedor.documento = request.POST['documento']
                    proveedor.ramo = request.POST['ramo']
                    proveedor.tipo_docu = request.POST['tipo_docu']
                    proveedor.represen = request.POST['represen']
                    proveedor.ced_repre = request.POST['ced_repre']
                    proveedor.tlf = request.POST['tlf']
                    proveedor.email = request.POST['email']
                    proveedor.direccion = request.POST['direccion']
                    proveedor.save()
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'
            
            elif action == 'fields_save':
                changes = json.loads(request.POST['changes'])
                if len(changes)>0:
                    AuditMixin.fields_save(changes)
            
            elif action == 'delete':
                perms = ('erp.delete_proveedor',)
                if request.user.has_perms(perms):          
                    proveedor =  Proveedor.objects.get(pk=request.POST['id'])
                    proveedor.delete()                    
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Proveedores'
        context['btn_name'] = 'Nuevo Proveedor'
        context['frmProvee'] = ProveedorForm()
        return context