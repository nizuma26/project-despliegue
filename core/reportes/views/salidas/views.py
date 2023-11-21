from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from core.erp.models import DetSalidaProd, SalidaProduc
from core.reportes.forms import ReportForm
#ESTA LIBRERIA PERMITE CONDICIONAR LOS FILTROS CUANDO UNA CONSULTA DA NULOS
from django.db.models.functions import Coalesce

from django.db.models import Sum

class ReportSalidasView(TemplateView):
    template_name= 'salida/reportsal.html'


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
                search =  DetSalidaProd.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(salida__fecha_salida__range=[start_date, end_date])
                for s in search:
                    data.append([
                        # s.id,
                        s.prod.nombre,
                        s.prod.descripcion,                        
                        s.salida.tipo_salida.denominacion,                        
                        s.codbien.codbien,                        
                        s.salida.fecha_salida.strftime('%Y-%m-%d'),
                        format(s.precio, '.2f'),
                        s.cant,
                        # format(s.salida.iva, '.2f'),
                        # format(s.subtotal, '.2f'),                        
                        # format(ingre.ingresoPro.total, '.2f'),
                    ])
                cant = search.aggregate(r=Coalesce(Sum('cant'), 0)).get('r')
                # subtotal = search.aggregate(r=Coalesce(Sum('subtotal'), 0)).get('r')
                # iva = search.aggregate(r=Coalesce(Sum('iva'), 0)).get('r')

                data.append([
                    '---',
                    '---',
                    '---',
                    '---',
                    '---',
                    '---',
                    cant,
                    # format(iva, '.2f'),
                    # format(subtotal, '.2f'),
                ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Distribuciones de Productos'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('report:salida_report')
        context['form'] = ReportForm()
        return context