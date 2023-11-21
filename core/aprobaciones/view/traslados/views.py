import json
from core.erp.forms import TrasladoProdForm
from core.reportes.forms import ReportForm
from core.erp.models import TrasladoProduc, DetTrasladoProd, InventarioBienes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
#from xhtml2pdf import pisa
from core.erp.mixins import ValidatePermissionRequiredMixin

class AprobacionTrasFormView(LoginRequiredMixin, ValidatePermissionRequiredMixin, FormView):
    model = TrasladoProduc
    form_class = ReportForm
    template_name = 'traslados/list.html'
    permission_required = 'aprobaciones.approve_movimientos'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = TrasladoProduc.objects.filter(estado='PAP')
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(fecha_traslado__range=[start_date, end_date])
                for i in queryset:
                    item = {}
                    item['id'] = i.id
                    item['usuario'] = i.usuario.username
                    item['cod_traslado'] = i.cod_traslado
                    item['origen'] = i.origen.nombre
                    item['destino'] = i.destino.nombre
                    item['tipo_traslado'] = i.tipo_traslado.denominacion
                    item['fecha_traslado'] = i.fecha_traslado
                    item['estado'] = i.estado
                    data.append(item)

            elif action == 'detail':
                data = []                
                for i in DetTrasladoProd.objects.filter(trasproduc_id=request.POST['id']).prefetch_related('prod'):
                    item = {}
                    item['products'] = i.prod.nombre + ' / ' +i.prod.descripcion
                    item['depart_origen'] = i.codubica.nombre
                    item['depart_destino'] = i.ubica_destino.nombre
                    item['codbien'] = i.codbien.codbien
                    item['user'] = i.trasproduc.usuario.username
                    item['observ'] = i.trasproduc.observ
                    item['resp_origen'] = i.trasproduc.respon_origen
                    item['resp_destino'] = i.trasproduc.respon_destino
                    data.append(item)
            
            elif action == 'edit':
                traslado = TrasladoProduc.objects.get(id=request.POST['param_id'])
                traslado.estado = request.POST['new_estado']
                traslado.save()

                if traslado.estado == 'APR':
                    detail = DetTrasladoProd.objects.filter(trasproduc_id=traslado.id)
                    for i in detail:
                        invbienes = InventarioBienes.objects.filter(codbien_id=i.codbien_id)
                        invbienes.update(ult_proc='Traslado', unidad_id=traslado.destino_id, ubica_fisica_id=i.ubica_destino_id, tipo_proc_id=traslado.tipo_traslado_id, date_joined=traslado.fecha_traslado)

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Traslados por Aprobar'
        context['entity'] = 'Actualizar'
        context['frmStatusTras'] = TrasladoProdForm
        return context
