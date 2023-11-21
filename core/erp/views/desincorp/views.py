import json
import os
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from core.erp.forms import DesincProdForm, UnidadForm, FormDepart, FormConcepMov
from core.erp.models import DesincProduc, DetDesincProd, Unidad, Departamento, CodBienes, DetSalidaProd, ConcepMovimiento, InventarioBienes, Empresa, DetTrasladoProd
from core.reportes.forms import ReportForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, CreateView, UpdateView, DeleteView, View
from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.urls import reverse_lazy
from decimal import Decimal
from datetime import datetime

from core.erp.mixins import Perms_Check

class DesincListView(LoginRequiredMixin, Perms_Check, FormView):
    model = DesincProduc
    form_class = ReportForm
    template_name = 'desincorp/list.html'
    permission_required = 'erp.view_desincproduc'

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
                queryset = DesincProduc.objects.all()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(fecha_desinc__range=[start_date, end_date])
                for i in queryset:
                    item = {}
                    item['id'] = i.id
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
            
            elif action == 'delete':
                desinc = DesincProduc.objects.prefetch_related('usuario', 'origen', 'tipo_desinc').get(pk=request.POST['id'])
                desinc.delete()                   
                    
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Desincorporaciones en Unidad'
        context['create_url'] = reverse_lazy('erp:desinc_create')
        context['list_url'] = reverse_lazy('erp:desinc_list')
        context['entity'] = 'Desincorporaciones'
        context['btn_name'] = 'Nuevo Registro'
        return context

