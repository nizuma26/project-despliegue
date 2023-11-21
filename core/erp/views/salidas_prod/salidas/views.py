import json
import os
from django.conf import settings
from django.db.models import F
from django.db import transaction
from django.db.models import Q
from core.erp.forms import SalidasForm, UnidadForm, FormDepart, FormConcepMov
from core.reportes.forms import ReportForm
from core.erp.models import ControlStock, Unidad, SalidaProduc, DetSalidaProd, DetSalidaInsumos, Almacen, Empresa, Departamento, CodBienes, ConcepMovimiento
from core.aprobaciones.models import Aprobaciones
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, CreateView, UpdateView, DetailView, View
from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.urls import reverse_lazy
from decimal import Decimal
from datetime import date, datetime
from core.erp.mixins import Perms_Check
from core.solicitudes.models import Solicitudes

class SalidaListView(LoginRequiredMixin, Perms_Check, FormView):
    model = SalidaProduc
    form_class = ReportForm
    template_name = 'salidas_prod/list.html'
    permission_required = 'erp.view_salidaproduc'

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
                queryset = SalidaProduc.objects.prefetch_related('tipo_salida', 'origen', 'destino').all()
                #print(len(queryset.detsalidaprod_salida_set.all()))
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(fecha_salida__range=[start_date, end_date])
                for i in queryset:
                    item = {}
                    item['codigo'] = i.cod_salida
                    item['tipo_salida'] = {'denominacion': i.tipo_salida.denominacion, 'bienes': i.tipo_salida.salida_bienes}
                    item['tipo_sal'] = i.tipo_salida.codigo
                    item['origen'] = i.origen.nombre
                    item['destino'] = i.destino.nombre
                    item['fecha'] = i.fecha_salida.strftime('%Y-%m-%d')
                    item['total'] = i.total
                    item['estado'] = i.estado
                    item['id'] = i.id
                    item['det'] = i.detsalidaprod_salida_set.all().count()
                    data.append(item)                

            elif action == 'detail_bm':
                data = []
                for i in DetSalidaProd.objects.prefetch_related('prod', 'salida', 'codbien', 'codubica').filter(salida_id=request.POST['id']):
                    item = {}
                    item['id'] = i.id
                    item['codubica'] = i.codubica.nombre
                    item['codbien'] = i.codbien.codbien
                    item['category'] = i.prod.categorias.nombre
                    item['product'] = i.prod.nombre + ' / ' +i.prod.descripcion
                    item['price'] = i.precio
                    data.append(item)
            
            elif action == 'detail_mc':
                data = []
                for i in DetSalidaInsumos.objects.prefetch_related('prod', 'salida').filter(salida_id=request.POST['id']):
                    item = {}
                    item['id'] = i.id
                    item['products'] = i.prod.nombre +' / '+ i.prod.descripcion
                    item['categoria'] = i.prod.categorias.nombre
                    item['precio'] = i.precio
                    item['cantidad'] = i.cant
                    item['lote'] = i.nro_lote
                    item['fecha_venc'] = i.fecha_venc
                    data.append(item)

            elif action == 'delete':
                perms = ('erp.delete_salidaproduc',)
                if request.user.has_perms(perms):
                    salida = SalidaProduc.objects.get(pk=request.POST['id'])
                    salida.delete()
                else:
                    data['error'] = 'No tiene permisos para realizar esta acción'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Distribución de Productos'
        context['create_url'] = reverse_lazy('erp:salida_create')
        context['list_url'] = reverse_lazy('erp:salida_list')
        context['entity'] = 'Distribuciones'
        context['btn_name'] = 'Nuevo Registro'
       # context['form'] = SalidasForm()
        return context

