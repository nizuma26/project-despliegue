import json
from django.http import JsonResponse
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from core.solicitudes.models import Solicitudes, DetSolicitud
from core.erp.models import Producto, InventarioBienes, Unidad, ConcepMovimiento, ControlStock
from core.erp.mixins import Perms_Check
from core.reportes.forms import ReportForm
from core.solicitudes.forms import FormSolicitud
from core.aprobaciones.models import Aprobaciones
from django.urls import reverse_lazy
from decimal import Decimal
from django.views.generic import CreateView, UpdateView, FormView, DetailView

class SolicitudListView(LoginRequiredMixin, Perms_Check, FormView):
    form_class = ReportForm
    template_name = 'movimientos/list.html'
    permission_required = 'solicitudes.view_solicitudes'

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
                queryset = Solicitudes.objects.select_related('user', 'unidad_origen', 'unidad_destino', 'concepto').filter(user=self.request.user)
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(fecha__range=[start_date, end_date])
                for i in queryset:
                    item = {}
                    item['codigo'] = i.codigo
                    item['fecha'] = i.fecha.strftime('%y-%m-%d')
                    item['unidad_origen'] = i.unidad_origen.nombre
                    item['usuario'] = i.user.get_full_name()
                    item['prioridad'] = i.get_prioridad_display()
                    item['tipo'] = i.get_tipo_solicitud_display()
                    item['estado'] = i.estado
                    item['id'] = i.id
                    data.append(item)

            elif action == 'delete':
                solic = Solicitudes.objects.prefetch_related('user', 'unidad').get(pk=request.POST['id'])                   
                solic.delete()
            
            elif action == 'delete_multiple':
                with transaction.atomic():
                    perms = ('solicitudes.view_solicitudes',)
                    if request.user.has_perms(perms):
                        ids = json.loads(request.POST['id'])
                        solic = Solicitudes.objects.prefetch_related('user', 'unidad').filter(id__in=ids, estado='EN CREACIÓN')
                        solic.delete()
                    else:
                        data['error'] = 'No tiene permisos para realizar esta acción'
                
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)     

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['title'] = 'Mis Solicitudes'
        context['btn_name'] = 'Nueva Solicitud'
        context['create_url'] = reverse_lazy('solicitudes:solicitud_create')        
        return context