class DesincCreateView(LoginRequiredMixin, Perms_Check, CreateView):
    model = DesincProduc
    form_class = DesincProdForm
    template_name = 'desincorp/create.html'
    success_url = reverse_lazy('erp:desinc_list')
    url_redirect = success_url
    permission_required = 'erp.add_desincproduc'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['idsCodbien'])
                term = request.POST['term'].strip() 
                inventory = InventarioBienes.objects.prefetch_related('prod', 'unidad', 'ubica_fisica').filter(unidad_id__in=request.POST['idorigen']).exclude(ult_proc='Desincorporado').exclude(codbien_id__in=ids_exclude)
                
                for i in inventory:
                    item = {}
                    item['full_name'] = i.prod.nombre + ' / ' + i.prod.descripcion
                    item['imagen'] = i.prod.get_imagen()                    
                    item['categoria'] = i.prod.categorias.nombre
                    item['prod'] = i.prod_id
                    item['codbien'] = i.codbien.toJSON()
                    item['codubica'] = i.ubica_fisica.toJSON()
                    item['id'] = i.id
                    data.append(item)

            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['idsCodbien'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text':term})

                inventory = InventarioBienes.objects.prefetch_related('prod', 'unidad', 'ubica_fisica').filter(unidad_id__in=request.POST['idorigen']).exclude(ult_proc='Desincorporado').exclude(codbien_id__in=ids_exclude)

                for i in inventory:
                    item = {}
                    item['full_name'] = i.prod.nombre + ' / ' + i.prod.descripcion
                    item['imagen'] = i.prod.get_imagen()                    
                    item['categoria'] = i.prod.categorias.nombre
                    item['prod'] = i.prod_id
                    item['codbien'] = i.codbien.toJSON()
                    item['codubica'] = i.ubica_fisica.toJSON()
                    item['id'] = i.id
                    data.append(item)
                    
            elif action == 'add':
                with transaction.atomic():
                    desincorp = json.loads(request.POST['desincorp'])
                    desinc = DesincProduc()
                    desinc.cod_desinc = desincorp['cod_desinc']
                    desinc.origen_id = desincorp['origen']
                    desinc.respon_origen = desincorp['respon_origen']
                    desinc.tipo_desinc_id= desincorp['tipo_desinc']                    
                    desinc.fecha_desinc = desincorp['fecha_desinc']
                    desinc.usuario = self.request.user
                    desinc.observ = desincorp['observ']
                    desinc.estado = desincorp['estado']
                    desinc.soportedocum = desincorp['soportedocum']
                    desinc.save()

                    for i in desincorp['produc_desinc']:
                        det = DetDesincProd()
                        det.codbien_id = int(i['codbien']['id'])
                        det.codubica_id = int(i['codubica']['id'])
                        det.desinc_id = desinc.id
                        det.prod_id = i['prod']
                        det.save()

                    data = {'id': desinc.id}

            elif action == 'search_responorigen':
                data = []
                #data = [{'id': '', 'text': '-----------'}]
                for i in Unidad.objects.filter(id=request.POST['id']):
                    item = {}
                    item['nombrejefe'] = i.nombrejefe + ' - ' + i.ced_resp
                    data.append(item)  

            elif action == 'create_concepto':
                with transaction.atomic():
                    frmConcepMov =  FormConcepMov(request.POST)
                    data = frmConcepMov.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
            #para que se pueda serializar agrego el safe=False
        return JsonResponse(data, safe=False)   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creando Nueva Desincorporación'
        context['entity'] = 'Desincorporación'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['iva'] = Empresa.objects.values('nameimpuesto', ('iva')).last()
        context['frmUnidad'] = UnidadForm()
        context['frmdepar'] = FormDepart()
        context['frmConcepMov'] = FormConcepMov()
        # context['btn_name'] = 'Nuevo Ingreso'
        context['det'] = []
        return context

class DesincUpdateView(LoginRequiredMixin, Perms_Check, UpdateView):
    model = DesincProduc
    form_class = DesincProdForm
    template_name = 'desincorp/create.html'
    success_url = reverse_lazy('erp:desinc_list')
    url_redirect = success_url
    permission_required = 'erp.change_desincproduc'


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        instance = self.get_object()
        form = DesincProdForm(instance=instance)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['idsCodbien'])
                term = request.POST['term'].strip() 
                inventory = InventarioBienes.objects.prefetch_related('prod', 'unidad', 'ubica_fisica').filter(unidad_id__in=request.POST['idorigen']).exclude(ult_proc='Desincorporado').exclude(codbien_id__in=ids_exclude)
                
                for i in inventory:
                    item = {}
                    item['full_name'] = i.prod.nombre + ' / ' + i.prod.descripcion
                    item['imagen'] = i.prod.get_imagen()                    
                    item['categoria'] = i.prod.categorias.nombre
                    item['prod'] = i.prod_id
                    item['codbien'] = i.codbien.toJSON()
                    item['codubica'] = i.ubica_fisica.toJSON()
                    item['id'] = i.id
                    data.append(item)

            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['idsCodbien'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text':term})

                inventory = InventarioBienes.objects.prefetch_related('prod', 'unidad', 'ubica_fisica').filter(unidad_id__in=request.POST['idorigen']).exclude(ult_proc='Desincorporado').exclude(codbien_id__in=ids_exclude)

                for i in inventory:
                    item = {}
                    item['full_name'] = i.prod.nombre + ' / ' + i.prod.descripcion
                    item['imagen'] = i.prod.get_imagen()                    
                    item['categoria'] = i.prod.categorias.nombre
                    item['prod'] = i.prod_id
                    item['codbien'] = i.codbien.toJSON()
                    item['codubica'] = i.ubica_fisica.toJSON()
                    item['id'] = i.id
                    data.append(item)
                   
            elif action == 'edit':
                with transaction.atomic():
                    desincorp = json.loads(request.POST['desincorp'])
                    desinc = self.get_object()
                    desinc.cod_desinc = desincorp['cod_desinc']
                    desinc.origen_id = desincorp['origen']
                    desinc.respon_origen = desincorp['respon_origen']
                    desinc.tipo_desinc_id= desincorp['tipo_desinc']                    
                    desinc.fecha_desinc = desincorp['fecha_desinc']
                    desinc.usuario = self.request.user
                    desinc.observ = desincorp['observ']
                    desinc.estado = desincorp['estado']
                    desinc.soportedocum = desincorp['soportedocum']
                    desinc.save()                    
                    detdesinc = DetDesincProd.objects.prefetch_related('desinc').filter(desinc_id=self.get_object().id)
                    detdesinc.delete()

                    for i in desincorp['produc_desinc']:
                        det = DetDesincProd()
                        det.codbien_id = int(i['codbien']['id'])
                        det.codubica_id = int(i['codubica']['id'])
                        det.desinc_id = desinc.id
                        det.prod_id = int(i['prod'])
                        det.save()

                    data = {'id': desinc.id}

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
            for i in DetDesincProd.objects.prefetch_related('prod', 'codbien', 'codubica').filter(desinc_id=self.get_object().id):
               item = {}
               item = i.prod.toJSON()
               item['full_name'] = i.prod.nombre + ' / ' + i.prod.categorias.nombre
               item['categoria'] = i.prod.categorias.nombre
               item['codbien'] = {'id': i.codbien.id, 'name': i.codbien.codbien}
               item['codubica'] = {'id': i.codubica.id, 'name': i.codubica.nombre}
               item['prod'] = i.prod_id
               data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):     
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edición de la Desincorporación: {self.object.cod_desinc}'
        context['entity'] = 'Desincorporación'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['frmConcepMov'] = FormConcepMov()
        context['det'] = json.dumps(self.get_details_product(), cls=DecimalEncoder)
        return context

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)

class DesincFacturaPdfView(View):
   def get(self, request, *args, **kwargs):
        try:
            template = get_template('desincorp/PDF_Desinc.html')
            # encab_distrib= trasladoProduc.objects.get(id=self.kwargs['pk']).values('cod_traslado', 'origen', 'origen__nombre',  'destino', 'destino__nombre', 'destino__nombrejefe', 'tipo_traslado', 'tipo_comprob', 'num_comprob', 'subtotal', 'iva', 'total', 'fecha_traslado', 'usuario', 'observ', 'estado', 'aprobado')
            encab_desinc= DesincProduc.objects.get(pk=self.kwargs['pk'])
            detalle_desinc= DetDesincProd.objects.filter(desinc_id=self.kwargs['pk']).order_by('codubica_id')
            context = {
            'encab_desinc': encab_desinc,
            'detalle_desinc': detalle_desinc,
            'comp': {'fecha': datetime.now, 'name': 'Dirección Regional de Salud Estado Portuguesa', 'rif': 'G-20008795-1', 'tlf': '(0257) - 2531550 - 2512246 - 2534014', 'redsocial': 'http://saludportuguesa.gob.ve; twitter: @saludportuguesa', 'address': 'Carrera 3 con calle 09 Antiguo Hospital, Sector Curazao Guanare Portuguesa Venezuela'},
            'icon': '{}{}'.format(settings.MEDIA_URL, 'imagportadalogin/klipartzcom.png')
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:desinc_list'))