class SalidaCreateView(LoginRequiredMixin, Perms_Check, CreateView):
    model = SalidaProduc
    form_class = SalidasForm
    template_name = 'salidas_prod/create.html'
    success_url = reverse_lazy('erp:salida_list')
    url_redirect = success_url
    permission_required = 'erp.add_salidaproduc'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def reserved(self, almacen, productos):
        for i in productos:
            stock = ControlStock.objects.filter(almacenes_id=almacen, productos_id=i['id'])
            stock.update(apartados=F('apartados') + i['cant'])
            print('ALMACEN_ID: ', almacen, 'PRODUCTOS: ', i['id'])

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            
            if action == 'search_products':
                data = []                 
                datos_cantprod = json.loads(request.POST['datos_cantprod'])
                term = request.POST['term'].strip()                
                products = ControlStock.objects.filter(almacenes_id__in=request.POST['idorigen'], stock_actual__gt=0, productos__activo__in='1', productos__grupobien__cod_grupo='02').prefetch_related('productos', 'almacenes')
                
                for i in products:
                    for l in datos_cantprod:
                        if(i.productos.id == l['id']):
                            i.stock_actual= int(i.stock_actual) - int(l['cantprod'])                         
                    if(i.stock_actual>0):
                        item = {}
                        item['id'] = i.productos.id
                        item['full_name'] = i.productos.nombre + ' / ' + i.productos.descripcion
                        item['categoria'] = i.productos.categorias.nombre
                        item['imagen'] = i.productos.get_imagen()
                        item['precio'] = i.precio
                        item['stock'] = i.stock_actual
                        item['reserved'] = i.apartados
                        data.append(item) 
            
            elif action == 'search_suministros':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                products = ControlStock.objects.prefetch_related('productos', 'almacenes').filter(almacenes_id__in=request.POST['idorigen2'], 
                stock_actual__gt=0, productos__activo__in='1', productos__grupobien__cod_grupo='04').exclude(productos_id__in=ids_exclude)
                for i in products:
                    item = {}
                    item['id'] = i.productos.id
                    item['codigo'] = i.productos.codigo
                    item['imagen'] = i.productos.get_imagen()
                    item['full_name'] = f'{i.productos.nombre} {i.productos.descripcion}'
                    item['stock_actual'] = i.stock_actual
                    item['reserved'] = i.apartados
                    item['precio'] = i.precio
                    item['lote'] = i.productos.lote
                    item['nro_lote'] = ""
                    item['fecha_venc'] = ""
                    data.append(item)
                    
            elif action == 'search_autocomplete':
                data = []
                datos_cantprod = json.loads(request.POST['datos_cantprod'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text':term})
                products = ControlStock.objects.prefetch_related('productos', 'almacenes').filter(almacenes_id__in=request.POST['idorigen'], stock_actual__gt=0, productos__activo__in='1', productos__grupobien__cod_grupo='02')

                if len(term):
                    products = products.filter(productos__nombre__icontains=term)

                for i in products[0:20]:
                    for l in datos_cantprod:
                        if(i.productos.id == l['id']):
                            i.stock_actual= int(i.stock_actual) - int(l['cantprod'])                         
                        
                    if(i.stock_actual>0):
                        item = {}
                        item['id'] = i.productos.id
                        item['full_name'] = i.productos.nombre + ' / ' + i.productos.descripcion
                        item['categoria'] = i.productos.categorias.nombre
                        item['imagen'] = i.productos.get_imagen()
                        item['precio'] = i.precio
                        item['stock'] = i.stock_actual
                        item['text'] = i.productos.nombre
                        data.append(item)

            elif action == 'search_autocomplete_suminist':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text':term})
                products = ControlStock.objects.filter(almacenes_id__in=request.POST['idorigen2'], stock_actual__gt=0, productos__activo__in='1', productos__grupobien__cod_grupo='04')
                
                if len(term):
                    products = products.filter(productos__nombre__icontains=term).exclude(productos_id__in=ids_exclude)
                
                for i in products[0:20]:
                    item = {}
                    item['id'] = i.productos.id
                    item['codigo'] = i.productos.codigo
                    item['imagen'] = i.productos.get_imagen()
                    item['full_name'] = f'{i.productos.nombre} {i.productos.descripcion}'
                    item['stock_actual'] = i.stock_actual
                    item['precio'] = i.precio
                    item['lote'] = i.productos.lote
                    item['nro_lote'] = ""
                    item['fecha_venc'] = ""
                    item['text'] = i.productos.nombre
                    data.append(item)

            elif action == 'add':
                with transaction.atomic():
                    code = request.POST['code']
                    salidas = json.loads(request.POST['salidas'])
                    salida = SalidaProduc()
                    salida.cod_salida = salidas['cod_salida']
                    salida.origen_id = salidas['origen']
                    salida.respon_origen = salidas['respon_origen']
                    salida.destino_id = salidas['destino']
                    salida.respon_destino = salidas['respon_destino']
                    salida.tipo_salida_id = salidas['tipo_salida']
                    salida.tipo_comprob = salidas['tipo_comprob']
                    salida.num_comprob = salidas['num_comprob']
                    salida.subtotal = Decimal(salidas['subtotal'])
                    salida.iva = Decimal(salidas['iva'])
                    salida.total = Decimal(salidas['total'])
                    salida.fecha_salida = salidas['fecha_salida']
                    salida.usuario = self.request.user
                    salida.observ = salidas['observ']
                    salida.estado = salidas['estado']
                    salida.save()

                    if len(salidas['produc_sal']) > 0:
                        self.reserved(salidas['origen'], salidas['produc_sal'])
                        if code == '51':
                            depart = Departamento.objects.filter(nombre='Depósito').values('id').first()
                            if (depart):
                                print('EXISTE')
                                print('DEPART', depart['id'])
                                for i in salidas['produc_sal']:
                                    det = DetSalidaProd()
                                    det.precio = Decimal(i['precio'])
                                    det.cant = 1
                                    det.subtotal = Decimal(i['subtotal'])
                                    det.codbien_id = int(i['codbien']['id'])
                                    det.codubica_id = depart['id']
                                    det.salida_id = salida.id
                                    det.prod_id = i['id']
                                    det.save()
                            
                                    det.codbien.estado = 'ASI'
                                    det.codbien.save()             
                            else:
                                deposito = Departamento.objects.create(
                                    nombre='Depósito'
                                )
                                for i in salidas['produc_sal']:
                                    det = DetSalidaProd()
                                    det.precio = Decimal(i['precio'])
                                    det.cant = 1
                                    det.subtotal = Decimal(i['subtotal'])
                                    det.codbien_id = int(i['codbien']['id'])
                                    det.codubica_id = deposito.id
                                    det.salida_id = salida.id
                                    det.prod_id = i['id']
                                    det.save()
                                    
                                    det.codbien.estado = 'ASI'
                                    det.codbien.save()
                                print('NO EXISTE')
                        else:
                            for i in salidas['produc_sal']:
                                det = DetSalidaProd()
                                det.precio = Decimal(i['precio'])
                                det.cant = 1
                                det.subtotal = Decimal(i['subtotal'])
                                det.codbien_id = int(i['codbien']['id'])
                                det.codubica_id = int(i['codubica']['id'])
                                det.salida_id = salida.id
                                det.prod_id = i['id']
                                det.save()
                                
                                det.codbien.estado = 'ASI'
                                det.codbien.save()                        
                    else:
                        self.reserved(salidas['origen'], salidas['produc_sal2'])
                        for i in salidas['produc_sal2']:
                            det = DetSalidaInsumos()
                            det.precio = Decimal(i['precio'])
                            det.cant = int(i['cant'])
                            det.subtotal = Decimal(i['subtotal'])
                            det.nro_lote = i['nro_lote']                       
                            det.fecha_venc = i['fecha_venc']
                            det.salida_id = salida.id
                            det.prod_id = i['id']
                            det.save()
                            
                    image = str(salida.usuario.image)
                    data = {'type': 'create_operation_notification',
                            'url': f'/erp/salida/detail/{salida.id}/',
                            'message': f'{salida.usuario.username} ha realizado la distribución {salida.cod_salida}', 
                            'status': salida.estado,
                            'title': salida.tipo_salida.denominacion,
                            'image': image,
                            'user_id': salida.usuario.id,
                            'permissions': 'approve_movimientos'
                            }
            
            elif action == 'type_bienes':
                id = request.POST['id']
                concepto = ConcepMovimiento.objects.filter(id=id).values('salida_bienes', 'codigo').first()
                data['salida_bienes'] = concepto['salida_bienes']
                data['codigo'] = concepto['codigo']
                print('data: ', data)

            elif action == 'search_responorigen':
                data = []
                for i in Unidad.objects.filter(id=request.POST['id']):
                    item = {}
                    item['nombrejefe'] = i.nombrejefe + ' - ' + i.ced_resp
                    item['unidad'] = i.tipo_unidad
                    data.append(item)
                    
            elif action == 'busca_ubicacionfisica':
                data = []
                term = request.POST['term'].strip()
                ubicafisica = Departamento.objects.filter()
                if len(term):
                    ubicafisica = ubicafisica.filter(nombre__icontains=term)
                for i in ubicafisica[0:10]:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            
            elif action == 'busca_codbien':
                data = []
                ids_exclude = json.loads(request.POST['idsCodbien'])
                term = request.POST['term'].strip()
                codbienes = CodBienes.objects.filter(estado__icontains='SAS')

                if len(term):
                    codbienes = codbienes.filter(codbien__icontains=term)
                for i in codbienes.exclude(id__in=ids_exclude)[0:6]:
                    item = i.toJSON()
                    item['value'] = i.codbien
                    data.append(item)

            elif action == 'create_unidad':
                with transaction.atomic():
                    frmDestino =  UnidadForm(request.POST)
                    data = frmDestino.save()
            elif action == 'create_departamento':
                with transaction.atomic():
                    frmDepar =  FormDepart(request.POST)
                    data = frmDepar.save()
            
            elif action == 'create_concepto':
                with transaction.atomic():
                    frmConcepMov =  FormConcepMov(request.POST)
                    data = frmConcepMov.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creando nueva Distribución'
        context['entity'] = 'Distribuciones'
        context['url'] = '/erp/salida/add/'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['iva'] = Empresa.objects.values('nameimpuesto', ('iva')).last()
        context['frmUnidad'] = UnidadForm()
        context['frmDepart'] = FormDepart()
        context['frmConcepMov'] = FormConcepMov()
        context['det'] = []
        return context

class SalidaUpdateView(LoginRequiredMixin, Perms_Check, UpdateView):
    model = SalidaProduc
    form_class = SalidasForm
    template_name = 'salidas_prod/create.html'
    success_url = reverse_lazy('erp:salida_list')
    url_redirect = success_url
    permission_required = 'erp.change_salidaproduc'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def reserved(self, almacen, productos):
        for i in productos:
            stock = ControlStock.objects.filter(almacenes_id=almacen, productos_id=i['id'])
            stock.update(apartados=F('apartados') + i['cant'])

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = SalidasForm(instance=instance)
        form.fields['destino'].queryset = Unidad.objects.filter(id=instance.destino.id)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'detail_data':
                data = []
                salida = self.get_object()
                
                if len(salida.detsalidaprod_salida_set.all()) > 0:
                    for i in salida.detsalidaprod_salida_set.all():
                        stock = ControlStock.objects.prefetch_related('almacenes', 'productos').filter(almacenes_id=salida.origen, productos_id=i.prod_id).values('stock_actual', 'precio').first()
                        item = {}
                        item['id'] = i.prod.id
                        item['full_name'] = f'{i.prod.nombre} - {i.prod.descripcion}'
                        item['stock_actual'] = stock['stock_actual']
                        item['precio'] = stock['precio']
                        item['codbien'] = i.codbien.toJSON()
                        item['codubica'] = i.codubica.toJSON()
                        item['cant'] = i.cant
                        item['fila'] = i.id  
                        data.append(item)
                    return JsonResponse({'items': data, 'type': 'BM'}, safe=False)
                else:
                    for i in salida.det_salidainsumos_set.all():
                        stock = ControlStock.objects.prefetch_related('almacenes', 'productos').filter(almacenes_id=salida.origen, productos_id=i.prod_id).values('stock_actual', 'precio').first()
                        item = {}
                        item['id'] = i.prod.id
                        item['codigo'] = i.prod.codigo
                        item['full_name'] = f'{i.prod.nombre} - {i.prod.descripcion}'
                        item['cant'] = i.cant
                        item['stock_actual'] = stock['stock_actual']
                        item['precio'] = stock['precio']
                        item['lote'] = i.prod.lote
                        item['nro_lote'] = i.nro_lote
                        item['fecha_venc'] = i.fecha_venc       
                        data.append(item)
                    return JsonResponse({'items': data, 'type': 'MC'}, safe=False)
                
            elif action == 'search_products':
                data = []                 
                datos_cantprod = json.loads(request.POST['datos_cantprod'])
                term = request.POST['term'].strip()                
                products = ControlStock.objects.filter(almacenes_id__in=request.POST['idorigen'], stock_actual__gt=0, productos__activo__in='1', productos__grupobien__cod_grupo='02').prefetch_related('productos', 'almacenes')
                if len(term):
                    products = products.filter(productos__nombre__icontains=term)
                for i in products:
                    for l in datos_cantprod:
                        if(i.productos.id == l['id']):
                            i.stock_actual= int(i.stock_actual) - int(l['cantprod'])                         
                    if(i.stock_actual>0):
                        item = {}
                        item['id'] = i.productos.id
                        item['full_name'] = i.productos.nombre + ' / ' + i.productos.descripcion
                        item['categoria'] = i.productos.categorias.nombre
                        item['imagen'] = i.productos.get_imagen()
                        item['precio'] = i.precio
                        item['stock'] = i.stock_actual
                        data.append(item) 
            
            elif action == 'search_suministros':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                products = ControlStock.objects.prefetch_related('productos', 'almacenes').filter(almacenes_id__in=request.POST['idorigen2'], stock_actual__gt=0, productos__activo__in='1', productos__grupobien__cod_grupo='04')
                for i in products.exclude(productos_id__in=ids_exclude):
                    item = {}
                    item['id'] = i.productos.id
                    item['codigo'] = i.productos.codigo
                    item['full_name'] = i.productos.nombre + ' / ' + i.productos.descripcion
                    item['imagen'] = i.productos.get_imagen()
                    item['lote'] = i.productos.lote
                    item['precio'] = i.precio
                    item['stock_actual'] = i.stock_actual
                    data.append(item)
                    
            elif action == 'search_autocomplete':
                data = []
                datos_cantprod = json.loads(request.POST['datos_cantprod'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text':term})
                products = ControlStock.objects.prefetch_related('productos', 'almacenes').filter(almacenes_id__in=request.POST['idorigen'], stock_actual__gt=0, productos__activo__in='1', productos__grupobien__cod_grupo='02')

                if len(term):
                    products = products.filter(productos__nombre__icontains=term)

                for i in products[0:20]:
                    for l in datos_cantprod:
                        if(i.productos.id == l['id']):
                            i.stock_actual= int(i.stock_actual) - int(l['cantprod'])                         
                        
                    if(i.stock_actual>0):
                        item = {}
                        item['id'] = i.productos.id
                        item['full_name'] = i.productos.nombre + ' / ' + i.productos.descripcion
                        item['categoria'] = i.productos.categorias.nombre
                        item['imagen'] = i.productos.get_imagen()
                        item['precio'] = i.precio
                        item['stock'] = i.stock_actual
                        item['text'] = i.productos.nombre
                        data.append(item)

            elif action == 'search_autocomplete_suminist':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text':term})
                products = ControlStock.objects.filter(almacenes_id__in=request.POST['idorigen2'], stock_actual__gt=0, productos__activo__in='1', productos__grupobien__cod_grupo='04')
                
                if len(term):
                    products = products.filter(productos__nombre__icontains=term).exclude(productos_id__in=ids_exclude)
                
                for i in products[0:20]:
                    item = {}
                    item['id'] = i.productos.id
                    item['codigo'] = i.productos.codigo
                    item['imagen'] = i.productos.get_imagen()
                    item['full_name'] = f'{i.productos.nombre} {i.productos.descripcion}'
                    item['stock_actual'] = i.stock_actual
                    item['precio'] = i.precio
                    item['lote'] = i.productos.lote
                    item['nro_lote'] = ""
                    item['fecha_venc'] = ""
                    item['text'] = i.productos.nombre
                    data.append(item)

            elif action == 'edit':
                with transaction.atomic():
                    code = request.POST['code']
                    salidas = json.loads(request.POST['salidas'])                    
                    salida = self.get_object()
                    salida.cod_salida = salidas['cod_salida']
                    salida.origen_id = salidas['origen']
                    salida.respon_origen = salidas['respon_origen']
                    salida.destino_id = salidas['destino']
                    salida.respon_destino = salidas['respon_destino']
                    salida.tipo_salida_id = salidas['tipo_salida']
                    salida.tipo_comprob = salidas['tipo_comprob']
                    salida.num_comprob = salidas['num_comprob']
                    salida.subtotal = Decimal(salidas['subtotal'])
                    salida.iva = Decimal(salidas['iva'])
                    salida.total = Decimal(salidas['total'])
                    salida.fecha_salida = salidas['fecha_salida']
                    salida.usuario = self.request.user
                    salida.observ = salidas['observ']
                    salida.estado = salidas['estado']
                    salida.save()

                    if len(salidas['produc_sal']) > 0:

                        detsalida = salida.detsalidaprod_salida_set.all()                    
                        for det in detsalida:
                            stock = ControlStock.objects.filter(almacenes_id=salidas['origen'], productos_id=det.prod.id)
                            stock.update(apartados=F('apartados') - det.cant)
                            det.codbien.estado = 'SAS'
                            det.codbien.save()                            
                        detsalida.delete()

                        self.reserved(salidas['origen'], salidas['produc_sal'])
                        if code == '51':
                            depart = Departamento.objects.filter(nombre='Depósito').values('id').first()
                            if (depart):
                                print('EXISTE')
                                for i in salidas['produc_sal']:
                                    det = DetSalidaProd()
                                    det.precio = Decimal(i['precio'])
                                    det.cant = 1
                                    det.subtotal = Decimal(i['subtotal'])
                                    det.codbien_id = int(i['codbien']['id'])
                                    det.codubica_id = depart['id']
                                    det.salida_id = salida.id
                                    det.prod_id = i['id']
                                    det.save()
                            
                                    det.codbien.estado = 'ASI'
                                    det.codbien.save()             
                            else:
                                deposito = Departamento.objects.create(
                                    nombre='Depósito'
                                )
                                for i in salidas['produc_sal']:
                                    det = DetSalidaProd()
                                    det.precio = Decimal(i['precio'])
                                    det.cant = 1
                                    det.subtotal = Decimal(i['subtotal'])
                                    det.codbien_id = int(i['codbien']['id'])
                                    det.codubica_id = deposito.id
                                    det.salida_id = salida.id
                                    det.prod_id = i['id']
                                    det.save()
                                    
                                    det.codbien.estado = 'ASI'
                                    det.codbien.save()
                                print('NO EXISTE')
                        else:                            
                            for i in salidas['produc_sal']:
                                det = DetSalidaProd()
                                det.precio = Decimal(i['precio'])
                                det.cant = 1
                                det.subtotal = Decimal(i['subtotal'])
                                det.codbien_id = int(i['codbien']['id'])
                                det.codubica_id = int(i['codubica']['id'])
                                det.salida_id = salida.id
                                det.prod_id = i['id']
                                det.save()
                                
                                det.codbien.estado = 'ASI'
                                det.codbien.save()                        
                    else:

                        detsalidaMc = salida.det_salidainsumos_set.all()
                        for det in detsalidaMc:
                            stock = ControlStock.objects.filter(almacenes_id=salidas['origen'], productos_id=det.prod.id)
                            stock.update(apartados=F('apartados') - det.cant)
                        detsalidaMc.delete()

                        self.reserved(salidas['origen'], salidas['produc_sal2'])
                        for i in salidas['produc_sal2']:
                            det = DetSalidaInsumos()
                            det.precio = Decimal(i['precio'])
                            det.cant = int(i['cant'])
                            det.subtotal = Decimal(i['subtotal'])
                            det.nro_lote = i['nro_lote']                       
                            det.fecha_venc = i['fecha_venc']
                            det.salida_id = salida.id
                            det.prod_id = i['id']
                            det.save()
                              
                    image = str(salida.usuario.image)
                    data = {'type': 'create_operation_notification',
                            'url': f'/erp/salida/detail/{salida.id}/',
                            'message': f'{salida.usuario.username} ha realizado la distribución {salida.cod_salida}', 
                            'status': salida.estado,
                            'title': salida.tipo_salida.denominacion,
                            'image': image,
                            'user_id': salida.usuario.id,
                            'permissions': 'approve_movimientos'
                            }

            elif action == 'search_concepto':
                data = []
                term = request.POST['term']
                concepto = ConcepMovimiento.objects.filter(
                    Q(denominacion__icontains=term) | Q(codigo__icontains=term)).filter(tipo_conc='SA', estado='ACT')[0:10]
                for i in concepto:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)

            elif action == 'busca_ubicacionfisica':
                data = []
                term = request.POST['term'].strip()
                ubicafisica = Departamento.objects.filter()
                if len(term):
                    ubicafisica = ubicafisica.filter(nombre__icontains=term)
                for i in ubicafisica:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)

            elif action == 'busca_codbien':
                data = []
                ids_exclude = json.loads(request.POST['idsCodbien'])
                term = request.POST['term'].strip()
                codbienes = CodBienes.objects.filter(estado__icontains='SAS')
                if len(term):
                    codbienes = codbienes.filter(codbien__icontains=term)
                for i in codbienes.exclude(id__in=ids_exclude)[0:3]:
                    item = i.toJSON()
                    item['value'] = i.codbien
                    data.append(item)     

            elif action == 'create_unidad':
                with transaction.atomic():
                    frmDestino =  UnidadForm(request.POST)
                    data = frmDestino.save()
            elif action == 'create_departamento':
                with transaction.atomic():
                    frmDepar =  FormDepart(request.POST)
                    data = frmDepar.save()
            elif action == 'create_concepto':
                with transaction.atomic():
                    frmConcepMov =  FormConcepMov(request.POST)
                    data = frmConcepMov.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetSalidaProd.objects.filter(salida_id=self.get_object().id):
                stock = ControlStock.objects.all()
                for s in stock.filter(almacenes_id=i.salida.origen, productos_id=i.prod_id):                
                    print(s)
                    item = i.prod.toJSON()
                    item['stock_actual'] = s.stock_actual
                    item['precio'] = s.precio
                    item['codbien'] = i.codbien.toJSON()
                    item['codubica'] = i.codubica.toJSON()
                    item['cant'] = i.cant
                    item['fila'] = i.id                          
                    data.append(item)
        except:
            pass
        return data   

    def get_details_mc(self):
        data = []
        try:
            for i in DetSalidaInsumos.objects.filter(salida_id=self.get_object().id):
                stock = ControlStock.objects.all()
                for s in stock.filter(almacenes_id=i.salida.origen, productos_id=i.prod_id):
                    item = s.toJSON()                    
                    item['cant'] = i.cant
                    item['prod'] = i.prod.toJSON()
                    item['stock_actual'] = s.stock_actual
                    item['precio'] = s.precio
                    item['nro_lote'] = i.nro_lote
                    item['fecha_venc'] = i.fecha_venc       
                    data.append(item)
                    print(data)
        except:
            pass
        return data           

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edición de la Distribución: {self.object.cod_salida}'
        context['entity'] = 'Salidas'
        context['url'] = f'/erp/salida/update/{self.object.id}/'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['iva'] = Empresa.objects.values('nameimpuesto', ('iva')).first()
        context['frmUnidad'] = UnidadForm()
        context['frmDepar'] = FormDepart()
        context['frmConcepMov'] = FormConcepMov()
        return context

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

class SalidaDetailView(LoginRequiredMixin, DetailView):
    model = SalidaProduc
    template_name = 'salidas_prod/detail.html'
    #permission_required = 'solicitudes.view_solicitudes'
    success_url = reverse_lazy('erp:salida_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):  
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        if action == 'detail_data':
            data = []
            salida = self.get_object()
            if len(salida.detsalidaprod_salida_set.all()) > 0:
                # print('LONGITUD: ', len(salida.detsalidaprod_salida_set.all()))
                for i in salida.detsalidaprod_salida_set.all():
                    stock = ControlStock.objects.prefetch_related('almacenes', 'productos').filter(almacenes_id=salida.origen, productos_id=i.prod_id).values('stock_actual', 'precio').first()
                    item = {}
                    item['full_name'] = f'{i.prod.nombre} - {i.prod.descripcion}'
                    item['stock_actual'] = stock['stock_actual']
                    item['precio'] = stock['precio']
                    item['codbien'] = i.codbien.codbien
                    item['codubica'] = i.codubica.nombre
                    item['cant'] = i.cant
                    data.append(item)
                return JsonResponse({'items': data, 'type': 'BM'}, safe=False)
            else:
                for i in salida.det_salidainsumos_set.all():
                    stock = ControlStock.objects.prefetch_related('almacenes', 'productos').filter(almacenes_id=salida.origen, productos_id=i.prod_id).values('stock_actual', 'precio').first()
                    item = {}
                    item['codigo'] = i.prod.codigo
                    item['full_name'] = f'{i.prod.nombre} - {i.prod.descripcion}'
                    item['cant'] = i.cant
                    item['stock_actual'] = stock['stock_actual']
                    item['precio'] = stock['precio']
                    item['lote'] = i.prod.lote
                    item['subtotal'] = i.subtotal
                    item['nro_lote'] = i.nro_lote
                    item['fecha_venc'] = i.fecha_venc       
                    data.append(item)
                return JsonResponse({'items': data, 'type': 'MC'}, safe=False)

    def motive(self, **kwargs):
        try:
            motive = Aprobaciones.objects.filter(codigo=self.get_object().cod_salida).values('motivo').latest('id')
        except Exception as e:
            motive = {'motivo': 'Sin motivo'}
        return motive
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Detalle de la Distribucion: {self.get_object().cod_salida}'
        context['list_url'] = self.success_url
        context['url'] = '/aprobaciones/distribucion/list/'
        context['motive'] = self.motive()
        context['entity'] = 'Distribuciones'
        context['options'] = {'APR': 'APROBADO', 'REC': 'RECHAZADO', 'RET': 'RETORNADO'}
        return context

class SalidaFacturaPdfView(Perms_Check, View):
    permission_required = 'erp.add_salidaproduc'

    def get(self, request, *args, **kwargs):
        try:            
            template = get_template('salidas_prod/inven_pordistribPDF.html')
        #  encab_distrib= SalidaProduc.objects.get(id=self.kwargs['pk']).values('cod_salida', 'origen', 'origen__nombre',  'destino', 'destino__nombre', 'destino__nombrejefe', 'tipo_salida', 'tipo_comprob', 'num_comprob', 'subtotal', 'iva', 'total', 'fecha_salida', 'usuario', 'observ', 'estado', 'aprobado')
            encab_distrib= SalidaProduc.objects.get(pk=self.kwargs['pk'])

            detalle_distrib= DetSalidaProd.objects.filter(salida_id=self.kwargs['pk']).order_by('codubica_id')

            context = {
            'encab_distrib': encab_distrib,
            'detalle_distrib': detalle_distrib,
            'comp': {'fecha': datetime.now, 'name': 'Dirección Regional de Salud Estado Portuguesa', 'rif': 'G-20008795-1', 'tlf': '(0257) - 2531550 - 2512246 - 2534014', 'redsocial': 'http://saludportuguesa.gob.ve; twitter: @saludportuguesa', 'address': 'Carrera 3 con calle 09 Antiguo Hospital, Sector Curazao Guanare Portuguesa Venezuela'},
            'icon': '{}{}'.format(settings.MEDIA_URL, 'imagportadalogin/klipartzcom.png')
            }

            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:salida_list'))

class SalidaSolicitudView(LoginRequiredMixin, Perms_Check, FormView):
    form_class = SalidasForm
    template_name = 'salidas_prod/create.html'
    permission_required = 'erp.add_salidaproduc'    
    #permission_required = 'solicitudes.view_solicitudes'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        perms = ('erp.add_salidaproduc',)
        self.code = Solicitudes.objects.get(pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def reserved(self, almacen, productos):
        for i in productos:
            stock = ControlStock.objects.filter(almacenes_id=almacen, productos_id=i['id'])
            stock.update(apartados=F('apartados') + i['cant'])
            print('ALMACEN_ID: ', almacen, 'PRODUCTOS: ', i['id'])

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        # print(salida)
        if action == 'convert_request':
            detail = []
            solic = Solicitudes.objects.select_related('unidad_origen', 'unidad_destino').get(pk=self.kwargs['pk'])
            responsable_origen = Almacen.objects.select_related('unidad').filter(id=solic.unidad_origen.id).values('responsable').first()
            header = {
                'tipo_salida': solic.concepto.id,
                'destino': solic.unidad_destino.id,                
                'representante_destino': solic.unidad_destino.nombrejefe,
                'representante_origen': responsable_origen['responsable'],
                'tipo_salida': solic.concepto.id,
                'code': solic.concepto.codigo,
                'tipo_bienes': solic.concepto.salida_bienes,
                }
            #data['concept'] =
            if solic.concepto.salida_bienes == 'MTC':
                for i in solic.solicitud_set.all():
                    stock = ControlStock.objects.prefetch_related('productos', 'almacenes').filter(almacenes_id=1, productos_id=i.productos.id)
                    for s in stock:
                        item = {}
                        item['id'] = s.productos.id
                        item['codigo'] = s.productos.codigo
                        item['full_name'] = f'{s.productos.nombre} {s.productos.descripcion}'
                        item['stock_actual'] = s.stock_actual
                        item['precio'] = s.precio
                        item['cant'] = i.cantidad_aprobada
                        item['lote'] = s.productos.lote
                        item['subtotal'] = 0.00
                        item['nro_lote'] = ""
                        item['fecha_venc'] = ""
                        detail.append(item)
            else:
                productos_control_stock = ControlStock.objects.filter(almacenes_id=1, productos__in=solic.solicitud_set.values_list('productos', flat=True), stock_actual__gt=0)

                for i in solic.solicitud_set.all():
                    stock = productos_control_stock.filter(productos_id=i.productos.id).values('id', 'stock_actual', 'precio').first()
                    
                    if stock is not None:
                        for r in range(i.cantidad_aprobada):
                            item = {}
                            item['id'] = i.productos.id
                            item['full_name'] = f'{i.productos.nombre} - {i.productos.descripcion}'
                            item['stock_actual'] = stock['stock_actual']
                            item['precio'] = stock['precio']
                            item['codbien'] = {'id': 0, 'codbien': ''}
                            item['codubica'] = {'id': 0, 'nombre': ''}
                            item['cant'] = 1
                            item['fila'] = stock['id']
                            detail.append(item)
                
            return JsonResponse({'header': header, 'detail': detail}, safe=False)

        # elif action == 'convert':
        #     code = request.POST['code']
        #     print('CODIGO: ', code)
        #     print('FUNCIONO LA CONVERSION: ')
        #     with transaction.atomic():
        #         code = request.POST['code']
        #         salidas = json.loads(request.POST['salidas'])
        #         salida = SalidaProduc()
        #         salida.cod_salida = salidas['cod_salida']
        #         salida.origen_id = salidas['origen']
        #         salida.respon_origen = salidas['respon_origen']
        #         salida.destino_id = salidas['destino']
        #         salida.respon_destino = salidas['respon_destino']
        #         salida.tipo_salida_id = salidas['tipo_salida']
        #         salida.tipo_comprob = salidas['tipo_comprob']
        #         salida.num_comprob = salidas['num_comprob']
        #         salida.subtotal = Decimal(salidas['subtotal'])
        #         salida.iva = Decimal(salidas['iva'])
        #         salida.total = Decimal(salidas['total'])
        #         salida.fecha_salida = salidas['fecha_salida']
        #         salida.usuario = self.request.user
        #         salida.observ = salidas['observ']
        #         salida.estado = salidas['estado']
        #         salida.save()
        #         solic = Solicitudes.objects.get(pk=self.kwargs['pk'])
        #         solic.estado = 'COMPLETADA'
        #         solic.save()
        #         if len(salidas['produc_sal']) > 0:
        #             self.reserved(salidas['origen'], salidas['produc_sal'])
        #             if code == '51':
        #                 depart = Departamento.objects.filter(nombre='Depósito').values('id').first()
        #                 if (depart):
        #                     print('EXISTE')
        #                     print('DEPART', depart['id'])
        #                     for i in salidas['produc_sal']:
        #                         det = DetSalidaProd()
        #                         det.precio = Decimal(i['precio'])
        #                         det.cant = 1
        #                         det.subtotal = Decimal(i['subtotal'])
        #                         det.codbien_id = int(i['codbien']['id'])
        #                         det.codubica_id = depart['id']
        #                         det.salida_id = salida.id
        #                         det.prod_id = i['id']
        #                         det.save()
                        
        #                         det.codbien.estado = 'ASI'
        #                         det.codbien.save()             
        #                 else:
        #                     deposito = Departamento.objects.create(
        #                         nombre='Depósito'
        #                     )
        #                     for i in salidas['produc_sal']:
        #                         det = DetSalidaProd()
        #                         det.precio = Decimal(i['precio'])
        #                         det.cant = 1
        #                         det.subtotal = Decimal(i['subtotal'])
        #                         det.codbien_id = int(i['codbien']['id'])
        #                         det.codubica_id = deposito.id
        #                         det.salida_id = salida.id
        #                         det.prod_id = i['id']
        #                         det.save()
                                
        #                         det.codbien.estado = 'ASI'
        #                         det.codbien.save()
        #                     print('NO EXISTE')
        #             else:
        #                 for i in salidas['produc_sal']:
        #                     det = DetSalidaProd()
        #                     det.precio = Decimal(i['precio'])
        #                     det.cant = 1
        #                     det.subtotal = Decimal(i['subtotal'])
        #                     det.codbien_id = int(i['codbien']['id'])
        #                     det.codubica_id = int(i['codubica']['id'])
        #                     det.salida_id = salida.id
        #                     det.prod_id = i['id']
        #                     det.save()
                            
        #                     det.codbien.estado = 'ASI'
        #                     det.codbien.save()                        
        #         else:
        #             self.reserved(salidas['origen'], salidas['produc_sal2'])
        #             for i in salidas['produc_sal2']:
        #                 det = DetSalidaInsumos()
        #                 det.precio = Decimal(i['precio'])
        #                 det.cant = int(i['cant'])
        #                 det.subtotal = Decimal(i['subtotal'])
        #                 det.nro_lote = i['nro_lote']                       
        #                 det.fecha_venc = i['fecha_venc']
        #                 det.salida_id = salida.id
        #                 det.prod_id = i['id']
        #                 det.save()
                        
        #         image = str(salida.usuario.image)
        #         data = {'type': 'create_operation_notification',
        #                 'url': f'/erp/salida/detail/{salida.id}/',
        #                 'message': f'{salida.usuario.username} ha realizado la distribución {salida.cod_salida}', 
        #                 'status': salida.estado,
        #                 'title': salida.tipo_salida.denominacion,
        #                 'image': image,
        #                 'user_id': salida.usuario.id,
        #                 'permissions': 'approve_movimientos'
        #                 }
        #         return JsonResponse(data, safe=False)
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Distribucion de la solicitud: {self.code.codigo}"
        context['url'] = f"/erp/salida/solicitud/{self.kwargs['pk']}/"
        context['iva'] = Empresa.objects.values('nameimpuesto', ('iva')).last()
        context['list_url'] = f"/solicitudes/solicitud/detail/{self.kwargs['pk']}/"
        context['frmDepart'] = FormDepart()
        context['entity'] = 'Volver'
        context['action'] = 'convert'
        return context






   
