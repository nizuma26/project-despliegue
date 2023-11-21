import json
import os
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from core.erp.forms import IngresosForm, ProveedorForm, FormConcepMov, LoteForm
from core.reportes.forms import ReportForm
from core.erp.models import Producto, Proveedor, IngresoProduc, DetIngresoProduc, Almacen, Empresa, Seriales, Lotes
from core.aprobaciones.models import Aprobaciones
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, CreateView, UpdateView, DetailView, View
from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.urls import reverse_lazy
from decimal import Decimal
from datetime import date, datetime
from core.erp.mixins import Perms_Check, AuditLog
from django.contrib.contenttypes.models import ContentType

from core.erp.mixins import  Perms_Check

class IngresoListView(LoginRequiredMixin, Perms_Check, FormView):
    form_class = ReportForm
    template_name = 'ingresos_prod/list.html'
    permission_required = 'erp.view_ingresoproduc'

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
                queryset = IngresoProduc.objects.all().select_related('tipo_ingreso').select_related('proveedor').select_related('almacen').prefetch_related('usuario')
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(fecha_ingreso__range=[start_date, end_date])
                for i in queryset:
                    item = {}
                    item['cod_ingreso'] = i.cod_ingreso
                    item['almacen'] = i.almacen.nombre
                    item['tipo_ingreso'] = i.tipo_ingreso.denominacion
                    item['fecha_ingreso'] = i.fecha_ingreso.strftime('%Y-%m-%d')
                    item['subtotal'] = i.subtotal
                    item['total'] = i.total
                    item['estado'] = i.estado
                    item['id'] = i.id
                    item['tipo_comprob'] = i.tipo_comprob
                    item['num_comprob'] = i.num_comprob
                    item['respon_almac'] = i.respon_almac
                    item['usuario'] = i.usuario.username
                    item['observ'] = i.observ
                    data.append(item)

            elif action == 'search_detalle_prod':
                data = []
                for i in DetIngresoProduc.objects.filter(ingresoPro_id=request.POST['id']).prefetch_related('prod'):
                    item = {}
                    item['product'] = i.prod.nombre + ' / ' + i.prod.descripcion
                    item['category'] = i.prod.categorias.nombre
                    item['price'] = i.precio
                    item['cant'] = i.cant
                    item['subtotal'] = i.subtotal
                    data.append(item)

            # elif action == 'delete':
            #     perms = ('erp.delete_ingresoproduc',)
            #     if request.user.has_perms(perms):
            #         almacen = Almacen.objects.get(pk=request.POST['id'])
            #         almacen.delete()
            #     else:
            #         data['error'] = 'No tiene permisos para realizar esta acción'
               
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Incorporación'
        context['create_url'] = reverse_lazy('erp:ingreso_create')
        context['list_url'] = reverse_lazy('erp:ingreso_list')
        context['btn_name'] = 'Nuevo Registro'
        return context

