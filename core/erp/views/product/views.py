import json
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from PIL import Image
from core.audit_log.models import UserActivity, DetUserActivity

from core.erp.forms import FormProducto, FormMarca, FormCategoria, FormModelo
from core.erp.models import Producto, Marca, Modelo, SubGrupoCtaBienes, GrupoCtaBienes, Moneda
from core.erp.mixins import Perms_Check, AuditLog
from django.contrib.contenttypes.models import ContentType

class ProductListView(LoginRequiredMixin, Perms_Check, ListView):
    model = Producto
    template_name = 'product/list.html'
    permission_required = 'erp.view_producto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']           
            if action == 'searchdata':
                data = []
                for i in Producto.objects.select_related('marca', 'categorias', 'modelo', 'grupobien', 'subgrupobien', 'moneda').prefetch_related('usuario').all():
                    item = {}
                    item['codigo'] = i.codigo
                    item['nombre'] = i.nombre
                    item['imagen'] = i.get_imagen()
                    item['categoria'] = i.categorias.nombre
                    item['marca'] = i.marca.marca
                    item['modelo'] = i.modelo.modelo
                    item['activo'] = i.activo
                    item['id'] = i.id                   
                    data.append(item)

            elif action == 'detail':               
                queryset = Producto.objects.select_related('marca', 'categorias', 'modelo', 'grupobien', 'subgrupobien', 'moneda').prefetch_related('usuario').filter(id=request.POST['id'])
                datos = []
                for i in queryset:
                    item = {
                        'codigo': i.codigo,
                        'nombre': i.nombre,
                        'imagen': i.get_imagen(),
                        'categoria': i.categorias.nombre,
                        'marca': i.marca.marca,
                        'modelo': i.modelo.modelo,
                        'activo': i.activo,
                        'id': i.id,
                        'descripcion': i.descripcion,
                        'grupo': i.grupobien.nombre,
                        'subgrupo': i.subgrupobien.denominacion,
                        'unidad_medida': i.unida_medida,
                        'moneda': i.moneda.get_full_name()
                    }                    
                    datos.append(item)
                    return JsonResponse(datos, safe=False)
            
            elif action == 'historical':
                data = []
                queryset = UserActivity.objects.prefetch_related('user').prefetch_related('content_type').filter(content_type__model='producto', object_id=request.POST['id']).order_by('-action_date', '-action_time')
                for i in queryset:
                    item ={}
                    item['date_joined'] = i.action_date.strftime('%Y-%m-%d') + ' / ' + i.action_time.strftime('%H:%M:%S')
                    item['user'] = i.user.username
                    item['action'] = i.action
                    item['device'] = i.device
                    data.append(item)

            elif action == 'inactivar':
                with transaction.atomic():
                    perms = ('erp.change_producto',)
                    if request.user.has_perms(perms):
                        status = Producto.objects.select_related('marca', 'categorias', 'modelo', 'grupobien', 'subgrupobien', 'moneda').prefetch_related('usuario').get(pk=request.POST['id'])
                        status.activo = False
                        status.save()                        
                        # AuditLog.save_log(user, id, content, object_str, 'Creado')
                        # AuditLog.fields_save(changes)
                    else:
                        data['error'] = 'No tiene permisos para realizar esta acción'
            
            elif action == 'activar':
                with transaction.atomic():
                    perms = ('erp.change_producto',)
                    if request.user.has_perms(perms):
                        status = Producto.objects.select_related('marca', 'categorias', 'modelo', 'grupobien', 'subgrupobien', 'moneda').prefetch_related('usuario').get(pk=request.POST['id'])
                        status.activo = True
                        status.save()
                        changes = [{'field': 'Estado', 'value_ant':  'False', 'value_act': 'True'}]
                        #AuditLog.fields_save(changes)
                    else:
                        data['error'] = 'No tiene permisos para realizar esta acción'        
            
            elif action == 'inactive_multiple':
                with transaction.atomic():
                    perms = ('erp.change_producto',)
                    if request.user.has_perms(perms):
                        ids = json.loads(request.POST['id'])                        
                        products = Producto.objects.select_related('marca', 'categorias', 'modelo', 'grupobien', 'subgrupobien', 'moneda').prefetch_related('usuario').filter(id__in=ids)
                        products.update(activo=False)
                    else:
                        data['error'] = 'No tiene permisos para realizar esta acción'
            
            elif action == 'active_multiple':
                with transaction.atomic():
                    perms = ('erp.change_producto',)
                    if request.user.has_perms(perms):
                        ids = json.loads(request.POST['id'])
                        products = Producto.objects.select_related('marca', 'categorias', 'modelo', 'grupobien', 'subgrupobien', 'moneda').prefetch_related('usuario').filter(id__in=ids)
                        products.update(activo=True)
                    else:
                        data['error'] = 'No tiene permisos para realizar esta acción'
            
            elif action == 'delete_multiple':
                with transaction.atomic():
                    perms = ('erp.delete_producto',)
                    if request.user.has_perms(perms):
                        ids = json.loads(request.POST['id'])
                        products = Producto.objects.select_related('marca', 'categorias', 'modelo', 'grupobien', 'subgrupobien', 'moneda').prefetch_related('usuario').filter(id__in=ids)
                        products.delete()
                    else:
                        data['error'] = 'No tiene permisos para realizar esta acción'
            
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Catálogo de Productos'
        context['create_url'] = reverse_lazy('erp:product_create')
        context['list_url'] = reverse_lazy('erp:product_list')
        context['btn_name'] = 'Nuevo Producto'
        context['entity'] = 'Catálogo'
        context['frmCateg'] = FormCategoria()
        context['frmMarca'] = FormMarca()
        context['frmModelos'] = FormModelo()
        return context

