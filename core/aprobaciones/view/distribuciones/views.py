from django.db import transaction
from django.db.models import F
from core.erp.forms import SalidasForm
from core.reportes.forms import ReportForm
from core.erp.models import SalidaProduc, DetSalidaProd, DetSalidaInsumos, InventarioBienes, ControlStock
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from core.erp.mixins import Perms_Check
from core.aprobaciones.models import Aprobaciones


class AprobacionDistFormView(LoginRequiredMixin, Perms_Check, FormView):
    model = SalidaProduc
    form_class = ReportForm
    template_name = 'distribuciones/list.html'
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
                queryset = SalidaProduc.objects.select_related('usuario', 'tipo_salida', 'destino', 'origen').filter(estado='POR APROBAR')
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(fecha_salida__range=[start_date, end_date])
                for i in queryset:
                    item = {}
                    item['codigo'] = i.cod_salida
                    item['usuario'] = i.usuario.username
                    item['tipo_salida'] = i.tipo_salida.denominacion
                    item['origen'] = i.origen.nombre
                    item['destino'] = i.destino.nombre
                    item['fecha'] = i.fecha_salida.strftime('%Y-%m-%d')
                    item['estado'] = i.get_estado_display()
                    item['id'] = i.id
                    data.append(item)

            elif action == 'search_detalle_prod':
                data = []
                for i in DetSalidaProd.objects.filter(salida_id=request.POST['id']):
                    item = {}
                    item['id'] = i.id
                    item['nombre'] = i.codubica.nombre
                    item['codbien'] = i.codbien.codbien
                    item['proddesc'] = i.prod.descripcion
                    item['prodcateg'] = i.prod.categorias.nombre
                    item['prodnombre'] = i.prod.nombre
                    item['precio'] = i.precio
                    data.append(item)

            elif action == 'search_detalle_mc':
                data = []
                for i in DetSalidaInsumos.objects.filter(salida_id=request.POST['id']):
                    item = {}
                    item['id'] = i.id
                    item['prod'] = i.prod.nombre +' / '+ i.prod.descripcion
                    item['categoria'] = i.prod.categorias.nombre
                    item['precio'] = i.precio
                    item['cantidad'] = i.cant
                    item['lote'] = i.nro_lote
                    item['fecha_venc'] = i.fecha_venc
                    data.append(item)
            
            elif action == 'manage_state':
                print('manage')
                with transaction.atomic():
                    status = request.POST["new_status"]
                    motive = request.POST["motive"]
                    id = request.POST["id"]
                    print('ID', id)
                    salida = SalidaProduc.objects.select_related('origen', 'destino', 'tipo_salida').get(id=id)
                    salida.estado = status
                    salida.save()

                    Aprobaciones.objects.create(
                        user_id=self.request.user.id,
                        accion=status,
                        motivo=motive,
                        operacion='Distribución',
                        codigo=salida.cod_salida
                    )
                    print('APPROVE', salida.destino.id)

                    if salida.estado == 'APROBADO':
                        detail = DetSalidaProd.objects.prefetch_related('salida','prod').filter(salida_id=salida.id)
                        if salida.detsalidaprod_salida_set.all().count() > 0:
                            detail = DetSalidaProd.objects.prefetch_related('salida','prod').filter(salida_id=salida.id)
                            for sal in detail:
                                almacen_origen = ControlStock.objects.filter(almacenes_id=salida.origen_id, productos_id=sal.prod_id)
                                almacen_destino = ControlStock.objects.filter(almacenes_id=salida.destino_id, productos_id=sal.prod_id)
                                
                                for s in almacen_origen:
                                    s.stock_actual -= sal.cant
                                    s.apartados -= sal.cant
                                    s.save()
                                
                                if (almacen_destino):
                                    almacen_destino.update(stock_actual=F('stock_actual') + sal.cant, precio=sal.precio)
                                else:
                                    products = ControlStock.objects.create(
                                        stock_actual = sal.cant,
                                        precio = sal.precio,
                                        almacenes_id = salida.destino.id,
                                        productos_id = sal.prod.id
                                    )
                                invbienes = InventarioBienes()
                                invbienes.codbien_id = sal.codbien_id
                                invbienes.prod_id = sal.prod_id
                                invbienes.unidad_id = sal.salida.destino_id
                                invbienes.ubica_fisica_id = sal.codubica_id
                                invbienes.tipo_proc_id = sal.salida.tipo_salida_id
                                invbienes.date_joined = sal.salida.fecha_salida
                                invbienes.ult_proc = 'DIST'
                                invbienes.salida_id = sal.salida_id
                                invbienes.save()
                        else:
                            mtc = salida.det_salidainsumos_set.all()
                            for sal in mtc:
                                almacen_origen = ControlStock.objects.prefetch_related('almacenes','productos').filter(almacenes_id=salida.origen.id, productos_id=sal.prod.id)
                                almacen_destino = ControlStock.objects.filter(almacenes_id=salida.destino.id, productos_id=sal.prod.id)
                                for s in almacen_origen:
                                    s.stock_actual -= sal.cant
                                    s.apartados -= sal.cant
                                    s.save()

                                if (almacen_destino):
                                    almacen_destino.update(stock_actual=F('stock_actual') + sal.cant, precio=sal.precio)
                                else:
                                    products = ControlStock.objects.create(
                                        stock_actual = sal.cant,
                                        precio = sal.precio,
                                        almacenes_id = salida.destino_id,
                                        productos_id = sal.prod_id
                                    )
                                

                    data = {'type': 'status_request_notification', 
                            'url': f'/erp/salida/detail/{salida.id}/',
                            'message': f'La distribución {salida.cod_salida} ha sido {status.lower()}', 
                            'title': 'Haga clic para ver el detalle de la distribución',
                            'user_id': salida.usuario.id, 
                            'state': status,
                            }       
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Distribuciones por Aprobar'
        context['entity'] = 'Actualizar'
        context['options'] = {'APR': 'APROBADO', 'REC': 'RECHAZADO', 'RET': 'RETORNADO'}
        context['url'] = '/aprobaciones/distribucion/list/'
        return context