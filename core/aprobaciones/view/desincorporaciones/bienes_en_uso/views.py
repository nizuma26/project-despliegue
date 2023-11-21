from core.erp.forms import DesincProdForm
from core.reportes.forms import ReportForm
from core.erp.models import DesincProduc, DetDesincProd, InventarioBienes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from core.erp.mixins import Perms_Check

class AprobacionDesincorpFormView(LoginRequiredMixin, Perms_Check, FormView):
    model = DesincProduc
    form_class = ReportForm
    template_name = 'desincorporaciones/bienes_en_uso/list.html'
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
                queryset = DesincProduc.objects.prefetch_related('usuario', 'origen', 'tipo_desinc').filter(estado='PAP')
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(fecha_desinc__range=[start_date, end_date])
                for i in queryset:
                    item = {}
                    item['id'] = i.id
                    item['usuario'] = i.usuario.username
                    item['cod_desinc'] = i.cod_desinc
                    item['origen'] = i.origen.nombre
                    item['tipo_desinc'] = i.tipo_desinc.denominacion
                    item['fecha_desinc'] = i.fecha_desinc
                    item['estado'] = i.estado
                    data.append(item)                    

            elif action == 'detail':
                data = []
                for i in DetDesincProd.objects.prefetch_related('prod', 'codbien', 'codubica').filter(desinc_id=request.POST['id']):
                    item = {}
                    item['id'] = i.id
                    item['products'] = i.prod.nombre + ' - ' + i.prod.descripcion
                    item['category'] = i.prod.categorias.nombre
                    item['depart'] = i.codubica.nombre
                    item['codbien'] = i.codbien.codbien
                    item['user'] = i.desinc.usuario.username
                    item['status'] = i.desinc.get_estado_display()
                    item['resp_origen'] = i.desinc.respon_origen
                    item['obs'] = i.desinc.observ
                    data.append(item)

            elif action == 'edit':
                desinc = DesincProduc.objects.get(id=request.POST['id'])
                desinc.estado = request.POST['new_estado']
                desinc.save()
                estado = request.POST['new_estado']

                if estado == 'APR':
                    detail = DetDesincProd.objects.prefetch_related('prod', 'codbien', 'codubica').filter(desinc_id=desinc.id)
                    for i in detail:
                        invbienes = InventarioBienes.objects.prefetch_related('prod', 'unidad', 'ubica_fisica').filter(codbien_id=i.codbien_id)

                        invbienes.update(ult_proc='Desincorporado', tipo_proc_id=desinc.tipo_desinc_id, date_joined=desinc.fecha_desinc)

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Desincorporaciones por Aprobar'
        context['entity'] = 'Actualizar'
        context['frmStatusDes'] = DesincProdForm
        return context
