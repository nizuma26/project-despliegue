import json
from django.http import JsonResponse
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from core.solicitudes.models import SolicSoporte, DetSolicSoporte
from core.erp.models import InventarioBienes
from core.erp.mixins import Perms_Check
from core.reportes.forms import ReportForm
from core.solicitudes.forms import FormSolicSoporte
from decimal import Decimal
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView

class SolicSoporteListView(LoginRequiredMixin, Perms_Check, FormView):
    form_class = ReportForm
    template_name = 'servicio_tec/list.html'

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
                queryset = SolicSoporte.objects.filter(usuario=self.request.user)
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(fecha__range=[start_date, end_date])
                for i in queryset:                    
                    data.append(i.toJSON())
            
            elif action == 'delete':
                solic = SolicSoporte.objects.filter(id=request.POST['id'])                   
                solic.delete()
                
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)     

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['title'] = 'Solicitud de Servico Técnico'
        context['btn_name'] = 'Nueva Solicitud'
        context['create_url'] = reverse_lazy('solicitudes:soporte_create')        
        return context

class SolicSoporteCreateView(LoginRequiredMixin, Perms_Check, CreateView):
    model = SolicSoporte
    form_class = FormSolicSoporte
    template_name = 'servicio_tec/create.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            #CONSULTAS
            #MODAL
            if action == 'search_products':
                data = []                 
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()

                for i in InventarioBienes.objects.filter(unidad_id__in=request.POST['idunidad']).exclude(ult_proc='DESINC').exclude(codbien_id__in=ids_exclude):
                    item = {}
                    item['full_name'] = i.prod.nombre + ' / ' + i.prod.descripcion
                    item['categ'] = i.prod.categorias.nombre
                    item['imagen'] = i.prod.get_imagen()                    
                    item['prod'] = i.prod_id
                    item['codbien'] = i.codbien.toJSON()
                    item['codubica'] = i.ubica_fisica.toJSON()
                    item['salida'] = i.salida_id
                    item['id'] = i.id
                    data.append(item)
            #BUSCADOR DE PRODUCTOS
            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['idsCodbien'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text':term})
                products = InventarioBienes.objects.filter(unidad_id__in=request.POST['idorigen']).exclude(ult_proc='DESINC').exclude(codbien_id__in=ids_exclude)

                if len(term):
                    products = products.filter(prod__nombre__icontains=term)
                for i in products:
                    item = {}
                    item['full_name'] = i.prod.nombre  + ' / ' + i.prod.descripcion
                    item['categ'] = i.prod.categorias.nombre
                    item['imagen'] = i.prod.get_imagen()                    
                    item['prod'] = i.prod_id
                    item['codbien'] = i.codbien.toJSON()
                    item['codubica'] = i.ubica_fisica.toJSON()
                    item['salida'] = i.salida_id
                    item['id'] = i.id
                    data.append(item)  
            #GUARDAR REGISTRO
            elif action == 'add':
                with transaction.atomic():
                    solicitudes = json.loads(request.POST['solicitud'])
                    solic = SolicSoporte()
                    solic.codigo = solicitudes['codigo']
                    solic.tipo_solic = solicitudes['tipo_solic']
                    solic.prioridad = solicitudes['prioridad']
                    solic.fecha = solicitudes['fecha']
                    solic.unidad_id = solicitudes['unidad']
                    solic.estado = solicitudes['estado']
                    solic.descrip = solicitudes['descrip']
                    solic.tipo_prod = solicitudes['tipo_prod']
                    solic.usuario = self.request.user
                    solic.save()                    
                    
                    if solic.tipo_solic == 'REP':
                        for i in solicitudes['productos']:
                            det = DetSolicSoporte()
                            det.prod_id = i['id']
                            det.diagnostico = i['diagnostico']                          
                            det.solic_soport_id = solic.id
                            det.save()
                        data = {'id': solic.id}           
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)      

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['title'] = 'Creando Nueva Solicitud'
        context['list_url'] = reverse_lazy('solicitudes:soporte_list')
        context['entity'] = 'Solicitudes de Servicio Técnico'
        context['action'] = 'add'
        context['det'] = []
        return context

class SolicSoporteUpdateView(LoginRequiredMixin, Perms_Check, UpdateView):
    model = SolicSoporte
    form_class = FormSolicSoporte
    template_name = 'servicio_tec/create.html'
    success_url = reverse_lazy('solicitudes:soporte_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            #CONSULTAS
            #MODAL
            if action == 'search_products':
                data = []                 
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()

                for i in InventarioBienes.objects.filter(unidad_id__in=request.POST['idunidad']).exclude(ult_proc='DESINC').exclude(codbien_id__in=ids_exclude):
                    item = {}
                    item['full_name'] = i.prod.nombre + ' / ' + i.prod.descripcion
                    item['categ'] = i.prod.categorias.nombre
                    item['imagen'] = i.prod.get_imagen()                    
                    item['prod'] = i.prod_id
                    item['codbien'] = i.codbien.toJSON()
                    item['codubica'] = i.ubica_fisica.toJSON()
                    item['salida'] = i.salida_id
                    item['id'] = i.id
                    data.append(item)
            #BUSCADOR
            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['idsCodbien'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text':term})
                products = InventarioBienes.objects.filter(unidad_id__in=request.POST['idorigen']).exclude(ult_proc='DESINC').exclude(codbien_id__in=ids_exclude)

                if len(term):
                    products = products.filter(prod__nombre__icontains=term)
                for i in products:
                    item = {}
                    item['full_name'] = i.prod.nombre  + ' / ' + i.prod.descripcion
                    item['categ'] = i.prod.categorias.nombre
                    item['imagen'] = i.prod.get_imagen()                    
                    item['prod'] = i.prod_id
                    item['codbien'] = i.codbien.toJSON()
                    item['codubica'] = i.ubica_fisica.toJSON()
                    item['salida'] = i.salida_id
                    item['id'] = i.id
                    data.append(item)  
            
            elif action == 'edit':
                with transaction.atomic():
                    solicitudes = json.loads(request.POST['solicitud'])              
                    solic = self.get_object()
                    solic.codigo = solicitudes['codigo']
                    solic.tipo_solic = solicitudes['tipo_solic']
                    solic.prioridad = solicitudes['prioridad']
                    solic.fecha = solicitudes['fecha']
                    solic.unidad_id = solicitudes['unidad']
                    solic.estado = solicitudes['estado']
                    solic.descrip = solicitudes['descrip']
                    solic.tipo_prod = solicitudes['tipo_prod']
                    solic.usuario = self.request.user
                    solic.save()           
                    
                    if solic.tipo_solic == 'REP':
                        solic.solic_soport_set.all().delete()
                        for i in solicitudes['productos']:
                            det = DetSolicSoporte()
                            det.prod_id = i['id']
                            det.diagnostico = i['diagnostico']                          
                            det.solic_soport_id = solic.id
                            det.save()
                        data = {'id': solic.id}              
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # Esta función trae los datos del detalle que están en otro modelo 
    def get_details_product(self):
        data = []
        try:
            for i in DetSolicSoporte.objects.filter(solic_soport_id=self.get_object().id):
                item = i.prod.toJSON()
                item['diagnostico'] = i.diagnostico
                item['categ'] = i.prod.categorias.nombre
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edición de la solicitud: {self.object.codigo}'
        context['entity'] = 'Volver al listado'
        context['list_url'] = self.success_url
        context['action'] = 'edit'        
        context['det'] = json.dumps(self.get_details_product(), cls=DecimalEncoder)
        return context

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)