import json
import os
from django.conf import settings
from django.db import transaction
from django.db.models import Q
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
from core.erp.forms import TrasladoProdForm, UnidadForm, FormDepart, FormConcepMov
from core.reportes.forms import ReportForm
from core.erp.models import TrasladoProduc, DetTrasladoProd, Unidad, Departamento, InventarioBienes
from core.erp.mixins import Perms_Check
from core.solicitudes.models import Solicitudes


class TrasladoListView(LoginRequiredMixin, Perms_Check, FormView):
    model = TrasladoProduc
    form_class = ReportForm
    template_name = 'traslado_prod/list.html'
    permission_required = 'erp.view_trasladoproduc'

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
                queryset = TrasladoProduc.objects.all()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(fecha_traslado__range=[start_date, end_date])
                for i in queryset:
                    item = {}
                    item['id'] = i.id
                    item['cod_traslado'] = i.cod_traslado
                    item['origen'] = i.origen.nombre
                    item['destino'] = i.destino.nombre
                    item['tipo_traslado'] = i.tipo_traslado.denominacion
                    item['fecha_traslado'] = i.fecha_traslado
                    item['estado'] = i.estado
                    data.append(item)
                    
            elif action == 'detail':
                data = []                
                for i in DetTrasladoProd.objects.filter(trasproduc_id=request.POST['id']).prefetch_related('prod'):
                    item = {}
                    item['products'] = i.prod.nombre + ' / ' +i.prod.descripcion
                    item['depart_origen'] = i.codubica.nombre
                    item['depart_destino'] = i.ubica_destino.nombre
                    item['codbien'] = i.codbien.codbien
                    item['user'] = i.trasproduc.usuario.username
                    item['observ'] = i.trasproduc.observ
                    item['resp_origen'] = i.trasproduc.respon_origen
                    item['resp_destino'] = i.trasproduc.respon_destino
                    data.append(item)
            
            elif action == 'delete':
                with transaction.atomic():
                    perms = ('erp.delete_trasladoproduc',)
                    if request.user.has_perms(perms):
                        traslado = TrasladoProduc.objects.get(pk=request.POST['id'])
                        traslado.delete()
                    else:
                        data['error'] = 'No tiene permisos para realizar esta acción'
                    
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Traslados'
        context['create_url'] = reverse_lazy('erp:traslado_create')
        context['list_url'] = reverse_lazy('erp:traslado_list')
        context['entity'] = 'Traslados'
        context['btn_name'] = 'Nuevo Registro'
        return context

class TrasladoCreateView(LoginRequiredMixin, Perms_Check, CreateView):
    model = TrasladoProduc
    form_class = TrasladoProdForm
    template_name = 'traslado_prod/create.html'
    success_url = reverse_lazy('erp:traslado_list')
    url_redirect = success_url
    permission_required = 'erp.add_trasladoproduc'

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

                for i in InventarioBienes.objects.filter(unidad_id__in=request.POST['idorigen']).exclude(ult_proc='DESINC').exclude(codbien_id__in=ids_exclude):
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

            elif action == 'search_responorigen':
                data = []
                for i in Unidad.objects.filter(id=request.POST['id']):
                    item = {}
                    item['nombrejefe'] = i.nombrejefe + ' - ' + i.ced_resp
                    data.append(item)  

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
            elif action == 'add':
                with transaction.atomic():
                    traslados = json.loads(request.POST['traslados'])
                    traslado = TrasladoProduc()
                    traslado.cod_traslado = traslados['cod_traslado']
                    traslado.origen_id = traslados['origen']
                    traslado.respon_origen = traslados['respon_origen']
                    traslado.destino_id = traslados['destino']
                    traslado.respon_destino = traslados['respon_destino']
                    traslado.tipo_traslado_id= traslados['tipo_traslado']                   
                    traslado.usuario = self.request.user                    
                    traslado.fecha_traslado = traslados['fecha_traslado']
                    traslado.observ = traslados['observ']
                    traslado.estado = traslados['estado']
                    traslado.soportedocum = traslados['soportedocum']
                    traslado.salida_id = traslados['salida']
                    traslado.save()
                    
                    for i in traslados['produc_tras']:
                        det = DetTrasladoProd()                        
                        det.codbien_id = int(i['codbien']['id'])
                        det.codubica_id = int(i['codubica']['id'])
                        det.ubica_destino_id = int(i['ubica_destino']['id'])
                        det.trasproduc_id = traslado.id
                        det.prod_id = i['prod']
                        det.save()

                        # invbienes = InventarioBienes.objects.get(codbien=int(i['codbien']['id']))                        
                        # if invbienes.ult_proc != 'DIST':
                        #     invbienes.ant_ult_proc = 'TRAS'
                        #     invbienes.ant_tipo_proc_id = traslados['tipo_traslado']
                        # invbienes.unidad_id = traslados['destino']
                        # invbienes.ubica_fisica_id =  int(i['ubica_destino']['id'])
                        # invbienes.tipo_proc_id = traslados['tipo_traslado']
                        # invbienes.ult_proc = 'TRAS'
                        # invbienes.date_joined = traslados['fecha_traslado']
                        # invbienes.save()

                    data = {'id': traslado.id}
            elif action == 'search_destino':
                data = []
                term = request.POST['term']
                destinos = Unidad.objects.filter(
                    Q(nombre__icontains=term) | Q(rif__icontains=term) | Q(nombrejefe__icontains=term))[0:20]
                for i in destinos:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)

            elif action == 'search_depart':               
                data = []
                term = request.POST['term'].strip()
                ubicafisica = Departamento.objects.filter()
                if len(term):
                    ubicafisica = ubicafisica.filter(nombre__icontains=term)
                for i in ubicafisica:
                    item = i.toJSON()
                    item['value'] = i.nombre
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
            #para que se pueda serializar agrego el safe=False
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Creando nuevo Traslado'
        context['entity'] = 'Traslados'
        context['list_url'] = self.success_url
        context['url'] = f'/erp/traslado/add/'
        context['action'] = 'add'
        context['frmUnidad'] = UnidadForm()
        context['frmdepar'] = FormDepart()
        context['frmConcepMov'] = FormConcepMov()
        # context['btn_name'] = 'Nuevo Ingreso'
        context['det'] = []
        return context