class ProductCreateView(LoginRequiredMixin, Perms_Check, CreateView):
    model = Producto
    form_class = FormProducto
    template_name = 'product/product_create.html'
    success_url = reverse_lazy('erp:product_list')
    permission_required = 'erp.add_producto'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_subgrupos_id':
                data = [{'id': '', 'text': '------------'}]
                for i in SubGrupoCtaBienes.objects.filter(grupo_id=request.POST['id']):
                    data.append({'id': i.id, 'text': i.cod_grusubgrusec + '  ' + i.denominacion})
            
            elif action == 'search_modelos_id':
                data = [{'id': '', 'text': '------------'}]
                for i in Modelo.objects.filter(marcas_id=request.POST['id']):
                    data.append({'id': i.id, 'text': i.modelo})

            elif action == 'add':                
                with transaction.atomic():
                    produc_catalago = json.loads(request.POST['produc_catalago'])
                    prod = Producto()
                    #prod.codigo = produc_catalago['codigo']
                    prod.nombre = produc_catalago['nombre']
                    prod.descripcion = produc_catalago['descripcion']
                    prod.componentes = produc_catalago['componentes']
                    prod.unida_medida = produc_catalago['unida_medida']                    
                    prod.activo = produc_catalago['activo']
                    prod.grupobien_id = produc_catalago['grupobien']['id']
                    prod.subgrupobien_id = produc_catalago['subgrupobien']['id']
                    prod.imagen = produc_catalago['imagen']                    
                    prod.categorias_id = produc_catalago['categorias']['id']
                    prod.pagaimpuesto = produc_catalago['pagaimpuesto']
                    prod.lote = produc_catalago['lote']
                    prod.serie = produc_catalago['serie']
                    prod.inventariable = produc_catalago['inventariable']
                    prod.marca_id = produc_catalago['marca']['id']
                    prod.modelo_id = produc_catalago['modelo']['id']
                    prod.moneda_id = produc_catalago['moneda']['id']
                    prod.usuario = self.request.user
                    prod.save()

                    user = self.request.user.id
                    id = prod.id
                    object_str = str(prod)
                    content = ContentType.objects.get(model='producto').id
                    AuditLog.save_log(user, id, content, object_str, 'Creado')

            elif action == 'create_Categoria':
                frmCateg =  FormCategoria(request.POST)
                data = frmCateg.save()

            elif action == 'create_Marca':
                frmMarca =  FormMarca(request.POST)
                data = frmMarca.save()
            
            elif action == 'marcas_autocomplete':
                data = []
                term = request.POST['term'].strip()
                marca = Marca.objects.all()
                if len(term):
                    marca = marca.filter(marca__icontains=term)[0:10]
                for i in marca:
                    item = i.toJSON()
                    item['value'] = i.marca
                    data.append(item)

            elif action == 'create_Modelo':
                frmModelos =  FormModelo(request.POST)
                data = frmModelos.save()
            else:
               data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Productos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['title'] = 'Creación de un Producto'
        context['frmCateg'] = FormCategoria()
        context['frmMarca'] = FormMarca()
        context['frmModelos'] = FormModelo()    
        return context

