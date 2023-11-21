from django.db import transaction
from django.db.models import F
from core.aprobaciones.models import Aprobaciones
from core.erp.forms import IngresosForm
from core.erp.models import IngresoProduc, DetIngresoProduc, ControlStock, Seriales, Lotes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from core.reportes.forms import ReportForm
from core.erp.mixins import Perms_Check

class AprobIncorpFormView(LoginRequiredMixin, Perms_Check, FormView):
    model = IngresoProduc
    form_class = ReportForm
    template_name = 'incorporaciones/list.html'
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
                queryset = IngresoProduc.objects.select_related('tipo_ingreso', 'almacen', 'usuario').all()
                queryset = queryset.filter(estado='POR APROBAR')
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(fecha_ingreso__range=[start_date, end_date])
                for i in queryset:
                    item = {}
                    item['cod_ingreso'] = i.cod_ingreso
                    item['almacen'] = i.almacen.nombre
                    item['usuario'] = i.usuario.username
                    item['tipo_ingreso'] = i.tipo_ingreso.denominacion
                    item['fecha_ingreso'] = i.fecha_ingreso.strftime('%Y-%m-%d')
                    item['total'] = i.total
                    item['estado'] = i.estado
                    item['id'] = i.id
                    item['num_comprob'] = i.num_comprob
                    data.append(item)

            elif action == 'search_detalle_prod':
                data = []
                for i in DetIngresoProduc.objects.filter(ingresoPro_id=request.POST['id']):
                    data.append(i.toJSON())

            elif action == 'manage_state':
                print('GET ACTION')
                with transaction.atomic():
                    status = request.POST["new_status"]
                    motive = request.POST["motive"]
                    ingreso = IngresoProduc.objects.get(id=request.POST['id'])
                    ingreso.estado = status
                    ingreso.save()

                    Aprobaciones.objects.create(
                        user_id=self.request.user.id,
                        accion=status,
                        motivo=motive,
                        operacion='Incorporación',
                        codigo=ingreso.cod_ingreso
                    )

                    if ingreso.estado == 'APROBADO':
                        for det in DetIngresoProduc.objects.filter(ingresoPro_id=ingreso.id):
                            stock = ControlStock.objects.prefetch_related('productos', 'almacenes').filter(almacenes_id=ingreso.almacen_id, productos_id=det.prod_id).prefetch_related('productos')
                            if stock:                          
                                stock.update(stock_actual=F('stock_actual') + det.cant, precio=det.precio)
                                
                            else:
                                stock = ControlStock.objects.create(
                                    stock_actual = det.cant,
                                    precio = det.precio,
                                    almacenes_id = det.ingresoPro.almacen_id,
                                    productos_id = det.prod_id
                                )

                            for s in Seriales.objects.filter(incorp_id=ingreso.id):
                                for id_stock in ControlStock.objects.filter(almacenes_id=ingreso.almacen_id, productos_id=s.prod_id):
                                    s.stock_id = id_stock.id
                                    s.disp = "Disponible"
                                    s.save()

                            for l in Lotes.objects.filter(incorp_id=ingreso.id):
                                for id_stock in ControlStock.objects.filter(almacenes_id=ingreso.almacen_id, productos_id=l.prod_id):
                                    l.stock_id = id_stock.id
                                    l.save()

                    data = {'type': 'status_request_notification', 
                            'url': f'/erp/ingreso/detail/{ingreso.id}/',
                            'message': f'La incorporación {ingreso.cod_ingreso} ha sido {status.lower()}', 
                            'title': 'Haga clic para ver el detalle de la incorporación',
                            'user_id': ingreso.usuario.id, 
                            'state': ingreso.estado,
                            }                                                  
                           
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Incorporaciones por Aprobar'
        context['entity'] = 'Actualizar'
        context['options'] = {'APR': 'APROBADO', 'REC': 'RECHAZADO', 'RET': 'RETORNADO'}
        context['url'] = '/aprobaciones/incorporacion/list/'
        return context