class TrasladoUpdateView(LoginRequiredMixin, Perms_Check, UpdateView):
    model = TrasladoProduc
    form_class = TrasladoProdForm
    template_name = 'traslado_prod/create.html'
    success_url = reverse_lazy('erp:traslado_list')
    url_redirect = success_url
    permission_required = 'erp.change_trasladoproduc'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = TrasladoProdForm(instance=instance)
        form.fields['destino'].queryset = Unidad.objects.filter(id=instance.destino.id)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []                 
                ids_exclude = json.loads(request.POST['idsCodbien'])
                term = request.POST['term'].strip()

                for i in InventarioBienes.objects.filter(unidad_id__in=request.POST['idorigen']).exclude(ult_proc='DESINC').exclude(codbien_id__in=ids_exclude):
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

            elif action == 'search_responorigen':
                data = []
                #data = [{'id': '', 'text': '-----------'}]
                for i in Unidad.objects.filter(id=request.POST['id']):
                    item = {}
                    item['nombrejefe'] = i.nombrejefe + ' - ' + i.ced_resp
                    data.append(item)  

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
                    traslados = json.loads(request.POST['traslados'])
                    traslado = self.get_object()
                    traslado.cod_traslado = traslados['cod_traslado']
                    traslado.destino_id = traslados['destino']
                    traslado.respon_destino = traslados['respon_destino']
                    traslado.tipo_traslado_id= traslados['tipo_traslado']                   
                    traslado.usuario = self.request.user                    
                    traslado.fecha_traslado = traslados['fecha_traslado']
                    traslado.observ = traslados['observ']
                    traslado.estado = traslados['estado']
                    traslado.soportedocum = traslados['soportedocum']
                    traslado.save()

                    dettras = DetTrasladoProd.objects.filter(trasproduc_id=self.get_object().id)
                    dettras.delete()
                    
                    for i in traslados['produc_tras']:
                        det = DetTrasladoProd()                        
                        det.codbien_id = int(i['codbien']['id'])
                        det.codubica_id = int(i['codubica']['id'])
                        det.ubica_destino_id = int(i['ubica_destino']['id'])
                        det.trasproduc_id = traslado.id
                        det.prod_id = i['prod']
                        det.save()
                    data = {'id': traslado.id}

            elif action == 'search_destino':
                data = []
                term = request.POST['term']
                destinos = Unidad.objects.filter(
                    Q(nombre__icontains=term) | Q(rif__icontains=term) | Q(nombrejefe__icontains=term))[0:20]
                for i in destinos:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
                    
            elif action == 'search_depart':               
                data = []
                term = request.POST['term'].strip()
                ubicafisica = Departamento.objects.filter()
                if len(term):
                    ubicafisica = ubicafisica.filter(nombre__icontains=term)
                for i in ubicafisica:
                    item = i.toJSON()
                    item['value'] = i.nombre
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
            for i in DetTrasladoProd.objects.filter(trasproduc_id=self.get_object().id):
               item = {}
               item = i.prod.toJSON()
               item['full_name'] = i.prod.nombre + ' / ' + i.prod.descripcion               
               item['categ'] = i.prod.categorias.nombre               
               item['codbien'] = i.codbien.toJSON()
               item['codubica'] = i.codubica.toJSON()
               item['ubica_destino'] = i.ubica_destino.toJSON()
               item['prod'] = i.prod_id
               data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edición del traslado: {self.object.cod_traslado}'
        context['entity'] = 'traslados'
        context['list_url'] = self.success_url
        context['url'] = f'/erp/traslado/update/{self.object.id}/'
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product(), cls=DecimalEncoder)
        context['frmUnidad'] = UnidadForm()
        context['frmdepar'] = FormDepart()
        context['frmConcepMov'] = FormConcepMov()
        return context

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)

class TrasladoFacturaPdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('traslado_prod/PDF_Tras.html')
            # encab_distrib= trasladoProduc.objects.get(id=self.kwargs['pk']).values('cod_traslado', 'origen', 'origen__nombre',  'destino', 'destino__nombre', 'destino__nombrejefe', 'tipo_traslado', 'tipo_comprob', 'num_comprob', 'subtotal', 'iva', 'total', 'fecha_traslado', 'usuario', 'observ', 'estado', 'aprobado')
            encab_tras= TrasladoProduc.objects.get(pk=self.kwargs['pk'])

            detalle_tras= DetTrasladoProd.objects.filter(trasproduc_id=self.kwargs['pk']).order_by('ubica_destino_id')

            context = {
            'encab_tras': encab_tras,
            'detalle_tras': detalle_tras,
            'comp': {'fecha': datetime.now, 'name': 'Dirección Regional de Salud Estado Portuguesa', 'rif': 'G-20008795-1', 'tlf': '(0257) - 2531550 - 2512246 - 2534014', 'redsocial': 'http://saludportuguesa.gob.ve; twitter: @saludportuguesa', 'address': 'Carrera 3 con calle 09 Antiguo Hospital, Sector Curazao Guanare Portuguesa Venezuela'},
            'icon': '{}{}'.format(settings.MEDIA_URL, 'imagportadalogin/klipartzcom.png')
            }

            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:traslado_list'))

class TrasladoSolicitudView(LoginRequiredMixin, Perms_Check, FormView):
    form_class = TrasladoProdForm
    template_name = 'traslado_prod/create.html'
    permission_required = 'erp.add_trasladoproduc'    
    #permission_required = 'solicitudes.view_solicitudes'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.code = Solicitudes.objects.prefetch_related('user', 'unidad').filter(pk=self.kwargs['pk']).values('codigo').first()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        # print(salida)
        if action == 'convert_request':
            detail = []
            solic = Solicitudes.objects.prefetch_related('user', 'unidad').get(pk=self.kwargs['pk'])
            responsable_origen = Unidad.objects.select_related('unidad').filter(id=1).values('nombrejefe').first()
            header = {
                'tipo_traslado': solic.concepto.id,
                'destino': solic.unidad.id,
                'representante_destino': solic.unidad.nombrejefe,
                'representante_origen': responsable_origen['nombrejefe'],
                }
            #data['concept'] =
            for i in solic.solicitud_set.filter(aprobado=True):
                inventory = InventarioBienes.objects.select_related('prod', 'codbien', 'ubica_fisica', 'unidad', 'tipo_proc').filter(id=i.inventario.id)
                for inv in inventory:
                    item = {}
                    item['id'] = inv.id
                    item['full_name'] = f'{inv.prod.nombre} {inv.prod.descripcion}'
                    item['categ'] = inv.prod.categorias.nombre
                    item['codbien'] = {'id': inv.codbien.id, 'codbien': inv.codbien.codbien}
                    item['codubica'] = {'id': inv.ubica_fisica.id, 'nombre': inv.ubica_fisica.nombre}
                    item['ubica_destino'] = {'id': 0, 'nombre': ''}
                    item['salida'] = inv.salida_id
                    detail.append(item)                
            return JsonResponse({'header': header, 'detail': detail}, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Traslado de la solicitud: {self.code['codigo']}"
        context['url'] = f"/erp/traslado/solicitud/{self.kwargs['pk']}/"
        context['list_url'] = f"/solicitudes/solicitud/detail/{self.kwargs['pk']}/"
        context['frmDepart'] = FormDepart()
        context['entity'] = 'Volver'
        context['action'] = 'convert'
        return context