class IngresoCreateView(LoginRequiredMixin, Perms_Check, CreateView):
    model = IngresoProduc
    form_class = IngresosForm
    template_name = 'ingresos_prod/create.html'
    success_url = reverse_lazy('erp:ingreso_list')
    url_redirect = success_url
    permission_required = 'erp.add_ingresoproduc'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':                
                data = []                 
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                queryset = Producto.objects.all().prefetch_related('usuario').prefetch_related('categorias')
                products = queryset.filter(activo__in ='1')

                if len(term):
                    products = products.filter(nombre__icontains=term)

                for i in products.exclude(id__in=ids_exclude):
                    item = {}
                    item['id'] = i.id
                    item['codigo'] = i.codigo
                    item['full_name'] = i.nombre +' / '+i.descripcion
                    item['categoria'] = i.categorias.nombre
                    item['imagen'] = i.get_imagen()
                    item['impuesto'] = i.pagaimpuesto
                    item['lote'] = i.lote
                    item['serie'] = i.serie
                    #item['value'] = i.nombre
                    data.append(item)

            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text':term})
                products = Producto.objects.filter(activo__in ='1').filter(nombre__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:20]:
                    item = {}
                    item['id'] = i.id
                    item['codigo'] = i.codigo
                    item['full_name'] = i.nombre +' / '+i.descripcion
                    item['categoria'] = i.categorias.nombre
                    item['imagen'] = i.get_imagen()
                    # item['impuesto'] = i.pagaimpuesto
                    # item['lote'] = i.lote
                    # item['serie'] = i.serie
                    item['text'] = i.nombre
                    data.append(item)

            elif action == 'search_responalmac':
                data = []
                for i in Almacen.objects.filter(id=request.POST['id']):
                    item = {}
                    item['responsable'] = i.responsable + ' - ' + i.cedula
                    data.append(item) 

            elif action == 'add':
                with transaction.atomic():
                    ingresos = json.loads(request.POST['ingresos'])
                    ingreso = IngresoProduc()
                    ingreso.almacen_id = ingresos['almacen']
                    ingreso.respon_almac = ingresos['respon_almac']
                    ingreso.tipo_ingreso_id = ingresos['tipo_ingreso']
                    ingreso.proveedor_id = ingresos['proveedor']
                    ingreso.tipo_comprob = ingresos['tipo_comprob']
                    ingreso.num_comprob = ingresos['num_comprob']
                    ingreso.subtotal = Decimal(ingresos['subtotal'])
                    ingreso.iva = Decimal(ingresos['iva'])
                    ingreso.total = Decimal(ingresos['total'])
                    ingreso.fecha_ingreso = ingresos['fecha_ingreso']
                    ingreso.usuario = self.request.user
                    ingreso.observ = ingresos['observ']
                    ingreso.estado = ingresos['estado']
                    ingreso.save()       

                    user = self.request.user.id
                    id = ingreso.id
                    object_str = str(ingreso)
                    content = ContentType.objects.get(model='ingresoproduc').id
                    AuditLog.save_log(user, id, content, object_str, 'Creado')            
                    
                    for i in ingresos['productos']:
                        det = DetIngresoProduc()
                        det.precio = Decimal(i['precio'])
                        det.cant = int(i['cant'])
                        det.subtotal = Decimal(i['subtotal'])
                        det.iva = Decimal(i['iva'])                                               
                        det.ingresoPro_id = ingreso.id
                        det.prod_id = i['id']
                        det.save()                    
                    
                    for s in ingresos['seriales']:
                        if len(s) > 0:
                            serial = Seriales()                      
                            serial.incorp_id = ingreso.id
                            serial.prod_id = s['prod_id']
                            serial.serial = s['serial']
                            serial.save()

                    for l in ingresos['lotes']:
                        if len(l) > 0:
                            lotes = Lotes()                      
                            lotes.incorp_id = ingreso.id
                            lotes.prod_id = l['prod_id']
                            lotes.nro_lote = l['nro_lote']
                            lotes.fecha_venc = l['fecha']
                            lotes.save()
                    image = str(ingreso.usuario.image)
                    data = {'type': 'create_operation_notification',
                            'url': f'/erp/ingreso/detail/{ingreso.id}/',
                            'message': f'{ingreso.usuario.username} ha realizado la incorporación {ingreso.cod_ingreso}', 
                            'status': ingreso.estado,
                            'title': ingreso.tipo_ingreso.denominacion,
                            'image': image,
                            'user_id': ingreso.usuario.id,
                            'permissions': 'approve_movimientos'
                            }
            
            elif action == 'search_proveedor':
                data = []
                term = request.POST['term']
                proveedors = Proveedor.objects.filter(
                    Q(empresa__icontains=term) | Q(ramo__icontains=term) | Q(documento__icontains=term))[0:20]
                for i in proveedors:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_proveedor':
                with transaction.atomic():
                    frmProvee =  ProveedorForm(request.POST)
                    data = frmProvee.save()
            
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
        context['title'] = 'Nueva Incorporación'
        context['entity'] = 'Incorporación'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['iva'] = Empresa.objects.values('nameimpuesto', ('iva')).last()
        context['det'] = []
        context['frmProvee'] = ProveedorForm()
        context['frmConcepMov'] = FormConcepMov()
        context['formLote'] = LoteForm()
        return context

