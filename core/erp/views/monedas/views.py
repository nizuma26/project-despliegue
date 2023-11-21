import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core.erp.forms import FormMoneda
from core.erp.mixins import Perms_Check
from core.erp.models import Moneda
from core.audit_log.mixins import AuditMixin

class MonedaListView(LoginRequiredMixin, Perms_Check, ListView):
    model = Moneda
    template_name = 'monedas/list.html'
    permission_required = 'erp.view_moneda'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']           
            if action == 'searchdata':
                data = []
                for i in Moneda.objects.all():
                    data.append(i.toJSON())

            elif action == 'add':
                perms = ('erp.add_moneda',)
                if request.user.has_perms(perms):
                    moneda = Moneda()                    
                    moneda.codigo = request.POST.get('codigo')
                    moneda.pais = request.POST.get('pais')
                    moneda.moneda = request.POST.get('moneda')
                    moneda.simbolo = request.POST.get('simbolo')
                    moneda.tasa_cambio = request.POST.get('tasa_cambio')
                    moneda.status = request.POST.get('status') == 'on'
                    moneda.save()                    
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'                
            
            elif action == 'edit':
                perms = ('erp.change_moneda',)
                if request.user.has_perms(perms):
                    moneda = Moneda.objects.get(pk=request.POST['id'])                    
                    moneda.codigo = request.POST.get('codigo')
                    moneda.pais = request.POST.get('pais')
                    moneda.moneda = request.POST.get('moneda')
                    moneda.simbolo = request.POST.get('simbolo')
                    moneda.tasa_cambio = request.POST.get('tasa_cambio')
                    moneda.status = request.POST.get('status') == 'on'
                    moneda.save()                                        
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'
            
            elif action == 'fields_save':
                changes = json.loads(request.POST['changes'])
                if len(changes)>0:
                    AuditMixin.fields_save(changes)

            elif action == 'delete':
                perms = ('erp.delete_moneda',)
                if request.user.has_perms(perms):
                    moneda = Moneda.objects.get(pk=request.POST['id'])
                    moneda.delete()                    
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'

            # elif action == 'activar':
            #     with transaction.atomic():
            #         perms = ('user.change_producto',)
            #         if request.user.has_perms(perms):
            #             status = Producto.objects.get(id=request.POST['id'])
            #             status.activo = True
            #             status.save()
            #         else:
            #             data['error'] = 'No tiene permisos para realizar esta acción'        
            
            # elif action == 'inactivar':
            #     with transaction.atomic():
            #         perms = ('user.change_producto',)
            #         if request.user.has_perms(perms):
            #             status = Producto.objects.get(id=request.POST['id'])
            #             status.activo = False
            #             status.save()
            #         else:
            #             data['error'] = 'No tiene permisos para realizar esta acción'

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Monedas'
        # context['create_url'] = reverse_lazy('erp:monedas_create')
        # context['list_url'] = reverse_lazy('erp:monedas_list')
        context['btn_name'] = 'Nuevo Registro'
        context['frmMoneda'] = FormMoneda()
        context['entity'] = 'Monedas'
        return context