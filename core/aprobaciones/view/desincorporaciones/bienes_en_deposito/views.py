from core.erp.forms import DesincAlmacenForm
from core.reportes.forms import ReportForm
from core.erp.models import DesincAlmacen, DetDesincAlmacen, ControlStock
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from core.erp.mixins import Perms_Check


class AprobacionDesincAlmacenFormView(LoginRequiredMixin, Perms_Check, FormView):
    model = DesincAlmacen
    form_class = ReportForm
    template_name = 'desincorporaciones/bienes_en_deposito/list.html'
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
                queryset = DesincAlmacen.objects.prefetch_related('usuario', 'almacen', 'tipo_desinc').filter(estado='PAP')
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(estado='PAP').filter(fecha_desinc__range=[start_date, end_date])
                for i in queryset:
                    item = {}
                    item['id'] = i.id
                    item['usuario'] = i.usuario.username
                    item['cod_desinc'] = i.cod_desinc
                    item['almacen'] = i.almacen.nombre
                    item['tipo_desinc'] = i.tipo_desinc.denominacion
                    item['fecha_desinc'] = i.fecha_desinc
                    item['total'] = i.total
                    item['estado'] = i.estado
                    data.append(item)

            elif action == 'search_detalle_prod':
                data = []
                for i in DetDesincAlmacen.objects.filter(desincorp_id=request.POST['id']):
                    item = {}
                    item['id'] = i.id
                    item['prodcate'] = i.prod.categorias.nombre
                    item['proddesc'] = i.prod.descripcion
                    item['prodnombre'] = i.prod.nombre
                    item['precio'] = i.precio
                    item['cant'] = i.cant
                    item['subtotal'] = i.subtotal
                    data.append(item)
                
            elif action == 'edit':
                desinc = DesincAlmacen.objects.get(id=request.POST['param_id'])
                desinc.estado = request.POST['new_estado']
                desinc.save()

                if desinc.estado == 'APR':
                    for det in DetDesincAlmacen.objects.filter(desincorp_id=request.POST['param_id']):
                        stock = ControlStock.objects.filter(almacenes_id=desinc.almacen_id, productos_id=det.prod_id)
                        for i in stock:
                            i.stock_actual -= det.cant
                            i.save()               
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Desincorporaciones en Almacén Por Aprobar'
        context['entity'] = 'Actualizar'
        context['frmStatusDesAlm'] = DesincAlmacenForm
        return context