class ProductUpdateView(LoginRequiredMixin, Perms_Check, UpdateView):
    model = Producto
    form_class = FormProducto
    template_name = 'product/product_create.html'
    success_url = reverse_lazy('erp:product_list')
    permission_required = 'erp.change_producto'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_subgrupos_id':
                data = [{'id': '', 'text': '------------'}]
                for i in SubGrupoCtaBienes.objects.filter(grupo_id=request.POST['id']):
                    data.append({'id': i.id, 'text': i.cod_grusubgrusec + '  ' + i.denominacion})
            
            elif action == 'search_modelos_id':
                data = [{'id': '', 'text': '------------'}]
                for i in Modelo.objects.filter(marcas_id=request.POST['id']):
                    data.append({'id': i.id, 'text': i.modelo})
            
            elif action == 'marcas_autocomplete':
                data = []
                term = request.POST['term'].strip()
                marca = Marca.objects.all()
                if len(term):
                    marca = marca.filter(marca__icontains=term)[0:10]
                for i in marca:
                    item = i.toJSON()
                    item['value'] = i.marca
                    data.append(item)
                    
            elif action == 'edit':
                with transaction.atomic():
                    fields_audit = self.get_object()
                    produc_catalago = json.loads(request.POST['produc_catalago'])
                    prod = self.get_object()
                    prod.codigo = produc_catalago['codigo']
                    prod.nombre = produc_catalago['nombre']
                    prod.descripcion = produc_catalago['descripcion']
                    prod.componentes = produc_catalago['componentes']
                    prod.unida_medida = produc_catalago['unida_medida']
                    prod.activo = produc_catalago['activo']
                    prod.grupobien_id = produc_catalago['grupobien']['id']
                    prod.subgrupobien_id = produc_catalago['subgrupobien']['id']
                    prod.categorias_id = produc_catalago['categorias']['id']
                    prod.pagaimpuesto = produc_catalago['pagaimpuesto']
                    prod.lote = produc_catalago['lote']
                    prod.serie = produc_catalago['serie']
                    prod.inventariable = produc_catalago['inventariable']
                    prod.marca_id = produc_catalago['marca']['id']
                    prod.moneda_id = produc_catalago['moneda']['id']
                    prod.modelo_id = produc_catalago['modelo']['id']
                    prod.usuario = self.request.user
                    prod.imagen = produc_catalago['imagen']
                    prod.save()

                    user = self.request.user.id
                    id = prod.id
                    object_str = str(prod)
                    content = ContentType.objects.get(model='producto').id
                    AuditLog.save_log(user, id, content, object_str, 'Modificado')

                    self.audit_fields(fields_audit, produc_catalago)
                    # imagen = produc_catalago['imagen']
                    # ruta_imagen = os.path.join('producto/', imagen) 
                    # img = Image.open(imagen)
                    # img = img.resize((800, 600))
                    # img.save(ruta_imagen, optimize=True, quality=70)
                
            
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['frmCateg'] = FormCategoria()
        context['frmMarca'] = FormMarca()
        context['frmModelos'] = FormModelo()
        return context

    def audit_fields(self, pre_value, post_value):
        changes = []
        fields = [
            {'field': 'Nombre', 'value_ant': pre_value.nombre, 'value_act': post_value['nombre']},
            {'field': 'Descripcion', 'value_ant': pre_value.descripcion, 'value_act': post_value['descripcion']},
            {'field': 'Unidad de medida', 'value_ant':  pre_value.unida_medida, 'value_act': post_value['unida_medida']},
            {'field': 'Estado', 'value_ant':  pre_value.activo, 'value_act': post_value['activo']},
            {'field': 'Categoría', 'value_ant':  pre_value.categorias.nombre, 'value_act':post_value['categorias']['name']},
            {'field': 'Moneda', 'value_ant':  pre_value.moneda.__str__(), 'value_act': post_value['moneda']['name']},
            {'field': 'Grupo', 'value_ant':  pre_value.grupobien.__str__(), 'value_act': post_value['grupobien']['name']},
            {'field': 'Subgrupo', 'value_ant':  pre_value.subgrupobien.__str__(), 'value_act':post_value['subgrupobien']['name']},
            {'field': 'Marca', 'value_ant':  pre_value.marca.marca, 'value_act': post_value['marca']['name']},
            {'field': 'Modelo', 'value_ant':  pre_value.modelo.modelo, 'value_act': post_value['modelo']['name']},
            {'field': 'IVA', 'value_ant':  pre_value.pagaimpuesto, 'value_act': post_value['pagaimpuesto']},
            {'field': 'Solicita lote', 'value_ant':  pre_value.lote, 'value_act': post_value['lote']},
            {'field': 'Solicita nº serie', 'value_ant':  pre_value.serie, 'value_act': post_value['serie']},
            {'field': 'Imagen', 'value_ant':  pre_value.imagen, 'value_act': post_value['imagen']},
        ]
        for i in fields:
            if i['value_ant'] != i['value_act']:
                changes.append(i)
        
        if len(changes) > 0:
            AuditLog.fields_save(changes)

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    permission_required = 'erp.delete_producto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            perms = ('erp.delete_producto',)
            if request.user.has_perms(perms):
                self.object.delete()
            else:
                data['error'] = 'No tiene permisos para realizar esta acción'
            
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Producto'
        context['entity'] = 'Productos'
       # context['list_url'] = self.success_url
        return context

