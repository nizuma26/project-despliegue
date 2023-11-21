import json
from core.erp.forms import FormConcepMov
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.erp.mixins import Perms_Check
from core.erp.models import ConcepMovimiento
from core.audit_log.mixins import AuditMixin


class ConcepMovListView(LoginRequiredMixin, Perms_Check, ListView):   
    model = ConcepMovimiento
    template_name = 'concepmov/list.html'
    permission_required = 'erp.view_concepmovimiento'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in ConcepMovimiento.objects.all():
                    data.append(i.toJSON())

            elif action == 'add':
                perms = ('erp.add_concepmovimiento',)
                if request.user.has_perms(perms):
                    concept = ConcepMovimiento()                    
                    concept.codigo = request.POST.get('codigo')
                    concept.denominacion = request.POST.get('denominacion')
                    concept.estado = request.POST.get('estado')
                    concept.tipo_conc = request.POST.get('tipo_conc')
                    concept.salida_bienes = request.POST.get('salida_bienes', None)
                    concept.save()                    
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'                
            
            elif action == 'edit':
                perms = ('erp.change_concepmovimiento',)
                if request.user.has_perms(perms):
                    print('asdasd')
                    concept = ConcepMovimiento.objects.get(pk=request.POST['id'])                    
                    concept.codigo = request.POST.get('codigo')
                    concept.denominacion = request.POST.get('denominacion')
                    concept.estado = request.POST.get('estado')
                    concept.tipo_conc = request.POST.get('tipo_conc')
                    concept.salida_bienes = request.POST.get('salida_bienes', None)
                    concept.save()                                        
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'
            
            elif action == 'fields_save':
                changes = json.loads(request.POST['changes'])
                AuditMixin.fields_save(changes)

            elif action == 'delete':
                perms = ('erp.change_concepmovimiento',)
                if request.user.has_perms(perms):
                    concept = ConcepMovimiento.objects.get(pk=request.POST['id'])
                    concept.delete()                    
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de conceptos de movimientos'
        context['entity'] = 'Conceptos'
        context['btn_name'] = 'Nuevo Concepto'
        context['frmConcepMov'] = FormConcepMov()
        return context