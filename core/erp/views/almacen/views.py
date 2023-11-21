import json
from core.erp.forms import FormAlmacen
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.erp.mixins import Perms_Check
from core.erp.models import Almacen, Unidad
from core.audit_log.mixins import AuditMixin


class AlmacenListView(LoginRequiredMixin, Perms_Check, ListView):   
    model = Almacen
    template_name = 'almacen/list.html'
    permission_required = 'erp.view_almacen'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Almacen.objects.all():
                    data.append(i.toJSON())

            elif action == 'add':
                perms = ('erp.add_almacen',)
                if request.user.has_perms(perms):
                    almacen = Almacen()                    
                    almacen.codigo = request.POST.get('codigo')
                    almacen.nombre = request.POST.get('nombre')
                    almacen.responsable = request.POST.get('responsable')
                    almacen.cedula = request.POST.get('cedula')
                    almacen.unidad = Unidad.objects.get(id = request.POST.get('unidad'))
                    #Unidad.objects.get(id = request.POST.get('nombre'))
                    almacen.save()                    
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción' 

            elif action == 'edit':
                perms = ('erp.change_almacen',)
                if request.user.has_perms(perms):
                    almacen = Almacen.objects.get(pk=request.POST['id'])                    
                    almacen.codigo = request.POST.get('codigo')
                    almacen.nombre = request.POST.get('nombre')
                    almacen.responsable = request.POST.get('responsable')
                    almacen.cedula = request.POST.get('cedula')
                    almacen.unidad = Unidad.objects.get(id = request.POST.get('unidad'))
                    almacen.save()
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'

            elif action == 'fields_save':
                changes = json.loads(request.POST['changes'])
                AuditMixin.fields_save(changes)

            elif action == 'delete':
                perms = ('erp.delete_almacen',)
                if request.user.has_perms(perms):
                    almacen = Almacen.objects.get(pk=request.POST['id'])
                    almacen.delete()
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción' 
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Almacen'
        context['entity'] = 'Almacen'
        context['btn_name'] = 'Nuevo Almacen'
        context['frmAlmacen'] = FormAlmacen()
        return context
