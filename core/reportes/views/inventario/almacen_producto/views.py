from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from core.erp.models import Producto, SalidaProduc, ControlStock
from core.reportes.forms import ReporAlmacenForm
#ESTA LIBRERIA PERMITE CONDICIONAR LOS FILTROS CUANDO UNA CONSULTA DA NULOS
from django.db.models.functions import Coalesce

from django.db.models import Sum

class ReportAlmacenProdView(TemplateView):
    template_name= 'inventario/almacen_prod/reportAlmac.html'


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                almacen=request.POST['almacen']
                categoria=request.POST['categoria']
                search =  ControlStock.objects.all()
                if categoria:
                    search = search.filter(almacenes_id__in=request.POST['almacen']).filter(productos__categorias_id__in=request.POST['categoria']).filter(stock_actual__gt=0)
                    for i in search:
                        item = {}                  
                        item['prod'] = i.productos.nombre
                        item['desc'] = i.productos.descripcion                  
                        item['categorias'] = i.productos.categorias.nombre
                        item['marca'] = i.productos.marca.marca
                        item['modelo'] = i.productos.modelo.modelo
                        item['stock'] = i.stock_actual    
                        data.append(item)
                        
                else:
                    search = search.filter(almacenes_id__in=request.POST['almacen']).filter(stock_actual__gt=0)
                    for i in search:
                        item = {}                  
                        item['prod'] = i.productos.nombre
                        item['desc'] = i.productos.descripcion                  
                        item['categorias'] = i.productos.categorias.nombre
                        item['marca'] = i.productos.marca.marca
                        item['modelo'] = i.productos.modelo.modelo
                        item['stock'] = i.stock_actual    
                        
                        data.append(item)
                
            
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Inventario en Almacén'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('report:almacen_report')
        context['form'] = ReporAlmacenForm()
        return context