class IngresoUpdateView(LoginRequiredMixin, Perms_Check, UpdateView):
    model = IngresoProduc
    form_class = IngresosForm
    template_name = 'ingresos_prod/create.html'
    success_url = reverse_lazy('erp:ingreso_list')
    url_redirect = success_url
    permission_required = 'erp.change_ingresoproduc'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            
            if action == 'search_products':                
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()               
                products = Producto.objects.filter(activo__in ='1')
                if len(term):
                    products = products.filter(Q(nombre__icontains=term) | Q(categorias_nombre__icontains=term))               
                for i in products.exclude(id__in=ids_exclude):
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)

            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text':term})
                products = Producto.objects.filter(activo__in ='1').filter(nombre__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:20]:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)

            elif action == 'search_responalmac':
                data = []
                for i in Almacen.objects.filter(id=request.POST['id']):
                    item = {}
                    item['responsable'] = i.responsable + ' - ' + i.cedula
                    data.append(item) 
            elif action == 'edit':
                with transaction.atomic():
                    ingresos = json.loads(request.POST['ingresos'])                    
                    ingreso = self.get_object()
                    ingreso.cod_ingreso = ingresos['cod_ingreso']
                    ingreso.almacen_id = ingresos['almacen']
                    ingreso.respon_almac = ingresos['respon_almac']
                    ingreso.tipo_ingreso_id = ingresos['tipo_ingreso']
                    ingreso.proveedor_id = ingresos['proveedor']
                    ingreso.tipo_comprob = ingresos['tipo_comprob']
                    ingreso.num_comprob = ingresos['num_comprob']
                    ingreso.subtotal = Decimal(ingresos['subtotal'])
                    ingreso.iva = Decimal(ingresos['iva'])
                    ingreso.total = Decimal(ingresos['total'])
                    ingreso.fecha_ingreso = ingresos['fecha_ingreso']
                    ingreso.usuario = self.request.user
                    ingreso.observ = ingresos['observ']
                    ingreso.estado = ingresos['estado']
                    ingreso.save()
                    ingreso.detingresoproduc_ingresopro_set.all().delete()
                    
                    for i in ingresos['productos']:
                        det = DetIngresoProduc()
                        det.precio = Decimal(i['precio'])
                        det.cant = int(i['cant'])
                        det.subtotal = Decimal(i['subtotal'])
                        det.iva = Decimal(i['iva'])
                        det.ingresoPro_id = ingreso.id
                        det.prod_id = i['id']
                        det.save()                    

                    user = ingreso.usuario.id
                    id = ingreso.id
                    object_str = str(ingreso)
                    content = ContentType.objects.get(model='ingresoproduc').id
                    AuditLog.save_log(user, id, content, object_str, 'Modificado')

                    image = str(ingreso.usuario.image)
                    data = {'type': 'create_operation_notification',
                            'url': f'/erp/ingreso/detail/{ingreso.id}/',
                            'message': f'{ingreso.usuario.username} ha realizado la incorporación {ingreso.cod_ingreso}', 
                            'status': ingreso.estado,
                            'title': ingreso.tipo_ingreso.denominacion,
                            'image': image,
                            'user_id': user,
                            'permissions': 'approve_movimientos'
                            }

            elif action == 'fields_save':
                changes = json.loads(request.POST['changes'])
                AuditLog.fields_save(changes)

            elif action == 'search_proveedor':
                data = []
                term = request.POST['term']
                proveedors = Proveedor.objects.filter(
                    Q(empresa__icontains=term) | Q(ramo__icontains=term) | Q(documento__icontains=term))[0:10]
                for i in proveedors:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_proveedor':
                with transaction.atomic():
                    frmProveedor = ProveedorForm(request.POST)
                    data = frmProveedor.save()
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
            for i in DetIngresoProduc.objects.filter(ingresoPro_id=self.get_object().id):
               # print(i)
                item = i.prod.toJSON()
                item['cant'] = i.cant
                item['precio'] = i.precio
                item['subtotal'] = i.subtotal
                item['iva'] = i.iva
                data.append(item)
        except:
            pass
        return data   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edición del Ingreso: {self.object.cod_ingreso}'
        context['entity'] = 'Incorporación'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['iva'] = Empresa.objects.values('nameimpuesto', ('iva')).last()
        # aqui para evitar errores de datos especialmente de null etc, los convierto en formato json.
        context['det'] = json.dumps(self.get_details_product(), cls=Encoder)
        context['frmProvee'] = ProveedorForm()
        context['frmConcepMov'] = FormConcepMov()
        return context

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)
       
class IncorpDetailView(LoginRequiredMixin, DetailView):
    model = IngresoProduc
    template_name = 'ingresos_prod/detail.html'
    success_url = reverse_lazy('erp:ingreso_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_detail(self):
        data = []
        incorp = self.get_object()        
        for i in incorp.detingresoproduc_ingresopro_set.all():
            item = {}
            item['code'] = i.prod.codigo
            item['id'] = i.prod.id
            item['full_name'] = i.prod.nombre + ' / ' + i.prod.descripcion
            item['precio'] = i.precio
            item['cantidad'] = i.cant
            item['iva'] = i.iva
            item['subtotal'] = i.subtotal
            data.append(item)
        return data
    
    def motive(self):
        try:
            motive = Aprobaciones.objects.filter(codigo=self.get_object().cod_ingreso).values('motivo').latest('id')
        except Exception as e:
            motive = {'motivo': 'Sin motivo'}
        return motive

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Detalle de la Incorporación: {self.get_object().cod_ingreso}'
        context['list_url'] = self.success_url
        context['entity'] = 'Incorporaciones'
        context['url'] = '/aprobaciones/incorporacion/list/'
        context['options'] = {'APR': 'APROBADO', 'REC': 'RECHAZADO', 'RET': 'RETORNADO'}
        context['motive'] = self.motive()
        context['det'] = self.get_detail()
        return context
    
class IngresoFacturaPdfView(Perms_Check, View):
    permission_required = 'erp.add_ingresoproduc'

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('ingresos_prod/guia_ingresoPDF.html')
            encab_ing= IngresoProduc.objects.prefetch_related('usuario', 'almacen', 'proveedor').get(pk=self.kwargs['pk'])
            detalle_ing= DetIngresoProduc.objects.prefetch_related('prod', 'ingresoPro').filter(ingresoPro_id=self.kwargs['pk']).order_by('prod_id')
            context = {
            'encab_ing': encab_ing,
            'detalle_ing': detalle_ing,
            'comp': {'fecha': datetime.now, 'name': 'Dirección Regional de Salud Estado Portuguesa', 'rif': 'G-20008795-1', 'tlf': '(0257) - 2531550 - 2512246 - 2534014', 'redsocial': 'http://saludportuguesa.gob.ve; twitter: @saludportuguesa', 'address': 'Carrera 3 con calle 09 Antiguo Hospital, Sector Curazao Guanare Portuguesa Venezuela'},
            'icon': '{}{}'.format(settings.MEDIA_URL, 'imagportadalogin/klipartzcom.png')
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        


   