class SolicitudCreateView(LoginRequiredMixin, Perms_Check, CreateView):
    model = Solicitudes
    form_class = FormSolicitud
    template_name = 'movimientos/create.html'
    permission_required = 'solicitudes.add_solicitudes'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            #CONSULTAS
            #MODAL
            if action == 'search_bienes_deposito':
                data = []
                type_bienes = request.POST['type_bienes']
                ids_exclude = json.loads(request.POST['ids'])
                products = Producto.objects.filter(activo__in ='1', grupobien__cod_grupo=type_bienes).exclude(id__in=ids_exclude)
                for i in products:
                    item = {}
                    item['full_name'] = i.nombre + ' / ' + i.descripcion
                    item['categoria'] = i.categorias.nombre
                    item['imagen'] = i.get_imagen()                    
                    item['prod_id'] = i.id
                    data.append(item)

            elif action == 'search_bienes_uso':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                unidad = request.POST['unidad_origen']
                inventario = InventarioBienes.objects.prefetch_related('unidad', 'ubica_fisica', 'prod', 'codbien', 'tipo_proc', 'salida').filter(unidad_id__in=unidad).exclude(ult_proc='Desincorporado').exclude(id__in=ids_exclude)
                for i in inventario:
                    item = {}
                    item['imagen'] = i.prod.get_imagen()
                    item['full_name'] = i.prod.nombre + ' / ' + i.prod.descripcion
                    item['categoria'] = i.prod.categorias.nombre
                    item['codigo_bien'] = i.codbien.codbien
                    item['departamento'] = i.ubica_fisica.nombre
                    item['id'] = i.id
                    item['prod_id'] = i.prod.id
                    data.append(item)
            
            elif action == 'autocomplete_bienes_deposito':
                data = []
                type_bienes = request.POST['type_bienes']  
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text':term})
                products = Producto.objects.filter(activo__in ='1', nombre__icontains=term, grupobien__cod_grupo=type_bienes).exclude(id__in=ids_exclude)
                for i in products[0:20]:
                    item = {}
                    item['prod_id'] = i.id
                    item['id'] = i.id
                    item['codigo'] = i.codigo
                    item['full_name'] = f'{i.nombre} / {i.descripcion}'
                    item['categoria'] = i.categorias.nombre
                    item['marca'] = i.marca.marca
                    item['modelo'] = i.modelo.modelo
                    item['imagen'] = i.get_imagen()
                    item['text'] = i.nombre
                    data.append(item)
            
            #BUSCADOR DE PRODUCTOS
            # elif action == 'search_autocomplete':
            #     data = []
            #     ids_exclude = json.loads(request.POST['idsCodbien'])
            #     term = request.POST['term'].strip()
            #     data.append({'id': term, 'text':term})
            #     products = InventarioBienes.objects.filter(unidad_id__in=request.POST['idorigen']).exclude(ult_proc='DESINC').exclude(codbien_id__in=ids_exclude)

            #     if len(term):
            #         products = products.filter(prod__nombre__icontains=term)
            #     for i in products:
            #         item = {}
            #         item['full_name'] = i.prod.nombre  + ' / ' + i.prod.descripcion
            #         item['categ'] = i.prod.categorias.nombre
            #         item['imagen'] = i.prod.get_imagen()                    
            #         item['prod'] = i.prod_id
            #         item['codbien'] = i.codbien.toJSON()
            #         item['codubica'] = i.ubica_fisica.toJSON()
            #         item['salida'] = i.salida_id
            #         item['id'] = i.id
            #         data.append(item)  
            elif action == 'search_concept':
                type = request.POST['type']
                data = [{'type': '', 'text': '------------'}]                
                concept = ConcepMovimiento.objects.filter(tipo_conc=type)
                if type == 'SA':
                    concept = concept.exclude(salida_bienes='AMB')
                for i in concept:
                    data.append({'id': i.id, 'text': i.codigo + '-' + i.denominacion})

            elif action == 'type_concept':
                # data = []
                id = request.POST['id']
                concept = ConcepMovimiento.objects.filter(id=id, tipo_conc='SA', estado='ACT').values('salida_bienes').first()
                data['type'] = concept['salida_bienes']

            # #GUARDAR REGISTRO
            elif action == 'add':
                with transaction.atomic():
                    solicitud = json.loads(request.POST['solicitud'])
                    solic = Solicitudes()
                    #solic.codigo = solicitudes['codigo']
                    solic.tipo_solicitud = solicitud['tipo_solicitud']
                    solic.concepto_id = solicitud['concepto']
                    solic.prioridad = solicitud['prioridad']
                    solic.fecha = solicitud['fecha']
                    solic.unidad_origen_id = solicitud['unidad_origen']
                    solic.unidad_destino_id = solicitud['unidad_destino']
                    solic.estado = solicitud['estado']
                    solic.descripcion = solicitud['descripcion']
                    solic.user_id = self.request.user.id
                    solic.save()
                    
                    for i in solicitud['productos']:
                        DetSolicitud.objects.create(
                            solicitud_id = solic.id,
                            productos_id = i['prod_id'],
                            inventario_id = i['id'],
                            cantidad = i['cantidad'],
                        )
                        image = str(solic.user.image)
                    data = {'type': 'create_operation_notification', 
                            'url': f'/solicitudes/solicitud/detail/{solic.id}', 
                            'message': f'{solic.user.username} ha realizado la solicitud {solic.codigo}', 
                            'status': solic.estado, 
                            'title': solic.get_tipo_solicitud_display(), 
                            'image': image, 
                            'user_id': solic.user.id,
                            'permissions': 'approve_solicitudes'
                            }
                    
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)      


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['title'] = 'Nueva Solicitud'
        context['list_url'] = reverse_lazy('solicitudes:solicitud_list')
        context['entity'] = 'Solicitudes'
        context['action'] = 'add'
        context['det'] = []
        return context

