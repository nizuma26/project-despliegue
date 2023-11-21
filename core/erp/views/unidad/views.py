import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from core.erp.models import Unidad
from core.erp.mixins import Perms_Check
from core.erp.forms import UnidadForm
from core.audit_log.mixins import AuditMixin

class UnidadListView(LoginRequiredMixin, Perms_Check, ListView):
    model = Unidad
    template_name = 'unidad/list.html'
    permission_required = 'erp.view_unidad'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Unidad.objects.all():
                    data.append(i.toJSON())

            elif action == 'add':
                perms = ('erp.add_unidad',)
                if request.user.has_perms(perms):
                    unidad = Unidad()
                    unidad.nombre = request.POST['nombre']
                    unidad.direccion = request.POST['direccion']
                    unidad.rif = request.POST['rif']
                    unidad.ced_resp = request.POST['ced_resp']
                    unidad.nombrejefe = request.POST['nombrejefe']
                    unidad.email = request.POST['email']
                    unidad.tlf = request.POST['tlf']
                    unidad.tipo_unidad = request.POST['tipo_unidad']
                    unidad.solic_almacen = request.POST.get('solic_almacen') == 'on'
                    unidad.save()                    
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'
            
            elif action == 'edit':
                perms = ('erp.change_unidad',)
                if request.user.has_perms(perms):
                    unidad = Unidad.objects.get(pk=request.POST['id'])
                    unidad.nombre = request.POST['nombre']
                    unidad.direccion = request.POST.get('direccion', )
                    unidad.rif = request.POST['rif']
                    unidad.ced_resp = request.POST['ced_resp']
                    unidad.nombrejefe = request.POST['nombrejefe']
                    unidad.email = request.POST.get('email', )
                    unidad.tlf = request.POST.get('tlf', )
                    unidad.tipo_unidad = request.POST['tipo_unidad']
                    unidad.solic_almacen = request.POST.get('solic_almacen') == 'on'
                    unidad.save()
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'
            
            elif action == 'fields_save':
                changes = json.loads(request.POST['changes'])
                if len(changes)>0:
                    AuditMixin.fields_save(changes)
            
            elif action == 'delete':
                perms = ('erp.delete_unidad',)
                if request.user.has_perms(perms):          
                    unidad =  Unidad.objects.get(pk=request.POST['id'])
                    unidad.delete()                    
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción' 
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Unidades'
        context['btn_name'] = 'Nueva unidad'
        context['entity'] = 'Unidades'
        context['frmUnidad'] = UnidadForm()
        return context