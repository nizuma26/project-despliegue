from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from core.erp.models import DetDesincAlmacen, DesincAlmacen
from core.reportes.forms import ReportForm
#ESTA LIBRERIA PERMITE CONDICIONAR LOS FILTROS CUANDO UNA CONSULTA DA NULOS
from django.db.models.functions import Coalesce

from django.db.models import Sum

class ReportDesincAlmView(TemplateView):
    template_name= 'desinc_almac/report_desincalm.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search =  DetDesincAlmacen.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(desincorp__fecha_desinc__range=[start_date, end_date])
                for d in search:
                    data.append([                        
                        d.prod.nombre,
                        d.prod.descripcion,                        
                        d.desincorp.tipo_desinc.denominacion,                        
                        d.desincorp.fecha_desinc.strftime('%Y-%m-%d'),
                        format(d.prod.precio, '.2f'),
                        d.cant,
                        # format(d.desincorp.iva, '.2f'),
                        # format(d.subtotal, '.2f'),                        
                        # format(ingre.ingresoPro.total, '.2f'),                                               
                    ])
                cant = search.aggregate(r=Coalesce(Sum('cant'), 0)).get('r')
                # subtotal = search.aggregate(r=Coalesce(Sum('subtotal'), 0)).get('r')
                # iva = search.aggregate(r=Coalesce(Sum('iva'), 0)).get('r')
                # total = search.aggregate(r=Coalesce(Sum('total'), 0)).get('r')

                        # item = {}                  
                        # item['id'] = ingre.id,                 
                        # item['prod'] = ingre.prod.nombre,
                        # item['desc'] = ingre.prod.descripcion, 
                        # item['fecha'] = ingre.ingresoPro.fecha_ingreso.strftime('%Y-%m-%d'),
                        # item['precio'] = ingre.prod.precio,
                        # item['cant'] = ingre.cant,
                        # item['iva'] = format(ingre.ingresoPro.iva, '.2f'),
                        # item['subtotal'] = format(ingre.ingresoPro.subtotal, '.2f'),

                data.append([
                    '---',
                    '---',
                    '---',
                    '---',
                    '---',
                    cant,
                    # format(iva, '.2f'),
                    # format(subtotal, '.2f'),                    
                    # format(total, '.2f'),
                ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Desincorporaciones en el Almacén'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('report:desinc_almacen_report')
        context['form'] = ReportForm()
        return context