class SolicitudUpdateView(LoginRequiredMixin, Perms_Check, UpdateView):
    model = Solicitudes
    form_class = FormSolicitud
    template_name = 'movimientos/create.html'
    success_url = reverse_lazy('solicitudes:solicitud_list')
    permission_required = 'solicitudes.change_solicitudes'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    # def get_form(self, form_class=None):
    #     instance = self.get_object()
    #     form = FormSolicitud(instance=instance)
    #     form.fields['unidad'].queryset = Unidad.objects.filter(id=instance.unidad.id)
    #     return form
    
    # def get_details_product(self):
    #     data = []
    #     solic = self.get_object()
    #     if solic.tipo_solicitud == 'DIST' or solic.tipo_solicitud == 'DES_DEPOSITO':
    #         for i in solic.solicitud_set.all():
    #             item = {}
    #             item['prod_id'] = i.productos.id
    #             item['full_name'] = i.productos.nombre + ' / ' + i.productos.descripcion
    #             item['categoria'] = i.productos.categorias.nombre
    #             item['cantidad'] = i.cantidad
    #             item['codigo_bien'] = 'S/N'
    #             item['id'] = None
    #             data.append(item)
    #         return json.dumps(data)
    #     else:
    #         for i in solic.solicitud_set.all():
    #             item = {}
    #             item['prod_id'] = i.productos.id
    #             item['full_name'] = i.productos.nombre + ' / ' + i.productos.descripcion
    #             item['categoria'] = i.productos.categorias.nombre
    #             item['cantidad'] = i.cantidad
    #             item['codigo_bien'] = i.inventario.codbien.codbien
    #             item['id'] = i.inventario_id
    #             data.append(item)
    #         return json.dumps(data)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            #CONSULTAS
            if action == 'detail_data':
                data = []
                solic = self.get_object()
                if solic.tipo_solicitud == 'DIST' or solic.tipo_solicitud == 'DES_DEPOSITO':
                    for i in solic.solicitud_set.all():
                        item = {}
                        item['prod_id'] = i.productos.id
                        item['full_name'] = i.productos.nombre + ' / ' + i.productos.descripcion
                        item['categoria'] = i.productos.categorias.nombre
                        item['cantidad'] = i.cantidad
                        item['codigo_bien'] = 'S/N'
                        item['id'] = None
                        data.append(item)
                    return JsonResponse({'items': data, 'type': 'BM'}, safe=False)
                else:
                    for i in solic.solicitud_set.all():
                        item = {}
                        item['prod_id'] = i.productos.id
                        item['full_name'] = i.productos.nombre + ' / ' + i.productos.descripcion
                        item['categoria'] = i.productos.categorias.nombre
                        item['cantidad'] = i.cantidad
                        item['codigo_bien'] = i.inventario.codbien.codbien
                        item['id'] = i.inventario_id
                        data.append(item)
                    return JsonResponse({'items': data, 'type': 'MC'}, safe=False)
                
            #MODAL
            elif action == 'search_bienes_deposito':
                data = []
                type_bienes = request.POST['type_bienes']
                ids_exclude = json.loads(request.POST['ids'])
                products = Producto.objects.select_related('marca', 'modelo', 'categorias', 'grupobien', 'subgrupobien', 'moneda').prefetch_related('usuario').filter(activo__in ='1', grupobien__cod_grupo=type_bienes).exclude(id__in=ids_exclude)
                for i in products:
                    item = {}
                    item['full_name'] = i.nombre + ' / ' + i.descripcion
                    item['categoria'] = i.categorias.nombre
                    item['imagen'] = i.get_imagen()                    
                    item['prod_id'] = i.id
                    data.append(item)

            elif action == 'search_bienes_uso':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                unidad = request.POST['unidad']
                inventario = InventarioBienes.objects.prefetch_related('unidad', 'ubica_fisica', 'prod', 'codbien', 'tipo_proc', 'salida').filter(unidad_id__in=unidad).exclude(ult_proc='Desincorporado').exclude(id__in=ids_exclude)
                for i in inventario:
                    item = {}
                    item['imagen'] = i.prod.get_imagen()
                    item['full_name'] = i.prod.nombre + ' / ' + i.prod.descripcion
                    item['categoria'] = i.prod.categorias.nombre
                    item['codigo_bien'] = i.codbien.codbien
                    item['departamento'] = i.ubica_fisica.nombre
                    item['id'] = i.id
                    item['prod_id'] = i.prod.id
                    data.append(item)
            
            elif action == 'autocomplete_bienes_deposito':
                data = []
                type_bienes = request.POST['type_bienes']  
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text':term})
                products = Producto.objects.select_related('marca', 'modelo', 'categorias', 'grupobien', 'subgrupobien', 'moneda').prefetch_related('usuario').filter(activo__in ='1', 
                nombre__icontains=term, grupobien__cod_grupo=type_bienes).exclude(id__in=ids_exclude)
                for i in products[0:20]:
                    item = {}
                    item['prod_id'] = i.id
                    item['id'] = i.id
                    item['codigo'] = i.codigo
                    item['full_name'] = f'{i.nombre} / {i.descripcion}'
                    item['categoria'] = i.categorias.nombre
                    item['marca'] = i.marca.marca
                    item['modelo'] = i.modelo.modelo
                    item['imagen'] = i.get_imagen()
                    item['text'] = i.nombre
                    data.append(item)

            elif action == 'search_concept':
                type = request.POST['type']
                data = [{'type': '', 'text': '------------'}]                
                concept = ConcepMovimiento.objects.filter(tipo_conc=type)
                if type == 'SA':
                    concept = concept.exclude(salida_bienes='AMB')
                for i in concept:
                    data.append({'id': i.id, 'text': i.codigo + '-' + i.denominacion})

            elif action == 'type_concept':
                id = request.POST['id']
                concept = ConcepMovimiento.objects.filter(id=id, tipo_conc='SA', estado='ACT').values('salida_bienes').first()
                data['type'] = concept['salida_bienes']

            #MODIFICAR REGISTRO
            elif action == 'edit':
                with transaction.atomic():
                    solicitud = json.loads(request.POST['solicitud'])
                    solic = self.get_object()
                    solic.tipo_solicitud = solicitud['tipo_solicitud']
                    solic.concepto_id = solicitud['concepto']
                    solic.prioridad = solicitud['prioridad']
                    solic.fecha = solicitud['fecha']
                    solic.unidad_origen_id = solicitud['unidad_origen']
                    solic.unidad_destino_id = solicitud['unidad_destino']
                    solic.estado = solicitud['estado']
                    solic.descripcion = solicitud['descripcion']
                    solic.user = self.request.user
                    solic.save()
                    solic.solicitud_set.all().delete()
                    
                    # if solic.tipo_solicitud == 'DIST' or solic.tipo_solicitud == 'DES_DEPOSITO':
                    for i in solicitud['productos']:
                        DetSolicitud.objects.create(
                            solicitud_id = solic.id,
                            productos_id = i['prod_id'],
                            inventario_id = i['id'],
                            cantidad = i['cantidad']
                        )
                    image = str(solic.user.image)
                    data = {'type': 'create_operation_notification', 
                            'url': f'/solicitudes/solicitud/detail/{solic.id}', 
                            'message': f'{solic.user.username} ha realizado la solicitud {solic.codigo}', 
                            'status': solic.estado, 
                            'title': solic.get_tipo_solicitud_display(), 
                            'image': image, 
                            'user_id': solic.user.id,
                            'permissions': 'approve_solicitudes'
                            }
                           
                    
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Solicitud'
        context['list_url'] = self.success_url
        context['entity'] = 'Solicitudes'
        context['action'] = 'edit'
        #context['det'] = self.get_details_product()
        return context

class SolicitudDetailView(LoginRequiredMixin, DetailView):
    model = Solicitudes
    template_name = 'movimientos/detail.html'
    #permission_required = 'solicitudes.view_solicitudes'
    success_url = reverse_lazy('solicitudes:solicitud_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):        
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        if action == 'detail_data':
            data = []
            solic = self.get_object()
            if solic.tipo_solicitud == 'DIST' or solic.tipo_solicitud == 'DES_DEPOSITO':
                for i in solic.solicitud_set.all():
                    stock = ControlStock.objects.prefetch_related('productos', 'almacenes').filter(almacenes_id=1, productos_id=i.productos.id).values('stock_actual').first()
                    item = {}
                    item['prod_id'] = i.productos.id
                    item['full_name'] = i.productos.nombre + ' / ' + i.productos.descripcion
                    item['categoria'] = i.productos.categorias.nombre                    
                    item['cantidad'] = i.cantidad
                    item['cantidad_aprobada'] = i.cantidad_aprobada
                    item['id'] = ''
                    if stock is None:
                        item['stock_actual'] = 0
                    else:
                        item['stock_actual'] = stock['stock_actual']
                    data.append(item)
                return JsonResponse({'items': data, 'type': 'EN_DEPOSITO', 'status': solic.estado, 'perm': request.user.has_perms(('solicitudes.approve_solicitudes',))}, safe=False)
            else:
                for i in solic.solicitud_set.all():
                    item = {}
                    item['prod_id'] = i.productos.id
                    item['full_name'] = i.productos.nombre + ' / ' + i.productos.descripcion
                    item['categoria'] = i.productos.categorias.nombre
                    item['cantidad'] = i.cantidad
                    item['codigo_bien'] = i.inventario.codbien.codbien
                    item['codigo_bien_id'] = i.inventario.codbien.id
                    item['aprobado'] = i.aprobado
                    item['id'] = i.inventario_id
                    data.append(item)
                return JsonResponse({'items': data, 'type': 'EN_USO', 'status': solic.estado, 'perm': request.user.has_perms(('solicitudes.approve_solicitudes',))}, safe=False)
    
    def motive(self, **kwargs):
        try:
            motive = Aprobaciones.objects.filter(codigo=self.get_object().codigo).values('motivo').latest('id')
        except Exception as e:
            motive = {'motivo': 'Sin motivo'}
        return motive
    
    def url_request(self, **kwargs):
        data = {}
        try:
            type_request = self.get_object().tipo_solicitud
            if type_request == 'DIST':
                data['url'] = f'/erp/salida/solicitud/{self.get_object().id}'
            elif type_request == 'TRAS':
                data['url'] = f'/erp/traslado/solicitud/{self.get_object().id}'
            elif type_request == 'DES_USO':
                data['url'] = f'/erp/desinc/solicitud/{self.get_object().id}'
            else:
                data['url'] = f'/erp/desinc_almacen/solicitud/{self.get_object().id}'
        except Exception as e:
            data['error'] = str(e)
        return data
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Detalle de la Solicitud: {self.get_object().codigo}'
        context['list_url'] = self.success_url
        context['entity'] = 'Solicitudes'
        context['motive'] = self.motive()
        context['url'] = '/aprobaciones/solicitud/movimiento/'
        context['url_request'] = self.url_request()
        context['options'] = {'APR': 'APROBADO', 'REC': 'RECHAZADO', 'RET': 'RETORNADO'}
        return context
    